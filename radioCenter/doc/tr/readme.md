# radyo merkezi

* Yazar: Ruslan Dolovaniuk (Ukrayna)
* PayPal: ruslan.dolovaniuk84@gmail.com

bu eklenti çevrimiçi radyo istasyonlarını dinlemenize ve ses akışını bir dosyaya kaydetmenize olanak tanır.
Bir radyo istasyonunun kaydedilmesi, başka bir radyo istasyonunun dinlenmesini engellemez.

Koleksiyonlara İnternet dizinlerinin yanı sıra m3u dosyalarının bulunduğu yerel bir dizin de eklemek mümkündür.
Yerel bir koleksiyon elde etmek için ayarlarda dizinin temel yolunu belirtmeniz gerekir.
Bu dizindeki ve tüm alt dizinlerindeki tüm m3u dosyaları otomatik olarak taranacaktır.

Warnings!
Checking radio stations from collections is a rather lengthy and resource-intensive process.
It is recommended to perform it in parts, periodically closing the window, and rerun it later.
After reopening the collections window, testing will continue until all radio stations have been checked.
Also, the health status of links often changes, so it is recommended to check the health of the link at the moment before adding it to the general list.


## Kısayol listesi:

* NVDA+ALT+P: radyoyu Çal/duraklat;
* NVDA+ALT+P çift tıklama: radyoyu kapatır;
* NVDA+ALT+M: sessize almayı etkinleştir/devre dışı bırak;
* NVDA+ALT+Yukarı Ok: sesi arttır;
* NVDA+ALT+Aşağı Ok: sesi azalt;
* NVDA+ALT+Sağ ok: sonraki istasyon;
* NVDA+ALT+Sol Ok: önceki istasyon;
* NVDA+ALT+O: istasyon bilgisini al;
* NVDA+ALT+R: Radyo merkezi penceresini açar;
* ESC: Kontrol Merkezi ve Koleksiyonlar pencerelerini kapatır;
* CTRL+C: radyo istasyonunun bağlantısını panoya kopyalar;

İstasyon listesinde manuel olarak sıralama yaparken:
* ALT+Yukarı Ok: istasyonu daha üst sıraya taşır;
* ALT+Aşağı ok: istasyonu daha alt sıraya taşır;

Koleksiyon listelerinde:
* ALT+Yukarı Ok veya ALT+Sağ Ok: bağlantıyı bir sonrakine geçirir (radyo istasyonunun ses akışına birden fazla bağlantısı varsa);
* ALT+Aşağı Ok veya ALT+Sol Ok: bağlantıyı bir öncekine geçirir (radyo istasyonunun ses akışına birden fazla bağlantısı varsa);
* CTRL+C: radyo istasyonunun bağlantısını panoya kopyalar;

## İstasyonları sıralama:
* sıralama yapmadan;
* ileri yönde isme göre;
* ters yönde isimle;
* ileri yönde öncelik ve isme göre;
* önceliğe ve isme göre ters yönde;
* manuel olarak;

## Değişiklik listesi:
### Sürüm 4.2.1
* m3u dosyasını işlerken varsa istasyon adının çıkarılması eklendi;
* Ayarlara istasyona bağlantı gösterilip gösterilmeyeceği seçeneği eklendi;
* Ayarlara, kontrol edilecek porsiyon başına istasyon sayısı için bir seçenek eklendi;
* istasyonları otomatik olarak kontrol ederken bazı hatalar düzeltildi;

### Sürüm 4.0.0
* nvda 2023 için, bir Radyo Tarayıcı hariç uyumlu hale getirilmiş koleksiyonlar;
* yerel depolamadaki m3u dosyalarını kontrol eden bir koleksiyon oluşturdu;
* nvda menüsüne bir kontrol menüsü eklendi;
* filtreleri ayrı bir iletişim kutusuna taşıdı;
* koleksiyonlardaki bir istasyonu manuel olarak kontrol ederken ses çalma eklendi;
* filtreler uygulandıktan sonra kayan istasyon kontrol hatası düzeltildi;

### Sürüm 3.6.0
* nvda 2023 ile uyumluluk için değişiklikler yapıldı (koleksiyonlar 2023 sürümü için devre dışı bırakıldı);
* m3u bağlantıları için destek eklendi;
* isme ve/veya bilgiye göre filtreleme yaparken büyük/küçük harfin göz ardı edilmesi eklendi;
* koleksiyonlarda ayrıştırma yapılırken radyo istasyonları adlarının başına ve sonuna boşlukların temizlenmesi eklendi;
* koleksiyonlardaki test düğmesini kullanarak manuel olarak kontrol ederken istasyon durumunun telaffuzu eklendi;
* koleksiyonları güncellerken oluşan kayan hata düzeltildi;

### Sürüm 3.2.0
* .pls bağlantıları için destek eklendi;
* kaydedilen dosyayı kaydederken ses akışı bilgilerinden bir ad eklendi;
* kayıt başlatılamadığında hata yönetimi eklendi;

### Sürüm 3.0.0
* kataloglardan radyo istasyonlarını seçmek için bir koleksiyon seçeneği oluşturuldu;
* radyo istasyonlarını içeren 3 koleksiyon eklendi;
* koleksiyonlardaki her radyo istasyonunun işlevsellik açısından otomatik olarak kontrol edilmesi için bir mekanizma oluşturuldu;
* işlevsellik açısından radyo istasyonunun manuel kontrolü eklendi;
* radyo istasyonunun çalınması doğrudan koleksiyon listesine eklendi;
* radyo istasyonlarını koleksiyondan genel listeye kaydetme eklendi;
* koleksiyonlara duruma göre filtreleme eklendi;
* koleksiyonlara başlıktaki metne göre filtreleme eklendi;
* koleksiyonlara ek bilgilerdeki metne göre filtreleme eklendi;
* ESC tuşuna basarak iletişim kutularını kapatma seçeneği eklendi;
* Ana listede ve koleksiyon listelerinde radyo istasyonunun bağlantısını panoya kopyalama özelliği eklendi;
* daha önce her zaman geçiş yapılamadığı için, kısayol tuşları kullanılarak istasyonlar arasında geçiş iyileştirildi;

### Sürüm 2.1.0
* istasyonların indekslenmesinde hatalar bulunursa kontrol ve düzeltme eklendi;
* İspanyolca yerelleştirme eklendi (Rémy Ruiz);
* Fransızca yerelleştirme eklendi (Rémy Ruiz);

### Sürüm 2.0.0
* bir dosyaya ses akışını kaydetme özelliği eklendi;

### Sürüm 1.5.3
* Çek yerelleştirmesi eklendi (Jiri Holz);

### Sürüm 1.5.1
* yeni bir radyo istasyonu eklemeden önce bir bağlantı işlevselliği kontrolü eklendi;
* radyo istasyonu bağlantısını değiştirmeden önce bir bağlantı işlevselliği kontrolü eklendi;
* operasyondaki bir dizi küçük hata düzeltildi;

### Sürüm 1.4.2
* istasyonların manuel olarak sıralanması eklendi;
* sessiz modu için bir tuş kombinasyonu eklendi;

### Sürüm 1.2.5
* nvda ayarlar paneline ayarlar eklendi;
* mevcut bir radyo istasyonunu düzenleme yeteneği eklendi;
* radyo istasyonlarını sıralamak için çeşitli seçenekler eklendi;
* sessize alma işlevi değiştirildi;
* birden fazla kontrol penceresinin açılması sorunu düzeltildi;

### Sürüm 1.1.1
* Türkçe yerelleştirme eklendi (Umut Korkmaz);

### Sürüm 1.1.0
* GUI kontrol merkezi eklendi;

### Sürüm 1.0.0
* temel vlc oynatıcısında çevrimiçi radyo oluşturuldu;
