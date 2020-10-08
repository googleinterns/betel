import enum


class Categories(enum.Enum):
    """Enum for the categories found in Google Play Store.

    The enum members are bound to category names (in string format)
    as expected to be scraped from the Google Play Store.

    These can be used for specifying the filtering parameter of the
    PlayAppPageScraper or the classes desired for classification
    (when building the data set with the ClassifierDataSetBuilder).
    """

    ART_AND_DESIGN = "art & design"
    AUGMENTED_REALITY = "augmented reality"
    AUTO_AND_VEHICLES = "auto & vehicles"
    BEAUTY = "beauty"
    BOOKS_AND_REFERENCE = "books & reference"
    BUSINESS = "business"
    COMICS = "comics"
    COMMUNICATION = "communication"
    DATING = "dating"
    DAYDREAM = "daydream"
    EDUCATION = "education"
    ENTERTAINMENT = "entertainment"
    EVENTS = "events"
    FINANCE = "finance"
    FOOD_AND_DRINK = "food & drink"
    GAME = "game"
    HEALTH_AND_FITNESS = "health & fitness"
    HOUSE_AND_HOME = "house & home"
    LIBRARIES_AND_DEMO = "libraries & demo"
    LIFESTYLE = "lifestyle"
    MAPS_AND_NAVIGATION = "maps & navigation"
    MEDICAL = "medical"
    MUSIC_AND_AUDIO = "music & audio"
    NEWS_AND_MAGAZINES = "news & magazines"
    PARENTING = "parenting"
    PERSONALIZATION = "personalization"
    PHOTOGRAPHY = "photography"
    PRODUCTIVITY = "productivity"
    SHOPPING = "shopping"
    SOCIAL = "social"
    SPORTS = "sports"
    TOOLS = "tools"
    TRAVEL_AND_LOCAL = "travel & local"
    VIDEO_PLAYERS_AND_EDITORS = "video players & editors"
    WEAR_OS = "wear os by google"
    WEATHER = "weather"
    GAME_ACTION = "action"
    GAME_ADVENTURE = "adventure"
    GAME_ARCADE = "arcade"
    GAME_BOARD = "board"
    GAME_CARD = "card"
    GAME_CASINO = "casino"
    GAME_CASUAL = "casual"
    GAME_EDUCATIONAL = "educational"
    GAME_MUSIC = "music"
    GAME_PUZZLE = "puzzle"
    GAME_RACING = "racing"
    GAME_ROLE_PLAYING = "role playing"
    GAME_SIMULATION = "simulation"
    GAME_SPORTS = "sports"
    GAME_STRATEGY = "strategy"
    GAME_TRIVIA = "trivia"
    GAME_WORD = "word"
