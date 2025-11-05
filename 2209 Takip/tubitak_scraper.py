"""
TÜBİTAK 2209-A Program sayfasından bilgi çekme modülü
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

TUBITAK_2209_URL = "https://tubitak.gov.tr/tr/burslar/lisans-onlisans/destek-programlari/2209-universite-ogrencileri-arastirma-projeleri-destekleme-programi"

def fetch_tubitak_announcements():
    """
    TÜBİTAK 2209-A sayfasından önemli bilgileri çek
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(TUBITAK_2209_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        announcements = []
        
        # Ana başlık ve önemli duyurular
        main_content = soup.find('div', class_='content') or soup.find('main') or soup.find('article')
        
        if main_content:
            # Önemli duyuru metinlerini bul (kalın yazılmış, vurgulu)
            important_texts = main_content.find_all(['strong', 'b', 'h2', 'h3'])
            
            for text_elem in important_texts:
                text = text_elem.get_text(strip=True)
                
                # Önemli bilgileri filtrele
                if any(keyword in text.lower() for keyword in [
                    'başvuru', 'çağrı', 'açılmıştır', 'tarih', 'son', 
                    '2025', '2024', 'kasım', 'aralık', 'ocak', 'şubat',
                    'tybs', 'yönetim bilgi sistemi', 'sonuç', 'değerlendirme'
                ]):
                    if len(text) > 20 and len(text) < 500:  # Uygun uzunlukta
                        announcements.append({
                            'text': text,
                            'type': 'important'
                        })
            
            # Başvuru tarihlerini bul
            date_patterns = [
                r'(\d{1,2}\s+(Kasım|Aralık|Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim)\s+\d{4})',
                r'(\d{1,2}\.\d{1,2}\.\d{4})',
                r'(\d{1,2}/\d{1,2}/\d{4})'
            ]
            
            full_text = main_content.get_text()
            for pattern in date_patterns:
                matches = re.findall(pattern, full_text, re.IGNORECASE)
                if matches:
                    for match in matches[:3]:  # İlk 3 eşleşme
                        date_text = match[0] if isinstance(match, tuple) else match
                        announcements.append({
                            'text': f'Başvuru Tarihi: {date_text}',
                            'type': 'date'
                        })
            
            # Özel linkler ve dosyalar
            links = main_content.find_all('a', href=True)
            for link in links:
                link_text = link.get_text(strip=True)
                href = link.get('href', '')
                
                if any(keyword in link_text.lower() for keyword in [
                    'çağrı duyurusu', 'başvuru', 'form', 'yönetmelik', 'esaslar'
                ]):
                    if href.startswith('http'):
                        announcements.append({
                            'text': link_text,
                            'link': href,
                            'type': 'link'
                        })
        
        # Sonuçları temizle ve birleştir
        unique_announcements = []
        seen_texts = set()
        
        for ann in announcements:
            text_key = ann['text'][:100]  # İlk 100 karakter
            if text_key not in seen_texts:
                seen_texts.add(text_key)
                unique_announcements.append(ann)
        
        return {
            'success': True,
            'announcements': unique_announcements[:10],  # En fazla 10
            'fetched_at': datetime.utcnow(),
            'source_url': TUBITAK_2209_URL
        }
        
    except requests.RequestException as e:
        return {
            'success': False,
            'error': f'Bağlantı hatası: {str(e)}',
            'fetched_at': datetime.utcnow()
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'İşlem hatası: {str(e)}',
            'fetched_at': datetime.utcnow()
        }

def get_latest_important_info():
    """
    En son önemli bilgiyi döndür - TÜBİTAK sayfasından direkt çek
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(TUBITAK_2209_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Sayfanın ana içeriğini bul
        main_content = soup.find('div', class_='content') or soup.find('main') or soup.find('article') or soup.find('body')
        
        if not main_content:
            return None
        
        # Önemli duyuruları içeren bölümleri bul
        # Genellikle kalın yazılmış (strong, b) veya başlık (h1, h2, h3) içinde
        important_elements = main_content.find_all(['strong', 'b', 'h1', 'h2', 'h3', 'p'])
        
        # Başvuru tarihleri ve önemli bilgileri içeren metinleri bul
        important_text = None
        
        for elem in important_elements:
            text = elem.get_text(strip=True)
            
            # Başvuru açılmış mı kontrolü
            if any(keyword in text.lower() for keyword in [
                'başvuruya açılmıştır', 'başvuru açılmıştır', 'çağrı açılmıştır',
                'başvurular', '2025 yılı çağrısı', 'tybs.tubitak.gov.tr'
            ]):
                # Yeterince uzun ve anlamlı mı kontrol et
                if len(text) > 30 and len(text) < 500:
                    important_text = text
                    break
        
        # Eğer direkt bulamadıysak, tüm metni tarayalım
        if not important_text:
            full_text = main_content.get_text()
            
            # Başvuru tarihi pattern'leri
            patterns = [
                r'2209-A.*?başvuruya açılmıştır.*?(\d{1,2}\s+(Kasım|Aralık|Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim)\s+\d{4}.*?17\.30)',
                r'başvurular.*?(\d{1,2}\s+(Kasım|Aralık|Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim)\s+\d{4}.*?17\.30)',
                r'2209-A.*?2025.*?çağrısı.*?başvuruya açılmıştır',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, full_text, re.IGNORECASE | re.DOTALL)
                if match:
                    # Eşleşen metni bul ve temizle
                    matched_text = match.group(0)
                    # Çok uzunsa kısalt
                    if len(matched_text) > 300:
                        matched_text = matched_text[:300] + '...'
                    important_text = matched_text.strip()
                    break
        
        # Eğer hala bulamadıysak, genel bir bilgi ver
        if not important_text:
            # En azından sayfanın başındaki önemli bilgiyi al
            first_paragraph = main_content.find('p')
            if first_paragraph:
                text = first_paragraph.get_text(strip=True)
                if len(text) > 50 and len(text) < 400:
                    important_text = text
        
        if important_text:
            return {
                'title': 'TÜBİTAK 2209-A Program Güncel Bilgisi',
                'content': important_text,
                'link': TUBITAK_2209_URL,
                'fetched_at': datetime.utcnow()
            }
        
        return None
        
    except requests.RequestException as e:
        # Hata durumunda sessizce None döndür (site çalışmaya devam etsin)
        print(f"⚠️ TÜBİTAK scraper hatası: {e}")
        return None
    except Exception as e:
        print(f"⚠️ TÜBİTAK scraper hatası: {e}")
        return None

