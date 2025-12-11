# Digitheta CNC Testere Aşınma Analizi - Proje Dokümantasyonu

Bu proje, Digitheta CNC Testere'nin testere bıçağı aşınma oranını tahmin eden bir makine öğrenmesi çözümüdür.

## 📁 Dokümantasyon İçeriği

1. **[01_Veri_Analizi.md](01_Veri_Analizi.md)** - Veri seti tanıtımı ve korelasyon analizi
2. **[02_SPC_Analizi.md](02_SPC_Analizi.md)** - İstatistiksel Proses Kontrolü (SPC) analizi
3. **[03_Makine_Ogrenmesi.md](03_Makine_Ogrenmesi.md)** - Model geliştirme ve hiperparametre optimizasyonu
4. **[04_Model_Performansi.md](04_Model_Performansi.md)** - Model performans metrikleri ve değerlendirme
5. **[05_Production_API.md](05_Production_API.md)** - Docker tabanlı production API dokümantasyonu
6. **[06_API_Test_Sonuclari.md](06_API_Test_Sonuclari.md)** - API test senaryoları ve sonuçları

## 🎯 Proje Özeti

### Veri Seti
- **Kayıt Sayısı**: 1,838 örnek
- **Süre**: 30 dakikalık operasyon
- **Frekans**: Dakikada 1 kesim
- **Malzeme**: Alüminyum 40×40mm bloklar

### Özellikler
- **Kesme Gücü** (W): Kesme işlemi sırasında harcanan güç
- **İlerleme Hızı** (mm/min): Testere bıçağının ilerleme hızı
- **RPM**: Testere bıçağının dönüş hızı

### Hedef Değişken
- **AşınmaOranı** (mm/saat): Testere bıçağının aşınma oranı

### Model Performansı
- **Algoritma**: GradientBoostingRegressor (Hyperparameter Tuned)
- **Test MAE**: 1.085 mm/saat
- **Test RMSE**: 1.503 mm/saat
- **Test R²**: 0.564

### Deployment
- **Platform**: Docker + FastAPI
- **API Endpoints**: Health check, single/batch prediction, model info
- **Documentation**: Swagger UI (http://localhost:8000/docs)

## 🚀 Hızlı Başlangıç

### Analiz Notebookları
```bash
cd notebooks_presentation/
jupyter notebook
```

### Production API
```bash
cd production_api/
docker-compose up -d

# Test
curl http://localhost:8000/health
```

## 📊 Proje Yapısı

```
GDG_HATAY/
├── Dataset.xlsx                      # Ham veri
├── correlation_analysis.ipynb        # Ana analiz notebook
├── RAPOR_Digitheta_CNC_Testere_Performans_Analizi.md  # Teknik rapor
├── models/                           # Kaydedilmiş modeller
│   ├── wear_gb_tuned_model.joblib
│   └── wear_gradientboosting_model.joblib
├── notebooks_presentation/           # Sunum için notebook'lar
│   ├── 01_data_overview.ipynb
│   ├── 02_correlation_analysis.ipynb
│   ├── 03_wear_prediction.ipynb
│   └── 04_model_test.ipynb
├── production_api/                   # Docker API
│   ├── app.py
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
└── docs/                            # Bu dokümantasyon
    ├── README.md
    ├── 01_Veri_Analizi.md
    ├── 02_SPC_Analizi.md
    ├── 03_Makine_Ogrenmesi.md
    ├── 04_Model_Performansi.md
    ├── 05_Production_API.md
    └── 06_API_Test_Sonuclari.md
```

## 👥 İletişim

Bu proje GDG Hatay için geliştirilmiştir.

## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.
