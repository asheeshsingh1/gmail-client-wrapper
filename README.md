# Gmail API Automation

A simple Python project for interacting with Gmail using the **Gmail API** and **OAuth 2.0**.

This project supports:

* Creating Gmail drafts
* Sending emails
* OAuth 2.0 authentication
* Reusing authenticated credentials through `token.json`
* Programmatic email composition using Python's `EmailMessage`

---

## Features

### Create Drafts

Create a Gmail draft programmatically:

```python
gmail_create_draft(
    to="recipient@example.com",
    subject="Automated draft",
    body="This is an automated draft."
)
```

### Send Emails

Send an email directly through Gmail:

```python
gmail_send_mail(
    to="recipient@example.com",
    subject="Automated email",
    body="This email was sent using the Gmail API."
)
```

---

## Architecture

```text
Python Application
       │
       ▼
OAuth 2.0 Authentication
       │
       ▼
   Gmail API
       │
       ├── Create Draft
       │
       └── Send Email
```

The application uses Google's OAuth 2.0 flow for a local desktop application.

```text
credentials.json
       │
       ▼
Google OAuth Login
       │
       ▼
   token.json
       │
       ▼
Gmail API Client
```

---

## Tech Stack

* Python 3
* Gmail API
* Google OAuth 2.0
* `google-api-python-client`
* `google-auth`
* `google-auth-oauthlib`

---

## Project Structure

```text
gmail/
│
├── main.py
├── credentials.json
├── token.json
├── .gitignore
└── README.md
```

### Files

| File               | Description                                           |
| ------------------ | ----------------------------------------------------- |
| `main.py`          | Gmail API implementation                              |
| `credentials.json` | OAuth client credentials downloaded from Google Cloud |
| `token.json`       | Generated OAuth access/refresh token                  |
| `.gitignore`       | Prevents credentials from being committed             |
| `README.md`        | Project documentation                                 |

---

# Setup

## 1. Create a Google Cloud Project

Go to the [Google Cloud Console](https://console.cloud.google.com/).

Create a new project or use an existing project.

---

## 2. Enable Gmail API

Open the API Library and enable:

**Gmail API**

You can also enable it using the Google Cloud CLI:

```bash
gcloud services enable gmail.googleapis.com
```

---

## 3. Configure OAuth Consent Screen

In Google Cloud Console:

```text
Google Auth Platform
        ↓
Branding
        ↓
Configure OAuth consent screen
```

Configure the application information.

For a personal/local application, you can use the appropriate testing configuration.

Add your Gmail account as a test user if the application is in testing mode.

---

## 4. Create OAuth Client

Go to:

```text
Google Auth Platform
        ↓
Clients
        ↓
Create Client
```

Select:

```text
Application type: Desktop app
```

Download the generated credentials file.

Rename it:

```text
credentials.json
```

Place it in the project root:

```text
gmail/
├── main.py
├── credentials.json
└── README.md
```

---

# Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -U \
    google-api-python-client \
    google-auth-httplib2 \
    google-auth-oauthlib
```

---

# Gmail OAuth Scope

The application uses:

```python
SCOPES = [
    "https://www.googleapis.com/auth/gmail.compose"
]
```

The `gmail.compose` scope allows the application to:

* Create drafts
* Read/write draft content
* Send messages

The application does not request full Gmail access when it isn't required.

---

# Authentication

The first time you run:

```bash
python main.py
```

Google will open a browser window.

Sign in with the Gmail account you want the application to use and grant the requested Gmail permissions.

After successful authentication, the application creates:

```text
token.json
```

The token is reused on subsequent executions.

You normally won't need to authenticate again unless the token is revoked or the requested scopes change.

---

# Important: Changing OAuth Scopes

If you change:

```python
SCOPES = [...]
```

delete the existing token:

```bash
rm token.json
```

Then run:

```bash
python main.py
```

Google will request authorization again with the new scopes.

---

# Creating a Draft

Example:

```python
gmail_create_draft(
    to="recipient@example.com",
    subject="Automated Draft",
    body="This is an automated draft."
)
```

The Gmail API returns a draft object containing the draft ID and associated message information.

Example output:

```text
Draft created successfully.
Draft ID: r123456789
```

The draft will appear in the Gmail **Drafts** folder.

---

# Sending an Email

Example:

```python
gmail_send_mail(
    to="recipient@example.com",
    subject="Automated Email",
    body="This email was sent using the Gmail API."
)
```

Example output:

```text
Email sent successfully.
Message ID: 18abc123456
```

The message will be sent directly through the authenticated Gmail account.

---

# Example

```python
from main import gmail_create_draft, gmail_send_mail


# Create a draft
gmail_create_draft(
    to="recipient@example.com",
    subject="Test Draft",
    body="This is a test draft."
)


# Send an email
gmail_send_mail(
    to="recipient@example.com",
    subject="Test Email",
    body="This is a test email."
)
```

---

# Security

**Never commit your OAuth credentials to Git.**

Add the following to `.gitignore`:

```gitignore
credentials.json
token.json
.venv/
__pycache__/
*.pyc
.env
```

Your `.gitignore` should look like:

```gitignore
# Google OAuth credentials
credentials.json
token.json

# Python
.venv/
__pycache__/
*.pyc

# Environment variables
.env

# macOS
.DS_Store
```

If credentials are accidentally committed to a public repository, revoke them immediately from Google Cloud and generate new credentials.

---

# Troubleshooting

## 403: Insufficient Authentication Scopes

If you see:

```text
HttpError 403
Request had insufficient authentication scopes
```

delete the existing token:

```bash
rm token.json
```

Then authenticate again:

```bash
python main.py
```

Make sure the required scope is present:

```python
SCOPES = [
    "https://www.googleapis.com/auth/gmail.compose"
]
```

---

## 403: Gmail API Has Not Been Used

If you see:

```text
Gmail API has not been used in project ... before
or it is disabled
```

enable Gmail API for the Google Cloud project associated with your OAuth credentials:

```bash
gcloud services enable gmail.googleapis.com
```

You can also enable it from the Google Cloud Console.

After enabling the API, wait a few minutes and run:

```bash
python main.py
```

again.

---

## Invalid Credentials

If you see an OAuth/client configuration error, verify that:

```text
credentials.json
```

is present in the project root and was downloaded from the correct Google Cloud project.

---

# Future Improvements

Possible extensions for this project:

* HTML email support
* CC and BCC
* File attachments
* Inline images
* Reply to an existing email
* Reply within an existing Gmail thread
* Forward emails
* Search Gmail messages
* Read emails
* Manage labels
* Delete drafts
* Schedule email workflows
* Email templates
* CLI interface
* FastAPI service around Gmail operations
* AI-powered email generation

---

# References

* [Gmail API](https://developers.google.com/workspace/gmail/api)
* [Gmail API Python Quickstart](https://developers.google.com/workspace/gmail/api/quickstart/python)
* [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
* [Google Cloud Console](https://console.cloud.google.com/)

---

## License

This project is for educational and personal automation purposes.
