# radioCenter  

* Autor: Ruslan Dolovaniuk (Ucraina)  
* PayPal: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=B3VG4L8B7CV3Y&source=url
* Telegram Channel: https://t.me/elrusapps
* Telegram Group: https://t.me/elrus_apps

Acest addon îți permite să asculți posturi de radio online și să salvezi fluxul audio într-un fișier.  
Înregistrarea unui post de radio nu interferează cu ascultarea altuia.  

Pe lângă cataloagele de pe internet, poți adăuga și un catalog local cu fișiere m3u în colecții.  
Pentru a obține o colecție locală, trebuie să specifici calea de bază către catalog în setări.  
Toate fișierele m3u din acest catalog și din subdirectoarele sale vor fi verificate automat.  

### Atenție!  
Verificarea posturilor de radio din colecții este un proces destul de lung și consumă multe resurse.  
Se recomandă să o faci pe bucăți, închizând periodic fereastra și rulând verificarea mai târziu.  
După redeschiderea ferestrei colecțiilor, testarea va continua până când toate posturile vor fi verificate.  
De asemenea, starea link-urilor se poate schimba des, așa că e bine să verifici funcționalitatea unui link înainte de a-l adăuga în lista generală.  

## Lista de comenzi rapide:  
* **NVDA+ALT+P**: redare/pauză radio;  
* **NVDA+ALT+P** (dublă tastare): oprește radio-ul;  
* **NVDA+ALT+SHIFT+R**: pornește/oprește înregistrarea;  
* **NVDA+ALT+M**: activează/dezactivează sunetul;  
* **NVDA+ALT+Săgeată sus**: volum mai mare;  
* **NVDA+ALT+Săgeată jos**: volum mai mic;  
* **NVDA+ALT+Săgeată dreapta**: postul următor;  
* **NVDA+ALT+Săgeată stânga**: postul anterior;  
* **NVDA+ALT+O**: afișează informații despre post;  
* **NVDA+ALT+R**: deschide fereastra de control;  
* **ESC**: închide ferestrele Control Center și Colecții;  
* **CTRL+C**: copiază link-ul postului de radio în clipboard;  

### Când sortezi manual lista de posturi:  
* **ALT+Săgeată sus**: mută postul mai sus în listă;  
* **ALT+Săgeată jos**: mută postul mai jos în listă;  

### În listele de colecții:  
* **ALT+Săgeată sus / ALT+Săgeată dreapta**: trece la următorul link (dacă postul are mai multe link-uri);  
* **ALT+Săgeată jos / ALT+Săgeată stânga**: trece la link-ul anterior (dacă postul are mai multe link-uri);  
* **CTRL+C**: copiază link-ul postului de radio în clipboard;  

## Sortarea posturilor:  
* fără sortare;  
* alfabetic (A-Z);  
* alfabetic invers (Z-A);  
* după prioritate și nume (A-Z);  
* după prioritate și nume (Z-A);  
* manual;  

## Lista modificărilor:  
### Versiunea 4.6.3  
* a fost adăugată localizare în română (Nicu Untilă);  

### Versiunea 4.5.0  
* a fost adăugat meniu contextual în lista de posturi radio din fereastra principală;  
* a fost adăugată comandă rapidă pentru înregistrarea unui post de radio;  
* a fost rezolvată problema care prevenea înregistrarea fără a reda postul mai întâi;  
* a fost corectată actualizarea etichetelor butoanelor din fereastra principală;  
* a fost corectată actualizarea etichetelor elementelor din meniul NVDA;  
* a fost sincronizată schimbarea etichetelor pe butoane, în meniul NVDA și în meniul contextual, atunci când se folosesc combinații de taste;  
* a fost adăugată traducere în arabă (وفيق طاهر);  

### Versiunea 4.2.1  
* extrage automat numele postului (dacă există) din fișierul m3u;  
* a fost adăugată opțiunea de a afișa link-ul unui post în setări;  
* a fost adăugată opțiunea de a seta numărul de posturi verificate într-o sesiune;  
* au fost corectate unele erori în verificarea automată a posturilor;  

### Versiunea 4.0.0  
* s-au făcut colecțiile compatibile cu NVDA 2023 (cu excepția Radio Browser);  
* a fost creată o colecție pentru verificarea fișierelor m3u din stocarea locală;  
* a fost adăugat un meniu de control în meniul NVDA;  
* au fost mutate filtrele într-o fereastră separată;  
* a fost adăugat sunet de redare când un post este verificat manual în colecții;  
* a fost corectată o eroare care apărea uneori la verificarea posturilor după aplicarea filtrelor;  

### Versiunea 3.6.0  
* au fost adăugate modificări pentru compatibilitate cu NVDA 2023 (colecțiile sunt dezactivate pentru această versiune);  
* a fost adăugat suport pentru link-uri m3u;  
* s-a făcut filtrarea insensibilă la majuscule/micuscule;  
* au fost eliminate spațiile de la începutul și sfârșitul numelui posturilor la procesare;  
* a fost adăugată anunțarea stării postului la verificarea manuală în colecții;  
* a fost corectată o eroare care apărea uneori la actualizarea colecțiilor;  

### Versiunea 3.2.0  
* a fost adăugat suport pentru fișiere .pls;  
* a fost adăugat numele postului în metadatele fișierului înregistrat;  
* a fost implementată rezolvarea de erori pentru situațiile în care înregistrarea nu poate începe;  

### Versiunea 3.0.0  
* a fost creat un sistem de colecții pentru selecția posturilor din cataloage;  
* au fost adăugate 3 colecții cu posturi de radio;  
* a fost implementată verificarea automată a funcționalității posturilor în colecții;  
* a fost adăugată verificarea manuală a unui post;  
* a fost adăugată redarea unui post direct din lista de colecții;  
* a fost adăugată salvarea posturilor în lista generală;  
* au fost adăugate filtre pentru colecții (după stare, titlu și informații suplimentare);  
* a fost adăugată posibilitatea de a închide ferestrele cu ESC;  
* a fost adăugată posibilitatea de a copia link-ul postului din lista principală și din colecții;  
* a fost îmbunătățită comutarea posturilor cu taste rapide;  

### Versiunea 2.1.0  
* a fost adăugată verificarea și corectarea indexării posturilor;  
* a fost adăugată localizare în spaniolă (Rémy Ruiz);  
* a fost adăugată localizare în franceză (Rémy Ruiz);  

### Versiunea 2.0.0  
* a fost adăugată posibilitatea de a înregistra fluxul audio într-un fișier;  

### Versiunea 1.5.3  
* a fost adăugată localizare în cehă (Jiri Holz);  

### Versiunea 1.5.1  
* a fost adăugată verificarea funcționalității unui link înainte de a-l adăuga sau modifica;  
* au fost corectate diverse erori minore;  

### Versiunea 1.4.2  
* a fost adăugată sortarea manuală a posturilor;  
* a fost adăugată combinație de taste pentru modul mute;  

### Versiunea 1.2.5  
* au fost adăugate setări în panoul de setări NVDA;  
* a fost adăugată posibilitatea de a edita un post existent;  
* au fost adăugate mai multe opțiuni de sortare;  
* a fost modificată funcția de muting;  
* a fost corectată problema deschiderii multiple a ferestrelor de control;  

### Versiunea 1.1.1  
* a fost adăugată localizare în turcă (Umut Korkmaz);  

### Versiunea 1.1.0  
* a fost adăugat centru de control GUI;  

### Versiunea 1.0.0  
* a fost creat radio online bazat pe VLC Player;  
