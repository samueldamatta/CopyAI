class DomainException(Exception):
    """Base class for all domain exceptions."""


class UserNotFoundError(DomainException):
    pass


class UserAlreadyExistsError(DomainException):
    pass


class InvalidCredentialsError(DomainException):
    pass


class InactiveUserError(DomainException):
    pass


class ConversationNotFoundError(DomainException):
    pass


class DocumentNotFoundError(DomainException):
    pass
