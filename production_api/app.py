from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
from typing import List
import os

# FastAPI uygulaması
app = FastAPI(
    title="Aşınma Oranı Tahmin API",
    description="Digitheta CNC Testere için aşınma oranı tahmin servisi",
    version="1.0.0"
)

# Model yükleme
MODEL_PATH = os.getenv("MODEL_PATH", "models/wear_gb_tuned_model.joblib")

try:
    model_data = joblib.load(MODEL_PATH)
    model = model_data['model']
    feature_cols = model_data['feature_cols']
    print(f"✅ Model başarıyla yüklendi: {MODEL_PATH}")
except Exception as e:
    print(f"❌ Model yüklenemedi: {e}")
    model = None
    feature_cols = []

# Veri modelleri
class PredictionInput(BaseModel):
    kesme_gucu: float
    ilerleme_hizi: float
    rpm: float

    class Config:
        json_schema_extra = {
            "example": {
                "kesme_gucu": 12.5,
                "ilerleme_hizi": 120.0,
                "rpm": 1200
            }
        }

class PredictionOutput(BaseModel):
    asinma_orani: float
    features: dict

class BatchPredictionInput(BaseModel):
    veriler: List[PredictionInput]

class BatchPredictionOutput(BaseModel):
    tahminler: List[float]
    ortalama: float
    min: float
    max: float

# API Endpoints
@app.get("/")
def root():
    """API ana sayfa"""
    return {
        "mesaj": "Aşınma Oranı Tahmin API",
        "versiyon": "1.0.0",
        "durum": "aktif" if model else "model yüklenemedi",
        "ozellikler": feature_cols
    }

@app.get("/health")
def health_check():
    """Sağlık kontrolü"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model yüklü değil")
    return {"durum": "saglikli", "model": "yuklendi"}

@app.post("/predict", response_model=PredictionOutput)
def predict(input_data: PredictionInput):
    """
    Tek bir örnek için aşınma oranı tahmini yapar.
    
    **Parametreler:**
    - kesme_gucu: Kesme gücü (kW)
    - ilerleme_hizi: İlerleme hızı (mm/min)
    - rpm: Devir/dakika
    
    **Döndürür:**
    - asinma_orani: Tahmin edilen aşınma oranı
    - features: Girdi özellikleri
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model yüklü değil")
    
    try:
        # Veriyi hazırla
        features = np.array([[
            input_data.kesme_gucu,
            input_data.ilerleme_hizi,
            input_data.rpm
        ]])
        
        # Tahmin yap
        prediction = float(model.predict(features)[0])
        
        return PredictionOutput(
            asinma_orani=round(prediction, 3),
            features={
                "Kesme Gücü": input_data.kesme_gucu,
                "İlerleme Hızı": input_data.ilerleme_hizi,
                "RPM": input_data.rpm
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tahmin hatası: {str(e)}")

@app.post("/predict/batch", response_model=BatchPredictionOutput)
def predict_batch(input_data: BatchPredictionInput):
    """
    Birden fazla örnek için toplu tahmin yapar.
    
    **Parametreler:**
    - veriler: PredictionInput listesi
    
    **Döndürür:**
    - tahminler: Her örnek için tahmin listesi
    - ortalama: Ortalama tahmin
    - min: Minimum tahmin
    - max: Maksimum tahmin
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model yüklü değil")
    
    try:
        # Tüm verileri matris olarak hazırla
        features_list = [
            [item.kesme_gucu, item.ilerleme_hizi, item.rpm]
            for item in input_data.veriler
        ]
        features = np.array(features_list)
        
        # Toplu tahmin
        predictions = model.predict(features).tolist()
        
        return BatchPredictionOutput(
            tahminler=[round(p, 3) for p in predictions],
            ortalama=round(float(np.mean(predictions)), 3),
            min=round(float(np.min(predictions)), 3),
            max=round(float(np.max(predictions)), 3)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Toplu tahmin hatası: {str(e)}")

@app.get("/model/info")
def model_info():
    """Model bilgilerini döndürür"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model yüklü değil")
    
    return {
        "model_tipi": type(model).__name__,
        "ozellikler": feature_cols,
        "ozellik_sayisi": len(feature_cols),
        "model_path": MODEL_PATH
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
