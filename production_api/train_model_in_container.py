#!/usr/bin/env python
"""
Container içinde modeli yeniden eğit
"""
import pandas as pd
import pickle
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# Veriyi yükle
print("📊 Veri yükleniyor...")
df = pd.read_excel('/tmp/Dataset.xlsx')
feature_cols = ['Kesme Gücü', 'İlerleme Hızı', 'RPM']
X = df[feature_cols]
y = df['AşınmaOranı']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# En iyi parametrelerle modeli oluştur
print("🤖 Model eğitiliyor...")
model = GradientBoostingRegressor(
    learning_rate=0.04116862951945296,
    max_depth=4,
    min_samples_leaf=3,
    min_samples_split=2,
    n_estimators=187,
    subsample=0.8037459218290637,
    random_state=42
)

# Modeli eğit
model.fit(X_train, y_train)

# Test skoru
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'✅ Model eğitildi!')
print(f'   Test MAE: {mae:.3f}')
print(f'   Test R²: {r2:.3f}')

# Kaydet (protocol 4 ile)
model_data = {
    'model': model,
    'feature_cols': feature_cols
}

print("💾 Model kaydediliyor...")
with open('models/wear_gb_tuned_model.joblib', 'wb') as f:
    pickle.dump(model_data, f, protocol=4)

print('✅ Model models/wear_gb_tuned_model.joblib olarak kaydedildi')
