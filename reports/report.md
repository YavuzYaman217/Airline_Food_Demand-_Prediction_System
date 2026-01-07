# Havayolu Yemek Talebi Tahmini Projesi Raporu

**Takım Adı:** Vector_Team

## 1. Problem Tanımı

Havayolları, her uçuş için ne kadar yemek hazırlanacağını tahmin etme konusunda önemli zorluklarla karşılaşmaktadır. Yanlış tahminler, hem gıda israfına hem de yolcu memnuniyetsizliğine yol açmaktadır. Bu proje, uçuş süresi, yolcu sayısı, demografik bilgiler ve seyahat düzenleri gibi çeşitli faktörlere dayanarak havayolu yemek talebini tahmin etmek için bir makine öğrenimi çözümü geliştirmeyi amaçlamaktadır.

## 2. Veri Seti Açıklaması

Proje için, gerçek havayolu uçuş verilerini simüle eden sentetik bir veri seti oluşturulmuştur. Veri seti, her biri benzersiz bir uçuşu temsil eden 5.000 satır içermektedir. Veri setindeki temel özellikler ve açıklamaları aşağıdaki tabloda sunulmuştur:

| Özellik Adı          | Tip       | Açıklama                                                               |
| :------------------- | :-------- | :--------------------------------------------------------------------- |
| `flight_id`          | Tamsayı   | Benzersiz uçuş tanımlayıcı                                              |
| `flight_duration`    | Ondalıklı | Uçuş süresi (1-12 saat)                                                |
| `passenger_count`    | Tamsayı   | Toplam yolcu sayısı (50-300)                                           |
| `adult_passengers`   | Tamsayı   | Yetişkin yolcu sayısı                                                  |
| `child_passengers`   | Tamsayı   | Çocuk yolcu sayısı                                                     |
| `business_class_ratio` | Ondalıklı | Business class yolcu oranı (0-1)                                       |
| `is_international`   | İkili (0/1) | Uçuşun uluslararası olup olmadığı                                       |
| `total_food_demand`  | Tamsayı   | **HEDEF DEĞİŞKEN** - İhtiyaç duyulan toplam yemek birimi sayısı         |

Veri setinin oluşturulmasında aşağıdaki kısıtlamalar dikkate alınmıştır:
*   `adult_passengers` + `child_passengers` = `passenger_count`
*   `business_class_ratio` 0 ile 1 arasında olmalıdır.
*   `flight_duration` 1 ile 12 saat arasında olmalıdır.
*   Uluslararası uçuşlar (`is_international` = 1) için `flight_duration` en az 3 saat olmalıdır.
*   `passenger_count` 50 ile 300 arasında olmalıdır.
*   `total_food_demand` >= `passenger_count` * 0.5 olmalıdır.
*   Veri setinde en az %15 uluslararası uçuş bulunmaktadır.
*   Veri seti hem kısa (1-3 saat) hem de uzun (8-12 saat) uçuşları içermektedir.

## 3. Metodoloji

Proje, aşağıdaki adımları içeren bir makine öğrenimi iş akışı kullanılarak gerçekleştirilmiştir:

### 3.1. Veri Üretimi

Belirtilen özellikler ve kısıtlamalar doğrultusunda sentetik bir veri seti Python kullanılarak oluşturulmuştur. Hedef değişken `total_food_demand`, uçuş süresi, uluslararası uçuş durumu, business class oranı ve çocuk yolcu oranı gibi en az 3 farklı özelliğe dayalı karmaşık bir formül kullanılarak hesaplanmıştır.

### 3.2. Keşifsel Veri Analizi (EDA)

Oluşturulan veri seti üzerinde kapsamlı bir keşifsel veri analizi yapılmıştır. Bu analiz, veri dağılımlarını, eksik değerleri, özellikler arasındaki korelasyonları ve hedef değişken ile ilişkileri anlamak için kullanılmıştır.

### 3.3. Modelleme

Yemek talebi tahmini için üç farklı makine öğrenimi modeli uygulanmış ve karşılaştırılmıştır:

1.  **Baseline Modeli (Ortalama Tahminci):** Test setindeki tüm tahminler için eğitim setindeki `total_food_demand` ortalaması kullanılmıştır.
2.  **Lineer Regresyon Modeli:** Temel bir regresyon modeli olarak Lineer Regresyon kullanılmıştır.
3.  **Alternatif Model (Random Forest Regressor):** Daha gelişmiş bir model olarak Random Forest Regressor seçilmiştir. Bu model, özellikler arasındaki doğrusal olmayan ilişkileri yakalama yeteneği ve özellik önem derecesi sağladığı için tercih edilmiştir.

Modellerin performansını değerlendirmek için R², Ortalama Mutlak Hata (MAE) ve Ortalama Kare Hata Kökü (RMSE) metrikleri kullanılmıştır. Veri seti %80 eğitim ve %20 test olarak ayrılmıştır.

### 3.4. İş Maliyeti Analizi (Bonus)

Tahmin hatalarının iş maliyeti üzerindeki etkisi de değerlendirilmiştir. Maliyet fonksiyonu aşağıdaki gibi tanımlanmıştır:
*   Fazla tahmin edilen her yemek birimi için 5 dolar maliyet.
*   Eksik tahmin edilen her yemek birimi için 20 dolar maliyet.

## 4. Sonuçlar

### 4.1. Model Karşılaştırması

Modellerin performans metrikleri aşağıdaki tabloda özetlenmiştir:

| Model                 | R²        | MAE       | RMSE      |
| :-------------------- | :-------- | :-------- | :-------- |
| Baseline (Mean)       | -0.0000   | 129.19    | 163.55    |
| Linear Regression     | 0.9027    | 40.00     | 51.01     |
| Random Forest (Tuned) | 0.9983    | 4.15      | 6.81      |

Random Forest modelinin, diğer modellere kıyasla mükemmel bir performans gösterdiği görülmektedir. R² değeri 0.9983 ile varyansın neredeyse tamamını açıklamaktadır.

### 4.2. Görselleştirmeler

#### Korelasyon Isı Haritası
![Korelasyon Isı Haritası](plots/correlation_heatmap.png)

#### Random Forest: Gerçek vs. Tahmin Edilen Değerler
![Random Forest: Gerçek vs. Tahmin Edilen Değerler](plots/rf_actual_vs_predicted.png)

#### Random Forest: Özellik Önem Derecesi
![Random Forest: Özellik Önem Derecesi](plots/feature_importance.png)

#### Artık Dağılımı (Random Forest)
![Artık Dağılımı (Random Forest)](plots/residuals_distribution.png)

### 4.3. İş Maliyeti Analizi Sonuçları

| Model                 | Toplam Maliyet ($) |
| :-------------------- | :----------------- |
| Baseline              | 1,608,265          |
| Linear Regression     | 495,804            |
| Random Forest         | 58,049             |

İş maliyeti analizi, Random Forest modelinin operasyonel maliyetleri minimize etmede en etkili çözüm olduğunu kanıtlamaktadır.

## 5. Sonuç ve Gelecek Çalışmalar

Bu proje, Vector_Team tarafından havayolu yemek talebi tahmini için geliştirilen kapsamlı bir çözümdür. Random Forest Regressor modeli, yüksek doğruluk ve düşük iş maliyeti ile en iyi performansı göstermiştir. Proje, tüm SRS ve MD spesifikasyonlarını tam olarak karşılamaktadır.

**Gelecek Çalışmalar:**
*   Gerçek dünya verileri ile modelin doğrulanması.
*   Daha karmaşık maliyet modellerinin entegrasyonu.
*   Yemek türlerine göre özelleştirilmiş tahmin modelleri.
