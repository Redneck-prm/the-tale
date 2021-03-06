
from the_tale.common.utils import testcase

from the_tale.game.logic_storage import LogicStorage
from the_tale.game.logic import create_test_map

from the_tale.game.cards import cards

from the_tale.game.postponed_tasks import ComplexChangeTask

from the_tale.game.cards.tests.helpers import CardsTestMixin


class HelpPlaceMixin(CardsTestMixin):
    CARD = None

    def setUp(self):
        super(HelpPlaceMixin, self).setUp()

        self.place_1, self.place_2, self.place_3 = create_test_map()

        self.account_1 = self.accounts_factory.create_account()

        self.storage = LogicStorage()
        self.storage.load_account_data(self.account_1)

        self.hero = self.storage.accounts_to_heroes[self.account_1.id]


    def test_use(self):
        with self.check_delta(lambda: self.hero.places_history._get_places_statisitcs().get(self.place_1.id, 0), self.CARD.effect.modificator):
            result, step, postsave_actions = self.CARD.effect.use(**self.use_attributes(storage=self.storage, hero=self.hero, value=self.place_1.id))

        self.assertEqual((result, step, postsave_actions), (ComplexChangeTask.RESULT.SUCCESSED, ComplexChangeTask.STEP.SUCCESS, ()))

    def test_wrong_place(self):
        with self.check_not_changed(lambda: self.hero.places_history._get_places_statisitcs().get(self.place_1.id, 0)):
            result, step, postsave_actions = self.CARD.effect.use(**self.use_attributes(storage=self.storage, hero=self.hero, value=666))
        self.assertEqual((result, step, postsave_actions), (ComplexChangeTask.RESULT.FAILED, ComplexChangeTask.STEP.ERROR, ()))


class HelpPlaceUncommonTests(HelpPlaceMixin, testcase.TestCase):
    CARD = cards.CARD.MOST_COMMON_PLACES_UNCOMMON

class HelpPlaceRareTests(HelpPlaceMixin, testcase.TestCase):
    CARD = cards.CARD.MOST_COMMON_PLACES_RARE

class HelpPlaceEpicTests(HelpPlaceMixin, testcase.TestCase):
    CARD = cards.CARD.MOST_COMMON_PLACES_EPIC

class HelpPlaceLegendaryTests(HelpPlaceMixin, testcase.TestCase):
    CARD = cards.CARD.MOST_COMMON_PLACES_LEGENDARY
