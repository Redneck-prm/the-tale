# coding: utf-8

def create_mob_for_hero(hero):
    from game.mobs.storage import mobs_storage
    return mobs_storage.get_random_mob(hero)
