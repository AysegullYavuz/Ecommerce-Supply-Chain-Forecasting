import pandas as pd
import numpy as np
import pyodbc  
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error

print("Kütüphaneler başarıyla yüklendi! Yapay zeka modülü hazır.")

# Tüm süreç try bloğunun içinde güvenle çalışıyor
try:
    # 1. SQL Server Bağlantısı
    conn = pyodbc.connect(
        'Driver={SQL Server};'
        'Server=.\\SQLEXPRESS;'  
        'Database=Ecommerce_SupplyChain_DB;'
        'Trusted_Connection=yes;'
    )
    print("Veri tabanına bağlantı başarıyla sağlandı! 🎉")
    
    # 2. SQL Sorgusunu Çalıştırma ve Veriyi Çekme
    query = "SELECT * FROM v_DailySupplyChainForecast ORDER BY Satis_Tarihi ASC;"
    df = pd.read_sql(query, conn)
    conn.close()
    print("--- Veri Başarıyla Çekildi ---")

    # 3. Zaman Serisi Düzenleme (Resampling)
    # Tarih sütununu gerçek datetime formatına çevirip indeks yapıyoruz
    df['Satis_Tarihi'] = pd.to_datetime(df['Satis_Tarihi'])
    df.set_index('Satis_Tarihi', inplace=True)

    # Satış olmayan boş günleri bulup 0 ile dolduruyoruz
    df = df.asfreq('D', fill_value=0)

    # 4. Öznitelik Mühendisliği (Feature Engineering)
    df['Yil'] = df.index.year
    df['Ay'] = df.index.month
    df['Haftanin_Gunu'] = df.index.dayofweek  # 0: Pazartesi, 6: Pazar
    df['Ayin_Gunu'] = df.index.day

    # Gecikme (Lag) özellikleri ekliyoruz
    df['Satis_1_Gun_Once'] = df['Gunluk_Satis_Adedi'].shift(1)
    df['Satis_7_Gun_Once'] = df['Gunluk_Satis_Adedi'].shift(7)

    # Geçmiş verisi olmayan ilk satırlardaki NaN değerleri temizliyoruz
    df.dropna(inplace=True)

    print("\n--- Zaman Serisi ve Öznitelikler Hazırlandı ---")
    print(df.head(10))
    print("\nYeni Veri Yapısı Bilgisi:")
    print(df.info())
# 5. Model Kütüphanelerini İçe Aktarma ve Veriyi Bölme
    from sklearn.ensemble import RandomForestRegressor
    
    # Bağımlı değişken (Hedef): Günlük Satış Adedi
    # Bağımsız değişkenler (Öznitelikler): Tahmin için kullanacağımız sütunlar
    X = df[['Yil', 'Ay', 'Haftanin_Gunu', 'Ayin_Gunu', 'Satis_1_Gun_Once', 'Satis_7_Gun_Once']]
    y = df['Gunluk_Satis_Adedi']
    
    # Zaman serisi mantığına uygun olarak veriyi kronolojik bölme (%80 Train, %20 Test)
    train_size = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:train_size], X.iloc[train_size:]
    y_train, y_test = y.iloc[:train_size], y.iloc[train_size:]
    
    print(f"\nVeri bölündü: Eğitim Seti = {len(X_train)} gün, Test Seti = {len(X_test)} gün")
    
    # 6. Modeli Oluşturma ve Eğitme
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    print("Random Forest Regressor modeli başarıyla eğitildi! 🤖")
    
    # 7. Test Seti Üzerinde Tahmin Yapma ve Başarı Metrikleri
    y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    print("\n--- Model Performans Sonuçları ---")
    print(f"Ortalama Mutlak Hata (MAE): {mae:.2f} ürün")
    print(f"Hata Kareler Ortalamasının Kökü (RMSE): {rmse:.2f} ürün")
    
    # 8. Gelecek Tahmin Girdisi Gösterme (Örnek)
    print("\nTest setindeki ilk 5 günün Gerçek vs Tahmin Değerleri:")
    kararsilastirma_df = pd.DataFrame({'Gerçek': y_test.values, 'Tahmin': np.round(y_pred)}, index=y_test.index)
    print(kararsilastirma_df.head(5))
    
    # 9. Tahmin Sonuçlarını SQL Server'a Geri Yazma
    # SQL Server bağlantısını tekrar açıyoruz
    conn = pyodbc.connect(
        'Driver={SQL Server};'
        'Server=.\\SQLEXPRESS;'  
        'Database=Ecommerce_SupplyChain_DB;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    
    # Eğer tablo daha önceden varsa temizleyelim
    cursor.execute("IF OBJECT_ID('Olist_Model_Predictions', 'U') IS NOT NULL DROP TABLE Olist_Model_Predictions;")
    
    # Yeni tahmin tablosunu oluşturalım
    cursor.execute("""
        CREATE TABLE Olist_Model_Predictions (
            Satis_Tarihi DATE,
            Gercek_Satis INT,
            Tahmin_Satis INT
        );
    """)
    
    # Tahmin verilerini satır satır SQL'e insert edelim
    for index, row in kararsilastirma_df.iterrows():
        cursor.execute("""
            INSERT INTO Olist_Model_Predictions (Satis_Tarihi, Gercek_Satis, Tahmin_Satis) 
            VALUES (?, ?, ?);
        """, index.strftime('%Y-%m-%d'), int(row['Gerçek']), int(row['Tahmin']))
        
    conn.commit()
    conn.close()
    print("\n🎉 Tahmin sonuçları 'Olist_Model_Predictions' tablosu olarak SQL Server'a başarıyla kaydedildi!")
    
except Exception as e:
    print("Bir hata oluştu: ", e)