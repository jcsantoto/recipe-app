from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from itsdangerous import URLSafeTimedSerializer
from src.flask_files.config import Config

serializer = URLSafeTimedSerializer(Config.SECRET_KEY)

api_key = Config.sendgrid_key
sender_email = 'foodcraft@surfluxlabs.top'


def send_email(message: Mail):
    sg = SendGridAPIClient(api_key=api_key)
    response = sg.send(message)

    if response.status_code == 202:
        print('Email sent successfully!')
    else:
        print('Email sending failed.')
        print(response.body)


def create_message(recipient: str, subject: str, body: str):
    message = Mail(
        from_email=sender_email,
        to_emails=recipient,
        subject=subject,
        plain_text_content=body
    )

    return message


def create_confirmation_email(recipient: str, confirmation_link: str):
    subject = 'Confirm Your Email'

    body = f"Please click the following link to confirm your email:\n {confirmation_link} \nThis link will expire in 15 minutes."

    message = Mail(
        from_email=sender_email,
        to_emails=recipient,
        subject=subject,
        plain_text_content=body)

    return message


def generate_token(email, salt):
    return serializer.dumps(email, salt=salt)


def confirm_token(token, salt, expiration=900):
    try:
        email = serializer.loads(
            token,
            salt=salt,
            max_age=expiration
        )
        return email
    except:
        return None
