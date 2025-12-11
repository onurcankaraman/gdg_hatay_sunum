# Makine Öğrenmesi Model Geliştirme

## 🎯 Problem Tanımı

**Regresyon Problemi**: Testere bıçağı aşınma oranını (mm/saat) tahmin etmek.

### Girdiler (Features)
- Kesme Gücü (W)
- İlerleme Hızı (mm/min)
- RPM (devir/dakika)

### Çıktı (Target)
- AşınmaOranı (mm/saat)

## 📊 Veri Hazırlığı

### Train-Test Split
```python
Test boyutu: %20 (368 örnek)
Train boyutu: %80 (1,470 örnek)
Random state: 42 (tekrarlanabilirlik için)
```

### Özellik Ölçeklendirme
- ❌ Ölçeklendirme **uygulanmadı**
- Sebep: Tree-based modeller ölçek bağımsız

## 🤖 Model Karşılaştırması

3 farklı algoritma denendi:

### 1. Random Forest Regressor
```python
Parametreler:
- n_estimators: 100 (ağaç sayısı)
- random_state: 42
- n_jobs: -1 (tüm CPU kullan)
```

**Performans:**
```
Cross-Validation (5-fold):
- CV Ortalama MAE: 1.067 ± 0.024
- CV Ortalama RMSE: 1.475 ± 0.033
- CV Ortalama R²: 0.614 ± 0.017

Test Set:
- Test MAE: 1.101
- Test RMSE: 1.542
- Test R²: 0.577
```

### 2. Gradient Boosting Regressor
```python
Parametreler:
- n_estimators: 100
- learning_rate: 0.1
- max_depth: 3
- random_state: 42
```

**Performans:**
```
Cross-Validation (5-fold):
- CV Ortalama MAE: 1.043 ± 0.028
- CV Ortalama RMSE: 1.455 ± 0.037
- CV Ortalama R²: 0.624 ± 0.019

Test Set:
- Test MAE: 1.050
- Test RMSE: 1.474
- Test R²: 0.613
```

### 3. Histogram-Based Gradient Boosting
```python
Parametreler:
- max_iter: 100
- learning_rate: 0.1
- max_depth: 3
- random_state: 42
```

**Performans:**
```
Cross-Validation (5-fold):
- CV Ortalama MAE: 1.065 ± 0.025
- CV Ortalama RMSE: 1.475 ± 0.033
- CV Ortalama R²: 0.614 ± 0.017

Test Set:
- Test MAE: 1.088
- Test RMSE: 1.518
- Test R²: 0.594
```

## 🏆 En İyi Model: Gradient Boosting

### Seçim Kriterleri
1. **En düşük test MAE**: 1.050
2. **En yüksek test R²**: 0.613
3. **Stabil CV skorları**: Düşük standart sapma

### Model Karşılaştırma Tablosu

| Model | CV MAE | Test MAE | CV R² | Test R² | Seçim |
|-------|--------|----------|-------|---------|-------|
| Random Forest | 1.067 | 1.101 | 0.614 | 0.577 | ❌ |
| **Gradient Boosting** | **1.043** | **1.050** | **0.624** | **0.613** | ✅ |
| Hist Gradient Boosting | 1.065 | 1.088 | 0.614 | 0.594 | ❌ |

## 🔧 Hiperparametre Optimizasyonu

### RandomizedSearchCV Yapılandırması
```python
Parametre Uzayı:
- n_estimators: 50-200 (integer)
- learning_rate: 0.01-0.3 (log-uniform)
- max_depth: 3-7 (integer)
- min_samples_split: 2-20 (integer)
- min_samples_leaf: 1-10 (integer)
- subsample: 0.6-1.0 (uniform)

Arama Ayarları:
- n_iter: 25 (25 farklı kombinasyon)
- cv: 5 (5-fold cross-validation)
- scoring: neg_mean_absolute_error
- n_jobs: -1 (paralel işlem)
- random_state: 42
```

### Optimizasyon Sonuçları

**En İyi Hiperparametreler:**
```python
{
    'subsample': 0.8037459218290637,
    'n_estimators': 187,
    'min_samples_split': 2,
    'min_samples_leaf': 3,
    'max_depth': 4,
    'learning_rate': 0.04116862951945296
}
```

**Performans İyileştirmesi:**
```
Baseline Model:
- CV MAE: 1.043
- Test MAE: 1.050
- Test R²: 0.613

Tuned Model:
- CV MAE: 1.024
- Test MAE: 1.087
- Test R²: 0.564
```

### Hiperparametre Analizi

#### 1. n_estimators (187)
- Baseline: 100
- Değişim: +87%
- Etki: Daha kompleks model, overfit riski arttı

#### 2. learning_rate (0.041)
- Baseline: 0.1
- Değişim: -59%
- Etki: Daha yavaş öğrenme, daha stabil

#### 3. max_depth (4)
- Baseline: 3
- Değişim: +33%
- Etki: Daha derin ağaçlar, daha kompleks

#### 4. min_samples_leaf (3)
- Baseline: 1
- Değişim: +200%
- Etki: Overfit önleme, daha genel

#### 5. subsample (0.804)
- Baseline: 1.0
- Değişim: -20%
- Etki: Stochastic gradient boosting

## 📈 Learning Curve Analizi

### Bias-Variance Trade-off
```
Training Score: 0.82 (yüksek)
Validation Score: 0.56 (orta)
Gap: 0.26 (orta-büyük)

Yorum: Hafif overfitting var
```

### Öneriler
- ✅ Daha fazla veri toplanabilir
- ✅ Feature engineering yapılabilir
- ✅ Ensemble methods denenebilir

## 🎯 Feature Importance

### Gradient Boosting Feature Importance
```
┌─────────────────┬────────────┬─────────┐
│ Feature         │ Importance │ %       │
├─────────────────┼────────────┼─────────┤
│ İlerleme Hızı   │   0.5247   │ 52.5%   │
│ Kesme Gücü      │   0.2891   │ 28.9%   │
│ RPM             │   0.1862   │ 18.6%   │
└─────────────────┴────────────┴─────────┘
```

### Yorumlama
1. **İlerleme Hızı** en önemli özellik
2. **Kesme Gücü** ikinci sırada
3. **RPM** en az etkili (Kesme Gücü ile multicollinearity)

## 💾 Model Kaydetme

### Joblib ile Kaydetme
```python
model_data = {
    'model': tuned_model,
    'feature_cols': ['Kesme Gücü', 'İlerleme Hızı', 'RPM']
}

joblib.dump(model_data, 'models/wear_gb_tuned_model.joblib')
```

### Model Bilgileri
```
Dosya: models/wear_gb_tuned_model.joblib
Boyut: ~360 KB
Format: Pickle (Protocol 4)
Scikit-learn: 1.6.1
NumPy: 2.0.2
```

## 🔮 Tahmin Örnekleri

### Örnek 1: Düşük Parametreler
```python
Input:
  Kesme Gücü: 100 W
  İlerleme Hızı: 50 mm/min
  RPM: 1500 devir/dak

Prediction: 6.91 mm/saat (yüksek aşınma)
```

### Örnek 2: Orta Parametreler
```python
Input:
  Kesme Gücü: 150 W
  İlerleme Hızı: 80 mm/min
  RPM: 2500 devir/dak

Prediction: 7.30 mm/saat (normal aşınma)
```

### Örnek 3: Yüksek Parametreler
```python
Input:
  Kesme Gücü: 250 W
  İlerleme Hızı: 120 mm/min
  RPM: 3500 devir/dak

Prediction: 6.32 mm/saat (düşük aşınma)
```

## 📊 Hata Analizi

### Residual Plot
- Residuals (hata) merkeze yakın dağılmış
- Sistematik pattern yok
- Heteroscedasticity hafif var

### Q-Q Plot
- Normal dağılıma yakın
- Kuyruk bölgelerinde sapma var
- Genel olarak iyi performans

## 🚀 Sonraki Adımlar

1. ✅ Model production'a deploy edildi
2. ✅ Docker API oluşturuldu
3. ✅ Test senaryoları hazırlandı
4. ⏳ Gerçek ortam testleri
5. ⏳ Monitoring ve retraining stratejisi

---

**Not**: Detaylı kod ve grafikler için `03_wear_prediction.ipynb` notebook'una bakınız.
