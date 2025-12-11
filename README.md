# 🔧 Digitheta CNC Testere Aşınma Analizi Projesi

**GDG Hatay - Machine Learning Workshop**

Bu proje, Digitheta CNC Testere'nin testere bıçağı aşınma oranını makine öğrenmesi ile tahmin eden kapsamlı bir çözümdür.

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](production_api/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9-3776AB?logo=python)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6.1-F7931E?logo=scikit-learn)](https://scikit-learn.org/)

---

## 📊 Proje Özeti

### 🎯 Problem
Alüminyum blokların kesilmesi sırasında testere bıçağının aşınma oranını **gerçek zamanlı tahmin etmek**.

### 💡 Çözüm
- **Veri Analizi**: Korelasyon ve SPC (Statistical Process Control) analizi
- **Machine Learning**: Gradient Boosting Regressor ile tahmin modeli
- **Production API**: Docker tabanlı FastAPI REST servisi

### 📈 Sonuçlar
- **Model Performansı**: MAE 1.087 mm/saat, R² 0.564
- **API Response Time**: < 5ms (batch prediction)
- **Deployment**: Production-ready Docker container

---

## 🚀 Hızlı Başlangıç

### 1️⃣ Gereksinimler
```bash
- Python 3.9+
- Docker & Docker Compose
- Jupyter Notebook
```

### 2️⃣ Notebook Analizi
```bash
cd notebooks_presentation/
jupyter notebook
```

**Notebook Sırası:**
1. `01_data_overview.ipynb` - Veri keşfi
2. `02_correlation_analysis.ipynb` - Korelasyon analizi
3. `03_wear_prediction.ipynb` - Model eğitimi
4. `04_model_test.ipynb` - Model testi

### 3️⃣ Production API
```bash
cd production_api/
docker-compose up -d

# Test
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"kesme_gucu": 150.0, "ilerleme_hizi": 80.0, "rpm": 2500.0}'
```

**Swagger UI**: http://localhost:8000/docs

---

## 📁 Proje Yapısı

```
GDG_HATAY/
├── 📊 Dataset.xlsx                         # Ham veri (1,838 örnek)
├── 📄 RAPOR_Digitheta_CNC_Testere_Performans_Analizi.md  # Teknik rapor
│
├── 📚 docs/                                # Detaylı dokümantasyon
│   ├── README.md                           # Dokümantasyon indeksi
│   ├── 01_Veri_Analizi.md                 # Korelasyon ve istatistikler
│   ├── 02_SPC_Analizi.md                  # İstatistiksel proses kontrolü
│   ├── 03_Makine_Ogrenmesi.md             # Model geliştirme
│   ├── 04_Model_Performansi.md            # Performans değerlendirme
│   ├── 05_Production_API.md               # API dokümantasyonu
│   └── 06_API_Test_Sonuclari.md          # Test sonuçları
│
├── 📓 notebooks_presentation/              # Jupyter Notebook'lar
│   ├── 01_data_overview.ipynb
│   ├── 02_correlation_analysis.ipynb
│   ├── 03_wear_prediction.ipynb
│   └── 04_model_test.ipynb
│
├── 🤖 models/                              # Eğitilmiş modeller
│   ├── wear_gb_tuned_model.joblib         # Tuned model (Production)
│   └── wear_gradientboosting_model.joblib # Baseline model
│
└── 🐳 production_api/                      # Docker REST API
    ├── app.py                              # FastAPI application
    ├── Dockerfile                          # Container image
    ├── docker-compose.yml                  # Orchestration
    ├── requirements.txt                    # Dependencies
    ├── test_api.py                         # API test script
    └── README.md                           # Deployment guide
```

---

## 📊 Veri Seti

### Genel Bilgiler
- **Kayıt Sayısı**: 1,838 örnek
- **Süre**: 30 dakikalık operasyon
- **Frekans**: Dakikada 1 kesim
- **Malzeme**: Alüminyum 40×40mm bloklar
- **Makine**: Digitheta CNC Testere

### Değişkenler

| Değişken | Açıklama | Birim | Tip |
|----------|----------|-------|-----|
| Kesme Gücü | Kesme işleminde harcanan güç | W | Özellik |
| İlerleme Hızı | Testere bıçağının ilerleme hızı | mm/min | Özellik |
| RPM | Testere bıçağının dönüş hızı | devir/dak | Özellik |
| **AşınmaOranı** | Testere bıçağı aşınma oranı | **mm/saat** | **Hedef** |

---

## 🧪 Analiz Sonuçları

### 1. Korelasyon Analizi
```
İlerleme Hızı ↔ AşınmaOranı:  r = -0.746 (güçlü negatif)
Kesme Gücü ↔ AşınmaOranı:     r = -0.745 (güçlü negatif)
RPM ↔ AşınmaOranı:            r = -0.745 (güçlü negatif)
```

**Fiziksel Yorumlama**: Yüksek kesme gücü/hız → Alüminyum yumuşar → Az aşınma

### 2. SPC (Statistical Process Control)
```
Proses Kararlılığı:  %99.7 kontrol içi ✅
ISO 9001 Uygunluk:   ✅ Standartlara uygun
Process Capability:  Cpk > 1.00 (yeterli)
```

### 3. Machine Learning
```
Model: Gradient Boosting Regressor (Hyperparameter Tuned)

Performans:
├─ Test MAE:   1.087 mm/saat
├─ Test RMSE:  1.503 mm/saat
├─ Test R²:    0.564
└─ Test MAPE:  18.4%

Hiperparametreler:
├─ n_estimators:      187
├─ learning_rate:     0.0412
├─ max_depth:         4
├─ min_samples_leaf:  3
└─ subsample:         0.804
```

### 4. Production API
```
Endpoints:         5 (health, predict, batch, model info, root)
Response Time:     < 5ms (batch)
Deployment:        Docker + FastAPI
Status:            ✅ Production Ready
Test Success:      7/7 (100%)
```

---

## 🔧 Teknoloji Stack

### Analiz & ML
- **Python**: 3.9
- **pandas**: Veri manipülasyonu
- **numpy**: Numerik hesaplamalar
- **scikit-learn**: Machine learning (1.6.1)
- **matplotlib/seaborn**: Görselleştirme
- **scipy**: İstatistiksel testler

### Production
- **FastAPI**: REST API framework (0.104.1)
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **Docker**: Containerization
- **Docker Compose**: Orchestration

---

## 📚 Dokümantasyon

Detaylı dokümantasyon için [`docs/`](docs/) klasörüne bakınız:

1. **[Veri Analizi](docs/01_Veri_Analizi.md)** - Korelasyon ve istatistikler
2. **[SPC Analizi](docs/02_SPC_Analizi.md)** - Proses kontrolü
3. **[Makine Öğrenmesi](docs/03_Makine_Ogrenmesi.md)** - Model geliştirme
4. **[Model Performansı](docs/04_Model_Performansi.md)** - Değerlendirme
5. **[Production API](docs/05_Production_API.md)** - API dokümantasyonu
6. **[API Test Sonuçları](docs/06_API_Test_Sonuclari.md)** - Test raporları

---

## 🎯 Önemli Bulgular

### 💡 Fiziksel İlişkiler
1. **Yüksek Kesme Gücü** → Düşük aşınma (r = -0.745)
2. **Yüksek İlerleme Hızı** → Düşük aşınma (r = -0.746)
3. **Yüksek RPM** → Düşük aşınma (r = -0.745)

### 📊 Model Insights
- İlerleme hızı **en önemli özellik** (importance: 52.5%)
- Kesme gücü ve RPM yüksek korelasyonlu (r = 1.000)
- Model tahminleri **%86 < 1.5 mm/saat hata**

### 🚀 Production Metrikleri
- API response time: **< 5ms** (batch 10 örnek)
- Throughput: **> 200 req/sec** (batch)
- Container memory: **~150 MB**
- Health check: **%100 uptime**

---

## 🧪 API Kullanım Örnekleri

### cURL
```bash
# Sağlık kontrolü
curl http://localhost:8000/health

# Tekli tahmin
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "kesme_gucu": 150.0,
    "ilerleme_hizi": 80.0,
    "rpm": 2500.0
  }'

# Toplu tahmin
curl -X POST http://localhost:8000/predict/batch \
  -H "Content-Type: application/json" \
  -d '{
    "veriler": [
      {"kesme_gucu": 150.0, "ilerleme_hizi": 80.0, "rpm": 2500.0},
      {"kesme_gucu": 200.0, "ilerleme_hizi": 100.0, "rpm": 3000.0}
    ]
  }'
```

### Python
```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={
        "kesme_gucu": 150.0,
        "ilerleme_hizi": 80.0,
        "rpm": 2500.0
    }
)
print(response.json())
# {"asinma_orani": 7.304, "features": {...}}
```

---

## 📈 Sonraki Adımlar

### Kısa Vadeli
- [ ] API key authentication ekle
- [ ] Input range validation
- [ ] Rate limiting implementasyonu
- [ ] Monitoring (Prometheus/Grafana)

### Orta Vadeli
- [ ] Model versioning sistemi
- [ ] A/B testing altyapısı
- [ ] Auto-scaling setup
- [ ] Database logging

### Uzun Vadeli
- [ ] Real-time model retraining
- [ ] Advanced analytics dashboard
- [ ] Multi-model ensemble
- [ ] Cloud deployment (AWS/GCP/Azure)

---

## 👥 Katkıda Bulunanlar

**GDG Hatay** için geliştirilmiştir.

---

## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

---

## 🔗 Faydalı Linkler

- **Teknik Rapor**: [RAPOR_Digitheta_CNC_Testere_Performans_Analizi.md](RAPOR_Digitheta_CNC_Testere_Performans_Analizi.md)
- **API Dokümantasyonu**: [production_api/README.md](production_api/README.md)
- **Swagger UI**: http://localhost:8000/docs (API çalıştırıldığında)
- **Docker Hub**: (opsiyonel - image yüklenirse)

---

## 📧 İletişim

Sorularınız için GDG Hatay ekibi ile iletişime geçebilirsiniz.

---

**⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!**
