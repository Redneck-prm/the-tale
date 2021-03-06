# coding: utf-8
import datetime

from dext.settings import settings

from the_tale.common.utils.workers import BaseWorker

from the_tale.post_service.prototypes import MessagePrototype
from the_tale.post_service.conf import post_service_settings


class MessageSenderException(Exception): pass

class Worker(BaseWorker):
    GET_CMD_TIMEOUT = 0.1
    NO_CMD_TIMEOUT = 5.0

    def clean_queues(self):
        super(Worker, self).clean_queues()
        self.stop_queue.queue.purge()

    def initialize(self):
        if not post_service_settings.ENABLE_MESSAGE_SENDER:
            return False

        self.initialized = True
        self.next_message_process_time = datetime.datetime.now()
        self.logger.info('MESSAGE SENDER INITIALIZED')

    def process_no_cmd(self):
        if self.next_message_process_time < datetime.datetime.now():
            if not self.send_message(MessagePrototype.get_priority_message()):
                self.next_message_process_time = datetime.datetime.now() + datetime.timedelta(seconds=post_service_settings.MESSAGE_SENDER_DELAY)

    def send_message(self, message):

        if message is None:
            return False

        if (not post_service_settings.ENABLE_MESSAGE_SENDER or
            (settings.get(post_service_settings.SETTINGS_ALLOWED_KEY) is None and
             message.handler.settings_type_uid not in settings.get(post_service_settings.SETTINGS_FORCE_ALLOWED_KEY, ''))):
            self.logger.info('skip message %s' % message.uid)
            message.skip()
            return True

        self.logger.info('process message %s' % message.uid)

        message.process()

        if message.state.is_PROCESSED:
            self.logger.info('message %s status %s' % (message.uid, message.state))
        else:
            self.logger.error('message %s status %s ' % (message.uid, message.state))

        return True

    def cmd_send_now(self, message_id):
        return self.send_cmd('send_now', {'message_id': message_id})

    def process_send_now(self, message_id):
        self.send_message(MessagePrototype.get_by_id(message_id))
