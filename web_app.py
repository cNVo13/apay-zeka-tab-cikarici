import streamlit as st
import pretty_midi
import os

# Sitenin başlığı ve açıklaması
st.set_page_config(page_title="Yapay Zeka Tab Çıkarıcı", page_icon="🎸")
st.title("🎸 Yapay Zeka ile Gitar Tabı Çıkarıcı")
st.write("Sesi yükle, yapay zeka dinlesin ve sana saniye saniye tabları döksün!")

# Standart gitar tel frekansları
gitar_telleri = {
    1: 64, 2: 59, 3: 55, 4: 50, 5: 45, 6: 40
}

# Kullanıcıdan müzik dosyası alma butonu
yuklenen_dosya = st.file_uploader("Bir ses dosyası yükle (WAV veya MP3)", type=["wav", "mp3"])

if yuklenen_dosya is not None:
    st.success("Müzik başarıyla yüklendi! İşlem başlatılıyor...")
    
    # Yüklenen dosyayı geçici olarak kaydet
    with open("gecici_sarki.wav", "wb") as f:
        f.write(yuklenen_dosya.getbuffer())
    
    # Basic Pitch yapay zekasını çalıştır (Terminal komutunu arka planda tetikler)
    with st.spinner('Yapay zeka akorları çözümlüyor, bu biraz sürebilir...'):
        os.system("basic-pitch ./ gecici_sarki.wav")
    
    st.success("Polifonik analiz tamamlandı! Tablar hazırlanıyor...")
    
    # Çıkan MIDI dosyasını oku ve Tablara çevir
    try:
        midi_dosyasi = "gecici_sarki_basic_pitch.mid"
        midi_veri = pretty_midi.PrettyMIDI(midi_dosyasi)
        
        # Ekrana tablo başlıklarını yazdır
        st.write("### 🎶 Çıkarılan Gitar Tabları")
        tablo_verisi = []
        
        for enstruman in midi_veri.instruments:
            for nota in enstruman.notes[:50]: # İlk 50 notayı al
                zaman = round(nota.start, 2)
                midi_no = nota.pitch
                nota_adi = pretty_midi.note_number_to_name(midi_no)
                
                uygun_tel = 6
                perde = 0
                
                for tel, tel_baslangic in sorted(gitar_telleri.items()):
                    if midi_no >= tel_baslangic and (midi_no - tel_baslangic) <= 14:
                        uygun_tel = tel
                        perde = midi_no - tel_baslangic
                        break
                
                # Tablo satırını oluştur
                tablo_verisi.append({
                    "Zaman (sn)": f"{zaman:.2f}", 
                    "Nota": nota_adi, 
                    "Tel": f"{uygun_tel}. Tel", 
                    "Perde": perde
                })
        
        # Veriyi web sitesinde şık bir tablo olarak göster
        st.table(tablo_verisi)
        
    except Exception as e:
        st.error("Tablar oluşturulurken bir hata oluştu. Lütfen tekrar dene.")