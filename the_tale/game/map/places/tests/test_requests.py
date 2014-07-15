# coding: utf-8
import datetime
import jinja2

import mock

from django.core.urlresolvers import reverse

from the_tale.common.utils.testcase import TestCase

from the_tale.accounts.logic import register_user
from the_tale.accounts.prototypes import AccountPrototype

from the_tale.game.heroes.prototypes import HeroPrototype

from the_tale.game.logic import create_test_map


class TestShowRequests(TestCase):

    def setUp(self):
        super(TestShowRequests, self).setUp()
        self.place_1, self.place_2, self.place_3 = create_test_map()

        result, account_id, bundle_id = register_user('user', 'user@test.com', '111111')
        self.account = AccountPrototype.get_by_id(account_id)

    @mock.patch('the_tale.game.map.places.prototypes.PlacePrototype.is_new', True)
    def test_place_new_place_message(self):
        self.check_html_ok(self.request_html(reverse('game:map:places:show', args=[self.place_1.id])), texts=['pgf-new-place-message'])

    @mock.patch('the_tale.game.map.places.prototypes.PlacePrototype.is_new', False)
    def test_place_new_place_message__not_new(self):
        self.check_html_ok(self.request_html(reverse('game:map:places:show', args=[self.place_1.id])), texts=[('pgf-new-place-message', 0)])

    @mock.patch('the_tale.game.map.places.prototypes.PlacePrototype.is_frontier', True)
    def test_place_frontier_message(self):
        self.check_html_ok(self.request_html(reverse('game:map:places:show', args=[self.place_1.id])), texts=['pgf-frontier-message'])

    @mock.patch('the_tale.game.map.places.prototypes.PlacePrototype.is_frontier', False)
    def test_place_frontier_message__not_new(self):
        self.check_html_ok(self.request_html(reverse('game:map:places:show', args=[self.place_1.id])), texts=[('pgf-frontier-message', 0)])

    def test_wrong_place_id(self):
        self.check_html_ok(self.request_html(reverse('game:map:places:show', args=['wrong_id'])), texts=['places.place.wrong_format'])

    def test_place_does_not_exist(self):
        self.check_html_ok(self.request_html(reverse('game:map:places:show', args=[666])), texts=['places.place.not_found'], status_code=404)

    def check_no_heroes(self):
        texts = [('pgf-no-heroes-message', 1 + len(self.place_1.persons))]
        self.check_html_ok(self.request_html(reverse('game:map:places:show', args=[self.place_1.id])), texts=texts)

    def check_heroes(self):
        result, account_id, bundle_id = register_user('test_user', 'test_user@test.com', '111111')
        hero_1 = HeroPrototype.get_by_account_id(account_id)

        result, account_id, bundle_id = register_user('test_user_2', 'test_user_2@test.com', '111111')
        hero_2 = HeroPrototype.get_by_account_id(account_id)

        result, account_id, bundle_id = register_user('test_user_3', 'test_user_3@test.com', '111111')
        hero_3 = HeroPrototype.get_by_account_id(account_id)

        hero_1.premium_state_end_at = datetime.datetime.now() + datetime.timedelta(seconds=60)
        hero_1.preferences.set_place(self.place_1)
        hero_1.preferences.set_friend(self.place_1.persons[0])
        hero_1.preferences.set_enemy(self.place_1.persons[-1])
        hero_1.save()

        hero_2.premium_state_end_at = datetime.datetime.now() + datetime.timedelta(seconds=60)
        hero_2.preferences.set_place(self.place_1)
        hero_2.preferences.set_friend(self.place_1.persons[-1])
        hero_2.preferences.set_enemy(self.place_1.persons[0])
        hero_2.save()

        hero_3.preferences.set_place(self.place_1)
        hero_3.preferences.set_friend(self.place_1.persons[-1])
        hero_3.preferences.set_enemy(self.place_1.persons[0])
        hero_3.save()

        texts = [(jinja2.escape(hero_1.name), 3),
                 (jinja2.escape(hero_2.name), 3),
                 (jinja2.escape(hero_3.name), 0)]

        self.check_html_ok(self.request_html(reverse('game:map:places:show', args=[self.place_1.id])), texts=texts)


    def test_no_heroes__unlogined(self):
        self.check_no_heroes()

    def test_no_heroes__logined(self):
        self.request_login(self.account.email)
        self.check_no_heroes()

    def test_heroes__unlogined(self):
        self.check_heroes()

    def test_heroes__logined(self):
        self.request_login(self.account.email)
        self.check_heroes()