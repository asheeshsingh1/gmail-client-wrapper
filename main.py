import os
import base64
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = [
    "https://www.googleapis.com/auth/gmail.compose"
]


def get_gmail_service():
    """Authenticate and return Gmail API service."""

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build(
        "gmail",
        "v1",
        credentials=creds
    )


def create_email(
    to: str,
    subject: str,
    body: str,
    sender: str = None
):
    """Create an EmailMessage object."""

    message = EmailMessage()

    message.set_content(body)

    if sender:
        message["From"] = sender

    message["To"] = to
    message["Subject"] = subject

    return message


def encode_message(message: EmailMessage) -> str:
    """Encode an email message for Gmail API."""

    return base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()


def gmail_create_draft(
    to: str,
    subject: str,
    body: str,
    sender: str = None
):
    """Create a Gmail draft."""

    try:
        service = get_gmail_service()

        message = create_email(
            to=to,
            subject=subject,
            body=body,
            sender=sender
        )

        encoded_message = encode_message(message)

        create_message = {
            "message": {
                "raw": encoded_message
            }
        }

        draft = (
            service.users()
            .drafts()
            .create(
                userId="me",
                body=create_message
            )
            .execute()
        )

        print(f"Draft created successfully.")
        print(f"Draft ID: {draft['id']}")

        return draft

    except HttpError as error:
        print(f"An error occurred while creating draft: {error}")
        return None


def gmail_send_mail(
    to: str,
    subject: str,
    body: str,
    sender: str = None
):
    """Send an email using Gmail API."""

    try:
        service = get_gmail_service()

        message = create_email(
            to=to,
            subject=subject,
            body=body,
            sender=sender
        )

        encoded_message = encode_message(message)

        send_message = {
            "raw": encoded_message
        }

        sent_message = (
            service.users()
            .messages()
            .send(
                userId="me",
                body=send_message
            )
            .execute()
        )

        print("Email sent successfully.")
        print(f"Message ID: {sent_message['id']}")

        return sent_message

    except HttpError as error:
        print(f"An error occurred while sending email: {error}")
        return None


if __name__ == "__main__":

    # Create draft
    gmail_create_draft(
        to="asheesh1.singh@gmail.com",
        subject="Automated draft",
        body="This is automated draft mail",
        sender="asheeshsingh0112@gmail.com"
    )

    # Send email
    gmail_send_mail(
        to="asheesh1.singh@gmail.com",
        subject="Automated email",
        body="This is an automated email sent using the Gmail API.",
        sender="asheeshsingh0112@gmail.com"
    )