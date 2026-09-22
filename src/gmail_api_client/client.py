import base64
import os
from email.message import EmailMessage
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource, build
from googleapiclient.errors import HttpError

from .exceptions import (
    GmailAuthenticationError,
    GmailDraftError,
    GmailSendError,
)


SCOPES = [
    "https://www.googleapis.com/auth/gmail.compose"
]


class GmailClient:
    """Client for interacting with the Gmail API."""

    def __init__(
        self,
        credentials_path: str = "credentials.json",
        token_path: str = "token.json",
    ):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = self._authenticate()

    def _authenticate(self) -> Resource:
        """Authenticate the user and create Gmail API service."""

        creds: Optional[Credentials] = None

        try:
            if os.path.exists(self.token_path):
                creds = Credentials.from_authorized_user_file(
                    self.token_path,
                    SCOPES,
                )

            if not creds or not creds.valid:

                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())

                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path,
                        SCOPES,
                    )

                    creds = flow.run_local_server(port=0)

                with open(self.token_path, "w") as token:
                    token.write(creds.to_json())

            return build(
                "gmail",
                "v1",
                credentials=creds,
            )

        except Exception as error:
            raise GmailAuthenticationError(
                f"Failed to authenticate with Gmail: {error}"
            ) from error

    @staticmethod
    def _create_message(
        to: str,
        subject: str,
        body: str,
        sender: Optional[str] = None,
    ) -> EmailMessage:
        """Create an email message."""

        message = EmailMessage()

        message.set_content(body)

        if sender:
            message["From"] = sender

        message["To"] = to
        message["Subject"] = subject

        return message

    @staticmethod
    def _encode_message(message: EmailMessage) -> str:
        """Encode an email for the Gmail API."""

        return base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode()

    def create_draft(
        self,
        to: str,
        subject: str,
        body: str,
        sender: Optional[str] = None,
    ):
        """Create a Gmail draft."""

        try:
            message = self._create_message(
                to=to,
                subject=subject,
                body=body,
                sender=sender,
            )

            encoded_message = self._encode_message(message)

            return (
                self.service.users()
                .drafts()
                .create(
                    userId="me",
                    body={
                        "message": {
                            "raw": encoded_message,
                        }
                    },
                )
                .execute()
            )

        except HttpError as error:
            raise GmailDraftError(
                f"Failed to create Gmail draft: {error}"
            ) from error

    def send_mail(
        self,
        to: str,
        subject: str,
        body: str,
        sender: Optional[str] = None,
    ):
        """Send an email through Gmail."""

        try:
            message = self._create_message(
                to=to,
                subject=subject,
                body=body,
                sender=sender,
            )

            encoded_message = self._encode_message(message)

            return (
                self.service.users()
                .messages()
                .send(
                    userId="me",
                    body={
                        "raw": encoded_message,
                    },
                )
                .execute()
            )

        except HttpError as error:
            raise GmailSendError(
                f"Failed to send Gmail message: {error}"
            ) from error