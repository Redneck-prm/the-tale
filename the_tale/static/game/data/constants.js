
if (!window.pgf) {
    pgf = {};
}

if (!pgf.game) {
    pgf.game = {};
}

pgf.game.constants = {

    ACTOR_TYPE: {"PERSON": 0, "PLACE": 1, "MONEY_SPENDING": 1000},

    GENDER_TO_STR: {"0": "MASCULINE", "1": "FEMININE", "2": "NEUTER"},

    GENDER_TO_TEXT: {"0": "мужчина", "1": "женщина", "2": "оно"},

    PERSON_TYPE_TO_TEXT: {"0": "кузнец", "1": "рыбак", "2": "портной", "3": "плотник", "4": "охотник", "5": "стражник", "6": "торговец", "7": "трактирщик", "8": "вор", "9": "фермер", "10": "шахтёр", "11": "священник", "12": "лекарь", "13": "алхимик", "14": "палач", "15": "волшебник", "16": "мэр", "17": "бюрократ", "18": "аристократ", "19": "бард", "20": "дрессировщик", "21": "скотовод"},

    RACE_TO_STR: {"0": "HUMAN", "1": "ELF", "2": "ORC", "3": "GOBLIN", "4": "DWARF"},

    RACE_TO_TEXT: {"0": "человек", "1": "эльф", "2": "орк", "3": "гоблин", "4": "дварф"},
    
    PVP_COMBAT_STYLES_ADVANTAGES: {"0": {"0": 1.0, "1": 1.33, "2": 0.67, "3": 1.17, "4": 0.83, "5": 1.0}, "1": {"0": 0.67, "1": 1.0, "2": 1.33, "3": 0.83, "4": 1.0, "5": 1.17}, "2": {"0": 1.33, "1": 0.67, "2": 1.0, "3": 1.0, "4": 1.17, "5": 0.83}, "3": {"0": 0.83, "1": 1.17, "2": 1.0, "3": 1.0, "4": 0.92, "5": 1.08}, "4": {"0": 1.17, "1": 1.0, "2": 0.83, "3": 1.08, "4": 1.0, "5": 0.92}, "5": {"0": 1.0, "1": 0.83, "2": 1.17, "3": 0.92, "4": 1.08, "5": 1.0}},
    
    TERRAIN_ID_TO_STR: {"0": "WATER_DEEP", "1": "WATER_SHOAL", "2": "MOUNTAINS_HIGH", "3": "MOUNTAINS_LOW", "4": "PLANE_SAND", "5": "PLANE_DRY_LAND", "6": "PLANE_MUD", "7": "PLANE_DRY_GRASS", "8": "PLANE_GRASS", "9": "PLANE_SWAMP_GRASS", "10": "PLANE_CONIFER_FOREST", "11": "PLANE_GREENWOOD", "12": "PLANE_SWAMP_FOREST", "13": "PLANE_JUNGLE", "14": "PLANE_WITHERED_FOREST", "15": "HILLS_SAND", "16": "HILLS_DRY_LAND", "17": "HILLS_MUD", "18": "HILLS_DRY_GRASS", "19": "HILLS_GRASS", "20": "HILLS_SWAMP_GRASS", "21": "HILLS_CONIFER_FOREST", "22": "HILLS_GREENWOOD", "23": "HILLS_SWAMP_FOREST", "24": "HILLS_JUNGLE", "25": "HILLS_WITHERED_FOREST"},

    BUILDING_TYPE_TO_STR: {"0": "SMITHY", "1": "FISHING_LODGE", "2": "TAILOR_SHOP", "3": "SAWMILL", "4": "HUNTER_HOUSE", "5": "WATCHTOWER", "6": "TRADING_POST", "7": "INN", "8": "DEN_OF_THIEVE", "9": "FARM", "10": "MINE", "11": "TEMPLE", "12": "HOSPITAL", "13": "LABORATORY", "14": "SCAFFOLD", "15": "MAGE_TOWER", "16": "GUILDHALL", "17": "BUREAU", "18": "MANOR", "19": "SCENE", "20": "MEWS", "21": "RANCH"}
};