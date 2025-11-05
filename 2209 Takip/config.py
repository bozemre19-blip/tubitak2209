import os
from datetime import timedelta

class Config:
    # Secret key for session management - MUST be set via environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError(
            "SECRET_KEY environment variable must be set! "
            "For local development, create a .env file with: SECRET_KEY=your-secret-key-here"
        )
    
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
    
    # Site URL (Render'da veya local'de)
    BASE_URL = os.environ.get('BASE_URL') or 'https://tubitak2209.onrender.com'

