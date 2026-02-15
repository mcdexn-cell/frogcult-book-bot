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
    MANGA = "манга"
    COMICS = "комікси"


class BookGenreCategory(StrEnum):
    """
    Enum for book genre category.
    """

    FANTASY_FANTASTIC = 'фантастика, фентезі'
    DETECTIVE_THRILLER = 'детективи, трилери'
    ROMANCE = 'романи'
    NONFICTION = 'нон-фікшн'
    GRAPHIC = 'графічні'
    OTHER = 'інше'


GENRE_TO_CATEGORY_MAP = {
    BookGenre.FANTASY: BookGenreCategory.FANTASY_FANTASTIC,
    BookGenre.SCIENCE_FICTION: BookGenreCategory.FANTASY_FANTASTIC,
    BookGenre.THRILLER: BookGenreCategory.DETECTIVE_THRILLER,
    BookGenre.HORROR: BookGenreCategory.DETECTIVE_THRILLER,
    BookGenre.DETECTIVE: BookGenreCategory.DETECTIVE_THRILLER,
    BookGenre.ACTION: BookGenreCategory.ROMANCE,
    BookGenre.ADVENTURE: BookGenreCategory.ROMANCE,
    BookGenre.HISTORICAL_NOVEL: BookGenreCategory.ROMANCE,
    BookGenre.ROMANCE: BookGenreCategory.ROMANCE,
    BookGenre.DRAMA: BookGenreCategory.ROMANCE,
    BookGenre.COMEDY: BookGenreCategory.ROMANCE,
    BookGenre.MYSTICISM: BookGenreCategory.ROMANCE,
    BookGenre.FOLKLORE: BookGenreCategory.OTHER,
    BookGenre.POETRY: BookGenreCategory.OTHER,
    BookGenre.PROSE: BookGenreCategory.ROMANCE,
    BookGenre.CLASSIC_LITERATURE: BookGenreCategory.ROMANCE,
    BookGenre.CONTEMPORARY_LITERATURE: BookGenreCategory.ROMANCE,
    BookGenre.BIOGRAPHY: BookGenreCategory.OTHER,
    BookGenre.PSYCHOLOGICAL_PROSE: BookGenreCategory.ROMANCE,
    BookGenre.PHILOSOPHICAL_PROSE: BookGenreCategory.ROMANCE,
    BookGenre.SOCIAL_PROSE: BookGenreCategory.ROMANCE,
    BookGenre.POST_APOCALYPTIC: BookGenreCategory.FANTASY_FANTASTIC,
    BookGenre.DYSTOPIA: BookGenreCategory.FANTASY_FANTASTIC,
    BookGenre.UTOPIA: BookGenreCategory.FANTASY_FANTASTIC,
    BookGenre.CYBERPUNK: BookGenreCategory.FANTASY_FANTASTIC,
    BookGenre.STEAMPUNK: BookGenreCategory.FANTASY_FANTASTIC,
    BookGenre.SPACE_OPERA: BookGenreCategory.FANTASY_FANTASTIC,
    BookGenre.MILITARY_FICTION: BookGenreCategory.FANTASY_FANTASTIC,
    BookGenre.URBAN_FANTASY: BookGenreCategory.FANTASY_FANTASTIC,
    BookGenre.EPIC_FANTASY: BookGenreCategory.FANTASY_FANTASTIC,
    BookGenre.DARK_FANTASY: BookGenreCategory.FANTASY_FANTASTIC,
    BookGenre.PARANORMAL_ROMANCE: BookGenreCategory.FANTASY_FANTASTIC,
    BookGenre.SPY_NOVEL: BookGenreCategory.DETECTIVE_THRILLER,
    BookGenre.POLITICAL_THRILLER: BookGenreCategory.DETECTIVE_THRILLER,
    BookGenre.CRIME_NOVEL: BookGenreCategory.DETECTIVE_THRILLER,
    BookGenre.NOIR: BookGenreCategory.DETECTIVE_THRILLER,
    BookGenre.WESTERN: BookGenreCategory.DETECTIVE_THRILLER,
    BookGenre.FAMILY_SAGA: BookGenreCategory.ROMANCE,
    BookGenre.EROTICA: BookGenreCategory.ROMANCE,
    BookGenre.YOUNG_ADULT: BookGenreCategory.ROMANCE,
    BookGenre.CHILDREN_LITERATURE: BookGenreCategory.OTHER,
    BookGenre.JOURNALISM: BookGenreCategory.NONFICTION,
    BookGenre.ACADEMIC_LITERATURE: BookGenreCategory.NONFICTION,
    BookGenre.POPULAR_SCIENCE: BookGenreCategory.NONFICTION,
    BookGenre.SELF_HELP: BookGenreCategory.NONFICTION,
    BookGenre.BUSINESS: BookGenreCategory.NONFICTION,
    BookGenre.PSYCHOLOGY: BookGenreCategory.NONFICTION,
    BookGenre.PHILOSOPHY: BookGenreCategory.NONFICTION,
    BookGenre.RELIGION: BookGenreCategory.NONFICTION,
    BookGenre.TRAVEL: BookGenreCategory.NONFICTION,
    BookGenre.COOKING: BookGenreCategory.NONFICTION,
    BookGenre.GRAPHIC_NOVEL: BookGenreCategory.GRAPHIC,
    BookGenre.COMICS: BookGenreCategory.GRAPHIC,
    BookGenre.MANGA: BookGenreCategory.GRAPHIC,
}


STATUS_REWRITE_RULES = {
    BookStatus.NEW: [BookStatus.PREORDER, BookStatus.COMING_SOON],
    BookStatus.PREORDER: [BookStatus.COMING_SOON],
    BookStatus.COMING_SOON: [],
}


BOOK_STATUS_UKRAINIAN_TEXT = {
    BookStatus.NEW: 'новинки',
    BookStatus.PREORDER: 'передзамовлення',
    BookStatus.COMING_SOON: 'анонс',
}
