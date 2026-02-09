"""
Provide exceptions for users.
"""

class UserError(Exception):
    """
    Base user error.
    """


class AuthorSubscriptionLimitReachedError(UserError):
    """
    Error thrown when author's subscription limit is reached.
    """
