
import random

from dext.common.utils import storage

from tt_logic.beings import relations as beings_relations

from the_tale.common.utils.logic import random_value_by_priority

from . import logic
from . import models
from . import objects
from . import exceptions


class MobsStorage(storage.CachedStorage):
    SETTINGS_KEY = 'mob records change time'
    EXCEPTION = exceptions.MobsStorageError

    def _construct_object(self, model):
        return logic.construct_from_model(model)

    def _get_all_query(self):
        return models.MobRecord.objects.all()

    def _update_cached_data(self, item):
        self._mobs_by_uuids[item.uuid] = item
        self._types_count[item.type] = len([mob for mob in self.all() if mob.type == item.type])
        self.mobs_number = len(self.all())

    def _reset_cache(self):
        self._mobs_by_uuids = {}
        self._types_count = {mob_type: 0 for mob_type in beings_relations.TYPE.records}
        self.mobs_number = 0

    def get_by_uuid(self, uuid):
        self.sync()
        return self._mobs_by_uuids.get(uuid)

    def has_mob(self, uuid):
        self.sync()
        return uuid in self._mobs_by_uuids

    def mob_type_fraction(self, mob_type): return self._types_count[mob_type] / float(self.mobs_number)

    def get_available_mobs_list(self, level, terrain=None, mercenary=None):
        self.sync()

        mobs = (record
                for record in self.all()
                if record.state.is_ENABLED and record.level <= level and (terrain is None or terrain in record.terrains))

        if mercenary is not None:
            mobs = (record for record in mobs if record.is_mercenary == mercenary)

        return list(mobs)

    def choose_mob(self, mobs_choices):
        global_actions_mobs = []
        normal_mobs = []

        for mob in mobs_choices:
            if mob.global_action_probability > 0:
                global_actions_mobs.append(mob)
            else:
                normal_mobs.append(mob)

        action_probability = sum(mob.global_action_probability for mob in global_actions_mobs if mob.global_action_probability)

        if random.random() > action_probability:
            return random.choice(normal_mobs)

        return random_value_by_priority((mob, mob.global_action_probability) for mob in global_actions_mobs)

    def get_random_mob(self, hero, mercenary=None, is_boss=False):
        self.sync()

        choices = self.get_available_mobs_list(level=hero.level, terrain=hero.position.get_terrain(), mercenary=mercenary)

        if not choices:
            return None

        mob_record = self.choose_mob(choices)

        return objects.Mob(record_id=mob_record.id,
                           level=hero.level,
                           is_boss=is_boss,
                           action_type=hero.actions.current_action.ui_type,
                           terrain=hero.position.get_terrain())

    def create_mob_for_hero(self, hero):
        return self.get_random_mob(hero)


mobs = MobsStorage()
