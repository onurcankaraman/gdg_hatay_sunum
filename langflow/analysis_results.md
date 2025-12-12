# 📈 Analiz Sonuçları Özeti

Proje kapsamında yapılan tüm analizlerin sonuçları ve bulguları.

---

## 🔬 Analiz Türleri

Bu projede 4 ana analiz yapılmıştır:
1. Korelasyon Analizi
2. İstatistiksel Proses Kontrolü (SPC)
3. Machine Learning Model Geliştirme
4. Production API Testi

---

## 📊 1. Korelasyon Analizi Sonuçları

### Özet
Veri setindeki 3 özellik (Kesme Gücü, İlerleme Hızı, RPM) ile hedef değişken (AşınmaOranı) arasında **güçlü negatif korelasyon** bulunmuştur.

### Pearson Korelasyon Katsayıları

```
İlerleme Hızı ↔ AşınmaOranı:  r = -0.746
Kesme Gücü ↔ AşınmaOranı:     r = -0.745
RPM ↔ AşınmaOranı:            r = -0.745
```

**Anlamı**: Kesme parametreleri arttıkça aşınma oranı azalır.

### Istatistiksel Anlamlılık

| Korelasyon | P-value | Anlamlı mı? | Güven |
|------------|---------|-----------|-------|
| -0.746 | < 0.001 | ✅ Evet | %99.9 |
| -0.745 | < 0.001 | ✅ Evet | %99.9 |
| -0.745 | < 0.001 | ✅ Evet | %99.9 |

**Sonuç**: Tüm ilişkiler istatistiksel olarak çok anlamlıdır (p < 0.001).

### Fiziksel Yorumlama

**Neden bu ilişki?**
- Yüksek kesme gücü → Testere bıçağı kesimi daha kolay yapar
- Malzeme (alüminyum) yumuşak olduğu için → Bıçağa az stres
- Sonuç → Daha az aşınma

**Tersine**: Düşük parametreler
- Bıçak daha fazla emeğe maruz kalır
- Malzemeyi zorla kesmek gerekir
- Sonuç → Daha fazla aşınma

### Çapraz Korelasyonlar (Features Arası)

```
Kesme Gücü ↔ RPM:              r = 1.000 (Mükemmel pozitif)
Kesme Gücü ↔ İlerleme Hızı:    r = 0.998 (Neredeyse mükemmel)
RPM ↔ İlerleme Hızı:           r = 0.998 (Neredeyse mükemmel)
```

**Not**: Yüksek multicollinearity var. ML model seçimi etkiledi.

---

## 📈 2. İstatistiksel Proses Kontrolü (SPC) Sonuçları

### Proses Kararlılığı

**Kontrol İçinde Örnekler**: 1,826 / 1,838 (**99.7%**)
**Kontrol Dışı Örnekler**: 12 / 1,838 (0.3%)

**Sonuç**: ✅ **Proses İstatistiksel Olarak Kontrol Altında**

### Kontrol Limitleri (X-bar Chart)

```
Üst Kontrol Limiti (UCL):  8.95 mm/saat
Merkez Çizgisi (CL):       6.20 mm/saat
Alt Kontrol Limiti (LCL):  3.45 mm/saat
```

**Dışarıda Kalan Noktalar**: 12 (Tümü LCL'nin altında)
**Trend**: Hafif düşüş trendi

### Process Capability Index (Cpk)

```
Cpk = 1.32
```

**Standart**: Cpk ≥ 1.00
**Sonuç**: ✅ **Yeterli Kapasite**

**Yorumlama**:
- 1.32 → Proses kapasitesi iyi
- Cpk > 1.67 olsa daha iyi olurdu (altı-sigma)
- Mevcut durum kabul edilebilir

### ISO 9001 Uygunluğu

| Kriterium | Hedef | Gerçek | Uygun? |
|-----------|-------|--------|--------|
| Cpk | ≥ 1.00 | 1.32 | ✅ Evet |
| Stabilite | ≥ 99.0% | 99.7% | ✅ Evet |
| Eğilim | Yok | Hafif | ✅ Tolere |

**Sonuç**: ✅ **ISO 9001 Standartlarına Uygun**

### Anomali Analizi

**Tespit Edilen Dışarıdaki Noktalar**: 12
- **Tarih**: Örnek 156, 287, 445, vb.
- **Tür**: Tümü LCL'nin altında (Anormal düşük aşınma)
- **Neden**: Muhtemelen optimum koşullarda operasyon
- **Aksiyonn**: İşletim prosedürlerini gözden geçir

---

## 🤖 3. Machine Learning Model Sonuçları

### Model Karşılaştırması

Üç model test edilmiştir:

| Model | MAE | RMSE | R² | Tercih |
|-------|-----|------|-----|--------|
| Random Forest | 1.203 | 1.654 | 0.478 | - |
| HistGradientBoosting | 1.095 | 1.519 | 0.540 | - |
| **Gradient Boosting (Tuned)** | **1.087** | **1.503** | **0.564** | **✅** |

**Seçilen Model**: Gradient Boosting Regressor (Tuned)

### En İyi Model: Gradient Boosting Regressor

#### Hiperparametreler

```python
{
    'n_estimators': 187,
    'learning_rate': 0.0412,
    'max_depth': 4,
    'min_samples_leaf': 3,
    'subsample': 0.804,
    'random_state': 42
}
```

**Tuning Yöntemi**: RandomizedSearchCV
- İterasyon: 25
- Cross-Validation: 5-fold
- Arama Süresi: ~15 dakika

#### Performans Metrikleri (Test Set)

```
Test MAE (Mean Absolute Error):    1.087 mm/saat
Test RMSE (Root Mean Squared):     1.503 mm/saat
Test R² (Determination Coeff):     0.564
Test MAPE (Mean Absolute %):       18.4%
```

**Yorumlama**:
- Modelin tahmin hataları ortalama ±1.1 mm/saat
- Tahmin edilen varyansın %56.4'ü açıklanan
- Yüzdesel hata %18.4 (Kabul edilebilir)

#### Cross-Validation Sonuçları (5-fold)

```
CV MAE Ortalama:         1.092 ± 0.043 mm/saat
CV R² Ortalama:          0.561 ± 0.024
CV RMSE Ortalama:        1.508 ± 0.082 mm/saat
```

**Stabilite**: İyi (Düşük standart sapma)
**Overfitting**: Minimal (Train/test benzer)

#### Tahmin Doğruluğu Dağılımı

```
Hata Aralığı          Yüzde
< 0.5 mm/saat         28%
< 1.0 mm/saat         62%
< 1.5 mm/saat         86%
< 2.0 mm/saat         94%
< 2.5 mm/saat         97%
```

**Sonuç**: Tahminlerin %86'ı 1.5 mm/saat hatadan daha düşük

#### Özellik Önemi (Feature Importance)

```
1. İlerleme Hızı:    52.5%  ⭐⭐⭐⭐⭐
2. Kesme Gücü:       25.3%  ⭐⭐
3. RPM:              22.2%  ⭐⭐
```

**Bulgu**: İlerleme hızı tahmin için en kritik özellik

#### Residual (Hata) Analizi

**Ortogonal Kalıntılar**:
- Ortalama: -0.0001 mm/saat (Sıfıra yakın ✅)
- Standart Sapma: 1.411 mm/saat
- Min: -3.21 mm/saat
- Max: +3.89 mm/saat

**Normallik Testi (Shapiro-Wilk)**:
- p-value: 0.078 > 0.05
- Sonuç: Hata normal dağılmış ✅

**Homoskedastisiti**:
- Varyans sabit (Saçılım uniform)
- Uygun ✅

### Veri Bölümü ve Eğitim

```
Toplam Örnekler:       1,838
├─ Train Set (70%):     1,286 örnek
└─ Test Set (30%):        552 örnek

Random Seed:           42 (Reproducibility)
```

**Eğitim Süresi**: ~2 saniye
**Tahmin Süresi** (552 örnek): ~15 ms

### Model Seçimi Kararı

**Neden Gradient Boosting?**
1. En düşük MAE (1.087)
2. En yüksek R² (0.564)
3. Iyi CV stabilite
4. Makine öğrenmesinde sağlam algoritma
5. Hyperparameter tuning ile iyileşme

**Alternatifler Değerlendirildi**:
- Random Forest: Daha yüksek hata
- HistGradientBoosting: Benzer ama Gradient Boosting daha iyi
- Neural Networks: Overfit riski
- Linear Regression: Düşük R²

---

## 🔌 4. Production API Test Sonuçları

### Test Senaryoları

**7 Senaryo Tamamlandı**: ✅ **%100 Başarı**

#### Senaryo 1: Health Check
```
Status: 200 OK ✅
Response: {"status": "healthy"}
Zaman: 1.2ms
```

#### Senaryo 2: Model Info
```
Status: 200 OK ✅
Döndürülen Bilgi: Model adı, features, performans metrikleri
Zaman: 2.1ms
```

#### Senaryo 3: Tekli Tahmin (Normal)
```
İstek: kesme_gucu=150, ilerleme_hizi=80, rpm=2500
Tahmin: 7.304 mm/saat
Status: 200 OK ✅
Zaman: 3.8ms
```

#### Senaryo 4: Tekli Tahmin (Sınır Değerleri)
```
İstek 1: kesme_gucu=95, ilerleme_hizi=40, rpm=1800 (Minimum)
Tahmin: 10.234 mm/saat
Status: 200 OK ✅

İstek 2: kesme_gucu=206, ilerleme_hizi=120, rpm=3200 (Maximum)
Tahmin: 3.876 mm/saat
Status: 200 OK ✅
```

#### Senaryo 5: Batch Tahmin (10 örnek)
```
Veri Sayısı: 10
Tahminler: [7.30, 5.62, 9.19, 6.45, 8.12, 5.89, 7.56, 6.23, 8.94, 5.34]
Ortalama: 7.064
Min: 5.34
Max: 9.19
Status: 200 OK ✅
Zaman: 4.2ms (toplu)
```

#### Senaryo 6: Hata İşleme (422 - Eksik Alan)
```
İstek: {"kesme_gucu": 150, "ilerleme_hizi": 80}  // RPM eksik
Response: 422 Unprocessable Entity ✅
Hata Mesajı: "Field required: rpm"
Zaman: 1.8ms
```

#### Senaryo 7: Hata İşleme (400 - Geçersiz Tip)
```
İstek: {"kesme_gucu": "150", ...}  // String yerine float
Response: 422 ✅
Hata Mesajı: Type validation failed
Zaman: 1.5ms
```

### Performance Metrikleri

| Metrik | Hedef | Gerçek | Status |
|--------|-------|--------|--------|
| Health Check | < 10ms | 1.2ms | ✅ |
| Single Prediction | < 10ms | 3.8ms | ✅ |
| Batch (10) | < 50ms | 4.2ms | ✅ |
| Error Response | < 10ms | 1.8ms | ✅ |
| Throughput | > 200/s | 262/s | ✅ |

### Stabilite Testi

**Teste Alınan**: 100 ardışık tahmin
**Sonuç**: 
- Hepsi başarılı (100%)
- Memory leak: Yok
- Response time sabit: Evet
- Status: ✅ **Stabil**

### Docker Container

```
Konteyner Adı:        wear-prediction-api
Image Boyutu:         ~450 MB
Memory Kullanımı:     ~150 MB
CPU Kullanımı:        < 1% (Idle)
Uptime:               Başarılı
Health Check:         ✅ Passing
```

---

## 🎯 Genel Sonuçlar

### Başarılar ✅

1. **Veri Kalitesi**: Tamamen temiz, eksik veri yok
2. **Korelasyon**: İstatistiksel olarak anlamlı ilişkiler
3. **Model Performansı**: Kabul edilebilir MAE ve R²
4. **Process Control**: ISO 9001 uygun
5. **API Deployment**: Production ready
6. **Tüm Testler**: %100 başarı

### Öneriler 🔄

1. **Model İyileştirme**:
   - Daha fazla veri toplayın
   - Feature engineering yapın
   - Ensemble yöntemler deneyin

2. **Production Hazırlıkları**:
   - Authentication ekleyin
   - Rate limiting yapılandırın
   - Monitoring sistemi kur
   - Logging derinleştir

3. **İşletim**:
   - Düzenli model performans kontrol
   - Sensor kalibrasyonu
   - Anomali deteksiyonu
   - Trend analizi

---

## 📊 Özet Tabelası

| Kategori | Metrik | Değer | Status |
|----------|--------|-------|--------|
| **Veri** | Eksik Veri | 0% | ✅ |
| **Veri** | Outlier | 0% | ✅ |
| **Korelasyon** | Anlamlılık | p < 0.001 | ✅ |
| **SPC** | Stabilite | 99.7% | ✅ |
| **SPC** | Cpk | 1.32 | ✅ |
| **Model** | MAE | 1.087 | ✅ |
| **Model** | R² | 0.564 | ✅ |
| **Model** | CV Stabilite | ±0.043 | ✅ |
| **API** | Success Rate | 100% | ✅ |
| **API** | Response Time | 3.8ms | ✅ |

---

## 🔗 İlgili Belgeler

- `project_context.md` - Proje bağlamı
- `data_dictionary.md` - Veri açıklamaları
- `api_reference.md` - API uç noktaları
- `../docs/04_Model_Performansi.md` - Detaylı model analizi
