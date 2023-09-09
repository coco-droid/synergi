import imaplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def mail_tool(action, params):
    if action == "send":
        # Set up SMTP connection
        if params["sender_profile"] == "gmail":
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
        elif params["sender_profile"] == "yahoo":
            smtp_server = "smtp.mail.yahoo.com"
            smtp_port = 587
        elif params["sender_profile"] == "proton":
            smtp_server = "mail.protonmail.com"
            smtp_port = 587
        else:
            raise ValueError("Invalid sender profile")

        # Set up message
        if params["is_html"]:
            msg = MIMEMultipart()
            msg.attach(MIMEText(params["message"], 'html'))
        else:
            msg = MIMEText(params["message"])

        # Set up sender and recipient
        msg['From'] = params["username"]
        msg['To'] = params["recipient_email"]

        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(params["username"], params["password"])
            server.sendmail(params["username"], params["recipient_email"], msg.as_string())

    elif action == "get":
        # Set up IMAP connection
        if params["sender_profile"] == "gmail":
            imap_server = "imap.gmail.com"
            imap_port = 993
        elif params["sender_profile"] == "yahoo":
            imap_server = "imap.mail.yahoo.com"
            imap_port = 993
        elif params["sender_profile"] == "proton":
            imap_server = "mail.protonmail.com"
            imap_port = 993
        else:
            raise ValueError("Invalid sender profile")

        # Log in to account
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)
        mail.login(params["username"], params["password"])

        # Select mailbox
        mail.select("inbox")

        # Search for emails
        result, data = mail.search(None, params["date_filter"])
        email_ids = data[0].split()

        # Get email data
        emails = []
        for email_id in email_ids:
            result, data = mail.fetch(email_id, "(RFC822)")
            emails.append(data[0][1])

        # Close mailbox
        mail.close()
        mail.logout()

        return emails

    else:
        raise ValueError("Invalid action")

# Example usage
params = {
    "sender_profile": "gmail",
    "username": "robensjeanbaptiste29@gmail.com",
    "password": "robegeniepanda2004",
    "recipient_email": "friseurdefeise@gmail.com",
    "message": "Hello, world!",
    "is_html": False
}
mail_tool("send", params)

params = {
    "sender_profile": "gmail",
    "username": "friseurdefeise@gmail.com",
    "password": "robegeniepanda2004",
    "date_filter": "SINCE 01-Jan-2022"
}
emails = mail_tool("get", params)
print(emails)
