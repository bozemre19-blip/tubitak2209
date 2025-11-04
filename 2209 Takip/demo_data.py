"""
Demo veri oluşturma scripti
Bu script, sistemde örnek sınıflar, öğrenciler ve ödevler oluşturur.
"""

from app import app, db
from models import User, Class, Assignment, Submission
from datetime import datetime, timedelta
import os

def create_demo_data():
    with app.app_context():
        print("🔄 Demo veriler oluşturuluyor...")
        
        # Admin kullanıcısını kontrol et
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("❌ Admin kullanıcısı bulunamadı!")
            return
        
        # Demo öğrenciler oluştur
        students = []
        demo_students = [
            {"username": "ahmet.yilmaz", "email": "ahmet@example.com", "full_name": "Ahmet Yılmaz"},
            {"username": "ayse.kaya", "email": "ayse@example.com", "full_name": "Ayşe Kaya"},
            {"username": "mehmet.demir", "email": "mehmet@example.com", "full_name": "Mehmet Demir"},
            {"username": "zeynep.celik", "email": "zeynep@example.com", "full_name": "Zeynep Çelik"},
            {"username": "ali.yildiz", "email": "ali@example.com", "full_name": "Ali Yıldız"},
        ]
        
        print("\n👥 Öğrenciler oluşturuluyor...")
        for student_data in demo_students:
            existing = User.query.filter_by(username=student_data["username"]).first()
            if not existing:
                student = User(
                    username=student_data["username"],
                    email=student_data["email"],
                    full_name=student_data["full_name"],
                    role='student'
                )
                student.set_password('12345')  # Basit şifre
                db.session.add(student)
                students.append(student)
                print(f"  ✅ {student_data['full_name']} oluşturuldu (şifre: 12345)")
            else:
                students.append(existing)
                print(f"  ℹ️  {student_data['full_name']} zaten mevcut")
        
        db.session.commit()
        
        # Demo sınıflar oluştur
        print("\n📚 Sınıflar oluşturuluyor...")
        demo_classes = [
            {
                "name": "Python Programlama",
                "code": "PY2024",
                "description": "Python programlama diline giriş ve temel konular"
            },
            {
                "name": "Veri Bilimi ve Analizi",
                "code": "DS2024",
                "description": "Veri bilimi teknikleri ve analiz yöntemleri"
            },
            {
                "name": "Web Geliştirme",
                "code": "WEB2024",
                "description": "Modern web teknolojileri ve framework'ler"
            }
        ]
        
        classes = []
        for class_data in demo_classes:
            existing = Class.query.filter_by(code=class_data["code"]).first()
            if not existing:
                new_class = Class(
                    name=class_data["name"],
                    code=class_data["code"],
                    description=class_data["description"],
                    created_by=admin.id
                )
                db.session.add(new_class)
                classes.append(new_class)
                print(f"  ✅ {class_data['name']} ({class_data['code']}) oluşturuldu")
            else:
                classes.append(existing)
                print(f"  ℹ️  {class_data['name']} zaten mevcut")
        
        db.session.commit()
        
        # Öğrencileri sınıflara kaydet
        print("\n🔗 Öğrenciler sınıflara kaydediliyor...")
        for i, student in enumerate(students):
            # Her öğrenci farklı sayıda sınıfa kayıt olsun
            for j, cls in enumerate(classes):
                if j <= i % 3:  # Her öğrenci 1-3 sınıfa kayıtlı
                    if cls not in student.enrolled_classes:
                        student.enrolled_classes.append(cls)
                        print(f"  ✅ {student.full_name} → {cls.name}")
        
        db.session.commit()
        
        # Demo ödevler oluştur
        print("\n📝 Ödevler oluşturuluyor...")
        assignments_data = [
            {
                "class_idx": 0,  # Python
                "assignments": [
                    {
                        "title": "İlk Python Programı",
                        "description": "Merhaba Dünya programı yazın ve temel veri tiplerini kullanın. Program en az 3 farklı veri tipi içermeli ve ekrana çıktı vermelidir.",
                        "days_from_now": 7,
                        "max_score": 100
                    },
                    {
                        "title": "Döngüler ve Koşullar",
                        "description": "For ve while döngülerini kullanarak 1-100 arası asal sayıları bulan bir program yazın. If-else yapılarını kullanarak çözümleyin.",
                        "days_from_now": 14,
                        "max_score": 100
                    },
                    {
                        "title": "Fonksiyonlar ve Modüller",
                        "description": "Matematiksel işlemler yapan (toplama, çıkarma, çarpma, bölme) fonksiyonlar içeren bir modül oluşturun.",
                        "days_from_now": -3,  # Geçmiş tarih
                        "max_score": 100
                    }
                ]
            },
            {
                "class_idx": 1,  # Veri Bilimi
                "assignments": [
                    {
                        "title": "Veri Analizi Projesi",
                        "description": "Pandas kütüphanesini kullanarak verilen CSV dosyasını analiz edin. En az 5 farklı istatistiksel hesaplama yapın.",
                        "days_from_now": 10,
                        "max_score": 100
                    },
                    {
                        "title": "Veri Görselleştirme",
                        "description": "Matplotlib veya Seaborn ile veri setinizdeki ilişkileri gösteren en az 5 farklı grafik oluşturun.",
                        "days_from_now": 21,
                        "max_score": 100
                    }
                ]
            },
            {
                "class_idx": 2,  # Web
                "assignments": [
                    {
                        "title": "HTML ve CSS ile Web Sayfası",
                        "description": "Modern ve responsive bir kişisel web sayfası tasarlayın. Bootstrap kullanabilirsiniz.",
                        "days_from_now": 5,
                        "max_score": 100
                    }
                ]
            }
        ]
        
        for assignment_group in assignments_data:
            cls = classes[assignment_group["class_idx"]]
            
            for assignment_data in assignment_group["assignments"]:
                due_date = datetime.utcnow() + timedelta(days=assignment_data["days_from_now"])
                
                existing = Assignment.query.filter_by(
                    title=assignment_data["title"],
                    class_id=cls.id
                ).first()
                
                if not existing:
                    assignment = Assignment(
                        title=assignment_data["title"],
                        description=assignment_data["description"],
                        class_id=cls.id,
                        due_date=due_date,
                        max_score=assignment_data["max_score"]
                    )
                    db.session.add(assignment)
                    print(f"  ✅ {cls.name} → {assignment_data['title']}")
        
        db.session.commit()
        
        print("\n" + "="*50)
        print("✅ Demo veriler başarıyla oluşturuldu!")
        print("="*50)
        print("\n📊 Oluşturulan Veriler:")
        print(f"  👥 Öğrenci sayısı: {len(students)}")
        print(f"  📚 Sınıf sayısı: {len(classes)}")
        print(f"  📝 Toplam ödev sayısı: {Assignment.query.count()}")
        print("\n🔑 Giriş Bilgileri:")
        print("  Admin:")
        print("    Kullanıcı adı: admin")
        print("    Şifre: admin123")
        print("\n  Örnek Öğrenci:")
        print("    Kullanıcı adı: ahmet.yilmaz")
        print("    Şifre: 12345")
        print("\n🌐 Uygulamayı başlatmak için:")
        print("  python app.py")
        print("  Tarayıcıda: http://localhost:5000")

if __name__ == '__main__':
    create_demo_data()

