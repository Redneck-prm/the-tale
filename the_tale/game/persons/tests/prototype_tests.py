# coding: utf-8
from django.test import TestCase

from accounts.logic import register_user

from game.prototypes import TimePrototype
from game.logic import create_test_map
from game.heroes.prototypes import HeroPrototype

from game.persons.models import PERSON_STATE

from game.persons.tests.helpers import create_person

class PrototypeTests(TestCase):

    def setUp(self):
        self.p1, self.p2, self.p3 = create_test_map()

        self.person = create_person(self.p1, PERSON_STATE.IN_GAME)

        result, account_id, bundle_id = register_user('test_user1', 'test_user1@test.com', '111111')
        self.hero_1 = HeroPrototype.get_by_account_id(account_id)

        result, account_id, bundle_id = register_user('test_user2', 'test_user2@test.com', '111111')
        self.hero_2 = HeroPrototype.get_by_account_id(account_id)

        result, account_id, bundle_id = register_user('test_user3', 'test_user3@test.com', '111111')
        self.hero_3 = HeroPrototype.get_by_account_id(account_id)

        current_time = TimePrototype.get_current_time()
        current_time.increment_turn()

        self.hero_1.mark_as_active()
        self.hero_2.mark_as_active()


    def test_initialize(self):
        self.assertEqual(self.person.friends_number, 0)
        self.assertEqual(self.person.enemies_number, 0)

    def test_update_friends_number(self):
        self.hero_1.preferences.friend_id = self.person.id
        self.hero_1.save()

        self.hero_2.preferences.friend_id = self.person.id
        self.hero_2.save()

        self.hero_2.preferences.friend_id = self.person.id
        self.hero_2.save()

        self.person.update_friends_number()
        self.person.update_enemies_number()

        self.assertEqual(self.person.friends_number, 2)
        self.assertEqual(self.person.enemies_number, 0)

    def test_update_enemies_number(self):
        self.hero_1.preferences.enemy_id = self.person.id
        self.hero_1.save()

        self.hero_2.preferences.enemy_id = self.person.id
        self.hero_2.save()

        self.hero_2.preferences.enemy_id = self.person.id
        self.hero_2.save()

        self.person.update_friends_number()
        self.person.update_enemies_number()

        self.assertEqual(self.person.friends_number, 0)
        self.assertEqual(self.person.enemies_number, 2)