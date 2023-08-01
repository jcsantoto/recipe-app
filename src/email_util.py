from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from itsdangerous import URLSafeTimedSerializer
from src.flask_files.config import Config
from flask import url_for

serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
api_key = Config.sendgrid_key
sender_email = 'foodcraft@surfluxlabs.top'


def send_email(message: Mail):
    """
    Sends the email provided in the parameter using SendGrid API
    :param message: Mail object
    :return: None
    """
    sg = SendGridAPIClient(api_key=api_key)
    response = sg.send(message)

    if response.status_code == 202:
        print('Email sent successfully!')
    else:
        print('Email sending failed.')
        print(response.body)


def create_message(recipient: str, subject: str, body: str):
    """
    Creates and returns a Mail object with the specified parameters
    :param recipient: The email address of the recipient
    :param subject: The subject of the email
    :param body: The body of the email
    :return: Mail object
    """
    message = Mail(
        from_email=sender_email,
        to_emails=recipient,
        subject=subject,
        plain_text_content=body
    )

    return message


def create_confirmation_email(recipient: str, confirmation_link: str):
    """
    Creates the confirmation email
    :param recipient: The email address of the recipient
    :param confirmation_link: Confirmation link
    :return: Mail object
    """
    subject = 'Confirm Your Email'

    body = f"Please click the following link to confirm your email:\n {confirmation_link} \nThis link will expire in 15 minutes."

    message = create_message(recipient, subject, body)

    return message


def create_password_reset_email(recipient: str, reset_link: str):
    """
    Creates the password reset email
    :param recipient: The email address of the recipient
    :param reset_link: Reset link
    :return: Mail object
    """
    subject = 'Reset Your Password'

    body = f"Please click the following link to reset your password:\n {reset_link} \nThis link will expire in 15 minutes."

    message = create_message(recipient, subject, body)

    return message


def generate_token(email, salt):
    """
    Generates the token specific to user's email
    :param email: recipient email
    :param salt: salt
    :return: token
    """
    return serializer.dumps(email, salt=salt)


def confirm_token(token, salt, expiration=900):
    """
    Verifies token and returns the email address that was associated.
    :param token: The token needed to verify a user's email address
    :param salt: salt
    :param expiration: How long in seconds before the token expires
    :return: email address
    """
    try:
        email = serializer.loads(
            token,
            salt=salt,
            max_age=expiration
        )
        return email
    except:
        return None


def generate_confirmation_link(token, route):
    confirmation_link = url_for(route, token=token, _external=True)
    return confirmation_link
