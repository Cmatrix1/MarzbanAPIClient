class MarzbanAPIException(Exception):
    """Base class for Marzban API exceptions."""
    pass

class ValidationError(MarzbanAPIException):
    """Raised for validation errors (HTTP 422)."""
    pass

class ConflictError(MarzbanAPIException):
    """Raised for conflict errors, such as when a resource already exists (HTTP 409)."""
    pass

class UnauthorizedError(MarzbanAPIException):
    """Raised for unauthorized access errors (HTTP 403)."""
    pass

class NotFoundError(MarzbanAPIException):
    """Raised when a resource is not found (HTTP 404)."""
    pass

class BadRequestError(MarzbanAPIException):
    """Raised for bad request errors, such as date issues (HTTP 400)."""
    pass

class TokenError(MarzbanAPIException):
    """Raised when there is an issue with authentication tokens."""
    pass
