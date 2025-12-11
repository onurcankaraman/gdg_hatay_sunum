# Veri Analizi ve Korelasyon Çalışması

## 📊 Veri Seti Tanıtımı

### Genel Bilgiler
- **Dosya**: `Dataset.xlsx`
- **Toplam Kayıt**: 1,838 örnek
- **Zaman Aralığı**: 30 dakikalık operasyon
- **Örnekleme Frekansı**: Dakikada 1 kesim
- **Makine**: Digitheta CNC Testere
- **İşlenen Malzeme**: Alüminyum 40×40mm bloklar

### Değişkenler

| Değişken | Açıklama | Birim | Tip |
|----------|----------|-------|-----|
| zaman | Zaman damgası | - | Datetime |
| AşınmaOranı | Testere bıçağı aşınma oranı | mm/saat | Hedef |
| Kesme Gücü | Kesme işleminde harcanan güç | W (Watt) | Özellik |
| İlerleme Hızı | Testere bıçağının ilerleme hızı | mm/min | Özellik |
| RPM | Testere bıçağının dönüş hızı | devir/dakika | Özellik |

## 📈 Tanımlayıcı İstatistikler

### AşınmaOranı (Hedef Değişken)
```
Ortalama:     7.13 mm/saat
Std Sapma:    2.40 mm/saat
Minimum:      0.73 mm/saat
Q1 (25%):     5.67 mm/saat
Medyan (50%): 7.44 mm/saat
Q3 (75%):     8.99 mm/saat
Maksimum:    12.39 mm/saat
```

### Kesme Gücü
```
Ortalama:   150.14 W
Std Sapma:   50.12 W
Minimum:     50.01 W
Maksimum:   249.99 W
```

### İlerleme Hızı
```
Ortalama:    79.95 mm/min
Std Sapma:   28.82 mm/min
Minimum:     20.02 mm/min
Maksimum:   139.97 mm/min
```

### RPM
```
Ortalama:   2500.7 devir/dakika
Std Sapma:   866.5 devir/dakika
Minimum:    1000.5 devir/dakika
Maksimum:   4000.0 devir/dakika
```

## 🔗 Korelasyon Analizi

### Korelasyon Matrisi

|  | AşınmaOranı | Kesme Gücü | İlerleme Hızı | RPM |
|--|-------------|------------|---------------|-----|
| **AşınmaOranı** | 1.000 | -0.745 | -0.746 | -0.745 |
| **Kesme Gücü** | -0.745 | 1.000 | 0.917 | 1.000 |
| **İlerleme Hızı** | -0.746 | 0.917 | 1.000 | 0.917 |
| **RPM** | -0.745 | 1.000 | 0.917 | 1.000 |

### Önemli Bulgular

#### 1. Hedef Değişken ile Korelasyonlar (Negatif - Güçlü)
- **Kesme Gücü ↔ AşınmaOranı**: r = -0.745
  - Kesme gücü arttıkça aşınma oranı **azalıyor**
  - Güçlü negatif korelasyon
  
- **İlerleme Hızı ↔ AşınmaOranı**: r = -0.746
  - İlerleme hızı arttıkça aşınma oranı **azalıyor**
  - En güçlü negatif korelasyon
  
- **RPM ↔ AşınmaOranı**: r = -0.745
  - RPM arttıkça aşınma oranı **azalıyor**
  - Güçlü negatif korelasyon

#### 2. Özellikler Arası Korelasyonlar (Pozitif - Çok Güçlü)
- **Kesme Gücü ↔ RPM**: r = 1.000
  - Mükemmel pozitif korelasyon (multicollinearity)
  
- **Kesme Gücü ↔ İlerleme Hızı**: r = 0.917
  - Çok güçlü pozitif korelasyon
  
- **İlerleme Hızı ↔ RPM**: r = 0.917
  - Çok güçlü pozitif korelasyon

## 🎯 Fiziksel Yorumlama

### Neden Yüksek Parametrelerde Aşınma Azalıyor?

1. **Termal Etki**
   - Yüksek hızda kesim → Daha fazla ısı üretimi
   - Alüminyum yumuşar → Kesme kolaylaşır
   - Testere üzerinde daha az mekanik stres

2. **Kesme Mekaniği**
   - Yüksek RPM → Talaş boyutu küçülür
   - Küçük talaş → Daha az sürtünme
   - Az sürtünme → Az aşınma

3. **İlerleme Hızı**
   - Hızlı ilerleme → Temas süresi kısalır
   - Kısa temas → Az ısıl döngü
   - Az ısıl döngü → Az yorulma aşınması

## 📉 Veri Kalitesi

### Eksik Değerler
```
AşınmaOranı:     0 eksik (0.0%)
Kesme Gücü:      0 eksik (0.0%)
İlerleme Hızı:   0 eksik (0.0%)
RPM:             0 eksik (0.0%)
```

✅ Veri setinde **hiç eksik değer yok**.

### Veri Dağılımı
- Tüm özellikler yaklaşık **uniform (düzgün) dağılım** gösteriyor
- Aykırı değer (outlier) sayısı minimal
- Veri dengeli ve temiz

## 🔍 Görselleştirme

### 1. Korelasyon Heatmap
- Tüm değişkenler arası ilişkileri gösterir
- Renkler: Mavi (negatif) → Kırmızı (pozitif)
- Boyut: Korelasyon katsayısının büyüklüğü

### 2. Scatter Plot Matrix
- Her özelliğin birbiriyle ilişkisini gösterir
- Diagonal: Histogram (dağılım)
- Off-diagonal: Scatter plots (ilişki)

### 3. Zaman Serisi Grafikleri
- Tüm değişkenlerin zamana göre değişimi
- Trend analizi
- Döngüsel paternler

## 💡 Çıkarımlar

1. **Model için en önemli özellikler**:
   - İlerleme Hızı (r = -0.746)
   - Kesme Gücü (r = -0.745)
   - RPM (r = -0.745)

2. **Multicollinearity riski**:
   - Kesme Gücü ve RPM arasında mükemmel korelasyon (r = 1.000)
   - Model oluştururken dikkat edilmeli
   - Feature selection gerekebilir

3. **Tahmin başarısı beklentisi**:
   - Güçlü korelasyonlar → İyi tahmin performansı bekleniyor
   - R² score > 0.55 hedefleniyor

## 📚 Sonraki Adımlar

1. ✅ SPC (Statistical Process Control) analizi
2. ✅ Makine öğrenmesi model geliştirme
3. ✅ Hyperparameter tuning
4. ✅ Model deployment (Docker API)

---

**Not**: Detaylı analizler için `correlation_analysis.ipynb` notebook'una bakınız.
