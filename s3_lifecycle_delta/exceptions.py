# s3_lifecycle_delta/exceptions.py

class LifecycleError(Exception):
    """Base exception for s3_lifecycle_delta policy errors."""
    def __init__(self, message: str = None, *, details: dict = None):
        super().__init__(message)
        self.details = details or {}

class ValidationError(LifecycleError):
    """Raised when s3_lifecycle_delta policy validation fails."""
    pass

class DiffError(LifecycleError):
    """Raised when diff computation encounters an error."""
    pass

class ApplyError(LifecycleError):
    """Raised when applying s3_lifecycle_delta policy to S3 fails."""
    pass
