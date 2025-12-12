# 🔌 API Referans Dokümantasyonu

Tüm REST API uç noktalarının detaylı açıklaması ve kullanım örnekleri.

---

## 📌 Temel Bilgiler

**Base URL**: `http://localhost:8000`
**Protocol**: HTTP/REST
**Content-Type**: `application/json`
**Authentication**: Şu an yok (Production'da eklenecek)

---

## ✅ Health Check Endpoint

### Uç Nokta
```
GET /health
```

### Açıklama
API'nin çalışıp çalışmadığını kontrol eder. Load balancer'lar ve monitoring sistemleri tarafından kullanılır.

### İstek
```bash
curl -X GET "http://localhost:8000/health"
```

### Başarılı Yanıt (200 OK)
```json
{
  "status": "healthy"
}
```

### Hata Yanıtları
- **503 Service Unavailable**: API çalışmıyor veya model yüklenemedi

---

## 📊 Model Bilgisi Endpoint

### Uç Nokta
```
GET /model/info
```

### Açıklama
Modelin meta verilerini ve performans metriklerini döndürür.

### İstek
```bash
curl -X GET "http://localhost:8000/model/info"
```

### Başarılı Yanıt (200 OK)
```json
{
  "model_name": "Gradient Boosting Regressor",
  "version": "1.0",
  "features": [
    "Kesme Gücü",
    "İlerleme Hızı",
    "RPM"
  ],
  "target": "AşınmaOranı",
  "target_unit": "mm/saat",
  "performance_metrics": {
    "test_mae": 1.087,
    "test_rmse": 1.503,
    "test_r2": 0.564,
    "test_mape": 18.4,
    "cv_mae_mean": 1.092,
    "cv_mae_std": 0.043,
    "cv_r2_mean": 0.561,
    "cv_r2_std": 0.024
  },
  "feature_importance": {
    "İlerleme Hızı": 0.525,
    "Kesme Gücü": 0.253,
    "RPM": 0.222
  },
  "hyperparameters": {
    "n_estimators": 187,
    "learning_rate": 0.0412,
    "max_depth": 4,
    "min_samples_leaf": 3,
    "subsample": 0.804
  },
  "training_data_info": {
    "total_samples": 1838,
    "train_samples": 1286,
    "test_samples": 552,
    "features": 3
  }
}
```

### HTTP Status Kodları
- **200 OK**: Başarılı
- **500 Internal Server Error**: Model yüklenirken hata

---

## 🔮 Tekli Tahmin Endpoint

### Uç Nokta
```
POST /predict
```

### Açıklama
Verilen özellikler için aşınma oranı tahmini yapar.

### İstek Schema

```json
{
  "kesme_gucu": number,        // float, 95-206 W aralığında
  "ilerleme_hizi": number,     // float, 40-120 mm/min aralığında
  "rpm": number                 // float, 1800-3200 aralığında
}
```

### İstek Örneği

**cURL**:
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "kesme_gucu": 150.0,
    "ilerleme_hizi": 80.0,
    "rpm": 2500.0
  }'
```

**Python**:
```python
import requests

payload = {
    "kesme_gucu": 150.0,
    "ilerleme_hizi": 80.0,
    "rpm": 2500.0
}

response = requests.post(
    "http://localhost:8000/predict",
    json=payload
)

print(response.json())
```

**JavaScript**:
```javascript
const payload = {
    kesme_gucu: 150.0,
    ilerleme_hizi: 80.0,
    rpm: 2500.0
};

fetch('http://localhost:8000/predict', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
})
.then(r => r.json())
.then(data => console.log(data));
```

### Başarılı Yanıt (200 OK)

```json
{
  "asinma_orani": 7.304,
  "asinma_orani_unit": "mm/saat",
  "features": {
    "Kesme Gücü": 150.0,
    "İlerleme Hızı": 80.0,
    "RPM": 2500.0
  },
  "model_version": "1.0",
  "timestamp": "2025-12-13T10:30:45.123456"
}
```

### Hata Yanıtları

**422 Unprocessable Entity** - Eksik veya geçersiz alan:
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "kesme_gucu"],
      "msg": "Field required",
      "input": {}
    }
  ]
}
```

**400 Bad Request** - Geçersiz veri tipi:
```json
{
  "detail": "kesme_gucu must be a number, got string"
}
```

**500 Internal Server Error** - Tahmin yapılırken hata:
```json
{
  "detail": "Error during prediction"
}
```

### Parametreler Hakkında Notlar

- **Tüm parametreler zorunludur**
- **Değerler float olmalıdır** (String değil)
- **Önerilen aralıklar dışında değerler hata vermez ama tahmin güvenilir olmayabilir**
- **Response time**: Ortalama < 5ms

---

## 📦 Toplu Tahmin (Batch) Endpoint

### Uç Nokta
```
POST /predict/batch
```

### Açıklama
Birden fazla örnek için tahmini toplu olarak yapar. Tekli tahminden daha hızlı ve verimlidir.

### İstek Schema

```json
{
  "veriler": [
    {
      "kesme_gucu": number,
      "ilerleme_hizi": number,
      "rpm": number
    }
  ]
}
```

**Kısıtlamalar**:
- Minimum array boyutu: 1
- Maximum array boyutu: 1000
- Her örnek 3 özellikten oluşmalı

### İstek Örneği

**cURL**:
```bash
curl -X POST "http://localhost:8000/predict/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "veriler": [
      {"kesme_gucu": 150.0, "ilerleme_hizi": 80.0, "rpm": 2500.0},
      {"kesme_gucu": 120.0, "ilerleme_hizi": 60.0, "rpm": 2200.0},
      {"kesme_gucu": 200.0, "ilerleme_hizi": 100.0, "rpm": 3000.0}
    ]
  }'
```

**Python**:
```python
import requests
import pandas as pd

# DataFrame'den batch tahmin
df = pd.DataFrame({
    'kesme_gucu': [150, 120, 200],
    'ilerleme_hizi': [80, 60, 100],
    'rpm': [2500, 2200, 3000]
})

payload = {
    "veriler": df.to_dict(orient='records')
}

response = requests.post(
    "http://localhost:8000/predict/batch",
    json=payload
)

results = response.json()
print(f"Tahminler: {results['tahminler']}")
print(f"Ortalama: {results['ortalama']:.2f}")
```

**R**:
```r
library(httr)
library(jsonlite)

data <- list(
  veriler = list(
    list(kesme_gucu = 150, ilerleme_hizi = 80, rpm = 2500),
    list(kesme_gucu = 120, ilerleme_hizi = 60, rpm = 2200)
  )
)

response <- POST(
  "http://localhost:8000/predict/batch",
  body = toJSON(data),
  content_type_json()
)

results <- fromJSON(content(response, "text"))
print(results$tahminler)
```

### Başarılı Yanıt (200 OK)

```json
{
  "tahminler": [7.304, 5.621, 9.187],
  "tahminler_unit": "mm/saat",
  "istatistikler": {
    "ortalama": 7.371,
    "min": 5.621,
    "max": 9.187,
    "standart_sapma": 1.623,
    "median": 7.304
  },
  "islem_süresi_ms": 3.45,
  "model_version": "1.0",
  "timestamp": "2025-12-13T10:35:22.654321"
}
```

### Hata Yanıtları

**400 Bad Request** - Boş array:
```json
{
  "detail": "veriler array'i en az 1 örnek içermelidir"
}
```

**400 Bad Request** - Çok büyük array:
```json
{
  "detail": "veriler array'i maksimum 1000 örnek içerebilir"
}
```

**422 Unprocessable Entity** - Eksik alan:
```json
{
  "detail": "Her örnek kesme_gucu, ilerleme_hizi ve rpm içermelidir"
}
```

### Performans Metrikleri

| Örnek Sayısı | Ortalama Süre | Throughput |
|--------------|---------------|-----------|
| 1 | < 5ms | > 200 req/sec |
| 10 | < 25ms | > 400 req/sec |
| 100 | < 150ms | > 650 req/sec |
| 1000 | < 1500ms | > 650 req/sec |

---

## 🌐 Root Endpoint

### Uç Nokta
```
GET /
```

### Açıklama
API'nin ana sayfasını döndürür. Temel bilgiler ve kullanılabilir uç noktaların listesi.

### İstek
```bash
curl -X GET "http://localhost:8000/"
```

### Yanıt (200 OK)
```json
{
  "message": "Aşınma Oranı Tahmin API'sine Hoş Geldiniz",
  "version": "1.0",
  "endpoints": {
    "health": "GET /health",
    "model_info": "GET /model/info",
    "predict": "POST /predict",
    "batch_predict": "POST /predict/batch",
    "docs": "GET /docs",
    "redoc": "GET /redoc"
  },
  "documentation": "http://localhost:8000/docs"
}
```

---

## 📖 Swagger UI

### Uç Nokta
```
GET /docs
```

**Açıklama**: Etkileşimli Swagger API dokümantasyonu
**URL**: http://localhost:8000/docs
**Özellikler**:
- İstek denemesi (Try it out)
- Schema görüntüleme
- Response örneği

---

## 🔄 API Kullanım Örnekleri

### Örnek 1: Tek Tahmin

```bash
#!/bin/bash

# Tek tahmin
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"kesme_gucu": 150, "ilerleme_hizi": 80, "rpm": 2500}'
```

### Örnek 2: Dosyadan Batch Tahmin (Python)

```python
import requests
import pandas as pd

# Excel dosyasından oku
df = pd.read_excel('data.xlsx')

# API için hazırla
payload = {
    "veriler": df[['Kesme Gücü', 'İlerleme Hızı', 'RPM']].rename(columns={
        'Kesme Gücü': 'kesme_gucu',
        'İlerleme Hızı': 'ilerleme_hizi'
    }).to_dict(orient='records')
}

# API'ye gönder
response = requests.post(
    "http://localhost:8000/predict/batch",
    json=payload
)

# Sonuçları aldı
results = response.json()
df['TahminEdilenAşınma'] = results['tahminler']

# Kaydet
df.to_excel('results.xlsx', index=False)
print(f"Tahminler tamamlandı. Ortalama aşınma: {results['istatistikler']['ortalama']:.2f}")
```

### Örnek 3: Streaming Tahmin (Python)

```python
import requests
import time

# Live sensörlerden veri alıp API'ye gönder
sensor_data = [
    {"kesme_gucu": 145, "ilerleme_hizi": 75, "rpm": 2450},
    {"kesme_gucu": 155, "ilerleme_hizi": 85, "rpm": 2550},
    {"kesme_gucu": 150, "ilerleme_hizi": 80, "rpm": 2500},
]

for data in sensor_data:
    response = requests.post("http://localhost:8000/predict", json=data)
    result = response.json()
    
    print(f"Zaman: {time.time()}")
    print(f"Aşınma: {result['asinma_orani']:.2f} mm/saat")
    print("---")
    
    time.sleep(1)
```

---

## ⚠️ Hata Yönetimi

### HTTP Status Kodları

| Kod | Anlamı | Aksiyon |
|-----|--------|--------|
| 200 | OK | Başarılı tahmin |
| 400 | Bad Request | İstek formatı hata (düzelt ve tekrar gönder) |
| 422 | Unprocessable Entity | Eksik/geçersiz alan |
| 500 | Internal Error | Sunucu hatası (destek ekibine bildir) |
| 503 | Service Unavailable | API çalışmıyor (bir süre bekle) |

### Hata Handling (Python)

```python
import requests

try:
    response = requests.post(
        "http://localhost:8000/predict",
        json={"kesme_gucu": 150, "ilerleme_hizi": 80, "rpm": 2500},
        timeout=5
    )
    
    # Status code kontrolü
    if response.status_code == 200:
        print(response.json())
    elif response.status_code == 422:
        print("Veri hatası:", response.json())
    else:
        print(f"Hata {response.status_code}: {response.text}")
        
except requests.ConnectionError:
    print("API'ye bağlanılamıyor. Sunucu çalışıyor mu?")
except requests.Timeout:
    print("İstek zaman aşımına uğradı")
except Exception as e:
    print(f"Beklenmeyen hata: {e}")
```

---

## 🔒 Best Practices

### 1. Timeout Ayarı
```python
response = requests.post(
    url,
    json=payload,
    timeout=10  # 10 saniye timeout
)
```

### 2. Retry Mekanizması
```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(
    total=3,
    connect=3,
    backoff_factor=0.3,
    status_forcelist=[500, 502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)

response = session.post(url, json=payload)
```

### 3. Input Validation
```python
def validate_input(kesme_gucu, ilerleme_hizi, rpm):
    assert 95 <= kesme_gucu <= 206, "Kesme Gücü aralık dışında"
    assert 40 <= ilerleme_hizi <= 120, "İlerleme Hızı aralık dışında"
    assert 1800 <= rpm <= 3200, "RPM aralık dışında"
    return True
```

### 4. Rate Limiting
```python
import time

class RateLimiter:
    def __init__(self, calls_per_second=100):
        self.min_interval = 1.0 / calls_per_second
        self.last_call = 0
    
    def __call__(self):
        elapsed = time.time() - self.last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_call = time.time()

limiter = RateLimiter(calls_per_second=100)
for request in requests:
    limiter()
    # API çağrısı yap
```

---

## 🔗 İlgili Belgeler

- `project_context.md` - Proje bağlamı
- `data_dictionary.md` - Veri sözlüğü
- `analysis_results.md` - Analiz sonuçları
- `../production_api/README.md` - Deployment rehberi
