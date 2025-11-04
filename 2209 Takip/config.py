import os
from datetime import timedelta

class Config:
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tubitak-2209-gizli-anahtar-2024'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tubitak2209.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload folder configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'xlsx', 'xls', 'pptx', 'ppt', 'txt', 'jpg', 'jpeg', 'png', 'gif'}
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

