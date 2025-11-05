from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# İlişki tablosu: Öğrenci - Sınıf (Çoka-Çok ilişki)
student_classes = db.Table('student_classes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('class_id', db.Integer, db.ForeignKey('class.id'), primary_key=True),
    db.Column('enrolled_at', db.DateTime, default=datetime.utcnow)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # 'admin' or 'student'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # İlişkiler
    enrolled_classes = db.relationship('Class', secondary=student_classes, 
                                       backref=db.backref('students', lazy='dynamic'))
    submissions = db.relationship('Submission', backref='student', lazy=True, cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy=True, cascade='all, delete-orphan', 
                                   foreign_keys='Notification.user_id')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # İlişkiler
    assignments = db.relationship('Assignment', backref='class_ref', lazy=True, cascade='all, delete-orphan')
    creator = db.relationship('User', foreign_keys=[created_by])
    
    def __repr__(self):
        return f'<Class {self.name}>'

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    max_score = db.Column(db.Integer, default=100)
    
    # İlişkiler
    submissions = db.relationship('Submission', backref='assignment', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Assignment {self.title}>'

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    student_comment = db.Column(db.Text)  # Öğrenci açıklaması
    score = db.Column(db.Integer)
    feedback = db.Column(db.Text)
    graded_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Submission {self.id} - Assignment {self.assignment_id}>'

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    file_name = db.Column(db.String(255))
    file_path = db.Column(db.String(500))
    is_important = db.Column(db.Boolean, default=False)
    
    # İlişkiler
    creator = db.relationship('User', foreign_keys=[created_by])
    class_ref = db.relationship('Class', backref=db.backref('announcements', lazy=True, cascade='all, delete-orphan'))
    reads = db.relationship('AnnouncementRead', backref='announcement', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Announcement {self.title}>'

class AnnouncementRead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    announcement_id = db.Column(db.Integer, db.ForeignKey('announcement.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    read_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # İlişkiler
    student = db.relationship('User', foreign_keys=[student_id])
    
    def __repr__(self):
        return f'<AnnouncementRead {self.announcement_id} by {self.student_id}>'

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'assignment', 'grade', 'announcement', 'submission', 'enrollment'
    icon = db.Column(db.String(50), default='bi-bell')  # Bootstrap icon class
    link = db.Column(db.String(500))  # Tıklayınca gidilecek link
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Notification {self.id} - {self.title}>'

class ProgramAnnouncement(db.Model):
    """TÜBİTAK 2209-A Programı ile ilgili genel duyurular"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    external_link = db.Column(db.String(500))  # TÜBİTAK sitesine link
    is_important = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)  # Aktif/pasif
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    creator = db.relationship('User', foreign_keys=[created_by])
    
    def __repr__(self):
        return f'<ProgramAnnouncement {self.id} - {self.title}>'

