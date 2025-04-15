from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'sua_chave_secreta_aqui'
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy()