import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_root():
    """Ana sayfa testi"""
    print("=" * 60)
    print("Test: Ana Sayfa (GET /)")
    print("=" * 60)
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_health():
    """Sağlık kontrolü testi"""
    print("=" * 60)
    print("Test: Sağlık Kontrolü (GET /health)")
    print("=" * 60)
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_predict():
    """Tek tahmin testi"""
    print("=" * 60)
    print("Test: Tek Tahmin (POST /predict)")
    print("=" * 60)
    
    payload = {
        "kesme_gucu": 12.5,
        "ilerleme_hizi": 120.0,
        "rpm": 1200
    }
    
    print(f"Request: {json.dumps(payload, indent=2, ensure_ascii=False)}")
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_batch_predict():
    """Toplu tahmin testi"""
    print("=" * 60)
    print("Test: Toplu Tahmin (POST /predict/batch)")
    print("=" * 60)
    
    payload = {
        "veriler": [
            {"kesme_gucu": 12.5, "ilerleme_hizi": 120.0, "rpm": 1200},
            {"kesme_gucu": 10.0, "ilerleme_hizi": 100.0, "rpm": 1150},
            {"kesme_gucu": 15.0, "ilerleme_hizi": 140.0, "rpm": 1250},
            {"kesme_gucu": 8.0, "ilerleme_hizi": 80.0, "rpm": 1100}
        ]
    }
    
    print(f"Request: {len(payload['veriler'])} örnek")
    response = requests.post(f"{BASE_URL}/predict/batch", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_model_info():
    """Model bilgisi testi"""
    print("=" * 60)
    print("Test: Model Bilgisi (GET /model/info)")
    print("=" * 60)
    response = requests.get(f"{BASE_URL}/model/info")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_edge_cases():
    """Sınır durumları testi"""
    print("=" * 60)
    print("Test: Sınır Durumları")
    print("=" * 60)
    
    # Minimum değerler
    print("\n1. Minimum değerler:")
    payload = {"kesme_gucu": 0.0, "ilerleme_hizi": 4.0, "rpm": 107}
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    print(f"   Input: {payload}")
    print(f"   Output: {response.json()['asinma_orani']}")
    
    # Maksimum değerler
    print("\n2. Maksimum değerler:")
    payload = {"kesme_gucu": 20.0, "ilerleme_hizi": 182.0, "rpm": 1295}
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    print(f"   Input: {payload}")
    print(f"   Output: {response.json()['asinma_orani']}")
    
    # Ortalama değerler
    print("\n3. Ortalama değerler:")
    payload = {"kesme_gucu": 11.24, "ilerleme_hizi": 91.40, "rpm": 1166}
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    print(f"   Input: {payload}")
    print(f"   Output: {response.json()['asinma_orani']}")
    print()

def run_all_tests():
    """Tüm testleri çalıştır"""
    try:
        print("\n🚀 API Test Başlıyor...\n")
        
        test_root()
        test_health()
        test_predict()
        test_batch_predict()
        test_model_info()
        test_edge_cases()
        
        print("=" * 60)
        print("✅ Tüm testler başarıyla tamamlandı!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("❌ HATA: API'ye bağlanılamadı!")
        print("Lütfen Docker konteynerinin çalıştığından emin olun:")
        print("  docker-compose up -d")
        print("veya")
        print("  docker run -d -p 8000:8000 --name wear-api wear-prediction-api")
        
    except Exception as e:
        print(f"❌ HATA: {e}")

if __name__ == "__main__":
    run_all_tests()
