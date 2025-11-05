import os
from datetime import timedelta

class Config:
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tubitak-2209-gizli-anahtar-2024'
    
    # Database configuration
    # PostgreSQL (Render'da) veya SQLite (local'de) kullan
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        # Render PostgreSQL URL'i postgres:// ile başlıyor, SQLAlchemy postgresql:// istiyor
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Local development için SQLite
        SQLALCHEMY_DATABASE_URI = 'sqlite:///tubitak2209.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload folder configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'xlsx', 'xls', 'pptx', 'ppt', 'txt', 'jpg', 'jpeg', 'png', 'gif'}
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Mail configuration (Gmail)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '2209takip@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'mrkldvjkskmzzgpa'  # App Password (boşluksuz: mrkl dvjk skmz zgpa)
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME') or '2209takip@gmail.com'
    MAIL_MAX_EMAILS = None
    MAIL_ASCII_ATTACHMENTS = False

