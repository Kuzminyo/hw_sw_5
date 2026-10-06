class ExchangeError(Exception):
    """Base class for all errors raised by the exchange package."""


class InvalidDaysError(ExchangeError):
    """Requested number of days is outside the allowed range."""


class ExchangeApiError(ExchangeError):
    """The remote API could not be reached or returned unusable data."""
