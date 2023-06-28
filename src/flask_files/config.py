from dotenv import load_dotenv
import os

class Config:
    load_dotenv()
    SECRET_KEY = os.environ.get('SECRET_KEY')
    URI = os.environ.get('URI')
    sendgrid_key = os.environ.get('SENDGRID_API_KEY')