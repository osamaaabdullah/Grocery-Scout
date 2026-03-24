from fastapi import HTTPException, status


class AppError(Exception):
    """Base class for all app exceptions. Never raise this directly."""
    def __init__(self, message: str = "An unexpected error occurred"):
        self.message = message
        super().__init__(message)

class AppInvalidTokenError(AppError):
    def __init__(self, message: str = "Invalid or expired token"):
        super().__init__(message)

class TokenExpiredError(AppInvalidTokenError):
    def __init__(self):
        super().__init__("Token has expired")


class InactiveUserError(AppError):
    def __init__(self):
        super().__init__("This account is inactive")


class UnverifiedUserError(AppError):
    def __init__(self):
        super().__init__("Email address has not been verified")


class InvalidCredentialsError(AppError):
    def __init__(self):
        super().__init__("Incorrect email or password")


class InsufficientPermissionsError(AppError):
    def __init__(self):
        super().__init__("You do not have permission to perform this action")


class UserNotFoundError(AppError):
    def __init__(self, email: str | None = None):
        msg = f"User '{email}' not found" if email else "User not found"
        super().__init__(msg)


class UserAlreadyExistsError(AppError):
    def __init__(self, email: str | None = None):
        msg = f"User '{email}' already exists" if email else "User already exists"
        super().__init__(msg)


class AlreadyVerifiedError(AppError):
    def __init__(self):
        super().__init__("This account is already verified")


class WeakPasswordError(AppError):
    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__("Password does not meet requirements")
        
class InvalidPostalCodeError(AppError):
    def __init__(self):
        super().__init__("Postal code is invalid")

EXCEPTION_MAP: dict[type[AppError], tuple[int, str]] = {
    InvalidPostalCodeError:      (status.HTTP_400_BAD_REQUEST, "Invalid postal code"),
    AppInvalidTokenError:        (status.HTTP_401_UNAUTHORIZED, "Invalid or expired token"),
    TokenExpiredError:           (status.HTTP_401_UNAUTHORIZED, "Token has expired"),
    InvalidCredentialsError:     (status.HTTP_401_UNAUTHORIZED, "Incorrect email or password"),
    InactiveUserError:           (status.HTTP_403_FORBIDDEN,    "Account is inactive"),
    UnverifiedUserError:         (status.HTTP_403_FORBIDDEN,    "Email not verified"),
    InsufficientPermissionsError:(status.HTTP_403_FORBIDDEN,    "Insufficient permissions"),
    UserNotFoundError:           (status.HTTP_404_NOT_FOUND,    "User not found"),
    UserAlreadyExistsError:      (status.HTTP_409_CONFLICT,     "User already exists"),
    AlreadyVerifiedError:        (status.HTTP_409_CONFLICT,     "Already verified"),
    WeakPasswordError:           (status.HTTP_422_UNPROCESSABLE_CONTENT, "Weak password"),
}


def to_http_exception(exc: AppError) -> HTTPException:
    status_code, detail = EXCEPTION_MAP.get(type(exc), (500, exc.message))
    
    # WeakPasswordError returns the full list of failures
    if isinstance(exc, WeakPasswordError):
        detail = exc.errors

    return HTTPException(status_code=status_code, detail=detail)