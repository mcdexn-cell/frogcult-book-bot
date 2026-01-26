"""
Provide enums for book.
"""

from enum import StrEnum, Enum


class BookStatus(StrEnum):
    PREORDER = 'preorder'
    COMING_SOON = 'coming_soon'
    NEW = 'new'


class BookGenre(Enum):
    """
    Enum of book genres.
    """
    FANTASY = "фентезі"
    SCIENCE_FICTION = "фантастика"
    THRILLER = "трилер"
    HORROR = "жахи"
    DETECTIVE = "детектив"
    ACTION = "бойовик"
    ADVENTURE = "пригоди"
    HISTORICAL_NOVEL = "історичний роман"
    ROMANCE = "любовний роман"
    DRAMA = "драма"
    COMEDY = "комедія"
    MYSTICISM = "містика"
    FOLKLORE = "фольклор"
    POETRY = "поезія"
    PROSE = "проза"
    CLASSIC_LITERATURE = "класична література"
    CONTEMPORARY_LITERATURE = "сучасна література"
    BIOGRAPHY = "біографія"
    PSYCHOLOGICAL_PROSE = "психологічна проза"
    PHILOSOPHICAL_PROSE = "філософська проза"
    SOCIAL_PROSE = "соціальна проза"
    POST_APOCALYPTIC = "постапокаліпсис"
    DYSTOPIA = "дистопія"
    UTOPIA = "утопія"
    CYBERPUNK = "кіберпанк"
    STEAMPUNK = "стімпанк"
    SPACE_OPERA = "космоопера"
    MILITARY_FICTION = "бойова фантастика"
    URBAN_FANTASY = "міський фентезі"
    EPIC_FANTASY = "епічний фентезі"
    DARK_FANTASY = "темний фентезі"
    PARANORMAL_ROMANCE = "паранормальний роман"
    SPY_NOVEL = "шпигунський роман"
    POLITICAL_THRILLER = "політичний трилер"
    CRIME_NOVEL = "кримінальний роман"
    NOIR = "нуар"
    WESTERN = "вестерн"
    FAMILY_SAGA = "сімейна сага"
    EROTICA = "еротика"
    YOUNG_ADULT = "young adult"
    CHILDREN_LITERATURE = "дитяча література"
    JOURNALISM = "публіцистика"
    ACADEMIC_LITERATURE = "наукова література"
    POPULAR_SCIENCE = "популярна наука"
    SELF_HELP = "самодопомога"
    BUSINESS = "бізнес"
    PSYCHOLOGY = "психологія"
    PHILOSOPHY = "філософія"
    RELIGION = "релігія"
    TRAVEL = "подорожі"
    COOKING = "кулінарія"
    GRAPHIC_NOVEL = "графічний роман"


STATUS_REWRITE_RULES = {
    BookStatus.NEW: [BookStatus.PREORDER, BookStatus.COMING_SOON],
    BookStatus.PREORDER: [BookStatus.COMING_SOON],
    BookStatus.COMING_SOON: [],
}
