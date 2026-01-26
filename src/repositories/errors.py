"""
Provide errors for repositories.
"""

class BookRepositoryError(Exception):
    """
    Base book repository error.
    """


class IsbnBatchIsTooBigError(BookRepositoryError):
    """
    Error raised when ISBN batch is too big.
    """
