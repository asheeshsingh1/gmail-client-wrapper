from gmail_api_client import GmailClient


gmail = GmailClient(
    credentials_path="credentials.json",
    token_path="token.json",
)

gmail.create_draft(
    to="recipient@example.com",
    subject="Test Draft",
    body="This is a test draft.",
)

gmail.send_mail(
    to="recipient@example.com",
    subject="Test Email",
    body="This is a test email.",
)