# 📋 Proje Bağlamı - GDG Hatay CNC Aşınma Tahmin Sistemi

Bu belge, Langflow RAG sistemi için proje hakkında tüm gerekli bağlamı içerir.

---

## 🎯 Proje Özeti

**Proje Adı**: Digitheta CNC Testere Aşınma Analizi ve Tahmin Sistemi
**Etkinlik**: Google Developer Groups Hatay DevFest 2025
**Amaç**: Testere bıçağının aşınma oranını gerçek zamanlı olarak tahmin etmek
**Durum**: Production Ready (Docker + FastAPI)

---

## 📊 Veri Seti Özellikleri

### Temel Bilgiler
- **Toplam Kayıt**: 1,838 örnek
- **Zaman Dönemi**: 30 dakikalık sürekli operasyon
- **Örnekleme Sıklığı**: 1 örnek/dakika
- **Malzeme**: Alüminyum 40×40mm bloklar
- **Makine**: Digitheta CNC Testere

### Değişkenler

| Değişken | Açıklama | Birim | Tür | Min | Max | Ortalama |
|----------|----------|-------|-----|-----|-----|----------|
| **Kesme Gücü** | Kesme işleminde harcanan güç | W | Özellik (float) | 95.2 | 205.8 | 150.3 |
| **İlerleme Hızı** | Testere bıçağının ilerleme hızı | mm/min | Özellik (float) | 40.5 | 119.8 | 80.1 |
| **RPM** | Testere bıçağının dönüş hızı | devir/dak | Özellik (float) | 1800 | 3200 | 2500 |
| **AşınmaOranı** | Testere bıçağı aşınma oranı | **mm/saat** | **Hedef (float)** | **0.5** | **12.8** | **6.2** |

### Veri Kalitesi
- **Eksik Değer**: 0 (Tamamen temiz)
- **Çıkış Değer**: Minimal (IQR yöntemi ile kontrol edildi)
- **Korelasyon Hatası**: Yok
- **Veri Tipi Uyuşmazlığı**: Yok

---

## 🔬 Analiz Sonuçları

### 1. Korelasyon Analizi

**Pearson Korelasyon Katsayıları** (hedef: AşınmaOranı):

| Özellik | Korelasyon | Anlamlılık | Tür |
|---------|------------|-----------|-----|
| İlerleme Hızı | **-0.746** | p < 0.001 | **Güçlü Negatif** ✅ |
| Kesme Gücü | **-0.745** | p < 0.001 | **Güçlü Negatif** ✅ |
| RPM | **-0.745** | p < 0.001 | **Güçlü Negatif** ✅ |

**Fiziksel Yorumlama:**
- Yüksek kesme gücü → Alüminyum daha kolay kesilir → Az aşınma
- Yüksek ilerleme hızı → İşlem hızlı tamamlanır → Az aşınma
- Yüksek RPM → Bıçak hızlı döner → Az aşınma

**Özellikler Arası Korelasyon:**
- Kesme Gücü ↔ RPM: r = 1.000 (mükemmel pozitif)
- Kesme Gücü ↔ İlerleme Hızı: r = 0.998 (neredeyse mükemmel)
- RPM ↔ İlerleme Hızı: r = 0.998 (neredeyse mükemmel)

---

### 2. İstatistiksel Proses Kontrolü (SPC)

**Proses Kararlılığı:**
- **Kontrol İçinde Örnekler**: 1,826 / 1,838 (**99.7%**)
- **Kontrol Dışı Örnekler**: 12 / 1,838 (0.3%)
- **Durum**: ✅ **İstatistiksel Olarak Kontrol Altında**

**ISO 9001 Uygunluk:**
- **Cpk (Process Capability Index)**: 1.32
- **Standart**: Cpk ≥ 1.00 ✅ UYGUN
- **Yorumlama**: Proses yeterli kapasitede

**X-bar Control Chart:**
- **Üst Kontrol Limiti (UCL)**: 8.95 mm/saat
- **Merkez Çizgisi (CL)**: 6.20 mm/saat
- **Alt Kontrol Limiti (LCL)**: 3.45 mm/saat
- **Kontrol Dışı Noktalar**: 12 (Düşük trend)

**Moving Range Chart:**
- **Ortalama MR**: 0.78 mm/saat
- **Üst Limit**: 2.02 mm/saat
- **Periyodik Varyasyon**: Stabil

---

### 3. Machine Learning Model Performansı

#### Model Seçimi
Üç model karşılaştırılmıştır:

| Model | MAE | RMSE | R² | MAPE | Tercih |
|-------|-----|------|-----|------|--------|
| Random Forest | 1.203 | 1.654 | 0.478 | 19.8% | - |
| HistGradientBoosting | 1.095 | 1.519 | 0.540 | 18.1% | - |
| **Gradient Boosting (Tuned)** | **1.087** | **1.503** | **0.564** | **18.4%** | **✅ En İyi** |

#### En İyi Model: Gradient Boosting Regressor (Tuned)

**Hiperparametreler:**
```python
{
    "n_estimators": 187,
    "learning_rate": 0.0412,
    "max_depth": 4,
    "min_samples_leaf": 3,
    "subsample": 0.804,
    "random_state": 42
}
```

**Test Set Performansı:**
- **MAE (Mean Absolute Error)**: 1.087 mm/saat
- **RMSE (Root Mean Squared Error)**: 1.503 mm/saat
- **R² (Determination Coefficient)**: 0.564
- **MAPE (Mean Absolute Percentage Error)**: 18.4%

**Cross-Validation (5-fold):**
- **CV MAE Ortalama**: 1.092 ± 0.043 mm/saat
- **CV R² Ortalama**: 0.561 ± 0.024
- **Stabilite**: İyi (düşük std dev)

**Tahmin Doğruluğu Analizi:**
- **Hata < 0.5 mm/saat**: 28% tahmin
- **Hata < 1.0 mm/saat**: 62% tahmin
- **Hata < 1.5 mm/saat**: 86% tahmin
- **Hata < 2.0 mm/saat**: 94% tahmin

**Özellik Önemi (Feature Importance):**
```
1. İlerleme Hızı:    52.5%
2. Kesme Gücü:       25.3%
3. RPM:              22.2%
```

#### Model Eğitimi Detayları

**Veri Bölümü:**
- **Train Set**: 70% (1,286 örnek)
- **Test Set**: 30% (552 örnek)
- **Rastgele Seed**: 42 (Reproducibility)

**Hiperparameter Tuning:**
- **Yöntem**: RandomizedSearchCV
- **İterasyon Sayısı**: 25
- **Cross-Validation Fold**: 5
- **Scoring Metriği**: Negative MAE

**Tuning Sonuçları:**
- **Best Parameters Bulundu**: Evet ✅
- **Best Cross-Val Score**: -1.092 MAE
- **Fit Süresi**: ~45 saniye
- **Tuning Süresi**: ~15 dakika

---

## 🏗️ Sistem Mimarisi

### Bileşenler

```
┌─────────────────────────────────────────────────────────────┐
│                    GDG Hatay Sunum                          │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
    ┌───▼──────┐      ┌──────▼──────┐      ┌──────▼──────┐
    │ Notebooks │      │ Production  │      │  Langflow   │
    │ Analysis  │      │ REST API    │      │  AI Agent   │
    └───┬──────┘      └──────┬──────┘      └──────┬──────┘
        │                    │                     │
        │              Docker Container      Docker Container
        │                    │                     │
        └────────────────────┼─────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   Models/Data   │
                    │  Shared Volume  │
                    └─────────────────┘
```

### Teknoloji Stack

**Veri Analizi:**
- Python 3.9
- pandas 2.0.3
- numpy 1.24.3
- scikit-learn 1.6.1
- scipy 1.11.4
- matplotlib 3.7.1
- seaborn 0.12.2

**Production API:**
- FastAPI 0.104.1
- Uvicorn 0.24.0
- Pydantic 2.5.0
- Docker & Docker Compose

**AI Agent:**
- Langflow 1.6.5
- Google Generative AI
- Python REPL
- API Request Component

---

## 🔌 API Endpoints

### Health Check
- **Endpoint**: `GET /health`
- **Amaç**: Sistem sağlığını kontrol et
- **Yanıt**: `{"status": "healthy"}`
- **Status Code**: 200

### Model Bilgisi
- **Endpoint**: `GET /model/info`
- **Amaç**: Model detaylarını getir
- **Yanıt**:
```json
{
  "model_name": "Gradient Boosting Regressor",
  "features": ["Kesme Gücü", "İlerleme Hızı", "RPM"],
  "target": "AşınmaOranı",
  "performance": {
    "mae": 1.087,
    "rmse": 1.503,
    "r2": 0.564
  }
}
```

### Tekli Tahmin
- **Endpoint**: `POST /predict`
- **Input**:
```json
{
  "kesme_gucu": 150.0,
  "ilerleme_hizi": 80.0,
  "rpm": 2500.0
}
```
- **Output**:
```json
{
  "asinma_orani": 7.304,
  "features": {
    "Kesme Gücü": 150.0,
    "İlerleme Hızı": 80.0,
    "RPM": 2500.0
  }
}
```
- **Response Time**: < 5ms

### Toplu Tahmin
- **Endpoint**: `POST /predict/batch`
- **Input**:
```json
{
  "veriler": [
    {"kesme_gucu": 150.0, "ilerleme_hizi": 80.0, "rpm": 2500.0},
    {"kesme_gucu": 120.0, "ilerleme_hizi": 60.0, "rpm": 2200.0}
  ]
}
```
- **Output**:
```json
{
  "tahminler": [7.304, 5.621],
  "ortalama": 6.463,
  "min": 5.621,
  "max": 7.304
}
```
- **Max Records**: 1000 (per request)
- **Response Time**: < 100ms (batch 10)

---

## 📁 Dosya Yapısı

```
production_api/
├── app.py                           # FastAPI uygulama
├── Dockerfile                       # Container image
├── docker-compose.yml               # Orchestration
├── requirements.txt                 # Dependencies
├── test_api.py                      # Test scriptleri
├── models/
│   └── wear_gb_tuned_model.joblib  # Production model
└── README.md                        # Deployment guide

notebooks_presentation/
├── 01_data_overview.ipynb          # Veri keşfi
├── 02_correlation_analysis.ipynb   # Korelasyon
├── 03_wear_prediction.ipynb        # Model eğitimi
└── 04_model_test.ipynb             # Test

langflow/
├── GDG Hatay Example.json          # Langflow project
└── README.md                        # Import guide
```

---

## 🚀 Deployment Bilgileri

### Docker Compose
```yaml
services:
  wear-prediction-api:
    port: 8000
    health_check: /health
  
  langflow:
    port: 7860
    database: SQLite
```

### Environment Variables
```bash
MODEL_PATH=models/wear_gb_tuned_model.joblib
LANGFLOW_DATABASE_URL=sqlite:///./langflow.db
```

### Başlatma Komutu
```bash
cd production_api/
docker-compose up -d
```

### Durdurma Komutu
```bash
docker-compose down
```

---

## 📈 Başarı Metrikleri

| Metrik | Hedef | Gerçek | Durum |
|--------|-------|--------|-------|
| Model R² | > 0.50 | 0.564 | ✅ |
| API Response Time | < 10ms | < 5ms | ✅ |
| Data Quality | 100% | 100% | ✅ |
| Process Stability | > 99% | 99.7% | ✅ |
| Deployment Status | Ready | ✅ | ✅ |

---

## 🔑 Önemli Bilgiler

### Veri Özellikleri
- Tüm değerler float tipinde
- Negatif değer bulunmaz
- Eksik veri yok
- Outlier işlemesi yapılmamıştır (doğal varyasyon)

### Model Kısıtlamaları
- Eğitim verisi dışında ekstrapolasyon yapılmamalı
- Kesme Gücü: 95-206 W aralığında
- İlerleme Hızı: 40-120 mm/min aralığında
- RPM: 1800-3200 aralığında

### Tahmin Kullanımı
- Tek tahminler < 1.1 mm/saat standart hata
- Batch tahminler daha stabil
- Ensemble yöntemi ile iyileştirme mümkün

---

## 👥 Proje Detayları

**Geliştirildiği Yer**: GDG Hatay DevFest 2025
**Veri Seti**: Anonimleştirilmiş endüstriyel veri
**Geçerlilik**: Genel makine öğrenmesi eğitimi
**Kullanım Amacı**: Eğitim, sunum, demo

---

## 🔗 İlgili Dosyalar

- `../README.md` - Ana proje dokümantasyonu
- `../production_api/README.md` - API deployment guide
- `../RAPOR_Digitheta_CNC_Testere_Performans_Analizi.md` - Teknik rapor
- `../docs/` - Detaylı analiz dokümantları
