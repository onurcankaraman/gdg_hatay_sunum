# Production API Dokümantasyonu

## 🚀 Genel Bakış

FastAPI tabanlı, Docker ile containerize edilmiş REST API servisi.

### Teknoloji Stack
- **Framework**: FastAPI 0.104.1
- **ASGI Server**: Uvicorn 0.24.0
- **Validation**: Pydantic 2.5.0
- **ML**: scikit-learn 1.6.1
- **Container**: Docker + Docker Compose
- **Python**: 3.9

## 📁 Proje Yapısı

```
production_api/
├── app.py                              # FastAPI uygulama kodu
├── Dockerfile                          # Docker image tanımı
├── docker-compose.yml                  # Orchestration config
├── requirements.txt                    # Python bağımlılıkları
├── test_api.py                         # Test script
├── train_model_in_container.py         # Model eğitim script
├── models/
│   └── wear_gb_tuned_model.joblib     # Eğitilmiş model
└── README.md                           # Deployment guide
```

## 🔧 Kurulum

### 1. Gereksinimler
```bash
- Docker Desktop (macOS/Windows) veya Docker Engine (Linux)
- Port 8000 kullanılabilir olmalı
```

### 2. Build ve Başlatma
```bash
cd production_api/
docker-compose up --build -d
```

### 3. Sağlık Kontrolü
```bash
curl http://localhost:8000/health
```

## 📡 API Endpoints

### 1. Root Endpoint
```http
GET /
```

**Response:**
```json
{
  "mesaj": "Aşınma Oranı Tahmin API",
  "versiyon": "1.0.0",
  "durum": "aktif",
  "ozellikler": ["Kesme Gücü", "İlerleme Hızı", "RPM"]
}
```

### 2. Health Check
```http
GET /health
```

**Response (Success):**
```json
{
  "durum": "saglikli",
  "model": "yuklendi"
}
```

**Response (Error):**
```json
{
  "detail": "Model yüklü değil"
}
```

**Status Codes:**
- `200`: Model yüklü ve çalışıyor
- `503`: Model yüklenmedi

### 3. Model Info
```http
GET /model/info
```

**Response:**
```json
{
  "model_tipi": "GradientBoostingRegressor",
  "ozellikler": ["Kesme Gücü", "İlerleme Hızı", "RPM"],
  "ozellik_sayisi": 3,
  "model_path": "models/wear_gb_tuned_model.joblib"
}
```

### 4. Single Prediction
```http
POST /predict
Content-Type: application/json
```

**Request Body:**
```json
{
  "kesme_gucu": 150.0,
  "ilerleme_hizi": 80.0,
  "rpm": 2500.0
}
```

**Response:**
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

**Validation Errors:**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "rpm"],
      "msg": "Field required"
    }
  ]
}
```

### 5. Batch Prediction
```http
POST /predict/batch
Content-Type: application/json
```

**Request Body:**
```json
{
  "veriler": [
    {"kesme_gucu": 150.0, "ilerleme_hizi": 80.0, "rpm": 2500.0},
    {"kesme_gucu": 200.0, "ilerleme_hizi": 100.0, "rpm": 3000.0}
  ]
}
```

**Response:**
```json
{
  "tahminler": [7.304, 7.124],
  "ortalama": 7.214,
  "min": 7.124,
  "max": 7.304
}
```

## 🧪 Kullanım Örnekleri

### cURL ile Test

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Single Prediction
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "kesme_gucu": 150.0,
    "ilerleme_hizi": 80.0,
    "rpm": 2500.0
  }'
```

#### Batch Prediction
```bash
curl -X POST http://localhost:8000/predict/batch \
  -H "Content-Type: application/json" \
  -d '{
    "veriler": [
      {"kesme_gucu": 150.0, "ilerleme_hizi": 80.0, "rpm": 2500.0},
      {"kesme_gucu": 200.0, "ilerleme_hizi": 100.0, "rpm": 3000.0}
    ]
  }'
```

### Python ile Test

```python
import requests

# API URL
BASE_URL = "http://localhost:8000"

# Health check
response = requests.get(f"{BASE_URL}/health")
print(response.json())

# Single prediction
data = {
    "kesme_gucu": 150.0,
    "ilerleme_hizi": 80.0,
    "rpm": 2500.0
}
response = requests.post(f"{BASE_URL}/predict", json=data)
print(response.json())

# Batch prediction
batch_data = {
    "veriler": [
        {"kesme_gucu": 150.0, "ilerleme_hizi": 80.0, "rpm": 2500.0},
        {"kesme_gucu": 200.0, "ilerleme_hizi": 100.0, "rpm": 3000.0}
    ]
}
response = requests.post(f"{BASE_URL}/predict/batch", json=batch_data)
print(response.json())
```

### JavaScript (Node.js) ile Test

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000';

// Single prediction
async function predict() {
  const data = {
    kesme_gucu: 150.0,
    ilerleme_hizi: 80.0,
    rpm: 2500.0
  };
  
  const response = await axios.post(`${BASE_URL}/predict`, data);
  console.log(response.data);
}

predict();
```

## 📊 Pydantic Models

### PredictionInput
```python
class PredictionInput(BaseModel):
    kesme_gucu: float       # Kesme gücü (W)
    ilerleme_hizi: float    # İlerleme hızı (mm/min)
    rpm: float              # RPM (devir/dakika)
```

### PredictionOutput
```python
class PredictionOutput(BaseModel):
    asinma_orani: float     # Tahmin edilen aşınma oranı
    features: dict          # Kullanılan özellikler
```

### BatchPredictionInput
```python
class BatchPredictionInput(BaseModel):
    veriler: List[PredictionInput]  # Tahmin listesi
```

### BatchPredictionOutput
```python
class BatchPredictionOutput(BaseModel):
    tahminler: List[float]  # Tahmin sonuçları
    ortalama: float         # Ortalama aşınma
    min: float              # Minimum aşınma
    max: float              # Maksimum aşınma
```

## 🐳 Docker Yapılandırması

### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Sistem bağımlılıkları
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıkları
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodu
COPY app.py .

# Model
RUN mkdir -p models
COPY models/wear_gb_tuned_model.joblib models/

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  wear-prediction-api:
    build: .
    container_name: wear-prediction-api
    ports:
      - "8000:8000"
    environment:
      - MODEL_PATH=models/wear_gb_tuned_model.joblib
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## 📝 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| MODEL_PATH | models/wear_gb_tuned_model.joblib | Model dosya yolu |

## 🔒 Güvenlik

### Öneriler (Production)
1. **API Key Authentication** ekleyin
2. **HTTPS/TLS** kullanın
3. **Rate Limiting** ekleyin
4. **CORS** yapılandırın
5. **Input Sanitization** yapın

### Örnek CORS Yapılandırması
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

## 📈 Performans

### Tahmin Süreleri
```
Single Prediction:  < 1 ms
Batch (10 samples): < 5 ms
Batch (100 samples): < 50 ms
```

### Resource Kullanımı
```
CPU: ~5% (idle)
Memory: ~150 MB
Disk: ~500 MB (image)
```

## 🔧 Troubleshooting

### Problem 1: Port Already in Use
```bash
# Port'u kullanan process'i bul
lsof -i :8000

# Container'ı farklı port'ta çalıştır
docker run -p 8001:8000 wear-prediction-api
```

### Problem 2: Model Yüklenmedi
```bash
# Container loglarını kontrol et
docker logs wear-prediction-api

# Model dosyasını kontrol et
docker exec wear-prediction-api ls -la models/
```

### Problem 3: Container Başlamıyor
```bash
# Build loglarını kontrol et
docker-compose up --build

# Temiz build
docker-compose down
docker rmi production_api-wear-prediction-api
docker-compose up --build
```

## 📚 API Dokümantasyonu

### Swagger UI
```
http://localhost:8000/docs
```
- İnteraktif API testi
- Otomatik şema dokümantasyonu
- Request/response örnekleri

### ReDoc
```
http://localhost:8000/redoc
```
- Okunabilir dokümantasyon
- Markdown desteği
- Daha detaylı açıklamalar

### OpenAPI JSON
```
http://localhost:8000/openapi.json
```
- Programatik erişim
- Client generation için

## 🚀 Deployment

### Production Checklist
- [ ] Environment variables ayarlandı
- [ ] HTTPS/TLS yapılandırıldı
- [ ] Authentication eklendi
- [ ] Monitoring kuruldu
- [ ] Logging yapılandırıldı
- [ ] Backup stratejisi oluşturuldu
- [ ] Load testing yapıldı
- [ ] Rate limiting eklendi

### Cloud Deployment

#### AWS (ECS)
```bash
# ECR'a push
docker tag wear-prediction-api:latest \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com/wear-api:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/wear-api:latest

# ECS task definition
# Fargate veya EC2 launch type
```

#### GCP (Cloud Run)
```bash
# Container Registry'ye push
docker tag wear-prediction-api:latest \
  gcr.io/<project-id>/wear-api:latest
docker push gcr.io/<project-id>/wear-api:latest

# Cloud Run deploy
gcloud run deploy wear-api \
  --image gcr.io/<project-id>/wear-api:latest \
  --platform managed \
  --port 8000
```

#### Azure (Container Instances)
```bash
# Container Registry'ye push
docker tag wear-prediction-api:latest \
  <registry-name>.azurecr.io/wear-api:latest
docker push <registry-name>.azurecr.io/wear-api:latest

# ACI deploy
az container create \
  --resource-group <rg-name> \
  --name wear-api \
  --image <registry-name>.azurecr.io/wear-api:latest \
  --cpu 1 --memory 1 \
  --port 8000
```

## 📊 Monitoring

### Önerilen Metrikler
- Request count (toplam istek)
- Response time (yanıt süresi)
- Error rate (hata oranı)
- Prediction distribution (tahmin dağılımı)
- Model drift (model kayması)

### Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 🔄 Model Güncelleme

### 1. Yeni Model Eğit
```bash
python train_model_in_container.py
```

### 2. Container'ı Güncelle
```bash
docker-compose down
docker-compose up --build -d
```

### 3. Rolling Update (Production)
```bash
# Blue-Green deployment
# Canary deployment
# A/B testing
```

---

**Not**: Detaylı deployment guide için `production_api/README.md` dosyasına bakınız.
