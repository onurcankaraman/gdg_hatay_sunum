# Sunum Not Defterleri Özeti

Bu klasör, Dataset.xlsx üzerinde yaptığımız analiz ve modelleme adımlarını sunum için üç bölüme ayırır.

## Dosyalar

- `01_data_overview.ipynb`: Veri yükleme, temel keşif (head/info/describe).
- `02_correlation_analysis.ipynb`: Korelasyon matrisi, ısı haritası, en yüksek pozitif/negatif çiftler.
- `03_wear_prediction.ipynb`: Aşınma oranı tahmini; model karşılaştırma (RF, GB, HGB), hata analizi, hiperparametre araması ve model kaydetme.
- `04_model_test.ipynb`: Kaydedilmiş modeli yükleme, test seti değerlendirmesi, yeni verilerle tahmin, batch prediction ve performans özeti.

## Çalıştırma Notları

- Veri yolu sabit: `/Users/onurcan/Documents/GDG_HATAY/Dataset.xlsx`.
- Python ortamında `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `joblib` kurulu olmalı.
- Modeller `models/` klasörüne kaydedilir.

## Kısa Bulgular

- Korelasyon: Kesme Gücü ↔ İlerleme Hızı çok güçlü pozitif; AşınmaOranı bazı değişkenlerle ters yönlü.
- En iyi model (hızlı karşılaştırma): GradientBoosting, MAE ~1.05 civarı.
- Hiperparametre araması ile GB: MAE ~1.09 (test), CV MAE ~1.29; model `models/wear_gb_tuned_model.joblib` olarak kaydedildi.

## Öneriler

- XGBoost/LightGBM deneyerek performans test edin.
- Basit bir API veya batch tahmin betiği ile `joblib` modellerini üretime alın.
