import smtplib
from email.mime.text import MIMEText

def send_verification_email(email, code):
    msg = MIMEText(f"Your verification code is: {code}")
    msg["Subject"] = "Verification Code"
    msg["From"] = "noreply@nexly.com"
    msg["To"] = email

    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 587) as server:
        server.login("27f99dd378fdf4", "67bf1fe41458aa")
        server.send_message(msg)
