import base64

import pytest
from googleapiclient.errors import HttpError
from unittest.mock import MagicMock, patch

from gmail_api_client import (
    GmailClient,
    GmailDraftError,
    GmailSendError,
)


@pytest.fixture
def gmail_client():
    """Create a GmailClient with mocked authentication."""

    with patch.object(
        GmailClient,
        "_authenticate",
        return_value=MagicMock(),
    ):
        client = GmailClient()

    return client


def test_create_message():
    message = GmailClient._create_message(
        to="recipient@example.com",
        subject="Test Subject",
        body="Test Body",
    )

    assert message["To"] == "recipient@example.com"
    assert message["Subject"] == "Test Subject"

    assert message.get_content_type() == "multipart/alternative"

    parts = message.get_payload()

    assert len(parts) == 2

    plain_part = parts[0]
    html_part = parts[1]

    assert plain_part.get_content_type() == "text/plain"
    assert html_part.get_content_type() == "text/html"

    assert plain_part.get_content().strip() == "Test Body"
    assert "Test Body" in html_part.get_content()


def test_create_message_with_sender():
    message = GmailClient._create_message(
        to="recipient@example.com",
        subject="Test Subject",
        body="Test Body",
        sender="sender@example.com",
    )

    assert message["From"] == "sender@example.com"
    assert message["To"] == "recipient@example.com"


def test_encode_message():
    message = GmailClient._create_message(
        to="recipient@example.com",
        subject="Test Subject",
        body="Test Body",
    )

    encoded = GmailClient._encode_message(message)

    assert isinstance(encoded, str)

    decoded = base64.urlsafe_b64decode(
        encoded
    ).decode()

    assert "recipient@example.com" in decoded
    assert "Test Subject" in decoded
    assert "Test Body" in decoded


def test_create_draft(gmail_client):
    mock_execute = MagicMock(
        return_value={
            "id": "draft-123",
            "message": {
                "id": "message-123",
            },
        }
    )

    gmail_client.service.users.return_value \
        .drafts.return_value \
        .create.return_value \
        .execute = mock_execute

    result = gmail_client.create_draft(
        to="recipient@example.com",
        subject="Test Draft",
        body="Draft body",
    )

    assert result["id"] == "draft-123"

    gmail_client.service.users.return_value \
        .drafts.return_value \
        .create.assert_called_once()


def test_send_mail(gmail_client):
    mock_execute = MagicMock(
        return_value={
            "id": "message-123",
        }
    )

    gmail_client.service.users.return_value \
        .messages.return_value \
        .send.return_value \
        .execute = mock_execute

    result = gmail_client.send_mail(
        to="recipient@example.com",
        subject="Test Email",
        body="Email body",
    )

    assert result["id"] == "message-123"

    gmail_client.service.users.return_value \
        .messages.return_value \
        .send.assert_called_once()


def test_create_draft_raises_gmail_draft_error(
    gmail_client,
):
    http_error = HttpError(
        resp=MagicMock(status=403),
        content=b'{"error": "Permission denied"}',
    )

    (
        gmail_client.service.users.return_value
        .drafts.return_value
        .create.return_value
        .execute.side_effect
    ) = http_error

    with pytest.raises(GmailDraftError):
        gmail_client.create_draft(
            to="recipient@example.com",
            subject="Test",
            body="Test",
        )


def test_send_mail_raises_gmail_send_error(
    gmail_client,
):
    http_error = HttpError(
        resp=MagicMock(status=403),
        content=b'{"error": "Permission denied"}',
    )

    (
        gmail_client.service.users.return_value
        .messages.return_value
        .send.return_value
        .execute.side_effect
    ) = http_error

    with pytest.raises(GmailSendError):
        gmail_client.send_mail(
            to="recipient@example.com",
            subject="Test",
            body="Test",
        )