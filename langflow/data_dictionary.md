# 📚 Veri Sözlüğü - GDG Hatay CNC Aşınma Sistemi

Bu belge, proje veri setindeki tüm değişkenlerin detaylı açıklamalarını içerir.

---

## 📊 Özellik Değişkenleri (Features)

### 1. Kesme Gücü (Cutting Power)

**Kolon Adı**: `Kesme Gücü`
**Veri Tipi**: Float (IEEE 754)
**Birim**: Watt (W)
**Kategori**: İnput Özelliği

**Açıklama**:
Testere bıçağının kesilmekte olan malzemeyi kesebilmek için harcadığı elektriksel güçtür. CNC testere motorunun çıkış gücünü temsil eder.

**Değer Aralığı**:
- **Minimum**: 95.2 W
- **Maximum**: 205.8 W
- **Ortalama**: 150.3 W
- **Standart Sapma**: 28.1 W
- **Quartile 1**: 127.4 W
- **Median (Q2)**: 150.1 W
- **Quartile 3**: 173.2 W

**İstatistikler**:
```
Çarpıklık (Skewness):    0.018 (Neredeyse simetrik)
Basıklık (Kurtosis):     -0.421 (Hafif datar)
```

**Korelasyon ile Hedef**:
- İlişki: r = -0.745 (Güçlü negatif)
- Yorum: Yüksek kesme gücü → Düşük aşınma

**Tahmin Önemisi**: 25.3% (Model'de 2. önemli)

**Pratik Kullanım Aralığı**:
- **Düşük Güç** (< 120 W): Çok ince işlemler, kütüğün ilk kesimleri
- **Normal Güç** (120-180 W): Standart kesilme operasyonu
- **Yüksek Güç** (> 180 W): Ağır kesilme, kalın malzeme

**İlgili Parametreler**:
- RPM ile ilişki: r = 1.000 (Mükemmel pozitif)
- İlerleme Hızı ile ilişki: r = 0.998 (Neredeyse mükemmel)

---

### 2. İlerleme Hızı (Feed Rate)

**Kolon Adı**: `İlerleme Hızı`
**Veri Tipi**: Float (IEEE 754)
**Birim**: Milimetre/Dakika (mm/min)
**Kategori**: İnput Özelliği

**Açıklama**:
Testere bıçağının malzeme içinde ilerleme hızıdır. CNC parametrelerinde ayarlanabilen bir değerdir ve malzemenin kesme hızını belirler.

**Değer Aralığı**:
- **Minimum**: 40.5 mm/min
- **Maximum**: 119.8 mm/min
- **Ortalama**: 80.1 mm/min
- **Standart Sapma**: 18.9 mm/min
- **Quartile 1**: 62.3 mm/min
- **Median (Q2)**: 80.0 mm/min
- **Quartile 3**: 98.5 mm/min

**İstatistikler**:
```
Çarpıklık (Skewness):    0.012 (Çok simetrik)
Basıklık (Kurtosis):     -0.487 (Hafif datar)
```

**Korelasyon ile Hedef**:
- İlişki: r = -0.746 (Güçlü negatif)
- Yorum: Yüksek ilerleme hızı → Düşük aşınma

**Tahmin Önemisi**: 52.5% (Model'de EN ÖNEMLİ)

**Pratik Kullanım Aralığı**:
- **Çok Yavaş** (< 50 mm/min): Hassas kesimler, inceltme
- **Yavaş** (50-75 mm/min): Kaliteli kesim, az aşınma
- **Normal** (75-95 mm/min): Standart operasyon (Tercih)
- **Hızlı** (> 95 mm/min): Hızlı kesim, verimlilik amaçlı

**Tahmin Modeline Etkisi**:
Bu özellik modelin en önemli predictor'udur. İlerleme hızındaki 1 mm/min değişim, tahmin edilen aşınma oranında belirgin etki yaratır.

---

### 3. RPM (Revolutions Per Minute)

**Kolon Adı**: `RPM`
**Veri Tipi**: Float (IEEE 754)
**Birim**: Devir/Dakika (rev/min)
**Kategori**: İnput Özelliği

**Açıklama**:
Testere bıçağının dakikada yaptığı dönüş sayısıdır. Motor hızı olarak da bilinir ve malzemenin kesme hızını etkiler.

**Değer Aralığı**:
- **Minimum**: 1800 rev/min
- **Maximum**: 3200 rev/min
- **Ortalama**: 2500 rev/min
- **Standart Sapma**: 421.3 rev/min
- **Quartile 1**: 2100 rev/min
- **Median (Q2)**: 2500 rev/min
- **Quartile 3**: 2900 rev/min

**İstatistikler**:
```
Çarpıklık (Skewness):    0.018 (Neredeyse simetrik)
Basıklık (Kurtosis):     -0.421 (Hafif datar)
```

**Korelasyon ile Hedef**:
- İlişki: r = -0.745 (Güçlü negatif)
- Yorum: Yüksek RPM → Düşük aşınma

**Tahmin Önemisi**: 22.2% (Model'de 3. önemli)

**Pratik Kullanım Aralığı**:
- **Düşük RPM** (< 2000): Kalın malzeme, sert materyel
- **Normal RPM** (2000-2800): Standart alüminyum kesilmesi
- **Yüksek RPM** (> 2800): İnce malzeme, hızlı kesim

**Teknik Notlar**:
- Kesme Gücü ile mükemmel korelasyon (r = 1.000)
- Bu nedenle multicollinearity riski var
- Model, özellik redundantsı göz ardı edebilir

---

## 🎯 Hedef Değişken

### Aşınma Oranı (Wear Rate)

**Kolon Adı**: `AşınmaOranı`
**Veri Tipi**: Float (IEEE 754)
**Birim**: Milimetre/Saat (mm/saat)
**Kategori**: Tahmin Hedefi (Target)

**Açıklama**:
Testere bıçağının 1 saat işletim süresi içinde kaybettiği malzeme miktarıdır. Bıçak kalite ve işlem parametrelerine bağlı olarak değişir.

**Değer Aralığı**:
- **Minimum**: 0.5 mm/saat
- **Maximum**: 12.8 mm/saat
- **Ortalama**: 6.2 mm/saat
- **Standart Sapma**: 2.3 mm/saat
- **Quartile 1**: 4.1 mm/saat
- **Median (Q2)**: 6.2 mm/saat
- **Quartile 3**: 8.3 mm/saat

**İstatistikler**:
```
Çarpıklık (Skewness):    0.012 (Simetrik dağılım)
Basıklık (Kurtosis):     -0.512 (Hafif datar)
```

**Dağılım**:
- **< 3 mm/saat**: 15% (Çok iyi durum)
- **3-6 mm/saat**: 42% (Normal işletim)
- **6-9 mm/saat**: 33% (İyi koşullar)
- **> 9 mm/saat**: 10% (Yüksek aşınma)

**Tahmin Hedefi Olarak Kullanım**:
Makine öğrenmesi modelinin tahmin etmeye çalıştığı değişkendir. Düşük RMSE (1.503) ve iyi R² (0.564) ile tahmin edilebilir.

**Kalite Metrikleri**:
- **Kabul Edilebilir Aşınma**: < 8 mm/saat
- **İdeal Aşınma**: < 5 mm/saat
- **Kritik Seviye**: > 10 mm/saat (Bıçak değiştirilmeli)

**Model Tahmin Doğruluğu**:
```
Hata < 0.5 mm/saat: 28%
Hata < 1.0 mm/saat: 62%
Hata < 1.5 mm/saat: 86%
Hata < 2.0 mm/saat: 94%
```

---

## 📈 Değişkenler Arası İlişkiler

### Korelasyon Matrisi

```
                Kesme Gücü  İlerleme Hızı  RPM  AşınmaOranı
Kesme Gücü         1.000      0.998       1.000   -0.745
İlerleme Hızı      0.998      1.000       0.998   -0.746
RPM                1.000      0.998       1.000   -0.745
AşınmaOranı       -0.745     -0.746      -0.745    1.000
```

### Açıklamalar

1. **Kesme Gücü ↔ RPM = 1.000** (Mükemmel pozitif)
   - Motor hızı arttıkça güç tüketimi artar
   - Sabit ilişki, deterministik

2. **Kesme Gücü ↔ İlerleme Hızı = 0.998** (Neredeyse mükemmel)
   - Hızlı ilerleme daha fazla güç gerektirir
   - İlişki doğrusal ve güçlü

3. **Tüm Özellikler ↔ AşınmaOranı = -0.745** (Güçlü negatif)
   - Parametreler arttıkça aşınma azalır
   - Fiziksel açıdan mantıklı (yumuşak malzeme, kolay kesim)

---

## 🔢 Veri İstatistikleri

### Merkez Eğilimleri (Central Tendency)

| Değişken | Ortalama | Median | Mod |
|----------|----------|--------|-----|
| Kesme Gücü | 150.3 W | 150.1 W | 148.5 W |
| İlerleme Hızı | 80.1 mm/min | 80.0 mm/min | 79.2 mm/min |
| RPM | 2500 rev/min | 2500 rev/min | 2497 rev/min |
| AşınmaOranı | 6.2 mm/saat | 6.2 mm/saat | 6.1 mm/saat |

### Yayılım Ölçüleri (Dispersion)

| Değişken | Std Dev | Varyans | CV (%) |
|----------|---------|---------|--------|
| Kesme Gücü | 28.1 W | 789.6 | 18.7% |
| İlerleme Hızı | 18.9 mm/min | 357.2 | 23.6% |
| RPM | 421.3 rev/min | 177,493 | 16.9% |
| AşınmaOranı | 2.3 mm/saat | 5.29 | 37.1% |

---

## 📌 Veri Kalitesi

### Eksik Veriler
- **Toplam**: 0 (% 0.0)
- **Durum**: ✅ Temiz

### Çıkış Değerler (Outliers)
- **Yöntem**: IQR (Interquartile Range)
- **IQR Mesafesi**: 1.5
- **Tespit Edilen**: 0 (% 0.0)
- **Durum**: ✅ Temiz

### Veri Tipi Uyuşmazlıkları
- **Durum**: ✅ Yok

### Formatı Hataları
- **Durum**: ✅ Yok

---

## 🎯 Kullanım Senaryoları

### Senaryo 1: Optimum İşletim
```
Hedef: Minimum aşınma
Parametreler:
- Kesme Gücü: 200 W (Yüksek)
- İlerleme Hızı: 110 mm/min (Yüksek)
- RPM: 3100 rev/min (Yüksek)
Beklenen Aşınma: ~3-4 mm/saat (Düşük)
```

### Senaryo 2: Ağır İşletim
```
Hedef: Kalın malzeme kesimi
Parametreler:
- Kesme Gücü: 100 W (Düşük)
- İlerleme Hızı: 50 mm/min (Düşük)
- RPM: 1900 rev/min (Düşük)
Beklenen Aşınma: ~10-11 mm/saat (Yüksek)
```

### Senaryo 3: Dengeli İşletim
```
Hedef: İyi kesim kalitesi ve aşınma bilgisi
Parametreler:
- Kesme Gücü: 150 W (Normal)
- İlerleme Hızı: 80 mm/min (Normal)
- RPM: 2500 rev/min (Normal)
Beklenen Aşınma: ~6-7 mm/saat (Normal)
```

---

## 🔗 İlgili Belgeler

- `project_context.md` - Genel proje bağlamı
- `api_reference.md` - API uç noktaları
- `analysis_results.md` - Analiz bulguları
- `../docs/01_Veri_Analizi.md` - Detaylı veri analizi
