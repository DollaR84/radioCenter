# radiocentrum

* Autor: Ruslan Dolovanyuk (Ukrajina)
* PayPal: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=B3VG4L8B7CV3Y&source=url
* Telegram Channel: https://t.me/elrusapps
* Telegram Group: https://t.me/elrus_apps

tento doplněk vám umožňuje poslouchat online rozhlasové stanice a uložit audio stream do souboru.
Nahrávání jedné rozhlasové stanice neruší poslech jiné rozhlasové stanice.

Ve sbírkách je možné kromě internetových adresářů přidat i lokální adresář se soubory m3u.
Chcete-li získat místní kolekci, musíte v nastavení zadat základní cestu k adresáři.
Všechny soubory m3u v tomto adresáři a všechny jeho podadresáře budou automaticky zkontrolovány.

Varování!
Kontrola rádiových stanic ze sbírek je poměrně zdlouhavý a náročný proces.
Doporučuje se provádět jej po částech, pravidelně zavírat okno a spouštět jej později.
Po opětovném otevření okna kolekcí bude testování pokračovat, dokud nebudou zkontrolovány všechny rádiové stanice.
Stav odkazů se také často mění, proto se doporučuje zkontrolovat stav odkazu v tuto chvíli před přidáním do obecného seznamu.


## Seznam klávesových zkratek:
* NVDA+ALT+P: přehrávání/pozastavení rádia;
* Dvojité kliknutí NVDA+ALT+P: vypněte rádio;
* NVDA+ALT+SHIFT+R: Povolí/zakáže nahrávání;
* NVDA+ALT+M: povolit/zakázat ztlumení;
* NVDA+ALT+šipka nahoru: zvýšení hlasitosti;
* NVDA+ALT+šipka dolů: snížení hlasitosti;
* NVDA+ALT+šipka vpravo: další stanice;
* NVDA+ALT+šipka doleva: Předchozí stanice;
* NVDA+ALT+O: získat informace o stanici;
* NVDA+ALT+R: otevření okna ovládacího centra;
* ESC: zavře okna Control Center a Collections;
* CTRL+C: zkopírujte odkaz na rozhlasovou stanici do schránky;

Při ručním řazení v seznamu stanic:
* ALT+šipka nahoru: přesune stanici na vyšší pozici;
* ALT+šipka dolů: přesunutí stanice na nižší pozici;

V seznamech sbírek:
* ALT+šipka nahoru nebo ALT+šipka doprava: přepnutí odkazu na další (pokud má rozhlasová stanice několik odkazů na audio stream);
* ALT+šipka dolů nebo ALT+šipka doleva: přepne odkaz na předchozí (pokud má rozhlasová stanice několik odkazů na audio stream);
* CTRL+C: zkopírujte odkaz na rozhlasovou stanici do schránky;

## Třídící stanice:
* bez řazení;
* podle jména směrem vpřed;
* podle jména v opačném směru;
* podle priority a jména v dopředném směru;
* podle priority a jména v opačném směru;
* ručně;

## Seznam změn:
### Verze 4.6.3  
* Přidána rumunská lokalizace (Nicu Untilă);

### Verze 4.5.0
* přidáno kontextové menu do seznamu rozhlasových stanic v hlavním okně;
* přidána kombinace kláves pro nahrávání rozhlasové stanice;
* pevná dostupnost nahrávání bez nutnosti spuštění přehrávání rozhlasové stanice;
* opravena změna popisků na tlačítkách v hlavním okně;
* opravena změna v popiscích prvků v servisním menu nvda;
* synchronizovaná změna popisků na tlačítkách hlavního okna, prvky servisního menu nvda, prvky kontextového menu, při stisknutí kombinací kláves;
* přidán arabský překlad (وفيق طاهر);

### Verze 4.2.1
* přidána extrakce názvu stanice, pokud existuje, při zpracování souboru m3u;
* Do nastavení přidána možnost, zda zobrazit odkaz na stanici;
* do nastavení byla přidána možnost pro počet stanic na kontrolovanou porci;
* opraveny některé chyby při automatické kontrole stanic;

### Verze 4.0.0
* pro nvda 2023 vyrobené kolekce kompatibilní, s výjimkou jednoho prohlížeče rádia;
* vytvořil kolekci kontrolních souborů m3u na místním úložišti;
* přidáno ovládací menu do menu nvda;
* přesunuty filtry do samostatného dialogového okna;
* přidáno přehrávání zvuku při ruční kontrole stanice ve sbírkách;
* opravena chyba kontroly plovoucí stanice po použití filtrů;

### Verze 3.6.0
* provedli změny pro kompatibilitu s nvda 2023 (sbírky jsou pro verzi 2023 zakázány);
* přidána podpora pro odkazy m3u;
* přidáno ignorování velikosti písmen při filtrování podle jména a/nebo informací;
* přidáno vymazání mezer na začátku a konci názvů rozhlasových stanic při analýze ve sbírkách;
* přidána výslovnost stavu stanice při ruční kontrole pomocí testovacího tlačítka v kolekcích;
* opravena plovoucí chyba při aktualizaci kolekcí;

### Verze 3.2.0
* přidána podpora pro odkazy .pls;
* přidán název z informace o audio streamu při ukládání nahraného souboru;
* přidáno zpracování chyb, když nelze spustit nahrávání;

### Verze 3.0.0
* vytvořil sbírkový mechanismus pro výběr rozhlasových stanic z katalogů;
* přidány 3 sbírky s rozhlasovými stanicemi;
* vytvořili mechanismus pro automatickou kontrolu funkčnosti každé rádiové stanice ve sbírkách;
* přidána manuální kontrola funkčnosti rádiové stanice;
* přidáno přehrávání rozhlasové stanice přímo v seznamu kolekcí;
* přidáno ukládání rozhlasových stanic z kolekce do obecného seznamu;
* přidáno filtrování ve sbírkách podle stavu;
* přidáno filtrování ve sbírkách podle textu v názvu;
* přidáno filtrování ve sbírkách podle textu v dalších informacích;
* přidáno zavírání dialogových oken stisknutím ESC;
* přidáno kopírování odkazu na rozhlasovou stanici do schránky v hlavním seznamu a v seznamech sbírek;
* vylepšené přepínání stanic pomocí horkých kláves, protože dříve se ne vždy přepínalo;

### Verze 2.1.0
* přidána kontrola a oprava, pokud jsou nalezeny chyby v indexování stanic;
* přidána španělská lokalizace (Rémy Ruiz);
* přidána francouzská lokalizace (Rémy Ruiz);

### Verze 2.0.0
* přidána možnost nahrávat audio stream do souboru;

### Verze 1.5.3
* přidána česká lokalizace (Jiri Holz);

### Verze 1.5.1
* přidána kontrola funkčnosti spojení před přidáním nové rozhlasové stanice;
* přidána kontrola funkčnosti spojení před změnou spojení rádiové stanice;
* opraveno několik drobných chyb v provozu;

### Verze 1.4.2
* přidáno ruční řazení stanic;
* přidána kombinace kláves pro režim ztlumení;

### Verze 1.2.5
* přidána nastavení do panelu nastavení nvda;
* přidána možnost upravovat existující rozhlasovou stanici;
* přidáno několik možností pro třídění rozhlasových stanic;
* změnila funkci ztlumení;
* opraven problém s otevíráním několika ovládacích oken;

### Verze 1.1.1
* přidána turecká lokalizace (Umut Korkmaz);

### Verze 1.1.0
* přidáno grafické rozhraní pro řídicí centrum;

### Verze 1.0.0
* vytvořil online rádio založené na přehrávači vlc;
