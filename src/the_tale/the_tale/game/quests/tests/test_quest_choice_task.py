# coding: utf-8
from unittest import mock

from questgen import facts

from the_tale.common.utils import testcase
from the_tale.common.postponed_tasks.tests.helpers import FakePostpondTaskPrototype
from the_tale.common.postponed_tasks.prototypes import POSTPONED_TASK_LOGIC_RESULT

from the_tale.game.logic import create_test_map
from the_tale.game.logic_storage import LogicStorage

from the_tale.game import turn

from the_tale.game.actions.prototypes import ActionIdlenessPrototype

from the_tale.game.quests.postponed_tasks import MakeChoiceTask

from the_tale.game.quests.tests.helpers import QuestTestsMixin, QuestWith2ChoicePoints


class MakeChoiceTaskTest(testcase.TestCase, QuestTestsMixin):

    def setUp(self):
        super(MakeChoiceTaskTest, self).setUp()
        create_test_map()

        account = self.accounts_factory.create_account()

        self.account_id = account.id
        self.storage = LogicStorage()
        self.storage.load_account_data(account)
        self.hero =self.storage.accounts_to_heroes[account.id]

        self.choice_1_uid = '[ns-0]choice_1'
        self.choice_2_uid = '[ns-0]choice_2'
        self.option_1_1_uid = '#option([ns-0]choice_1, [ns-0]choice_2, opt_2)'
        self.option_1_2_uid = '#option([ns-0]choice_1, [ns-0]finish_2, opt_1)'
        self.option_2_1_uid = '#option([ns-0]choice_2, [ns-0]finish_1_1, opt_2_1)'
        self.option_2_2_uid = '#option([ns-0]choice_2, [ns-0]finish_1_2, opt_2_2)'

    def create_task(self, option_uid, account_id=None):

        if account_id is None:
            account_id = self.account_id

        quest = self.turn_to_quest(self.storage, self.hero.id)

        self.assertTrue(self.choice_1_uid in quest.knowledge_base)
        self.assertTrue(self.choice_2_uid in quest.knowledge_base)
        self.assertTrue(self.option_1_1_uid in quest.knowledge_base)
        self.assertTrue(self.option_1_2_uid in quest.knowledge_base)
        self.assertTrue(self.option_2_1_uid in quest.knowledge_base)
        self.assertTrue(self.option_2_2_uid in quest.knowledge_base)

        task = MakeChoiceTask(account_id=account_id,
                              option_uid=option_uid)
        return task

    @mock.patch('questgen.quests.quests_base.QuestsBase._available_quests', lambda *argv, **kwargs: [QuestWith2ChoicePoints])
    def test_create(self):
        task = self.create_task(option_uid=self.option_1_1_uid)
        self.assertTrue(task.state.is_UNPROCESSED)

    @mock.patch('questgen.quests.quests_base.QuestsBase._available_quests', lambda *argv, **kwargs: [QuestWith2ChoicePoints])
    def test_serialization(self):
        task = self.create_task(option_uid=self.option_1_1_uid)
        self.assertEqual(task.serialize(), MakeChoiceTask.deserialize(task.serialize()).serialize())

    @mock.patch('questgen.quests.quests_base.QuestsBase._available_quests', lambda *argv, **kwargs: [QuestWith2ChoicePoints])
    def test_unknown_choice(self):
        task = self.create_task(option_uid='unknown_choice')
        self.assertEqual(task.process(FakePostpondTaskPrototype(), self.storage), POSTPONED_TASK_LOGIC_RESULT.ERROR)
        self.assertTrue(task.state.is_WRONG_POINT)

    @mock.patch('questgen.quests.quests_base.QuestsBase._available_quests', lambda *argv, **kwargs: [QuestWith2ChoicePoints])
    def test_no_quests(self):
        self.turn_to_quest(self.storage, self.hero.id)

        account = self.accounts_factory.create_account()

        self.storage.load_account_data(account)

        task = self.create_task(option_uid=self.option_1_1_uid, account_id=account.id)

        self.assertEqual(task.process(FakePostpondTaskPrototype(), self.storage), POSTPONED_TASK_LOGIC_RESULT.ERROR)
        self.assertTrue(task.state.is_QUEST_NOT_FOUND)

    @mock.patch('questgen.quests.quests_base.QuestsBase._available_quests', lambda *argv, **kwargs: [QuestWith2ChoicePoints])
    def test_wrong_point(self):
        task = self.create_task(option_uid=self.option_2_1_uid)
        self.assertEqual(task.process(FakePostpondTaskPrototype(), self.storage), POSTPONED_TASK_LOGIC_RESULT.ERROR)
        self.assertTrue(task.state.is_WRONG_POINT)

    @mock.patch('questgen.quests.quests_base.QuestsBase._available_quests', lambda *argv, **kwargs: [QuestWith2ChoicePoints])
    def test_already_chosen(self):
        task = self.create_task(option_uid=self.option_1_1_uid)
        self.assertEqual(task.process(FakePostpondTaskPrototype(), self.storage), POSTPONED_TASK_LOGIC_RESULT.SUCCESS)
        self.assertTrue(task.state.is_PROCESSED)

        task = self.create_task(option_uid=self.option_1_2_uid)
        self.assertEqual(task.process(FakePostpondTaskPrototype(), self.storage), POSTPONED_TASK_LOGIC_RESULT.ERROR)
        self.assertTrue(task.state.is_ALREADY_CHOSEN)

    @mock.patch('questgen.quests.quests_base.QuestsBase._available_quests', lambda *argv, **kwargs: [QuestWith2ChoicePoints])
    def test_success(self):
        with mock.patch('the_tale.game.quests.container.QuestsContainer.mark_updated') as mark_updated:
            self.assertTrue(all(not action.replane_required for action in self.hero.actions.actions_list))
            task = self.create_task(option_uid=self.option_1_1_uid)
            self.assertEqual(task.process(FakePostpondTaskPrototype(), self.storage), POSTPONED_TASK_LOGIC_RESULT.SUCCESS)
            self.assertTrue(task.state.is_PROCESSED)
            self.assertTrue(all(action.replane_required for action in self.hero.actions.actions_list))

        self.assertTrue(mark_updated.call_count >= 1)


    @mock.patch('questgen.quests.quests_base.QuestsBase._available_quests', lambda *argv, **kwargs: [QuestWith2ChoicePoints])
    def test_choose_second_choice_before_first_completed(self):
        task = self.create_task(option_uid=self.option_1_2_uid)
        self.assertEqual(task.process(FakePostpondTaskPrototype(), self.storage), POSTPONED_TASK_LOGIC_RESULT.SUCCESS)
        self.assertTrue(task.state.is_PROCESSED)

        task = self.create_task(option_uid=self.option_2_1_uid)
        self.assertEqual(task.process(FakePostpondTaskPrototype(), self.storage), POSTPONED_TASK_LOGIC_RESULT.ERROR)
        self.assertTrue(task.state.is_WRONG_POINT)

    @mock.patch('questgen.quests.quests_base.QuestsBase._available_quests', lambda *argv, **kwargs: [QuestWith2ChoicePoints])
    def test_choose_second_choice_after_first_completed(self):
        task = self.create_task(option_uid=self.option_1_2_uid)
        self.assertEqual(task.process(FakePostpondTaskPrototype(), self.storage), POSTPONED_TASK_LOGIC_RESULT.SUCCESS)
        self.assertTrue(task.state.is_PROCESSED)

        while True:
            self.assertNotEqual(self.hero.actions.current_action.TYPE, ActionIdlenessPrototype.TYPE)

            task = self.create_task(option_uid=self.option_2_1_uid)

            if task.process(FakePostpondTaskPrototype(), self.storage) == POSTPONED_TASK_LOGIC_RESULT.ERROR:
                break

            self.storage.process_turn()
            self.storage.save_changed_data()

            turn.increment()

    @mock.patch('questgen.quests.quests_base.QuestsBase._available_quests', lambda *argv, **kwargs: [QuestWith2ChoicePoints])
    def test_no_choices(self):
        task = self.create_task(option_uid=self.option_1_1_uid)

        knowledge_base = self.hero.quests.current_quest.knowledge_base
        finish_state = next(knowledge_base.filter(facts.Finish))
        self.hero.quests.current_quest.machine.pointer.change_in_knowlege_base(knowledge_base, state=finish_state.uid, jump=None)

        self.assertEqual(task.process(FakePostpondTaskPrototype(), self.storage), POSTPONED_TASK_LOGIC_RESULT.ERROR)
        self.assertTrue(task.state.is_NO_CHOICES_IN_QUEST)
