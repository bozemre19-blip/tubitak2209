from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from config import Config
from models import db, User, Class, Assignment, Submission, Announcement, AnnouncementRead, Notification, ProgramAnnouncement
import os
from datetime import datetime
# TÜBİTAK scraper özelliği kaldırıldı
# Email gönderme özelliği kaldırıldı

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
csrf = CSRFProtect(app)  # CSRF protection
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Bu sayfayı görüntülemek için giriş yapmalısınız.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# ============ Bildirim Sistemi ============

# Email gönderme fonksiyonu kaldırıldı (özellik kullanılmıyor)

def create_notification(user_id, title, message, notif_type, icon='bi-bell', link=None, send_email=False):
    """Bildirim oluştur (email gönderme kaldırıldı)"""
    # Site içi bildirim oluştur
    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        type=notif_type,
        icon=icon,
        link=link
    )
    db.session.add(notification)
    db.session.commit()
    
    # Email gönderme özelliği kaldırıldı

def notify_students_new_assignment(assignment, class_obj):
    """Yeni ödev eklendiğinde öğrencilere bildir"""
    try:
        students = list(class_obj.students)
        for student in students:
            try:
                create_notification(
                    user_id=student.id,
                    title='Yeni Ödev',
                    message=f'{class_obj.name} sınıfında yeni ödev: {assignment.title}',
                    notif_type='assignment',
                    icon='bi-file-earmark-text',
                    link=url_for('student_class_assignments', class_id=class_obj.id),
                    send_email=False
                )
            except Exception as e:
                # Tek bir öğrenciye bildirim göndermede hata olsa bile devam et
                print(f"⚠️ Öğrenci {student.id} bildirim hatası: {e}")
    except Exception as e:
        # Bildirim hatası kritik değil, sadece logla
        print(f"⚠️ Toplu bildirim gönderme hatası: {e}")

def notify_student_graded(submission, assignment, class_obj):
    """Ödev notlandırıldığında öğrenciye bildir"""
    create_notification(
        user_id=submission.student_id,
        title='Ödev Notlandırıldı',
        message=f'{assignment.title} ödevi notlandırıldı: {submission.score}/{assignment.max_score}',
        notif_type='grade',
        icon='bi-star-fill',
        link=url_for('student_class_assignments', class_id=class_obj.id)
    )

def notify_teacher_new_submission(teacher_id, student, assignment, class_obj):
    """Öğrenci ödev teslim ettiğinde öğretmene bildir"""
    try:
        create_notification(
            user_id=teacher_id,
            title='Yeni Ödev Teslimi',
            message=f'{student.full_name}, {assignment.title} ödevini teslim etti',
            notif_type='submission',
            icon='bi-upload',
            link=url_for('admin_assignment_submissions', assignment_id=assignment.id),
            send_email=False  # Email göndermeyi devre dışı bırak (timeout olmasın)
        )
    except Exception as e:
        # Bildirim hatası kritik değil, sadece logla
        print(f"⚠️ Bildirim gönderme hatası: {e}")

def notify_students_new_announcement(announcement, class_obj):
    """Yeni bilgilendirme eklendiğinde öğrencilere bildir"""
    try:
        students = list(class_obj.students)
        for student in students:
            try:
                create_notification(
                    user_id=student.id,
                    title='Yeni Bilgilendirme',
                    message=f'{class_obj.name}: {announcement.title}',
                    notif_type='announcement',
                    icon='bi-megaphone' if announcement.is_important else 'bi-info-circle',
                    link=url_for('student_classes'),
                    send_email=False
                )
            except Exception as e:
                # Tek bir öğrenciye bildirim göndermede hata olsa bile devam et
                print(f"⚠️ Öğrenci {student.id} bildirim hatası: {e}")
    except Exception as e:
        # Bildirim hatası kritik değil, sadece logla
        print(f"⚠️ Toplu bildirim gönderme hatası: {e}")

def notify_teacher_student_enrolled(teacher_id, student, class_obj):
    """Öğrenci sınıfa katıldığında öğretmene bildir"""
    try:
        create_notification(
            user_id=teacher_id,
            title='Yeni Öğrenci',
            message=f'{student.full_name}, {class_obj.name} sınıfına katıldı',
            notif_type='enrollment',
            icon='bi-person-plus',
            link=url_for('admin_class_detail', class_id=class_obj.id)
        )
    except Exception as e:
        # Bildirim hatası kritik değil, sadece logla
        print(f"⚠️ Bildirim gönderme hatası: {e}")

# Create database tables and upload folder
with app.app_context():
    try:
        # Önce tabloları oluştur
        db.create_all()
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # İlk admin kullanıcısını oluştur (yoksa)
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@tubitak.gov.tr',
                full_name='Sistem Yöneticisi',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin kullanıcısı oluşturuldu (Kullanıcı adı: admin, Şifre: admin123)")
    except Exception as e:
        print(f"⚠️ Database initialization hatası: {e}")
        import traceback
        traceback.print_exc()
        try:
            db.session.rollback()
        except:
            pass

# ============ Ana Sayfalar ============

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash(f'Hoş geldiniz, {user.full_name}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Kullanıcı adı veya şifre hatalı!', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            full_name = request.form.get('full_name')
            role = request.form.get('role')
            
            # Rol kontrolü
            if role not in ['student', 'admin']:
                flash('Geçersiz hesap türü seçildi!', 'danger')
                return render_template('register.html')
            
            # Kullanıcı adı veya email zaten var mı?
            if User.query.filter_by(username=username).first():
                flash('Bu kullanıcı adı zaten kullanılıyor!', 'danger')
                return render_template('register.html')
            
            if User.query.filter_by(email=email).first():
                flash('Bu email adresi zaten kayıtlı!', 'danger')
                return render_template('register.html')
            
            # Yeni kullanıcı oluştur
            user = User(
                username=username,
                email=email,
                full_name=full_name,
                role=role
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            role_text = 'öğretmen' if role == 'admin' else 'öğrenci'
            flash(f'Kayıt başarılı! {role_text.capitalize()} hesabınızla giriş yapabilirsiniz.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Kayıt hatası: {e}")
            import traceback
            traceback.print_exc()
            flash('Kayıt sırasında bir hata oluştu. Lütfen tekrar deneyin.', 'danger')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    # Mevcut şifreyi kontrol et
    if not current_user.check_password(current_password):
        flash('Mevcut şifreniz yanlış!', 'danger')
        return redirect(url_for('profile'))
    
    # Yeni şifrelerin eşleşmesini kontrol et
    if new_password != confirm_password:
        flash('Yeni şifreler eşleşmiyor!', 'danger')
        return redirect(url_for('profile'))
    
    # Şifre uzunluğunu kontrol et
    if len(new_password) < 6:
        flash('Şifre en az 6 karakter olmalıdır!', 'danger')
        return redirect(url_for('profile'))
    
    # Şifreyi güncelle
    current_user.set_password(new_password)
    db.session.commit()
    
    flash('Şifreniz başarıyla güncellendi!', 'success')
    return redirect(url_for('profile'))

@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    
    # Email başka bir kullanıcıda var mı kontrol et
    existing_user = User.query.filter_by(email=email).first()
    if existing_user and existing_user.id != current_user.id:
        flash('Bu email adresi başka bir kullanıcı tarafından kullanılıyor!', 'danger')
        return redirect(url_for('profile'))
    
    # Bilgileri güncelle
    current_user.full_name = full_name
    current_user.email = email
    db.session.commit()
    
    flash('Bilgileriniz başarıyla güncellendi!', 'success')
    return redirect(url_for('profile'))

@app.context_processor
def inject_notifications():
    """Her template'te bildirim sayısını göster"""
    if current_user.is_authenticated:
        unread_count = Notification.query.filter_by(
            user_id=current_user.id,
            is_read=False
        ).count()
        return dict(unread_notifications_count=unread_count)
    return dict(unread_notifications_count=0)

@app.route('/notifications')
@login_required
def notifications():
    """Bildirimler sayfası"""
    all_notifications = Notification.query.filter_by(
        user_id=current_user.id
    ).order_by(Notification.created_at.desc()).all()
    
    return render_template('notifications.html', notifications=all_notifications)

@app.route('/notifications/<int:notification_id>/mark-read', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    """Bildirimi okundu olarak işaretle"""
    notification = Notification.query.get_or_404(notification_id)
    
    if notification.user_id != current_user.id:
        flash('Bu bildirime erişim yetkiniz yok!', 'danger')
        return redirect(url_for('notifications'))
    
    notification.is_read = True
    db.session.commit()
    
    # Eğer link varsa oraya yönlendir
    if notification.link:
        return redirect(notification.link)
    
    return redirect(url_for('notifications'))

@app.route('/notifications/mark-all-read', methods=['POST'])
@login_required
def mark_all_notifications_read():
    """Tüm bildirimleri okundu olarak işaretle"""
    Notification.query.filter_by(
        user_id=current_user.id,
        is_read=False
    ).update({Notification.is_read: True})
    db.session.commit()
    
    flash('Tüm bildirimler okundu olarak işaretlendi!', 'success')
    return redirect(url_for('notifications'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Başarıyla çıkış yaptınız.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        # Admin için istatistikler - sadece kendi sınıfları
        my_classes = Class.query.filter_by(created_by=current_user.id).all()
        
        # Sadece kendi sınıflarındaki öğrenciler
        total_students = 0
        unique_students = set()
        for cls in my_classes:
            for student in cls.students:
                unique_students.add(student.id)
        total_students = len(unique_students)
        
        total_classes = len(my_classes)
        
        # Sadece kendi sınıflarındaki ödevler
        total_assignments = 0
        for cls in my_classes:
            total_assignments += len(cls.assignments)
        
        # Sadece kendi sınıflarındaki teslimler
        total_submissions = 0
        recent_submissions = []
        for cls in my_classes:
            for assignment in cls.assignments:
                total_submissions += len(assignment.submissions)
                for submission in assignment.submissions:
                    recent_submissions.append(submission)
        
        # Son teslimleri tarihe göre sırala
        recent_submissions.sort(key=lambda x: x.submitted_at, reverse=True)
        recent_submissions = recent_submissions[:10]
        
        # Son yayınlanan bilgilendirmeler
        recent_announcements = []
        for cls in my_classes:
            for announcement in cls.announcements:
                recent_announcements.append({
                    'announcement': announcement,
                    'class': cls,
                    'read_count': len(announcement.reads),
                    'student_count': cls.students.count()
                })
        
        # Tarihe göre sırala (en yeni üstte)
        recent_announcements.sort(key=lambda x: x['announcement'].created_at, reverse=True)
        recent_announcements = recent_announcements[:5]
        
        # TÜBİTAK 2209-A Program Duyuruları (aktif olanlar)
        program_announcements = ProgramAnnouncement.query.filter_by(
            is_active=True
        ).order_by(ProgramAnnouncement.is_important.desc(), ProgramAnnouncement.created_at.desc()).limit(5).all()
        
        return render_template('admin/dashboard.html',
                             total_students=total_students,
                             total_classes=total_classes,
                             total_assignments=total_assignments,
                             total_submissions=total_submissions,
                             recent_submissions=recent_submissions,
                             recent_announcements=recent_announcements,
                             program_announcements=program_announcements)
    else:
        # Öğrenci için sınıflar ve ödevler
        my_classes = current_user.enrolled_classes
        
        # Yaklaşan ödevler
        upcoming_assignments = []
        for cls in my_classes:
            for assignment in cls.assignments:
                if assignment.due_date > datetime.utcnow():
                    # Öğrenci bu ödevi teslim etti mi?
                    submission = Submission.query.filter_by(
                        assignment_id=assignment.id,
                        student_id=current_user.id
                    ).first()
                    upcoming_assignments.append({
                        'assignment': assignment,
                        'class': cls,
                        'submitted': submission is not None
                    })
        
        # Tarihe göre sırala
        upcoming_assignments.sort(key=lambda x: x['assignment'].due_date)
        
        # Son bilgilendirmeler - tüm kayıtlı sınıflardan
        recent_announcements = []
        for cls in my_classes:
            for announcement in cls.announcements:
                recent_announcements.append({
                    'announcement': announcement,
                    'class': cls
                })
        
        # Tarihe göre sırala (en yeni üstte)
        recent_announcements.sort(key=lambda x: x['announcement'].created_at, reverse=True)
        
        # TÜBİTAK 2209-A Program Duyuruları (aktif olanlar)
        program_announcements = ProgramAnnouncement.query.filter_by(
            is_active=True
        ).order_by(ProgramAnnouncement.is_important.desc(), ProgramAnnouncement.created_at.desc()).limit(5).all()
        
        return render_template('student/dashboard.html',
                             my_classes=my_classes,
                             upcoming_assignments=upcoming_assignments[:5],
                             recent_announcements=recent_announcements,  # Tüm bilgilendirmeleri göster
                             program_announcements=program_announcements)

# ============ Admin: Sınıf Yönetimi ============

@app.route('/admin/classes')
@login_required
def admin_classes():
    if current_user.role != 'admin':
        flash('Bu sayfaya erişim yetkiniz yok!', 'danger')
        return redirect(url_for('dashboard'))
    
    # Sadece kendi oluşturduğu sınıfları göster
    classes = Class.query.filter_by(created_by=current_user.id).all()
    return render_template('admin/classes.html', classes=classes)

@app.route('/admin/classes/create', methods=['POST'])
@login_required
def create_class():
    if current_user.role != 'admin':
        flash('Bu işlem için yetkiniz yok!', 'danger')
        return redirect(url_for('dashboard'))
    
    name = request.form.get('name')
    code = request.form.get('code', '').strip().upper()  # Büyük harfe çevir ve boşlukları temizle
    description = request.form.get('description')
    
    # Kod boş mu?
    if not code:
        flash('Sınıf kodu boş olamaz!', 'danger')
        return redirect(url_for('admin_classes'))
    
    # Kod zaten var mı? (Case-insensitive kontrol - tüm öğretmenler için global benzersizlik)
    existing_class = Class.query.filter(db.func.upper(Class.code) == code).first()
    if existing_class:
        flash(f'Bu sınıf kodu "{code}" zaten başka bir öğretmen tarafından kullanılıyor! Lütfen farklı bir kod seçin.', 'danger')
        return redirect(url_for('admin_classes'))
    
    new_class = Class(
        name=name,
        code=code,
        description=description,
        created_by=current_user.id
    )
    
    db.session.add(new_class)
    db.session.commit()
    
    flash(f'Sınıf "{name}" başarıyla oluşturuldu!', 'success')
    return redirect(url_for('admin_classes'))

@app.route('/admin/classes/<int:class_id>/delete', methods=['POST'])
@login_required
def delete_class(class_id):
    if current_user.role != 'admin':
        flash('Bu işlem için yetkiniz yok!', 'danger')
        return redirect(url_for('dashboard'))
    
    cls = Class.query.get_or_404(class_id)
    
    # Sadece kendi oluşturduğu sınıfı silebilir
    if cls.created_by != current_user.id:
        flash('Bu sınıfı silme yetkiniz yok!', 'danger')
        return redirect(url_for('admin_classes'))
    
    db.session.delete(cls)
    db.session.commit()
    
    flash(f'Sınıf "{cls.name}" silindi.', 'success')
    return redirect(url_for('admin_classes'))

@app.route('/admin/classes/<int:class_id>')
@login_required
def admin_class_detail(class_id):
    if current_user.role != 'admin':
        flash('Bu sayfaya erişim yetkiniz yok!', 'danger')
        return redirect(url_for('dashboard'))
    
    cls = Class.query.get_or_404(class_id)
    
    # Sadece kendi oluşturduğu sınıfı görebilir
    if cls.created_by != current_user.id:
        flash('Bu sınıfa erişim yetkiniz yok!', 'danger')
        return redirect(url_for('admin_classes'))
    
    students = cls.students.all()
    assignments = cls.assignments
    
    return render_template('admin/class_detail.html', cls=cls, students=students, assignments=assignments)

@app.route('/admin/classes/<int:class_id>/students/<int:student_id>/remove', methods=['POST'])
@login_required
def admin_remove_student(class_id, student_id):
    """Öğrenciyi sınıftan çıkar"""
    try:
        if current_user.role != 'admin':
            flash('Bu işlem için yetkiniz yok!', 'danger')
            return redirect(url_for('dashboard'))
        
        cls = Class.query.get_or_404(class_id)
        
        # Sadece kendi sınıfından öğrenci çıkarabilir
        if cls.created_by != current_user.id:
            flash('Bu sınıftan öğrenci çıkarma yetkiniz yok!', 'danger')
            return redirect(url_for('admin_classes'))
        
        student = User.query.get_or_404(student_id)
        
        # Öğrenci bu sınıfa kayıtlı mı?
        if cls in student.enrolled_classes:
            student.enrolled_classes.remove(cls)
            db.session.commit()
            flash(f'{student.full_name} sınıftan çıkarıldı.', 'success')
        else:
            flash('Bu öğrenci sınıfa kayıtlı değil!', 'warning')
        
        return redirect(url_for('admin_class_detail', class_id=class_id))
    except Exception as e:
        db.session.rollback()
        print(f"❌ Öğrenci çıkarma hatası: {e}")
        import traceback
        traceback.print_exc()
        flash('Öğrenci çıkarılırken bir hata oluştu!', 'danger')
        return redirect(url_for('admin_class_detail', class_id=class_id))

# ============ Admin: Ödev Yönetimi ============

@app.route('/admin/classes/<int:class_id>/assignments/create', methods=['POST'])
@login_required
def create_assignment(class_id):
    try:
        if current_user.role != 'admin':
            flash('Bu işlem için yetkiniz yok!', 'danger')
            return redirect(url_for('dashboard'))
        
        cls = Class.query.get_or_404(class_id)
        
        # Sadece kendi oluşturduğu sınıfa ödev verebilir
        if cls.created_by != current_user.id:
            flash('Bu sınıfa ödev verme yetkiniz yok!', 'danger')
            return redirect(url_for('admin_classes'))
        
        title = request.form.get('title')
        description = request.form.get('description')
        due_date_str = request.form.get('due_date')
        max_score = request.form.get('max_score', 100)
        
        if not due_date_str:
            flash('Teslim tarihi gereklidir!', 'danger')
            return redirect(url_for('admin_class_detail', class_id=class_id))
        
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Geçersiz tarih formatı!', 'danger')
            return redirect(url_for('admin_class_detail', class_id=class_id))
        
        assignment = Assignment(
            title=title,
            description=description,
            class_id=class_id,
            due_date=due_date,
            max_score=int(max_score)
        )
        
        db.session.add(assignment)
        db.session.commit()
        
        # Öğrencilere bildirim gönder (hata olsa bile devam et)
        notify_students_new_assignment(assignment, cls)
        
        flash(f'Ödev "{title}" başarıyla oluşturuldu!', 'success')
        return redirect(url_for('admin_class_detail', class_id=class_id))
    except Exception as e:
        db.session.rollback()
        print(f"❌ Ödev oluşturma hatası: {e}")
        import traceback
        traceback.print_exc()
        flash('Ödev oluşturulurken bir hata oluştu! Lütfen tekrar deneyin.', 'danger')
        return redirect(url_for('admin_class_detail', class_id=class_id))

@app.route('/admin/assignments/<int:assignment_id>/delete', methods=['POST'])
@login_required
def delete_assignment(assignment_id):
    try:
        if current_user.role != 'admin':
            flash('Bu işlem için yetkiniz yok!', 'danger')
            return redirect(url_for('dashboard'))
        
        assignment = Assignment.query.get_or_404(assignment_id)
        
        # Sadece kendi sınıfının ödevini silebilir
        if assignment.class_ref.created_by != current_user.id:
            flash('Bu ödevi silme yetkiniz yok!', 'danger')
            return redirect(url_for('admin_classes'))
        
        class_id = assignment.class_id
        assignment_title = assignment.title
        
        # Önce tüm submission dosyalarını fiziksel olarak sil
        deleted_files = 0
        for submission in assignment.submissions:
            if submission.file_path:
                for file_path in submission.file_path.split('|||'):
                    try:
                        if file_path and os.path.exists(file_path):
                            os.remove(file_path)
                            deleted_files += 1
                    except Exception as e:
                        print(f"⚠️ Dosya silme hatası: {e}")
        
        # Ödev silindiğinde bağlı submission'lar da otomatik silinecek (cascade)
        db.session.delete(assignment)
        db.session.commit()
        
        flash(f'Ödev "{assignment_title}" başarıyla silindi! ({deleted_files} dosya temizlendi)', 'success')
        
        # Nereden geldiyse oraya yönlendir
        referer = request.headers.get('Referer')
        if referer and 'submissions' in referer:
            return redirect(url_for('admin_class_detail', class_id=class_id))
        else:
            return redirect(url_for('admin_class_detail', class_id=class_id))
    except Exception as e:
        db.session.rollback()
        print(f"❌ Ödev silme hatası: {e}")
        import traceback
        traceback.print_exc()
        flash('Ödev silinirken bir hata oluştu!', 'danger')
        return redirect(url_for('admin_classes'))

@app.route('/admin/assignments/<int:assignment_id>/submissions')
@login_required
def admin_assignment_submissions(assignment_id):
    if current_user.role != 'admin':
        flash('Bu sayfaya erişim yetkiniz yok!', 'danger')
        return redirect(url_for('dashboard'))
    
    assignment = Assignment.query.get_or_404(assignment_id)
    
    # Sadece kendi sınıfının ödevini görebilir
    if assignment.class_ref.created_by != current_user.id:
        flash('Bu ödeve erişim yetkiniz yok!', 'danger')
        return redirect(url_for('admin_classes'))
    submissions = assignment.submissions
    
    # Sınıftaki tüm öğrenciler
    students = assignment.class_ref.students.all()
    
    # Hangi öğrenciler teslim etmiş?
    submitted_student_ids = [s.student_id for s in submissions]
    not_submitted_students = [s for s in students if s.id not in submitted_student_ids]
    
    return render_template('admin/assignment_submissions.html',
                         assignment=assignment,
                         submissions=submissions,
                         not_submitted_students=not_submitted_students)

@app.route('/admin/submissions/<int:submission_id>/grade', methods=['POST'])
@login_required
def grade_submission(submission_id):
    if current_user.role != 'admin':
        flash('Bu işlem için yetkiniz yok!', 'danger')
        return redirect(url_for('dashboard'))
    
    submission = Submission.query.get_or_404(submission_id)
    
    # Sadece kendi sınıfının ödevini notlandırabilir
    if submission.assignment.class_ref.created_by != current_user.id:
        flash('Bu ödevi notlandırma yetkiniz yok!', 'danger')
        return redirect(url_for('admin_classes'))
    
    score = request.form.get('score')
    feedback = request.form.get('feedback')
    
    submission.score = int(score) if score else None
    submission.feedback = feedback
    submission.graded_at = datetime.utcnow()
    
    db.session.commit()
    
    # Öğrenciye bildirim gönder
    notify_student_graded(submission, submission.assignment, submission.assignment.class_ref)
    
    flash('Not ve geri bildirim kaydedildi!', 'success')
    return redirect(url_for('admin_assignment_submissions', assignment_id=submission.assignment_id))

# ============ Öğrenci: Sınıflara Katılma ============

@app.route('/student/classes')
@login_required
def student_classes():
    if current_user.role != 'student':
        flash('Bu sayfaya erişim yetkiniz yok!', 'danger')
        return redirect(url_for('dashboard'))
    
    my_classes = current_user.enrolled_classes
    
    return render_template('student/classes.html',
                         my_classes=my_classes)

@app.route('/student/classes/enroll-by-code', methods=['POST'])
@login_required
def enroll_by_code():
    """Sınıfa kod ile katıl"""
    try:
        if current_user.role != 'student':
            flash('Bu işlem için yetkiniz yok!', 'danger')
            return redirect(url_for('dashboard'))
        
        class_code = request.form.get('class_code', '').strip().upper()
        
        if not class_code:
            flash('Lütfen bir sınıf kodu girin!', 'danger')
            return redirect(url_for('student_classes'))
        
        # Sınıf koduna göre sınıfı bul (case-insensitive)
        cls = Class.query.filter(
            db.func.upper(Class.code) == class_code,
            Class.is_active == True
        ).first()
        
        if not cls:
            flash(f'"{class_code}" kodlu bir sınıf bulunamadı! Lütfen kodun doğru olduğundan emin olun.', 'danger')
            return redirect(url_for('student_classes'))
        
        # Öğrenci zaten bu sınıfa kayıtlı mı?
        if cls in current_user.enrolled_classes:
            flash(f'"{cls.name}" sınıfına zaten kayıtlısınız!', 'warning')
        else:
            current_user.enrolled_classes.append(cls)
            db.session.commit()
            
            # Öğretmene bildirim gönder
            notify_teacher_student_enrolled(cls.created_by, current_user, cls)
            
            flash(f'"{cls.name}" sınıfına başarıyla katıldınız!', 'success')
        
        return redirect(url_for('student_classes'))
    except Exception as e:
        db.session.rollback()
        print(f"❌ Kod ile kayıt hatası: {e}")
        import traceback
        traceback.print_exc()
        flash('Sınıfa katılırken bir hata oluştu! Lütfen tekrar deneyin.', 'danger')
        return redirect(url_for('student_classes'))

@app.route('/student/classes/<int:class_id>/leave', methods=['POST'])
@login_required
def leave_class(class_id):
    if current_user.role != 'student':
        flash('Bu işlem için yetkiniz yok!', 'danger')
        return redirect(url_for('dashboard'))
    
    cls = Class.query.get_or_404(class_id)
    
    if cls in current_user.enrolled_classes:
        current_user.enrolled_classes.remove(cls)
        db.session.commit()
        flash(f'"{cls.name}" sınıfından ayrıldınız.', 'info')
    
    return redirect(url_for('student_classes'))

# ============ Öğrenci: Ödevler ============

@app.route('/student/classes/<int:class_id>/assignments')
@login_required
def student_class_assignments(class_id):
    if current_user.role != 'student':
        flash('Bu sayfaya erişim yetkiniz yok!', 'danger')
        return redirect(url_for('dashboard'))
    
    cls = Class.query.get_or_404(class_id)
    
    if cls not in current_user.enrolled_classes:
        flash('Bu sınıfa kayıtlı değilsiniz!', 'danger')
        return redirect(url_for('student_classes'))
    
    assignments = cls.assignments
    
    # Her ödev için teslim durumu
    assignment_data = []
    for assignment in assignments:
        submission = Submission.query.filter_by(
            assignment_id=assignment.id,
            student_id=current_user.id
        ).first()
        
        assignment_data.append({
            'assignment': assignment,
            'submission': submission,
            'is_late': datetime.utcnow() > assignment.due_date
        })
    
    return render_template('student/assignments.html',
                         cls=cls,
                         assignment_data=assignment_data)

@app.route('/student/assignments/<int:assignment_id>/submit', methods=['POST'])
@login_required
def submit_assignment(assignment_id):
    try:
        if current_user.role != 'student':
            flash('Bu işlem için yetkiniz yok!', 'danger')
            return redirect(url_for('dashboard'))
        
        assignment = Assignment.query.get_or_404(assignment_id)
        
        # Öğrenci bu sınıfa kayıtlı mı?
        if assignment.class_ref not in current_user.enrolled_classes:
            flash('Bu sınıfa kayıtlı değilsiniz!', 'danger')
            return redirect(url_for('student_classes'))
        
        # Çoklu dosya yükleme
        files = request.files.getlist('files')
        student_comment = request.form.get('student_comment', '').strip()
        
        if not files or all(f.filename == '' for f in files):
            flash('En az bir dosya seçmeniz gerekiyor!', 'danger')
            return redirect(url_for('student_class_assignments', class_id=assignment.class_id))
        
        # En fazla 3 dosya kontrolü
        valid_files = [f for f in files if f.filename != '']
        if len(valid_files) > 3:
            flash('En fazla 3 dosya yükleyebilirsiniz!', 'danger')
            return redirect(url_for('student_class_assignments', class_id=assignment.class_id))
        
        # Tüm dosyaları kontrol et
        for f in valid_files:
            if not allowed_file(f.filename):
                flash(f'Sadece PDF ve DOCX dosyaları yüklenebilir! ({f.filename})', 'danger')
                return redirect(url_for('student_class_assignments', class_id=assignment.class_id))
        
        # Dosyaları kaydet
        saved_filenames = []
        saved_filepaths = []
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        for idx, file in enumerate(valid_files):
            filename = secure_filename(file.filename)
            unique_filename = f"{current_user.id}_{assignment_id}_{timestamp}_{idx}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            
            # Dosya yükleme dizininin var olduğundan emin ol
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Dosyayı kaydet
            file.save(file_path)
            saved_filenames.append(filename)
            saved_filepaths.append(file_path)
        
        # Dosya adlarını ve yollarını birleştir
        combined_filenames = '|||'.join(saved_filenames)
        combined_filepaths = '|||'.join(saved_filepaths)
        
        # Daha önce teslim var mı? Varsa güncelle
        existing_submission = Submission.query.filter_by(
            assignment_id=assignment_id,
            student_id=current_user.id
        ).first()
        
        if existing_submission:
            # Eski dosyaları sil
            if existing_submission.file_path:
                for old_path in existing_submission.file_path.split('|||'):
                    try:
                        if old_path and os.path.exists(old_path):
                            os.remove(old_path)
                    except Exception as e:
                        print(f"⚠️ Eski dosya silme hatası: {e}")
            
            existing_submission.file_name = combined_filenames
            existing_submission.file_path = combined_filepaths
            existing_submission.student_comment = student_comment
            existing_submission.submitted_at = datetime.utcnow()
            flash(f'Ödeviniz güncellendi! ({len(saved_filenames)} dosya)', 'success')
        else:
            # Yeni teslim oluştur
            submission = Submission(
                assignment_id=assignment_id,
                student_id=current_user.id,
                file_name=combined_filenames,
                file_path=combined_filepaths,
                student_comment=student_comment
            )
            db.session.add(submission)
            flash(f'Ödeviniz başarıyla teslim edildi! ({len(saved_filenames)} dosya)', 'success')
            
            # Öğretmene bildirim gönder (hata olsa bile devam et)
            notify_teacher_new_submission(assignment.class_ref.created_by, current_user, assignment, assignment.class_ref)
        
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Ödev teslim hatası: {e}")
        import traceback
        traceback.print_exc()
        flash('Ödev teslim edilirken bir hata oluştu! Lütfen tekrar deneyin.', 'danger')
        # Kaydedilen dosyaları sil
        try:
            if 'saved_filepaths' in locals():
                for fp in saved_filepaths:
                    if os.path.exists(fp):
                        os.remove(fp)
        except:
            pass
        return redirect(url_for('student_class_assignments', class_id=assignment.class_id))
    
    return redirect(url_for('student_class_assignments', class_id=assignment.class_id))

# ============ Bilgilendirmeler ============

@app.route('/admin/classes/<int:class_id>/announcements/create', methods=['POST'])
@login_required
def create_announcement(class_id):
    try:
        if current_user.role != 'admin':
            flash('Bu işlem için yetkiniz yok!', 'danger')
            return redirect(url_for('dashboard'))
        
        cls = Class.query.get_or_404(class_id)
        
        # Sadece kendi oluşturduğu sınıfa bilgilendirme yapabilir
        if cls.created_by != current_user.id:
            flash('Bu sınıfa bilgilendirme yapma yetkiniz yok!', 'danger')
            return redirect(url_for('admin_classes'))
        
        title = request.form.get('title')
        content = request.form.get('content')
        is_important = request.form.get('is_important') == 'on'
        
        announcement = Announcement(
            title=title,
            content=content,
            class_id=class_id,
            created_by=current_user.id,
            is_important=is_important
        )
        
        # Dosya yüklendiyse
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_filename = f"announcement_{class_id}_{timestamp}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                announcement.file_name = filename
                announcement.file_path = file_path
        
        db.session.add(announcement)
        db.session.commit()
        
        # Öğrencilere bildirim gönder (hata olsa bile devam et)
        notify_students_new_announcement(announcement, cls)
        
        flash(f'Bilgilendirme "{title}" başarıyla yayınlandı!', 'success')
        return redirect(url_for('admin_class_detail', class_id=class_id))
    except Exception as e:
        db.session.rollback()
        print(f"❌ Bilgilendirme oluşturma hatası: {e}")
        import traceback
        traceback.print_exc()
        flash('Bilgilendirme oluşturulurken bir hata oluştu! Lütfen tekrar deneyin.', 'danger')
        return redirect(url_for('admin_class_detail', class_id=class_id))

@app.route('/admin/announcements/bulk-create', methods=['POST'])
@login_required
def bulk_create_announcement():
    """Toplu bilgilendirme gönder"""
    if current_user.role != 'admin':
        flash('Bu işlem için yetkiniz yok!', 'danger')
        return redirect(url_for('dashboard'))
    
    class_ids_str = request.form.get('class_ids', '')
    if not class_ids_str:
        flash('Lütfen en az bir sınıf seçin!', 'danger')
        return redirect(url_for('admin_classes'))
    
    class_ids = [int(id.strip()) for id in class_ids_str.split(',') if id.strip()]
    
    # Sadece kendi sınıflarını kontrol et
    classes = Class.query.filter(
        Class.id.in_(class_ids),
        Class.created_by == current_user.id
    ).all()
    
    if not classes:
        flash('Geçerli sınıf bulunamadı!', 'danger')
        return redirect(url_for('admin_classes'))
    
    title = request.form.get('title')
    content = request.form.get('content')
    is_important = request.form.get('is_important') == 'on'
    
    # Dosya yüklendiyse (her sınıf için aynı dosya kopyalanacak)
    file = None
    file_path = None
    filename = None
    if 'file' in request.files:
        file = request.files['file']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
    
    success_count = 0
    for cls in classes:
        announcement = Announcement(
            title=title,
            content=content,
            class_id=cls.id,
            created_by=current_user.id,
            is_important=is_important
        )
        
        # Dosya varsa her sınıf için ayrı kopya oluştur
        if file and filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_filename = f"announcement_{cls.id}_{timestamp}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.seek(0)  # Dosyayı başa al
            file.save(file_path)
            announcement.file_name = filename
            announcement.file_path = file_path
        
        db.session.add(announcement)
        db.session.commit()
        
        # Öğrencilere bildirim gönder
        notify_students_new_announcement(announcement, cls)
        success_count += 1
    
    flash(f'Bilgilendirme "{title}" {success_count} sınıfa başarıyla gönderildi!', 'success')
    return redirect(url_for('admin_classes'))

@app.route('/admin/assignments/bulk-create', methods=['POST'])
@login_required
def bulk_create_assignment():
    """Toplu ödev ver"""
    try:
        if current_user.role != 'admin':
            flash('Bu işlem için yetkiniz yok!', 'danger')
            return redirect(url_for('dashboard'))
        
        class_ids_str = request.form.get('class_ids', '')
        if not class_ids_str:
            flash('Lütfen en az bir sınıf seçin!', 'danger')
            return redirect(url_for('admin_classes'))
        
        class_ids = [int(id.strip()) for id in class_ids_str.split(',') if id.strip()]
        
        # Sadece kendi sınıflarını kontrol et
        classes = Class.query.filter(
            Class.id.in_(class_ids),
            Class.created_by == current_user.id
        ).all()
        
        if not classes:
            flash('Geçerli sınıf bulunamadı!', 'danger')
            return redirect(url_for('admin_classes'))
        
        title = request.form.get('title')
        description = request.form.get('description')
        due_date_str = request.form.get('due_date')
        max_score = request.form.get('max_score', 100)
        
        if not due_date_str:
            flash('Teslim tarihi gereklidir!', 'danger')
            return redirect(url_for('admin_classes'))
        
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Geçersiz tarih formatı!', 'danger')
            return redirect(url_for('admin_classes'))
        
        success_count = 0
        for cls in classes:
            try:
                assignment = Assignment(
                    title=title,
                    description=description,
                    class_id=cls.id,
                    due_date=due_date,
                    max_score=int(max_score)
                )
                
                db.session.add(assignment)
                db.session.commit()
                
                # Öğrencilere bildirim gönder (hata olsa bile devam et)
                notify_students_new_assignment(assignment, cls)
                success_count += 1
            except Exception as e:
                db.session.rollback()
                print(f"⚠️ Sınıf {cls.id} ödev oluşturma hatası: {e}")
                # Bir sınıfta hata olsa bile diğerlerine devam et
        
        flash(f'Ödev "{title}" {success_count} sınıfa başarıyla verildi!', 'success')
        return redirect(url_for('admin_classes'))
    except Exception as e:
        db.session.rollback()
        print(f"❌ Toplu ödev oluşturma hatası: {e}")
        import traceback
        traceback.print_exc()
        flash('Ödev oluşturulurken bir hata oluştu! Lütfen tekrar deneyin.', 'danger')
        return redirect(url_for('admin_classes'))

@app.route('/admin/announcements/<int:announcement_id>/delete', methods=['POST'])
@login_required
def delete_announcement(announcement_id):
    try:
        if current_user.role != 'admin':
            flash('Bu işlem için yetkiniz yok!', 'danger')
            return redirect(url_for('dashboard'))
        
        announcement = Announcement.query.get_or_404(announcement_id)
        
        # Sadece kendi oluşturduğu bilgilendirmeyi silebilir
        if announcement.created_by != current_user.id:
            flash('Bu bilgilendirmeyi silme yetkiniz yok!', 'danger')
            return redirect(url_for('admin_classes'))
        
        class_id = announcement.class_id
        announcement_title = announcement.title
        
        # Dosya varsa sil
        if announcement.file_path and os.path.exists(announcement.file_path):
            try:
                os.remove(announcement.file_path)
            except Exception as e:
                print(f"⚠️ Dosya silme hatası: {e}")
        
        db.session.delete(announcement)
        db.session.commit()
        
        flash(f'Bilgilendirme "{announcement_title}" başarıyla silindi!', 'success')
        
        # Nereden geldiyse oraya yönlendir
        referer = request.headers.get('Referer')
        if referer and 'dashboard' in referer:
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('admin_class_detail', class_id=class_id))
    except Exception as e:
        db.session.rollback()
        print(f"❌ Bilgilendirme silme hatası: {e}")
        import traceback
        traceback.print_exc()
        flash('Bilgilendirme silinirken bir hata oluştu!', 'danger')
        return redirect(url_for('admin_classes'))

# ============ TÜBİTAK 2209-A Program Duyuruları ============

@app.route('/admin/program-announcements')
@login_required
def admin_program_announcements():
    """Program duyurularını listele (admin)"""
    if current_user.role != 'admin':
        flash('Bu sayfaya erişim yetkiniz yok!', 'danger')
        return redirect(url_for('dashboard'))
    
    announcements = ProgramAnnouncement.query.order_by(
        ProgramAnnouncement.is_important.desc(),
        ProgramAnnouncement.created_at.desc()
    ).all()
    
    return render_template('admin/program_announcements.html', announcements=announcements)

@app.route('/admin/program-announcements/create', methods=['POST'])
@login_required
def create_program_announcement():
    """Program duyurusu oluştur"""
    if current_user.role != 'admin':
        flash('Bu işlem için yetkiniz yok!', 'danger')
        return redirect(url_for('dashboard'))
    
    title = request.form.get('title')
    content = request.form.get('content')
    external_link = request.form.get('external_link', '').strip()
    is_important = request.form.get('is_important') == 'on'
    is_active = request.form.get('is_active', 'on') == 'on'
    
    announcement = ProgramAnnouncement(
        title=title,
        content=content,
        external_link=external_link if external_link else None,
        is_important=is_important,
        is_active=is_active,
        created_by=current_user.id
    )
    
    db.session.add(announcement)
    db.session.commit()
    
    flash(f'Program duyurusu "{title}" başarıyla oluşturuldu!', 'success')
    return redirect(url_for('admin_program_announcements'))

@app.route('/admin/program-announcements/<int:announcement_id>/update', methods=['POST'])
@login_required
def update_program_announcement(announcement_id):
    """Program duyurusu güncelle"""
    if current_user.role != 'admin':
        flash('Bu işlem için yetkiniz yok!', 'danger')
        return redirect(url_for('dashboard'))
    
    announcement = ProgramAnnouncement.query.get_or_404(announcement_id)
    
    announcement.title = request.form.get('title')
    announcement.content = request.form.get('content')
    external_link = request.form.get('external_link', '').strip()
    announcement.external_link = external_link if external_link else None
    announcement.is_important = request.form.get('is_important') == 'on'
    announcement.is_active = request.form.get('is_active', 'on') == 'on'
    announcement.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    flash(f'Program duyurusu "{announcement.title}" güncellendi!', 'success')
    return redirect(url_for('admin_program_announcements'))

@app.route('/admin/program-announcements/<int:announcement_id>/delete', methods=['POST'])
@login_required
def delete_program_announcement(announcement_id):
    """Program duyurusu sil"""
    if current_user.role != 'admin':
        flash('Bu işlem için yetkiniz yok!', 'danger')
        return redirect(url_for('dashboard'))
    
    announcement = ProgramAnnouncement.query.get_or_404(announcement_id)
    title = announcement.title
    
    db.session.delete(announcement)
    db.session.commit()
    
    flash(f'Program duyurusu "{title}" silindi!', 'success')
    return redirect(url_for('admin_program_announcements'))

@app.route('/announcement/<int:announcement_id>/mark-read', methods=['POST'])
@login_required
def mark_announcement_read(announcement_id):
    if current_user.role != 'student':
        flash('Bu işlem için yetkiniz yok!', 'danger')
        return redirect(url_for('dashboard'))
    
    announcement = Announcement.query.get_or_404(announcement_id)
    
    # Öğrenci bu sınıfa kayıtlı mı?
    if announcement.class_ref not in current_user.enrolled_classes:
        flash('Bu bilgilendirmeye erişim yetkiniz yok!', 'danger')
        return redirect(url_for('dashboard'))
    
    # Daha önce okundu işareti var mı?
    existing_read = AnnouncementRead.query.filter_by(
        announcement_id=announcement_id,
        student_id=current_user.id
    ).first()
    
    if not existing_read:
        new_read = AnnouncementRead(
            announcement_id=announcement_id,
            student_id=current_user.id
        )
        db.session.add(new_read)
        db.session.commit()
        flash('Bilgilendirme okundu olarak işaretlendi!', 'success')
    
    return redirect(url_for('dashboard'))

@app.route('/admin/announcements/<int:announcement_id>/readers')
@login_required
def announcement_readers(announcement_id):
    if current_user.role != 'admin':
        flash('Bu sayfaya erişim yetkiniz yok!', 'danger')
        return redirect(url_for('dashboard'))
    
    announcement = Announcement.query.get_or_404(announcement_id)
    
    # Sadece kendi bilgilendirmesini görebilir
    if announcement.created_by != current_user.id:
        flash('Bu bilgilendirmeye erişim yetkiniz yok!', 'danger')
        return redirect(url_for('admin_classes'))
    
    # Sınıftaki tüm öğrenciler
    students = announcement.class_ref.students.all()
    
    # Okuyanlar
    readers = announcement.reads
    reader_ids = [r.student_id for r in readers]
    
    # Okumayanlar
    not_read_students = [s for s in students if s.id not in reader_ids]
    
    return render_template('admin/announcement_readers.html',
                         announcement=announcement,
                         readers=readers,
                         not_read_students=not_read_students,
                         total_students=len(students))

@app.route('/download/announcement/<int:announcement_id>')
@login_required
def download_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    
    # Erişim kontrolü - sınıftaki öğrenciler veya sınıfın sahibi
    if current_user.role == 'student':
        if announcement.class_ref not in current_user.enrolled_classes:
            flash('Bu dosyaya erişim yetkiniz yok!', 'danger')
            return redirect(url_for('dashboard'))
    elif current_user.role == 'admin':
        if announcement.created_by != current_user.id:
            flash('Bu dosyaya erişim yetkiniz yok!', 'danger')
            return redirect(url_for('dashboard'))
    
    if not announcement.file_path or not os.path.exists(announcement.file_path):
        flash('Dosya bulunamadı!', 'danger')
        return redirect(url_for('dashboard'))
    
    # Path traversal koruması - dosya yolunu normalize et ve kontrol et
    file_path = os.path.normpath(announcement.file_path)
    upload_dir = os.path.normpath(app.config['UPLOAD_FOLDER'])
    
    # Path traversal kontrolü - dosya upload klasörü dışına çıkmamalı
    if not file_path.startswith(upload_dir):
        flash('Geçersiz dosya yolu!', 'danger')
        return redirect(url_for('dashboard'))
    
    return send_file(file_path, as_attachment=True, download_name=announcement.file_name)

# ============ Dosya İndirme ============

@app.route('/download/<int:submission_id>')
@app.route('/download/<int:submission_id>/<int:file_index>')
@login_required
def download_submission(submission_id, file_index=0):
    submission = Submission.query.get_or_404(submission_id)
    
    # Erişim kontrolü
    if current_user.role == 'student' and submission.student_id != current_user.id:
        flash('Bu dosyaya erişim yetkiniz yok!', 'danger')
        return redirect(url_for('dashboard'))
    
    # Öğretmen sadece kendi sınıfının ödevlerini indirebilir
    if current_user.role == 'admin' and submission.assignment.class_ref.created_by != current_user.id:
        flash('Bu dosyaya erişim yetkiniz yok!', 'danger')
        return redirect(url_for('dashboard'))
    
    # Çoklu dosya desteği
    file_paths = submission.file_path.split('|||') if submission.file_path else []
    file_names = submission.file_name.split('|||') if submission.file_name else []
    
    if not file_paths or file_index >= len(file_paths):
        flash('Dosya bulunamadı!', 'danger')
        return redirect(url_for('dashboard'))
    
    file_path = file_paths[file_index]
    file_name = file_names[file_index] if file_index < len(file_names) else f'dosya_{file_index}'
    
    if not file_path or not os.path.exists(file_path):
        flash('Dosya bulunamadı!', 'danger')
        return redirect(url_for('dashboard'))
    
    # Path traversal koruması - dosya yolunu normalize et ve kontrol et
    file_path = os.path.normpath(file_path)
    upload_dir = os.path.normpath(app.config['UPLOAD_FOLDER'])
    
    # Path traversal kontrolü - dosya upload klasörü dışına çıkmamalı
    if not file_path.startswith(upload_dir):
        flash('Geçersiz dosya yolu!', 'danger')
        return redirect(url_for('dashboard'))
    
    return send_file(file_path, as_attachment=True, download_name=file_name)

# ============ Template Filtreleri ============

@app.template_filter('datetime')
def format_datetime(value):
    if value is None:
        return ""
    return value.strftime('%d.%m.%Y %H:%M')

@app.template_filter('date')
def format_date(value):
    if value is None:
        return ""
    return value.strftime('%d.%m.%Y')

# Template'lerde kullanmak için datetime.utcnow fonksiyonunu ekle
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow}

if __name__ == '__main__':
    # debug=True for development, set to False in production
    app.run(debug=True, host='127.0.0.1', port=8080)

