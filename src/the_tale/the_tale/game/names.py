# coding: utf-8

from utg import words as utg_words
from utg import relations as utg_relations

from the_tale.common.utils.decorators import lazy_property

from the_tale.game import relations


class NamesGenerators(object):
    __slots__ = ('elven', 'orcish', 'dwarfish', 'goblin', 'human', 'language')

    def __init__(self):
        import pynames

        self.elven = pynames.generators.elven.DnDNamesGenerator()
        self.orcish = pynames.generators.mongolian.MongolianNamesGenerator()
        self.dwarfish = pynames.generators.scandinavian.ScandinavianNamesGenerator()
        self.goblin = pynames.generators.korean.KoreanNamesGenerator()
        self.human = pynames.generators.russian.PaganNamesGenerator()

        self.language = pynames.LANGUAGE.RU

    def _get_name(self, race, gender):
        if race.is_HUMAN:
            return self.human.get_name(genders=[gender.pynames_id])
        if race.is_ELF:
            return self.elven.get_name(genders=[gender.pynames_id])
        if race.is_ORC:
            return self.orcish.get_name(genders=[gender.pynames_id])
        if race.is_GOBLIN:
            return self.goblin.get_name(genders=[gender.pynames_id])
        if race.is_DWARF:
            return self.dwarfish.get_name(genders=[gender.pynames_id])

    def get_name(self, race, gender):
        name_forms = self._get_name(race, gender).get_forms_for(gender=gender.pynames_id, language=self.language)

        name_forms += ['']*6

        name = utg_words.Word(type=utg_relations.WORD_TYPE.NOUN,
                              forms=name_forms,
                              properties=utg_words.Properties(utg_relations.ANIMALITY.ANIMATE, gender.utg_id))
        name.autofill_missed_forms()

        return name

    def get_fast_name(self, name, gender=relations.GENDER.MASCULINE):
        word = utg_words.Word.create_test_word(type=utg_relations.WORD_TYPE.NOUN,
                                               properties=utg_words.Properties(utg_relations.ANIMALITY.ANIMATE, gender.utg_id))
        word.forms = [name] * len(word.forms)

        return word

    def get_test_name(self, name='', gender=relations.GENDER.MASCULINE):
        name = utg_words.Word.create_test_word(type=utg_relations.WORD_TYPE.NOUN,
                                               prefix=('%s-' % name) if name else 't-',
                                               properties=utg_words.Properties(utg_relations.ANIMALITY.ANIMATE, gender.utg_id))

        return name


class ManageNameMixin(object):
    @lazy_property
    def utg_name(self):
        return utg_words.Word.deserialize(self.data['name'])

    @lazy_property
    def utg_name_form(self):
        return utg_words.WordForm(self.utg_name)

    @lazy_property
    def name(self): return self.utg_name.normal_form()

    def set_utg_name(self, word):
        del self.name
        del self.utg_name
        del self.utg_name_form

        if hasattr(self, '_model'):
            self._model.name = word.normal_form()

        self.data['name'] = word.serialize()


class ManageNameMixin2(object):
    __slots__ = ()

    @lazy_property
    def utg_name_form(self):
        return utg_words.WordForm(self.utg_name)

    @lazy_property
    def name(self): return self.utg_name.normal_form()

    def set_utg_name(self, word):
        del self.name
        del self.utg_name_form
        self.utg_name = word


_generator = None


def generator():
    global _generator

    if _generator is None:
        _generator = NamesGenerators()

    return _generator
