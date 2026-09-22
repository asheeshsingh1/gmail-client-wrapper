class GmailAPIError(Exception):
    """Base exception for all Gmail API client errors."""


class GmailAuthenticationError(GmailAPIError):
    """Raised when Gmail authentication fails."""


class GmailDraftError(GmailAPIError):
    """Raised when creating a Gmail draft fails."""


class GmailSendError(GmailAPIError):
    """Raised when sending an email fails."""