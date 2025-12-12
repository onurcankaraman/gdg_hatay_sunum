# 🤖 Langflow Agent - GDG Hatay Example

Bu klasör, **GDG Hatay DevFest 2025** etkinliği için hazırlanmış Langflow chatbot projesini içerir.

## 📋 Proje Hakkında

Bu Langflow projesi, CNC aşınma tahmini API'sini kullanabilen, dosya okuyabilen ve Python kodu çalıştırabilen akıllı bir AI ajanı içerir.

### Özellikler

- **📁 Dosya Okuma**: Excel, CSV, PDF ve diğer formatları okuma
- **🔧 API Entegrasyonu**: CNC aşınma tahmini API'sine istek gönderme
- **🐍 Python Interpreter**: Dinamik Python kodu çalıştırma
- **🤖 AI Agent**: Google Generative AI ile doğal dil anlama
- **💬 Chat Interface**: Kullanıcı dostu sohbet arayüzü

## 📚 RAG Dokümantasyonu

Langflow agent'inin etkili kullanımı için gerekli dokümantasyonlar:

### 1. 📖 **project_context.md** - Proje Bağlamı
- Proje genel özeti
- Sistem mimarisi
- Veri seti bilgileri
- API endpoints özeti
- Teknoloji stack
- Başarı metrikleri

→ **Ne zaman kullan**: Agent'e proje hakkında genel bilgi sorduğunuzda

### 2. 📚 **data_dictionary.md** - Veri Sözlüğü
- Tüm özellik tanımları (Kesme Gücü, İlerleme Hızı, RPM)
- Hedef değişken (AşınmaOranı) detayları
- Değer aralıkları ve istatistikler
- Değişkenler arası ilişkiler
- Veri kalitesi bilgisi

→ **Ne zaman kullan**: Veri hakkında sorular sorduğunuzda, özellik anlamını öğrenmek istediğinizde

### 3. 🔌 **api_reference.md** - API Referansı
- Tüm API endpoints açıklaması
- İstek/yanıt örnekleri
- Error handling
- Code samples (Python, cURL, JavaScript)
- Performance metrikleri
- Best practices

→ **Ne zaman kullan**: API çağrısı yapmak, tahmin almak, API hatasını anlamak istediğinizde

### 4. 📈 **analysis_results.md** - Analiz Sonuçları
- Korelasyon analizi bulguları
- İstatistiksel Proses Kontrolü (SPC) sonuçları
- Machine Learning model performansı
- Production API test sonuçları
- Genel sonuçlar ve öneriler

→ **Ne zaman kullan**: Analiz sonuçları hakkında bilgi istediğinizde, model performansını anlamak istediğinizde

## 🗄️ Qdrant Entegrasyonu (RAG)

- **Bağlantı**: `Host=localhost`, `Port=6333`, `HTTPS=False` (veya Docker network içinden `Host=qdrant`, `Port=6333`).
- **Embedded Dashboard**: Ek imaj gerekmeden Qdrant arayüzü için `http://localhost:6333/dashboard` adresini kullanabilirsiniz.
- **Health & Collections**: `http://localhost:6333/health` ve `http://localhost:6333/collections` ile hızlı kontrol.
- **Collection Oluşturma (REST)**:
  ```bash
  curl -X PUT "http://localhost:6333/collections/documents" \
    -H "Content-Type: application/json" \
    -d '{"vectors": {"size": 384, "distance": "Cosine"}}'
  ```
- **Langflow Qdrant Component**: Sadece Host/Port alanlarını doldurun, URL/Path/Location boş bırakın, HTTPS kutusu işaretli olmasın.

## 🚀 Kurulum ve Kullanım

### 1. Langflow Kurulumu

Docker Compose ile Langflow'u başlatın:

```bash
cd production_api/
docker-compose up -d
```

Langflow arayüzüne erişin: **http://localhost:7860**

### 2. Projeyi İçe Aktarma

1. Langflow arayüzünü açın (http://localhost:7860)
2. Sol üst köşedeki **"New Project"** butonuna tıklayın
3. **"Import"** seçeneğini seçin
4. `GDG Hatay Example.json` dosyasını seçin veya sürükleyip bırakın
5. Proje otomatik olarak yüklenecektir

### 3. API Yapılandırması

Projeyi içe aktardıktan sonra yapılandırma adımları:

#### API Request Bileşeni

API Request bileşeninde aşağıdaki ayarları yapın:

- **Method**: `POST`
- **URL**: `http://host.docker.internal:8000/predict`
- **Headers**: 
  ```json
  {
    "Content-Type": "application/json"
  }
  ```
- **Body**:
  ```json
  {
    "kesme_gucu": 150,
    "ilerleme_hizi": 80,
    "rpm": 2500
  }
  ```
- **Tool Name**: `wear_prediction_api`
- **Tool Description**: "CNC aşınma oranı tahmini yapar. Kesme gücü (W), ilerleme hızı (mm/min) ve RPM değerlerini alır."

#### Agent Bileşeni

Agent bileşeninde Google API key'inizi girin:

1. Agent node'una tıklayın
2. **"API Key"** alanına Google AI Studio'dan aldığınız API key'i girin
   - API Key almak için: https://aistudio.google.com/apikey
3. **System Prompt** özelleştirmesi (opsiyonel):
   ```
   Sen CNC makine operasyonları konusunda uzman bir asistansın. 
   Kullanıcılara aşınma tahmini, veri analizi ve Python hesaplamaları 
   konularında yardımcı oluyorsun.
   ```

### 4. Projeyi Çalıştırma

1. Sağ üst köşedeki **"Playground"** butonuna tıklayın
2. Chat penceresinde sorularınızı sorun:
   - "150W kesme gücü, 80 mm/min ilerleme hızı ve 2500 RPM için aşınma oranını tahmin et"
   - "Dataset.xlsx dosyasını oku ve özetle"
   - "Bu verilerin ortalamasını Python ile hesapla: [12.5, 18.3, 15.7]"

## 🔧 Bileşen Detayları

### File Component (Dosya Okuma)
- **Amaç**: Excel, CSV, PDF gibi dosyaları okur
- **Desteklenen Formatlar**: `.xlsx`, `.csv`, `.pdf`, `.txt`, `.json`
- **Kullanım**: "Dataset.xlsx dosyasını oku" gibi komutlarla

### Prompt Template (Dosya Oku Tool)
- **Amaç**: Dosya okuma işlemini AI agent için tool haline getirir
- **Input**: Dosya yolu
- **Output**: Dosya içeriği

### Python REPL Component
- **Amaç**: Dinamik Python kodu çalıştırır
- **Kullanım**: "Bu sayıların toplamını hesapla: [1, 2, 3, 4, 5]"
- **Güvenlik**: Sandbox ortamında çalışır

### API Request Component
- **Amaç**: CNC aşınma tahmini API'sine istek gönderir
- **Endpoint**: `http://host.docker.internal:8000/predict`
- **Tool Mode**: Aktif (agent tarafından otomatik kullanılır)

### Agent (Ana Bileşen)
- **Model**: Google Generative AI
- **Tools**: 4 tool (File, Prompt, Python, API)
- **Date Tool**: Aktif (güncel tarih bilgisi)

## 📝 Örnek Kullanım Senaryoları

### Senaryo 1: Aşınma Tahmini
```
Kullanıcı: 120W kesme gücü, 60 mm/min ilerleme hızı ve 2200 RPM için aşınma oranını tahmin et
Agent: [API'ye istek gönderir ve sonucu döner]
```

### Senaryo 2: Dosya Analizi
```
Kullanıcı: Dataset.xlsx dosyasını oku ve kaç satır var söyle
Agent: [Dosyayı okur ve analiz eder]
```

### Senaryo 3: Python Hesaplama
```
Kullanıcı: [150, 120, 180] değerlerinin ortalamasını hesapla
Agent: [Python interpreter kullanarak hesaplar] Ortalama: 150
```

### Senaryo 4: Karmaşık Workflow
```
Kullanıcı: Dataset.xlsx'teki tüm örnekler için aşınma tahmini yap ve ortalamasını hesapla
Agent: [Dosyayı okur → Her satır için API çağrısı yapar → Sonuçları toplar → Ortalama hesaplar]
```

## 🐛 Sorun Giderme

### API Bağlantı Hatası
- **Sorun**: "Connection refused" veya "Host not found"
- **Çözüm**: 
  - API'nin çalıştığından emin olun: `docker ps | grep wear-prediction-api`
  - URL'yi kontrol edin: `http://host.docker.internal:8000/predict`
  - Mac/Linux'ta `host.docker.internal` yerine `localhost` veya `127.0.0.1` deneyin

### Google API Key Hatası
- **Sorun**: "Invalid API key"
- **Çözüm**: 
  - API key'i doğru kopyaladığınızdan emin olun
  - Google AI Studio'da key'in aktif olduğunu kontrol edin: https://aistudio.google.com/apikey

### Dosya Okuma Hatası
- **Sorun**: "File not found"
- **Çözüm**: 
  - Dosya yolunu mutlak path olarak verin: `/app/Dataset.xlsx`
  - Langflow container'ına volume mount edildiğinden emin olun

### Python Execution Hatası
- **Sorun**: "Module not found"
- **Çözüm**: 
  - Sadece built-in Python kütüphaneleri kullanın
  - Dış kütüphane gerekiyorsa Langflow container'ına pip install edin

## 📚 Ek Kaynaklar

- **Langflow Dokümantasyonu**: https://docs.langflow.org
- **Google AI Studio**: https://aistudio.google.com
- **CNC API Dokümantasyonu**: `../production_api/README.md`
- **Proje Ana Dokümantasyonu**: `../README.md`

## ⚠️ Önemli Notlar

- Bu proje **eğitim amaçlı** hazırlanmıştır
- Gerçek production ortamında güvenlik önlemleri ekleyin (auth, rate limiting, input validation)
- Google API key'inizi **asla** public repository'ye commit etmeyin
- API limitlerine dikkat edin (özellikle batch işlemlerde)

---

**GDG Hatay DevFest 2025** için hazırlanmıştır 🎉
