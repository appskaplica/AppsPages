# AppsPages

Uygulamaların (gizli repolarda tutulan) herkese açık sayfaları — gizlilik politikaları, destek sayfaları vb. GitHub Pages ile `main` dalının kökünden yayınlanır.

Her uygulama kendi klasöründedir:

| Uygulama | Sayfa | Adres |
|---|---|---|
| WaterTracker | Gizlilik Politikası | https://appskaplica.github.io/AppsPages/watertracker/privacy.html |
| WaterTracker | Destek | https://appskaplica.github.io/AppsPages/watertracker/support.html |

## WaterTracker

Sayfalar uygulamanın 12 dilinde (`tr en de es fr it pt-BR ru ar zh-Hans ja ko`) `watertracker/<dil>/privacy.html` ve `watertracker/<dil>/support.html` olarak bulunur. `watertracker/privacy.html` ve `watertracker/support.html` tarayıcı diline göre ilgili sayfaya yönlendirir.

Metinler elle düzenlenmez; `tools/build_watertracker.py` içinde değiştirilip yeniden üretilir:

```bash
python3 tools/build_watertracker.py
```

App Store Connect'te her yerelleştirme için Privacy Policy URL ve Support URL alanlarına o dilin adresi (ör. `.../watertracker/de/privacy.html`) girilebilir.

Yeni uygulama eklerken bir klasör açıp `index.html` listesine bağlantısını ekleyin.
