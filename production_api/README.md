# Aşınma Oranı Tahmin API - Docker Production

Bu klasör, eğitilmiş aşınma oranı tahmin modelini REST API olarak Docker konteynerinde çalıştırmak için gerekli dosyaları içerir.

## Dosyalar

- `app.py`: FastAPI ile yazılmış REST API servisi
- `requirements.txt`: Python bağımlılıkları
- `Dockerfile`: Docker image tanımı
- `docker-compose.yml`: Docker Compose konfigürasyonu
- `test_api.py`: API test scriptleri

## API Endpoints

### GET `/`
Ana sayfa ve API bilgisi

### GET `/health`
Sağlık kontrolü

### POST `/predict`
Tek bir örnek için tahmin yapar.

**Request Body:**
```json
{
  "kesme_gucu": 12.5,
  "ilerleme_hizi": 120.0,
  "rpm": 1200
}
```

**Response:**
```json
{
  "asinma_orani": 1.234,
  "features": {
    "Kesme Gücü": 12.5,
    "İlerleme Hızı": 120.0,
    "RPM": 1200
  }
}
```

### POST `/predict/batch`
Birden fazla örnek için toplu tahmin yapar.

**Request Body:**
```json
{
  "veriler": [
    {"kesme_gucu": 12.5, "ilerleme_hizi": 120.0, "rpm": 1200},
    {"kesme_gucu": 10.0, "ilerleme_hizi": 100.0, "rpm": 1150}
  ]
}
```

**Response:**
```json
{
  "tahminler": [1.234, 2.456],
  "ortalama": 1.845,
  "min": 1.234,
  "max": 2.456
}
```

### GET `/model/info`
Model hakkında bilgi döndürür.

## Kurulum ve Çalıştırma

### 1. Modeli Kopyalayın
```bash
# Model dosyasını production_api klasörüne kopyalayın
mkdir -p models
cp ../models/wear_gradientboosting_tuned_model.joblib models/
```

### 2. Docker Image Oluşturun
```bash
docker build -t wear-prediction-api .
```

### 3. Konteyneri Çalıştırın

#### Opsiyon A: Docker run ile
```bash
docker run -d -p 8000:8000 --name wear-api wear-prediction-api
```

#### Opsiyon B: Docker Compose ile (Önerilen)
```bash
docker-compose up -d
```

### 4. API'yi Test Edin

#### Browser üzerinden
```
http://localhost:8000
http://localhost:8000/docs  # Swagger UI
http://localhost:8000/redoc # ReDoc
```

#### cURL ile
```bash
# Ana sayfa
curl http://localhost:8000/

# Sağlık kontrolü
curl http://localhost:8000/health

# Tek tahmin
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"kesme_gucu": 12.5, "ilerleme_hizi": 120.0, "rpm": 1200}'

# Toplu tahmin
curl -X POST http://localhost:8000/predict/batch \
  -H "Content-Type: application/json" \
  -d '{"veriler": [{"kesme_gucu": 12.5, "ilerleme_hizi": 120.0, "rpm": 1200}, {"kesme_gucu": 10.0, "ilerleme_hizi": 100.0, "rpm": 1150}]}'
```

#### Python ile
```python
import requests

# Tek tahmin
response = requests.post(
    "http://localhost:8000/predict",
    json={"kesme_gucu": 12.5, "ilerleme_hizi": 120.0, "rpm": 1200}
)
print(response.json())

# Toplu tahmin
response = requests.post(
    "http://localhost:8000/predict/batch",
    json={
        "veriler": [
            {"kesme_gucu": 12.5, "ilerleme_hizi": 120.0, "rpm": 1200},
            {"kesme_gucu": 10.0, "ilerleme_hizi": 100.0, "rpm": 1150}
        ]
    }
)
print(response.json())
```

## Logları Görüntüleme

```bash
# Docker run ile
docker logs wear-api

# Docker Compose ile
docker-compose logs -f
```

## Konteyneri Durdurma

```bash
# Docker run ile
docker stop wear-api
docker rm wear-api

# Docker Compose ile
docker-compose down
```

## Production Notları

1. **Güvenlik:**
   - API anahtarı veya JWT token ekleyin
   - HTTPS kullanın
   - Rate limiting ekleyin

2. **Monitoring:**
   - Prometheus metrics ekleyin
   - Logging seviyelerini ayarlayın
   - Health check endpoint'i kullanın

3. **Performans:**
   - Gunicorn workers sayısını artırın
   - Model yükleme önbelleği kullanın
   - Load balancer arkasına alın

4. **Model Güncelleme:**
   - Model versiyonlama sistemi ekleyin
   - A/B test için farklı model versiyonları
   - Otomatik model deployment pipeline

## Troubleshooting

**Model yüklenemedi hatası:**
- Model dosyasının doğru yolda olduğunu kontrol edin
- `docker-compose.yml` içindeki volume bağlantısını kontrol edin

**Port 8000 kullanımda:**
- Farklı port kullanın: `-p 8080:8000`
- Çakışan konteyneri durdurun

**Yavaş yanıt süreleri:**
- Gunicorn workers sayısını artırın
- Model prediction cache ekleyin
- Daha güçlü sunucu kullanın
