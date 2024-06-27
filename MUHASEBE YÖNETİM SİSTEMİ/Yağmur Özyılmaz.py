import sqlite3 # sqlite3 kütüphanesini dahil ediyoruz
import csv # csv kütüphanesini dahil ediyoruz
import hashlib # hashlib kütüphanesini dahil ediyoruz
import os # os kütüphanesini dahil ediyoruz
from getpass import getpass # getpass kütüphanesinden getpass fonksiyonunu dahil ediyoruz
from termcolor import colored # termcolor kütüphanesinden colored fonksiyonunu dahil ediyoruz

def ekrani_temizle(): # Ekranı temizlemek için kullanılan fonksiyon
    os.system("cls" if os.name == "nt" else "clear") # Windows için cls, Linux için clear komutu çalıştırılıyor

def baglan(): # Veritabanına bağlanmak için kullanılan fonksiyon
    connection = sqlite3.connect("gelir_gider.db") # Veritabanı dosyası oluşturuluyor
    cursor = connection.cursor() # Veritabanı üzerinde işlem yapmak için cursor oluşturuluyor
    return connection, cursor # connection ve cursor değişkenleri döndürülüyor

oturumSahibi = None # Oturum açan kullanıcının kullanıcı adını tutan değişken

def baglanti_olustur(): # Veritabanı bağlantısını oluşturan fonksiyon
    try: # Veritabanı bağlantısı oluşturmayı deniyoruz
        connection, cursor = baglan() # Veritabanı bağlantısı oluşturuluyor
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kullanici (
                id INTEGER PRIMARY KEY,
                ad VARCHAR(255),
                soyad VARCHAR(255),
                kullanici_adi VARCHAR(255),
                sifre VARCHAR(255),
                statu VARCHAR(255) DEFAULT 'user'
            )
        """) # Kullanıcı tablosu oluşturuluyor

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gelir_gider (
                id INTEGER PRIMARY KEY,
                sirket VARCHAR(255),
                isim VARCHAR(255),
                miktar INT,
                sahibi VARCHAR(255),
                tur VARCHAR(255)
            )    
        """) # Gelir gider tablosu oluşturuluyor

        connection.commit() # Veritabanı üzerindeki değişiklikler kaydediliyor

        cursor.execute("SELECT * FROM kullanici") # Kullanıcı tablosundaki tüm verileri çekiyoruz
        result = cursor.fetchone() # Verileri tek tek alıyoruz
        if result is None:  # Eğer kullanıcı tablosunda hiç veri yoksa
            sifre_hash = hashlib.md5("admin".encode()).hexdigest() # Şifreyi md5 ile şifreleyip veritabanına kaydediyoruz
            cursor.execute("INSERT INTO kullanici (ad, soyad, kullanici_adi, sifre, statu) VALUES (?, ?, ?, ?, ?)", # Yöneticiyi manuel olarak ekliyoruz.
                           ("admin", "admin", "admin", sifre_hash, "yonetici")) # Yönetici kullanıcı adı ve şifresi admin
            connection.commit() # Veritabanı üzerindeki değişiklikler kaydediliyor
        
        print(colored("Veritabanı bağlantısı başarılı.", "green")) # Veritabanı bağlantısı başarılı mesajı yazdırılıyor
    except Exception as error: # Eğer veritabanı bağlantısı oluşturulamazsa
        print(colored("Veritabanı bağlantısı hatası:", "red"), error) # Veritabanı bağlantısı hatası mesajı yazdırılıyor
        exit() # Programdan çıkılıyor

def giris_ekrani(): # Giriş ekranını oluşturan fonksiyon
    print(colored("Bu program gelir giderlerinizi daha kolay tutmanız için Yağmur Nisa Özyılmaz tarafından geliştirilmiştir.", "yellow")) # Programın geliştiricisini belirten mesaj yazdırılıyor
    print(colored("Muhasebe Programı \nHoş Geldiniz!", "green")) # Programın adını ve versiyonunu belirten mesaj yazdırılıyor
    print(colored("1. Giriş Yap\n2. Kayıt Ol", "blue")) # Giriş yapma ve kayıt olma seçenekleri yazdırılıyor
    secim = input(colored("Seçiminizi yapın: ", "magenta")) # Kullanıcıdan seçim yapması isteniyor
    ekrani_temizle() # Ekran temizleniyor
    if secim == "1": # Eğer kullanıcı giriş yapmak isterse
        kullanici_girisi() # Kullanıcı giriş ekranı açılıyor
    elif secim == "2": # Eğer kullanıcı kayıt olmak isterse
        kayit_ol() # Kayıt olma ekranı açılıyor
    else: # Eğer kullanıcı geçersiz bir seçim yaparsa
        print(colored("Geçersiz seçim. Lütfen tekrar deneyin.", "red")) # Geçersiz seçim mesajı yazdırılıyor
        giris_ekrani()  # Giriş ekranı açılıyor


def kayit_ol(): # Kayıt olma ekranını oluşturan fonksiyon
    ad = input("Ad: ") # Kullanıcıdan adı isteniyor
    soyad = input("Soyad: ") # Kullanıcıdan soyadı isteniyor
    kullanici_adi = input("Kullanıcı Adı: ") # Kullanıcıdan kullanıcı adı isteniyor
    sifre = getpass("Şifre: ") # Kullanıcıdan şifre isteniyor
    sifre_tekrar = getpass("Şifre Tekrar: ") # Kullanıcıdan şifre tekrar isteniyor
    connection, cursor = baglan() # Veritabanı bağlantısı oluşturuluyor
    cursor.execute("SELECT * FROM kullanici WHERE kullanici_adi = ?", (kullanici_adi,)) # Kullanıcı adı veritabanında aranıyor
    result = cursor.fetchone() # Verileri tek tek alıyoruz
    if result: # Eğer kullanıcı adı veritabanında varsa
        print(colored("Bu kullanıcı adı zaten kullanılıyor. Lütfen tekrar deneyin.", "red")) # Kullanıcı adı zaten kullanılıyor mesajı yazdırılıyor
        kayit_ol() # Kayıt olma ekranı açılıyor
    else: # Eğer kullanıcı adı veritabanında yoksa
        if sifre == sifre_tekrar: # Eğer şifreler eşleşiyorsa
            sifre = hashlib.md5(sifre.encode()).hexdigest() # Şifreyi md5 ile şifreleyip veritabanına kaydediyoruz
            cursor.execute("INSERT INTO kullanici (ad, soyad, kullanici_adi, sifre, statu) VALUES (?, ?, ?, ?, ?)", (ad, soyad, kullanici_adi, sifre, "kullanici")) # Kullanıcıyı veritabanına kaydediyoruz
            connection.commit() # Veritabanı üzerindeki değişiklikler kaydediliyor
            print(colored("Kayıt başarılı.", "green")) # Kayıt başarılı mesajı yazdırılıyor
            giris_ekrani() # Giriş ekranı açılıyor
        else: # Eğer şifreler eşleşmiyorsa
            print(colored("Şifreler eşleşmiyor. Lütfen tekrar deneyin.", "red")) # Şifreler eşleşmiyor mesajı yazdırılıyor
            kayit_ol() # Kayıt olma ekranı açılıyor

def kullanici_girisi(): # Kullanıcı giriş ekranını oluşturan fonksiyon
    kullanici_adi = input("Kullanıcı Adı: ") # Kullanıcıdan kullanıcı adı isteniyor
    sifre = getpass("Şifre: ") # Kullanıcıdan şifre isteniyor

    giris_kontrol(kullanici_adi, sifre) # Kullanıcı adı ve şifreyi kontrol eden fonksiyon çağırılıyor

def giris_kontrol(kullanici_adi, sifre): # Kullanıcı adı ve şifreyi kontrol eden fonksiyon
    global oturumSahibi # Oturum sahibini global değişken olarak tanımlıyoruz
    oturumSahibi = kullanici_adi # Oturum sahibini kullanıcı adı olarak belirliyoruz
    sifre = hashlib.md5(sifre.encode()).hexdigest() # Şifreyi md5 ile şifreliyoruz
    connection, cursor = baglan() # Veritabanı bağlantısı oluşturuyoruz
    cursor.execute("SELECT * FROM kullanici WHERE kullanici_adi = ? AND sifre = ?", (kullanici_adi, sifre)) # Kullanıcı adı ve şifreyi veritabanında arıyoruz
    result = cursor.fetchone() # Verileri tek tek alıyoruz
    if result: # Eğer kullanıcı adı ve şifre veritabanında varsa
        if result[5] == "kullanici": # Eğer kullanıcı tipi kullanıcı ise
            kullanici_ekrani() # Kullanıcı ekranını açan fonksiyon
        elif result[5] == "yonetici":  # Eğer kullanıcı tipi yönetici ise
            admin_ekrani() # Admin ekranını açan fonksiyon
        elif result[5] == "muhasebe": # Eğer kullanıcı tipi muhasebe ise
            muhasebe_ekrani() # Muhasebe ekranını açan fonksiyon
        else: # Eğer kullanıcı tipi hatalı ise
            ekrani_temizle() # Ekranı temizleyen fonksiyon
            print(colored("Kullanıcı tipi hatalı. Lütfen tekrar deneyin.", "red"))
            kullanici_girisi() # Kullanıcı giriş ekranını açan fonksiyon
    else: # Eğer kullanıcı adı veya şifre hatalı ise
        ekrani_temizle() # Ekranı temizleyen fonksiyon
        print(colored("Kullanıcı adı veya şifre hatalı. Lütfen tekrar deneyin.", "red")) # Kullanıcı adı veya şifre hatalı mesajı yazdırılıyor
        kullanici_girisi() # Kullanıcı giriş ekranını açan fonksiyon

def kullaniciEkraninaDon(): # Kullanıcı ekranına dönen fonksiyon
    connection, cursor = baglan() # Veritabanı bağlantısı oluşturuyoruz
    cursor.execute("SELECT * FROM kullanici WHERE kullanici_adi = ?", (oturumSahibi,)) # Oturum sahibinin kullanıcı adını veritabanında arıyoruz
    result = cursor.fetchone()  # Verileri tek tek alıyoruz
    input(colored("Devam etmek için bir tuşa basın...", "green")) # Devam etmek için bir tuşa basın mesajı yazdırılıyor
    if result[5] == "kullanici": # Eğer kullanıcı tipi kullanıcı ise
        kullanici_ekrani() # Kullanıcı ekranını açan fonksiyon
    elif result[5] == "yonetici": # Eğer kullanıcı tipi yönetici ise
        admin_ekrani() # Admin ekranını açan fonksiyon
    elif result[5] == "muhasebe": # Eğer kullanıcı tipi muhasebe ise
        muhasebe_ekrani() # Muhasebe ekranını açan fonksiyon
    else: # Eğer kullanıcı tipi hatalı ise
        ekrani_temizle() # Ekranı temizleyen fonksiyon
        print(colored("Kullanıcı tipi hatalı. Lütfen tekrar deneyin.", "red")) # Kullanıcı tipi hatalı mesajı yazdırılıyor
        kullanici_girisi() # Kullanıcı giriş ekranını açan fonksiyon

def kullanici_ekrani(): # Kullanıcı ekranını oluşturan fonksiyon
    ekrani_temizle() # Ekranı temizleyen fonksiyon
    print(colored("Hoş Geldiniz!", "green")) # Hoş geldiniz mesajı yazdırılıyor
    print(colored("1. Gelir Ekle\n2. Gider Ekle\n3. Fatura Görüntüle\n4. CSV Çıktısı Al\n5. Çıkış Yap", "blue")) # Seçenekler yazdırılıyor

    secim = input(colored("Seçiminizi yapın: ", "magenta")) # Kullanıcıdan seçim isteniyor
    ekrani_temizle() # Ekranı temizleyen fonksiyon
    if secim == "1": # Eğer seçim 1 ise
        gelir_ekle() # Gelir ekleme ekranını açan fonksiyon
    elif secim == "2": # Eğer seçim 2 ise
        gider_ekle() # Gider ekleme ekranını açan fonksiyon
    elif secim == "3":  # Eğer seçim 3 ise
        fatura_goruntule() # Fatura görüntüleme ekranını açan fonksiyon
    elif secim == "4": # Eğer seçim 4 ise
        kullanici_csv_ciktisi_al(x = oturumSahibi) # CSV çıktısı alma fonksiyonunu çağırıyoruz
    elif secim == "5": # Eğer seçim 5 ise
        exit() # Programı kapatıyoruz
    else: # Eğer seçim 1, 2, 3, 4 veya 5 değil ise
        print(colored("Geçersiz seçim. Lütfen tekrar deneyin.", "red")) # Geçersiz seçim mesajı yazdırılıyor
        kullanici_ekrani() # Kullanıcı ekranını açan fonksiyon

def admin_ekrani(): # Admin ekranını oluşturan fonksiyon
    ekrani_temizle() # Ekranı temizleyen fonksiyon
    print(colored("Hoş geldiniz, Yönetici!", "green")) # Hoş geldiniz, Yönetici! mesajı yazdırılıyor
    print(colored("1. Kullanıcının Gelirini Sil\n2. Kullanıcının Giderini Sil\n3. Kullanıcının Gelirini Düzenle\n4. Kullanıcının Giderini Düzenle\n5. Kullanıcının Gelirini Ekle\n6. Kullanıcının Giderini Ekle\n7. CSV Çıktısı Al\n8. Kullanıcı Ekle\n9. Kullanıcı Sil\n10. Kullanıcı Düzenle\n11. Kapat", "blue"))
    secim = input(colored("Seçiminizi yapın: ", "magenta")) # Kullanıcıdan seçim isteniyor
    ekrani_temizle() # Ekranı temizleyen fonksiyon
    if secim == "1": # Eğer seçim 1 ise
        kullanici_gelir_sil() # Kullanıcı gelir silme ekranını açan fonksiyon
    elif secim == "2":  # Eğer seçim 2 ise
        kullanici_gider_sil()   # Kullanıcı gider silme ekranını açan fonksiyon
    elif secim == "3": # Eğer seçim 3 ise
        kullanici_gelir_duzenle() # Kullanıcı gelir düzenleme ekranını açan fonksiyon
    elif secim == "4": # Eğer seçim 4 ise
        kullanici_gider_duzenle() # Kullanıcı gider düzenleme ekranını açan fonksiyon
    elif secim == "5": # Eğer seçim 5 ise
        kullanici_gelir_ekle() # Kullanıcı gelir ekleme ekranını açan fonksiyon
    elif secim == "6": # Eğer seçim 6 ise
        kullanici_gider_ekle() # Kullanıcı gider ekleme ekranını açan fonksiyon
    elif secim == "7": # Eğer seçim 7 ise
        kullaniciAdi = input(colored("Kullanıcı adı: ", "magenta")) # Kullanıcı adı isteniyor
        kullanici_csv_ciktisi_al(x = kullaniciAdi) # CSV çıktısı alma fonksiyonunu çağırıyoruz
    elif secim == "8": # Eğer seçim 8 ise
        kullanici_ekle() # Kullanıcı ekleme ekranını açan fonksiyon
    elif secim == "9": # Eğer seçim 9 ise
        kullanici_sil() # Kullanıcı silme ekranını açan fonksiyon
    elif secim == "10": # Eğer seçim 10 ise
        kullanici_duzenle() # Kullanıcı düzenleme ekranını açan fonksiyon
    elif secim == "11": # Eğer seçim 11 ise
        print(colored("Çıkış yapılıyor...", "red")) # Çıkış yapılıyor mesajı yazdırılıyor
        exit() # Programı kapatıyoruz
    else: # Eğer seçim 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 veya 11 değil ise
        print(colored("Geçersiz seçim. Lütfen tekrar deneyin.", "red")) # Geçersiz seçim mesajı yazdırılıyor
        admin_ekrani() # Admin ekranını açan fonksiyon

def muhasebe_ekrani(): # Muhasebe ekranını oluşturan fonksiyon
    ekrani_temizle() # Ekranı temizleyen fonksiyon
    print(colored("Hoş Geldiniz!", "green")) # Hoş geldiniz mesajı yazdırılıyor
    print(colored("1. Kullanıcının Gelirini Sil\n2. Kullanıcının Giderini Sil\n3. Kullanıcının Gelirini Düzenle\n4. Kullanıcının Giderini Düzenle\n5. Kullanıcının Gelirini Ekle\n6. Kullanıcının Giderini Ekle\n7. CSV Çıktısı Al\n8. Kapat", "blue"))
    secim = input(colored("Seçiminizi yapın: ", "magenta")) # Kullanıcıdan seçim isteniyor
    ekrani_temizle() # Ekranı temizleyen fonksiyon
    if secim == "1": # Eğer seçim 1 ise
        kullanici_gelir_sil() # Kullanıcı gelir silme ekranını açan fonksiyon
    elif secim == "2": # Eğer seçim 2 ise
        kullanici_gider_sil() # Kullanıcı gider silme ekranını açan fonksiyon
    elif secim == "3": # Eğer seçim 3 ise
        kullanici_gelir_duzenle() # Kullanıcı gelir düzenleme ekranını açan fonksiyon
    elif secim == "4": # Eğer seçim 4 ise
        kullanici_gider_duzenle() # Kullanıcı gider düzenleme ekranını açan fonksiyon
    elif secim == "5": # Eğer seçim 5 ise
        kullanici_gelir_ekle() # Kullanıcı gelir ekleme ekranını açan fonksiyon
    elif secim == "6": # Eğer seçim 6 ise
        kullanici_gider_ekle() # Kullanıcı gider ekleme ekranını açan fonksiyon
    elif secim == "7": # Eğer seçim 7 ise 
        kullaniciAdi = input(colored("Kullanıcı adı: ", "magenta")) # Kullanıcı adı isteniyor
        kullanici_csv_ciktisi_al(x = kullaniciAdi) # CSV çıktısı alma fonksiyonunu çağırıyoruz
    elif secim == "8": # Eğer seçim 8 ise
        print(colored("Çıkış yapılıyor...", "red")) # Çıkış yapılıyor mesajı yazdırılıyor
        exit() # Programı kapatıyoruz
    else: # Eğer seçim 1, 2, 3, 4, 5, 6, 7 veya 8 değil ise
        print(colored("Geçersiz seçim. Lütfen tekrar deneyin.", "red")) # Geçersiz seçim mesajı yazdırılıyor
        muhasebe_ekrani() # Muhasebe ekranını açan fonksiyon

def gelir_ekle(): # Gelir ekleme ekranını oluşturan fonksiyon
    sirket = input("Şirket Adı: ") # Şirket adı isteniyor
    isim = input("Gelir İsmi: ") # Gelir ismi isteniyor
    miktar = float(input("Gelir Miktarı: ")) # Gelir miktarı isteniyor
    connection, cursor = baglan() # Veritabanına bağlanıyoruz
    cursor.execute("SELECT * FROM gelir_gider WHERE sirket = ? AND isim = ? AND sahibi = ? AND tur = ?", (sirket, isim, oturumSahibi, "gelir")) # Veritabanında gelirin olup olmadığını kontrol ediyoruz
    result = cursor.fetchone() # Veritabanından gelen sonucu alıyoruz
    if result: # Eğer sonuç var ise
        cursor.execute("UPDATE gelir_gider SET miktar = miktar + ? WHERE sirket = ? AND isim = ? AND sahibi = ? AND tur = ?", (miktar, sirket, isim, oturumSahibi, "gelir")) # Veritabanında gelirin miktarını güncelliyoruz
        connection.commit() # Veritabanına kaydediyoruz
        print(colored("Gelir başarıyla güncellendi.", "green")) # Gelir güncellendi mesajı yazdırılıyor
    else: # Eğer sonuç yok ise
        cursor.execute("INSERT INTO gelir_gider (sirket, isim, miktar, sahibi, tur) VALUES (?, ?, ?, ?, ?)", (sirket, isim, miktar, oturumSahibi, "gelir")) # Veritabanına geliri ekliyoruz
        connection.commit() # Veritabanına kaydediyoruz
        print(colored("Gelir başarıyla eklendi.", "green")) # Gelir eklendi mesajı yazdırılıyor
    cursor.close() # Cursoru kapatıyoruz
    kullaniciEkraninaDon() # Kullanıcı ekranına dönen fonksiyon

def gider_ekle(): # Gider ekleme ekranını oluşturan fonksiyon
    sirket = input("Şirket Adı: ") # Şirket adı isteniyor
    isim = input("Gider İsmi: ") # Gider ismi isteniyor
    miktar = float(input("Gider Miktarı: ")) # Gider miktarı isteniyor
    connection, cursor = baglan() # Veritabanına bağlanıyoruz
    cursor.execute("SELECT * FROM gelir_gider WHERE sirket = ? AND isim = ? AND sahibi = ? AND tur = ?", (sirket, isim, oturumSahibi, "gider")) # Veritabanında giderin olup olmadığını kontrol ediyoruz
    result = cursor.fetchone() # Veritabanından gelen sonucu alıyoruz
    if result: # Eğer sonuç var ise
        cursor.execute("UPDATE gelir_gider SET miktar = miktar + ? WHERE sirket = ? AND isim = ? AND sahibi = ? AND tur = ?", (miktar, sirket, isim, oturumSahibi, "gider")) # Veritabanında giderin miktarını güncelliyoruz
        connection.commit() # Veritabanına kaydediyoruz
        print(colored("Gider başarıyla güncellendi.", "green")) # Gider güncellendi mesajı yazdırılıyor
    else: # Eğer sonuç yok ise
        cursor.execute("INSERT INTO gelir_gider (sirket, isim, miktar, sahibi, tur) VALUES (?, ?, ?, ?, ?)", (sirket, isim, miktar, oturumSahibi, "gider")) # Veritabanına gideri ekliyoruz
        connection.commit() # Veritabanına kaydediyoruz
        print(colored("Gider başarıyla eklendi.", "green")) # Gider eklendi mesajı yazdırılıyor
    cursor.close() # Cursoru kapatıyoruz
    kullaniciEkraninaDon() # Kullanıcı ekranına dönülmesini sağlayan fonksiyon 

def fatura_goruntule(): # Fatura görüntüleme ekranını oluşturan fonksiyon
    print("Fatura Görüntüleme") # Fatura görüntüleme başlığı yazdırılıyor
    sirket = input("Şirket Adı: ") # Şirket adı isteniyor
    connection, cursor = baglan() # Veritabanına bağlanıyoruz
    cursor.execute("SELECT * FROM gelir_gider WHERE sirket = ? AND sahibi = ?", (sirket, oturumSahibi)) # Veritabanında faturanın olup olmadığını kontrol ediyoruz
    result = cursor.fetchall() # Veritabanından gelen sonucu alıyoruz
    if result: # Eğer sonuç var ise
        print("Ad\t\tMiktarı\t\tTürü") # Başlık yazdırılıyor
        for row in result: # Sonuçlar yazdırılıyor
            print(row[2] + "\t\t" + str(row[3]) + "\t\t" + row[5]) # Sonuçlar yazdırılıyor
    else: # Eğer sonuç yok ise
        print(colored("Fatura bulunamadı.", "red")) # Fatura bulunamadı mesajı yazdırılıyor
    kullaniciEkraninaDon() # Kullanıcı ekranına dönülmesini sağlayan fonksiyon

def kullanici_csv_ciktisi_al(x): # Kullanıcıya ait faturaları CSV olarak çıkartan fonksiyon
    print("CSV Çıktısı Alma") # CSV çıktısı alma başlığı yazdırılıyor
    sirket = input("Şirket Adı: ") # Şirket adı isteniyor
    connection, cursor = baglan() # Veritabanına bağlanıyoruz
    cursor.execute("SELECT * FROM gelir_gider WHERE sirket = ? AND sahibi = ?", (sirket, x)) # Veritabanında faturanın olup olmadığını kontrol ediyoruz
    result = cursor.fetchall() # Veritabanından gelen sonucu alıyoruz
    if result: # Eğer sonuç var ise
        with open("cikti.csv", "w", newline="") as file: # CSV dosyası oluşturuyoruz
            writer = csv.writer(file) # CSV dosyasına yazmak için writer oluşturuyoruz
            toplamGelir, toplamGider = 0, 0 # Toplam gelir ve gideri tutmak için değişkenler oluşturuyoruz
            writer.writerow(["Ad"] + ["Miktarı"] + ["Türü"]) # Başlık yazdırılıyor
            for row in result: # Sonuçlar yazdırılıyor
                writer.writerow([row[2]] + [row[3]] + [row[5]]) # Sonuçlar yazdırılıyor
                if row[5] == "gelir": # Eğer sonuç gelir ise
                    toplamGelir += row[3] # Toplam gelire ekleniyor
                else:
                    toplamGider += row[3] # Toplam gider ekleniyor

            writer.writerow([]) # Boş satır yazdırılıyor
            writer.writerow(["Toplam Gelir TL"] + [toplamGelir]) # Toplam gelir yazdırılıyor
            writer.writerow(["Toplam Gider TL"] + [toplamGider]) # Toplam gider yazdırılıyor
            writer.writerow(["Toplam Kar TL"] + [toplamGelir - toplamGider]) # Toplam kar yazdırılıyor
        print(colored("CSV çıktısı başarıyla alındı.", "green")) # CSV çıktısı alındı mesajı yazdırılıyor
    else: # Eğer sonuç yok ise
        print(colored("Fatura bulunamadı.", "red")) # Fatura bulunamadı mesajı yazdırılıyor
    kullaniciEkraninaDon() # Kullanıcı ekranına dönülüyor

def kullaniciBul(kadi): # Kullanıcı adına göre kullanıcıyı bulan fonksiyon
    connection, cursor = baglan() # Veritabanına bağlanıyoruz
    cursor.execute("SELECT * FROM kullanici WHERE kullanici_adi = ?", (kadi,)) # Veritabanında kullanıcının olup olmadığını kontrol ediyoruz
    result = cursor.fetchone() # Veritabanından gelen sonucu alıyoruz
    if result: # Eğer sonuç var ise
        return result # Sonucu döndürüyoruz
    else: # Eğer sonuç yok ise
        return None # None döndürüyoruz

def kullanici_gelir_sil(): # Kullanıcı gelirini silen fonksiyon
    print("Kullanıcının gelirini sil") # Kullanıcının gelirini sil başlığı yazdırılıyor
    kadi = input("Kullanıcı Adı: ") # Kullanıcı adı isteniyor
    sirket = input("Şirket Adı: ") # Şirket adı isteniyor
    gelir = input("Gelir Adı: ")    # Gelir adı isteniyor
    kullanici = kullaniciBul(kadi) # Kullanıcı adına göre kullanıcıyı bul ve kullanici değişkenine ata
    if kullanici: # Eğer kullanıcı var ise
        connection, cursor = baglan() # Veritabanına bağlanıyoruz
        cursor.execute("SELECT * FROM gelir_gider WHERE sirket = ? AND isim = ? AND sahibi = ? AND tur = ?", (sirket, gelir, kadi, "gelir")) # Veritabanında gelirin olup olmadığını kontrol ediyoruz
        result = cursor.fetchone() # Veritabanından gelen sonucu alıyoruz
        if result: # Eğer sonuç var ise
            cursor.execute("DELETE FROM gelir_gider WHERE sirket = ? AND isim = ? AND sahibi = ? AND tur = ?", (sirket, gelir, kadi, "gelir")) # Veritabanından geliri sil
            connection.commit() # Veritabanına kaydet
            print(colored("Gelir başarıyla silindi.", "green")) # Gelir başarıyla silindi mesajı yazdırılıyor
        else: # Eğer sonuç yok ise
            print(colored("Gelir bulunamadı.", "red")) # Gelir bulunamadı mesajı yazdırılıyor
    else: # Eğer kullanıcı yok ise
        print(colored("Kullanıcı bulunamadı.", "red")) # Kullanıcı bulunamadı mesajı yazdırılıyor
    kullaniciEkraninaDon() # Kullanıcı ekranına dön
    
def kullanici_gider_sil(): # Kullanıcı giderini silen fonksiyon
    print("Kullanıcının giderini sil") # Kullanıcının giderini sil başlığı yazdırılıyor
    kadi = input("Kullanıcı Adı: ") # Kullanıcı adı isteniyor
    sirket = input("Şirket Adı: ") # Şirket adı isteniyor
    gider = input("Gider Adı: ")   # Gider adı isteniyor
    kullanici = kullaniciBul(kadi) # Kullanıcı adına göre kullanıcıyı bul ve kullanici değişkenine ata
    if kullanici: # Eğer kullanıcı var ise
        connection, cursor = baglan() # Veritabanına bağlanıyoruz
        cursor.execute("SELECT * FROM gelir_gider WHERE sirket = ? AND isim = ? AND sahibi = ? AND tur = ?", (sirket, gider, kadi, "gider")) # Veritabanında giderin olup olmadığını kontrol ediyoruz
        result = cursor.fetchone() # Veritabanından gelen sonucu alıyoruz
        if result: # Eğer sonuç var ise
            cursor.execute("DELETE FROM gelir_gider WHERE sirket = ? AND isim = ? AND sahibi = ? AND tur = ?", (sirket, gider, kadi, "gider")) # Veritabanından gideri sil
            connection.commit() # Veritabanına kaydet
            print(colored("Gider başarıyla silindi.", "green"))     # Gider başarıyla silindi mesajı yazdırılıyor
        else: # Eğer sonuç yok ise
            print(colored("Gider bulunamadı.", "red")) # Gider bulunamadı mesajı yazdırılıyor
    else: # Eğer kullanıcı yok ise
        print(colored("Kullanıcı bulunamadı.", "red")) # Kullanıcı bulunamadı mesajı yazdırılıyor
    kullaniciEkraninaDon() # Kullanıcı ekranına dön

def kullanici_gelir_duzenle(): # Kullanıcı gelirini düzenleyen fonksiyon
    print("Kullanıcının gelirini düzenle") # Kullanıcının gelirini düzenle başlığı yazdırılıyor
    kadi = input("Kullanıcı Adı: ") # Kullanıcı adı isteniyor
    sirket = input("Şirket Adı: ") # Şirket adı isteniyor
    gelir = input("Gelir Adı: ")  # Gelir adı isteniyor
    kullanici = kullaniciBul(kadi) # Kullanıcı adına göre kullanıcıyı bul ve kullanici değişkenine ata
    if kullanici: # Eğer kullanıcı var ise
        connection, cursor = baglan() # Veritabanına bağlanıyoruz
        cursor.execute("SELECT * FROM gelir_gider WHERE sirket = ? AND isim = ? AND sahibi = ? AND tur = ?", (sirket, gelir, kadi, "gelir")) # Veritabanında gelirin olup olmadığını kontrol ediyoruz
        result = cursor.fetchone() # Veritabanından gelen sonucu alıyoruz
        print("Gelir bilgileri: ", result) # Gelir bilgilerini yazdırıyoruz
        if result: # Eğer sonuç var ise
            miktar = float(input("Gelir Miktarı: ")) # Gelir miktarı isteniyor
            cursor.execute("UPDATE gelir_gider SET miktar = ? WHERE sirket = ? AND isim = ? AND sahibi = ? AND tur = ?", (miktar, sirket, gelir, kadi, "gelir")) # Veritabanında gelir miktarını güncelliyoruz
            connection.commit() # Veritabanına kaydet
            print(colored("Gelir başarıyla güncellendi.", "green")) # Gelir başarıyla güncellendi mesajı yazdırılıyor
        else: # Eğer sonuç yok ise
            print(colored("Gelir bulunamadı.", "red"))  # Gelir bulunamadı mesajı yazdırılıyor
    else:   # Eğer kullanıcı yok ise
        print(colored("Kullanıcı bulunamadı.", "red"))  # Kullanıcı bulunamadı mesajı yazdırılıyor
    kullaniciEkraninaDon() # Kullanıcı ekranına dön

def kullanici_gider_duzenle(): # Kullanıcı giderini düzenleyen fonksiyon
    print("Kullanıcının giderini düzenle") # Kullanıcının giderini düzenle başlığı yazdırılıyor
    kadi = input("Kullanıcı Adı: ") # Kullanıcı adı isteniyor
    sirket = input("Şirket Adı: ")  # Şirket adı isteniyor
    gider = input("Gider Adı: ")    # Gider adı isteniyor
    kullanici = kullaniciBul(kadi) # Kullanıcı adına göre kullanıcıyı bul ve kullanici değişkenine ata
    if kullanici: # Eğer kullanıcı var ise
        connection, cursor = baglan() # Veritabanına bağlanıyoruz
        cursor.execute("SELECT * FROM gelir_gider WHERE sirket = ? AND isim = ? AND sahibi = ? AND tur = ?", (sirket, gider, kadi, "gider")) # Veritabanında giderin olup olmadığını kontrol ediyoruz
        result = cursor.fetchone() # Veritabanından gelen sonucu alıyoruz
        print("Gider bilgileri: ", result) # Gider bilgilerini yazdırıyoruz
        if result: # Eğer sonuç var ise
            miktar = float(input("Gider Miktarı: ")) # Gider miktarı isteniyor
            cursor.execute("UPDATE gelir_gider SET miktar = ? WHERE sirket = ? AND isim = ? AND sahibi = ? AND tur = ?", (miktar, sirket, gider, kadi, "gider")) # Veritabanında gider miktarını güncelliyoruz
            connection.commit() # Veritabanına kaydet
            print(colored("Gider başarıyla güncellendi.", "green")) # Gider başarıyla güncellendi mesajı yazdırılıyor
        else: # Eğer sonuç yok ise
            print(colored("Gider bulunamadı.", "red")) # Gider bulunamadı mesajı yazdırılıyor
    else: # Eğer kullanıcı yok ise
        print(colored("Kullanıcı bulunamadı.", "red")) # Kullanıcı bulunamadı mesajı yazdırılıyor
    kullaniciEkraninaDon() # Kullanıcı ekranına dön

def kullanici_gelir_ekle(): # Kullanıcı gelirini ekleyen fonksiyon
    print("Kullanıcının gelirini ekleyin") # Kullanıcının gelirini ekleyin başlığı yazdırılıyor
    kadi = input("Kullanıcı Adı: ") # Kullanıcı adı isteniyor
    sirket = input("Şirket Adı: ") # Şirket adı isteniyor
    gelir = input("Gelir Adı: ") # Gelir adı isteniyor
    miktari = float(input("Gelir Miktarı: ")) # Gelir miktarı isteniyor
    kullanici = kullaniciBul(kadi) # Kullanıcı adına göre kullanıcıyı bul ve kullanici değişkenine ata
    if kullanici: # Eğer kullanıcı var ise
        connection, cursor = baglan() # Veritabanına bağlanıyoruz
        cursor.execute("SELECT * FROM gelir_gider WHERE sirket = ? AND isim = ? AND sahibi = ? AND tur = ?", (sirket, gelir, kadi, "gelir")) # Veritabanında gelirin olup olmadığını kontrol ediyoruz
        result = cursor.fetchone() # Veritabanından gelen sonucu alıyoruz
        if result: # Eğer sonuç var ise
            cursor.execute("UPDATE gelir_gider SET miktar = miktar + ? WHERE sirket = ? AND isim = ? AND sahibi = ? AND tur = ?", (miktari, sirket, gelir, kadi, "gelir")) # Veritabanında gelir miktarını güncelliyoruz
            connection.commit() # Veritabanına kaydet
            print(colored("Gelir başarıyla eklendi.", "green")) # Gelir başarıyla eklendi mesajı yazdırılıyor
        else: # Eğer sonuç yok ise
            cursor.execute("INSERT INTO gelir_gider (sirket, isim, miktar, sahibi, tur) VALUES (?, ?, ?, ?, ?)", (sirket, gelir, miktari, kadi, "gelir")) # Veritabanına geliri ekliyoruz
            connection.commit() # Veritabanına kaydet
            print(colored("Gelir başarıyla eklendi.", "green")) # Gelir başarıyla eklendi mesajı yazdırılıyor
    else: # Eğer kullanıcı yok ise
        print(colored("Kullanıcı bulunamadı.", "red")) # Kullanıcı bulunamadı mesajı yazdırılıyor
    kullaniciEkraninaDon() # Kullanıcı ekranına dön

def kullanici_gider_ekle(): # Kullanıcı giderini ekleyen fonksiyon
    print("Kullanıcının giderini ekleyin") # Kullanıcının giderini ekleyin başlığı yazdırılıyor
    kadi = input("Kullanıcı Adı: ") # Kullanıcı adı isteniyor
    sirket = input("Şirket Adı: ") # Şirket adı isteniyor
    gider = input("Gider Adı: ") # Gider adı isteniyor
    miktari = float(input("Gider Miktarı: ")) # Gider miktarı isteniyor
    kullanici = kullaniciBul(kadi) # Kullanıcı adına göre kullanıcıyı bul ve kullanici değişkenine ata
    if kullanici: # Eğer kullanıcı var ise
        connection, cursor = baglan() # Veritabanına bağlanıyoruz
        cursor.execute("SELECT * FROM gelir_gider WHERE sirket = ? AND isim = ? AND sahibi = ? AND tur = ?", (sirket, gider, kadi, "gider")) # Veritabanında giderin olup olmadığını kontrol ediyoruz
        result = cursor.fetchone() # Veritabanından gelen sonucu alıyoruz
        if result: # Eğer sonuç var ise 
            cursor.execute("UPDATE gelir_gider SET miktar = miktar + ? WHERE sirket = ? AND isim = ? AND sahibi = ? AND tur = ?", (miktari, sirket, gider, kadi, "gider")) # Veritabanında gider miktarını güncelliyoruz
            connection.commit() # Veritabanına kaydet
            print(colored("Gider başarıyla eklendi.", "green")) # Gider başarıyla eklendi mesajı yazdırılıyor
        else: # Eğer sonuç yok ise
            cursor.execute("INSERT INTO gelir_gider (sirket, isim, miktar, sahibi, tur) VALUES (?, ?, ?, ?, ?)", (sirket, gider, miktari, kadi, "gider")) # Veritabanına gideri ekliyoruz
            connection.commit() # Veritabanına kaydet
            print(colored("Gider başarıyla eklendi.", "green")) # Gider başarıyla eklendi mesajı yazdırılıyor
    else: # Eğer kullanıcı yok ise
        print(colored("Kullanıcı bulunamadı.", "red")) # Kullanıcı bulunamadı mesajı yazdırılıyor
    kullaniciEkraninaDon() # Kullanıcı ekranına dön

def kullanici_ekle(): # Kullanıcı ekleyen fonksiyon
    connection, cursor = baglan() # Veritabanına bağlan
    print(colored("Kullanıcı eklemek için gerekli bilgileri girin.\nStatü seçenekleri: yonetici, muhasebe, kullanici", "green")) # Kullanıcı eklemek için gerekli bilgileri girin mesajı yazdırılıyor
    isim = input("İsim: ") # İsim isteniyor
    soyisim = input("Soyisim: ") # Soyisim isteniyor
    kadi = input("Kullanıcı Adı: ") # Kullanıcı adı isteniyor
    sifre = input("Şifre: ") # Şifre isteniyor
    statu = input("Statü: ")  # Statü isteniyor
    if len(isim) < 2 or len(soyisim) < 2 or len(kadi) < 2 or len(sifre) < 2 or statu not in ["yonetici", "muhasebe", "kullanici"]: # Eğer girilen bilgilerden herhangi biri 2 karakterden az ise veya statü seçeneklerinden biri değil ise
        print(colored("Geçersiz bilgi girdiniz. Lütfen tekrar deneyin.", "red")) # Geçersiz bilgi girdiniz mesajı yazdırılıyor
        kullanici_ekle() # Kullanıcı eklemeyi tekrar dene
    else: # Eğer girilen bilgiler geçerli ise
        cursor.execute("SELECT * FROM kullanici WHERE kullanici_adi = ?", (kadi,)) # Veritabanında kullanıcı adının olup olmadığını kontrol ediyoruz
        result = cursor.fetchone() # Veritabanından gelen sonucu alıyoruz
        if result != None: # Eğer sonuç var ise
            print(colored("Bu kullanıcı adı zaten kullanılıyor. Lütfen tekrar deneyin.", "red")) # Bu kullanıcı adı zaten kullanılıyor mesajı yazdırılıyor
            kullanici_ekle() # Kullanıcı eklemeyi tekrar dene
        else: # Eğer sonuç yok ise
            cursor.execute("INSERT INTO kullanici (ad, soyad, kullanici_adi, sifre, statu) VALUES (?, ?, ?, ?, ?)", (isim, soyisim, kadi, hashlib.md5(sifre.encode()).hexdigest(), statu)) # Veritabanına kullanıcıyı ekliyoruz
            connection.commit() # Veritabanına kaydet
            print(colored("{} Kullanıcısı başarıyla eklendi.".format(kadi), "green")) # Kullanıcı başarıyla eklendi mesajı yazdırılıyor
            cursor.close() # Cursor'ı kapat
            connection.close() # Bağlantıyı kapat
            admin_ekrani() # Admin ekranına dön

def kullanici_sil(): # Kullanıcı silen fonksiyon
    kadi = input("Silinecek kullanıcının kullanıcı adını girin: ") # Silinecek kullanıcının kullanıcı adı isteniyor
    if kadi == oturumSahibi: # Eğer silinecek kullanıcı oturum sahibi ise
        print(colored("Kendinizi silemezsiniz. Lütfen tekrar deneyin.", "red")) # Kendinizi silemezsiniz mesajı yazdırılıyor
        kullanici_sil() # Kullanıcı silmeyi tekrar dene
    connection, cursor = baglan() # Veritabanına bağlan
    cursor.execute("SELECT * FROM kullanici WHERE kullanici_adi = ?", (kadi,)) # Veritabanında kullanıcı adının olup olmadığını kontrol ediyoruz
    result = cursor.fetchone() # Veritabanından gelen sonucu alıyoruz
    if result == None: # Eğer sonuç yok ise
        print(colored("Kullanıcı bulunamadı. Lütfen tekrar deneyin.", "red")) # Kullanıcı bulunamadı mesajı yazdırılıyor
        kullanici_sil() # Kullanıcı silmeyi tekrar dene
    else: # Eğer sonuç var ise
        cursor.execute("DELETE FROM kullanici WHERE kullanici_adi = ?", (kadi,)) # Veritabanından kullanıcıyı siliyoruz
        connection.commit() # Veritabanına kaydet
        print(colored("{} Kullanıcısı başarıyla silindi.".format(kadi), "green")) # Kullanıcı başarıyla silindi mesajı yazdırılıyor
        cursor.close() # Cursor'ı kapat
        connection.close() # Bağlantıyı kapat
        admin_ekrani() # Admin ekranına dön


def kullanici_duzenle(): # Kullanıcı düzenleyen fonksiyon
    kadi = input("Düzenlenecek kullanıcının kullanıcı adını girin: ") # Düzenlenecek kullanıcının kullanıcı adı isteniyor
    if kadi == oturumSahibi: # Eğer düzenlenecek kullanıcı oturum sahibi ise
        print(colored("Kendinizi düzenleyemezsiniz. Lütfen tekrar deneyin.", "red")) # Kendinizi düzenleyemezsiniz mesajı yazdırılıyor
        kullanici_duzenle() # Kullanıcı düzenlemeyi tekrar dene
    connection, cursor = baglan() # Veritabanına bağlan
    cursor.execute("SELECT * FROM kullanici WHERE kullanici_adi = ?", (kadi,)) # Veritabanında kullanıcı adının olup olmadığını kontrol ediyoruz
    result = cursor.fetchone() # Veritabanından gelen sonucu alıyoruz
    if result == None: # Eğer sonuç yok ise
        print(colored("Kullanıcı bulunamadı. Lütfen tekrar deneyin.", "red")) # Kullanıcı bulunamadı mesajı yazdırılıyor
        kullanici_duzenle() # Kullanıcı düzenlemeyi tekrar dene
    else: # Eğer sonuç var ise
        statu = input("Statü seçenekleri: yonetici, muhasebe, kullanici\nStatü: ") # Statü isteniyor
        if statu not in ["yonetici", "muhasebe", "kullanici"]: # Eğer statü seçeneklerden biri değil ise
            print(colored("Geçersiz bilgi girdiniz. Lütfen tekrar deneyin.", "red"))    # Geçersiz bilgi girdiniz mesajı yazdırılıyor
            kullanici_duzenle() # Kullanıcı düzenlemeyi tekrar dene
        else: # Eğer statü seçeneklerden biri ise
            cursor.execute("UPDATE kullanici SET statu = ? WHERE kullanici_adi = ?", (statu, kadi)) # Veritabanında kullanıcının statüsünü güncelliyoruz
            connection.commit() # Veritabanına kaydet
            print(colored("{} Kullanıcısının statüsü başarıyla güncellendi.".format(kadi), "green")) # Kullanıcının statüsü başarıyla güncellendi mesajı yazdırılıyor
            cursor.close() # Cursor'ı kapat
            connection.close() # Bağlantıyı kapat
            admin_ekrani() # Admin ekranına dön

ekrani_temizle() # Ekranı temizle
baglanti = baglanti_olustur() # Veritabanı bağlantısını oluştur
giris_ekrani() # Giriş ekranını göster