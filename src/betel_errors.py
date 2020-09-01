class BetelError(Exception):
    """Raise when an exception occurs."""


class PlayScrapingError(BetelError):
    """Raise when certain attributes can't be found within the Play page."""


class AccessError(BetelError):
    """Raise on URL or HTTP errors."""
    def __init__(self, message, exception):
        super(AccessError, self).__init__(message + (": %s" % exception))
