"""
SQLite'dan PostgreSQL'e veri aktarım script'i
Bu script mevcut SQLite veritabanındaki tüm verileri PostgreSQL'e aktarır.
"""

import sqlite3
import os
from urllib.parse import urlparse
import psycopg2
from psycopg2.extras import execute_values

def get_sqlite_data():
    """SQLite veritabanından tüm verileri al"""
    sqlite_path = 'tubitak2209.db'
    
    if not os.path.exists(sqlite_path):
        print(f"❌ SQLite dosyası bulunamadı: {sqlite_path}")
        return None
    
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("✅ SQLite veritabanına bağlandı")
    
    # Tüm tabloları al
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall() if row[0] != 'sqlite_sequence']
    
    print(f"📊 Bulunan tablolar: {', '.join(tables)}")
    
    data = {}
    for table in tables:
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        data[table] = rows
        print(f"  ✅ {table}: {len(rows)} kayıt")
    
    conn.close()
    return data, tables

def parse_postgres_url(database_url):
    """PostgreSQL URL'ini parse et"""
    parsed = urlparse(database_url)
    return {
        'host': parsed.hostname,
        'port': parsed.port or 5432,
        'database': parsed.path[1:],  # Baştaki / işaretini kaldır
        'user': parsed.username,
        'password': parsed.password
    }

def migrate_to_postgresql(database_url, data, tables):
    """PostgreSQL'e veri aktar"""
    print("\n🔄 PostgreSQL'e bağlanılıyor...")
    
    try:
        # PostgreSQL bağlantısı
        conn_params = parse_postgres_url(database_url)
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        print("✅ PostgreSQL'e bağlandı")
        
        # Tabloları sırayla aktar
        table_order = ['user', 'class', 'assignment', 'submission', 'announcement', 
                      'announcement_read', 'notification', 'student_classes']
        
        for table in table_order:
            if table not in tables:
                continue
                
            rows = data[table]
            if not rows:
                print(f"  ⏭️  {table}: Boş, atlanıyor")
                continue
            
            print(f"\n📤 {table} aktarılıyor... ({len(rows)} kayıt)")
            
            # Sütun isimlerini al
            cursor.execute(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = '{table}' 
                ORDER BY ordinal_position
            """)
            columns = [row[0] for row in cursor.fetchall()]
            
            if not columns:
                print(f"  ⚠️  {table} tablosu PostgreSQL'de bulunamadı, atlanıyor")
                continue
            
            # Verileri aktar
            for row in rows:
                row_dict = dict(row)
                # Sadece PostgreSQL'deki sütunları kullan
                filtered_dict = {k: row_dict[k] for k in columns if k in row_dict}
                
                cols = list(filtered_dict.keys())
                vals = list(filtered_dict.values())
                placeholders = ', '.join(['%s'] * len(vals))
                
                query = f"""
                    INSERT INTO {table} ({', '.join(cols)})
                    VALUES ({placeholders})
                    ON CONFLICT DO NOTHING
                """
                
                try:
                    cursor.execute(query, vals)
                except Exception as e:
                    print(f"  ⚠️  Hata: {e}")
                    print(f"      Kayıt: {filtered_dict}")
            
            print(f"  ✅ {table}: {len(rows)} kayıt aktarıldı")
        
        conn.commit()
        conn.close()
        print("\n✅ Migration tamamlandı!")
        return True
        
    except Exception as e:
        print(f"\n❌ Hata: {e}")
        return False

def main():
    print("=" * 60)
    print("🚀 SQLite → PostgreSQL Migration Script")
    print("=" * 60)
    
    # 1. SQLite verilerini al
    result = get_sqlite_data()
    if not result:
        return
    
    data, tables = result
    
    # 2. PostgreSQL URL'ini al
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        database_url = input("\n📝 PostgreSQL DATABASE_URL girin: ").strip()
    
    if not database_url:
        print("❌ DATABASE_URL gerekli!")
        return
    
    # 3. Onay al
    print(f"\n⚠️  UYARI: Bu işlem PostgreSQL veritabanına veri ekleyecek.")
    print(f"📊 Aktarılacak toplam kayıt sayısı:")
    total = sum(len(rows) for rows in data.values())
    print(f"   {total} kayıt")
    
    confirm = input("\n❓ Devam etmek istiyor musunuz? (evet/hayır): ").strip().lower()
    if confirm not in ['evet', 'e', 'yes', 'y']:
        print("❌ İşlem iptal edildi")
        return
    
    # 4. Migration yap
    success = migrate_to_postgresql(database_url, data, tables)
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 Migration başarıyla tamamlandı!")
        print("=" * 60)
        print("\n📝 Sonraki adımlar:")
        print("1. Render'da web servisinize DATABASE_URL environment variable ekleyin")
        print("2. Render'da servisi yeniden deploy edin")
        print("3. Verilerin doğru geldiğini kontrol edin")
    else:
        print("\n❌ Migration başarısız oldu!")

if __name__ == '__main__':
    main()

