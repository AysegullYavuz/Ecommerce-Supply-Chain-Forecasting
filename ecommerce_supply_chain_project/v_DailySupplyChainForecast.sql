-- =================================================================================
-- Proje Adı: E-Commerce Supply Chain & Demand Forecasting Project
-- Modül: Data Preparation & Verification (SQL Server Katmanı)
-- Açıklama: Olist veri setindeki sipariş, ürün ve kalem verilerini birleştirerek
--            'beleza_saude' (Sağlık & Güzellik) kategorisi için günlük bazda
--            toplam satış adedi ve günlük ciro metriklerini çıkaran View yapısı.
-- =================================================================================

CREATE VIEW v_DailySupplyChainForecast AS
SELECT 
    CAST(o.order_purchase_timestamp AS DATE) AS Satis_Tarihi,
    COUNT(i.product_id) AS Gunluk_Satis_Adedi,
    ROUND(SUM(CAST(i.price AS FLOAT)), 2) AS Gunluk_Ciro
FROM olist_orders_dataset o
INNER JOIN olist_order_items_dataset i ON o.order_id = i.order_id
INNER JOIN olist_products_dataset p ON i.product_id = p.product_id
WHERE p.product_category_name = 'beleza_saude'
GROUP BY CAST(o.order_purchase_timestamp AS DATE);