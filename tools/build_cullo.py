#!/usr/bin/env python3
"""Cullo gizlilik ve destek sayfalarını uygulamanın 4 dilinde üretir.

Metinleri bu dosyada düzenleyip çalıştırın:  python3 tools/build_cullo.py
Çıktı: cullo/<dil>/privacy.html ve cullo/<dil>/support.html
"""
from html import escape
from pathlib import Path

APP = "Cullo"
EMAIL = "appskaplica@gmail.com"
OUT = Path(__file__).resolve().parent.parent / "cullo"
QUOTA_MB = 50   # Cullo'daki FreeQuota.limitBytes
TRIAL_DAYS = 3  # Products.storekit: yıllık planın tanıtım teklifi

# Her dilde: uygulamadaki arayüz etiketleri (Cullo'nun Localizable.xcstrings metinleriyle aynı),
# iOS menü yolları ve sayfa metinleri. Metinlerde {etiket} yer tutucuları aynı sözlükten doldurulur.
L = {
    "tr": dict(
        name="Türkçe",
        premiumTab="Premium", restore="Satın Alımları Geri Yükle", manage="Aboneliği Yönet",
        guide="Son Silinenler'i boşalt — rehber", showHidden="Gizlenen grupları göster",
        notSimilar="Benzer değil — bu grubu gizle", rescan="Yeniden tara", shrinkAll="Hepsini sırayla küçült",
        recentlyDeleted="Son Silinenler", utilities="Araçlar",
        subsPath="Ayarlar › [adınız] › Abonelikler", photosPrivacyPath="Ayarlar › Gizlilik ve Güvenlik › Fotoğraflar",
        updated="Son güncelleme: 8 Kasım 2026",
        privacy="Gizlilik Politikası", support="Destek", languages="Diller",
        p_title="Cullo Gizlilik Politikası",
        p_intro="Cullo, iPhone'unuzdaki kopya ve benzer fotoğrafları, seri çekimleri, ekran görüntülerini ve büyük videoları bulup yer açmanıza yardımcı olan bir iOS uygulamasıdır. Bu sayfa uygulamanın hangi verileri kullandığını, nerede sakladığını ve nasıl kullandığını açıklar.",
        h_collect="Topladığımız veriler",
        collect="Hiçbirini. Cullo'nun sunucusu, hesap sistemi, analitik ya da reklam aracı yoktur ve sizi takip etmeyiz. Fotoğraflarınız, videolarınız ve analiz sonuçları cihazınızdan hiçbir zaman çıkmaz; biz göremeyiz. Tek istisna, bize kendiniz e-posta göndermeyi seçmenizdir (aşağıya bakın).",
        h_photos="Fotoğraf arşiviniz",
        photos_read="<strong>Analiz:</strong> İzin verdiğinizde Cullo fotoğraf ve videolarınızı yalnızca iPhone'unuzda analiz eder: birebir kopyaları dosya özetiyle (SHA-256), benzer kareleri, netliği, açık gözleri ve yüz kalitesini Apple'ın Vision çerçevesiyle bulur. Analiz için yalnızca cihazınızda bulunan dosyalar okunur; yalnızca iCloud'da duran orijinaller analiz için indirilmez.",
        photos_view="<strong>Görüntüleme:</strong> Bir fotoğrafı tam ekran açtığınızda ya da bir videoyu oynattığınızda orijinal yalnızca iCloud'daysa iOS onu Apple'ın sunucularından getirir. Bu, Fotoğraflar uygulamasında olduğu gibi Apple tarafından yapılır; bizim sunucumuzdan geçmez.",
        photos_delete="<strong>Silme:</strong> Cullo hiçbir şeyi kendiliğinden silmez. Seçtiğiniz öğeler ancak sizin ve ardından iOS'un onayıyla “{recentlyDeleted}” albümüne taşınır ve orada 30 gün kalır. iCloud Fotoğrafları açıksa silme, aynı Apple Hesabı'ndaki tüm cihazlarınıza yansır.",
        photos_shrink="<strong>Video küçültme:</strong> Küçültme cihazınızda yapılır. Yeni sürüm önce geçici bir dosya olarak hazırlanır; onaylarsanız arşivinize kaydedilir, orijinal “{recentlyDeleted}”e taşınır. Onaylamadığınız geçici dosyalar silinir.",
        h_device="Cihazınızda saklanan veriler",
        dev_results="<strong>Tarama sonuçları:</strong> Son taramanın grupları yalnızca fotoğraf tanımlayıcılarıyla (görüntü içeriği olmadan) uygulamanın kendi alanında saklanır; böylece sonuçlar her açılışta yeniden taranmadan gelir. Dosya boyutları ve kalite puanları da hızlanmak için önbellekte tutulur.",
        dev_prefs="<strong>Tercihler:</strong> “Benzer değil” diyerek gizlediğiniz gruplar ve küçültülemeyen videoların listesi cihazınızda saklanır.",
        dev_widget="<strong>Widget ve istatistikler:</strong> Depolama özeti, temizlenebilir alan ve temizlik istatistikleri (silinen öğe sayıları ve kazanılan alan) widget'ın da okuyabilmesi için uygulamanın paylaşılan alanında tutulur. Bunlar yalnızca sayılardır; fotoğraf ya da tanımlayıcı içermez.",
        dev_quota="<strong>Ücretsiz kota:</strong> Ücretsiz planda kullandığınız silme miktarı (tek bir sayı) cihazınızın Anahtar Zinciri'nde saklanır; böylece uygulamayı yeniden yüklemek kotayı sıfırlamaz. Kişisel veri içermez ve cihazınızdan çıkmaz.",
        h_feedback="E-postayla iletişim",
        p_feedback="Bize e-posta gönderirseniz e-posta adresinizi ve mesajınızı yalnızca yanıt vermek için kullanırız ve kimseyle paylaşmayız.",
        h_purchases="Satın almalar",
        purchases="Pro abonelikler Apple tarafından App Store üzerinden işlenir. Ödeme bilgilerinize erişimimiz yoktur. Aboneliğinizi {subsPath} bölümünden yönetebilir veya iptal edebilirsiniz.",
        h_delete="Verilerinizi silme",
        delete="Uygulamayı silmek tarama sonuçlarını, önbelleği, tercihleri ve istatistikleri cihazınızdan kaldırır. Ücretsiz kotanın kullanılan miktarını tutan sayı, kotanın yeniden yüklemeyle sıfırlanmaması için Anahtar Zinciri'nde kalır. Cullo'nun fotoğraf arşivinize erişimini istediğiniz zaman {photosPrivacyPath} bölümünden kapatabilirsiniz.",
        h_children="Çocuklar",
        children="Uygulama çocuklardan bilerek veri toplamaz; zaten hiçbir kullanıcıdan kişisel veri toplamaz.",
        h_changes="Değişiklikler",
        changes="Bu politika değişirse güncel hâli yeni tarihiyle bu sayfada yayınlanır.",
        h_contact="İletişim",
        p_contact="Gizlilikle ilgili sorularınız için: {mail}",
        s_title="Cullo Destek",
        s_intro="Bir sorunuz, bulduğunuz bir hata ya da bir fikriniz mi var? Bize yazın; her mesajı okuyoruz.",
        s_contact="E-posta: {mail}. iOS sürümünüzü, iPhone modelinizi ve sorunu kısaca yazmanız size daha hızlı yardımcı olmamızı sağlar.",
        h_faq="Sık sorulan sorular",
        faq=[
            ("Ücretsiz planda neler var?",
             "Tarama, tüm kategoriler ve ne kadar yer açabileceğinizin tahmini ücretsizdir. Ücretsiz planda öğeleri tek tek, toplam {quota} MB'a kadar silebilirsiniz; bu kota uygulamayı yeniden yükleyince sıfırlanmaz. Sınırsız silme, toplu seçim ve “hepsini sil”, video küçültme ve otomatik en iyi kare Pro'ya dahildir."),
            ("Ücretsiz deneme var mı?",
             "Yıllık planda {trial} günlük ücretsiz deneme vardır. Deneme bitmeden en az 24 saat önce iptal etmezseniz abonelik yıllık ücretle otomatik başlar. Fiyatlar uygulamadaki satın alma ekranında yerel para biriminizle gösterilir."),
            ("Aboneliğimi nasıl yönetir veya iptal ederim?",
             "Uygulamada {premiumTab} sekmesini açıp <em>{manage}</em> düğmesine dokunun ya da {subsPath} bölümüne gidin. Abonelik, dönem bitmeden en az 24 saat önce iptal edilmezse otomatik yenilenir."),
            ("Pro satın aldım ama açılmadı.",
             "{premiumTab} sekmesinde <em>{restore}</em> düğmesine dokunun. Satın alırken kullandığınız Apple Hesabı ile giriş yaptığınızdan emin olun."),
            ("Nasıl iade alabilirim?",
             "Ödemeleri Apple işlediği için iade talebi Apple'a <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a> adresinden yapılır."),
            ("Sildim ama boş alan artmadı.",
             "iOS silinen öğeleri 30 gün boyunca “{recentlyDeleted}” albümünde tutar; alan bu albüm boşaltılınca açılır. Fotoğraflar uygulamasında aşağı kaydırıp {utilities} altında “{recentlyDeleted}”e dokunun ve tümünü silin. Uygulamada {premiumTab} › <em>{guide}</em> adım adım gösterir. Apple bu albümü yalnızca sizin boşaltmanıza izin verir."),
            ("iCloud Fotoğrafları açıksa ne olur?",
             "Cullo'da sildiğiniz öğe, aynı Apple Hesabı'ndaki iPad, Mac ve iCloud.com'dan da silinir. “iPhone Saklama Alanını Optimize Et” açıksa bazı orijinaller yalnızca iCloud'dadır; bunları silmek iPhone'da değil iCloud'da yer açar. Cullo bu iki miktarı ayrı gösterir."),
            ("Benzer olmayan fotoğraflar aynı grupta.",
             "Grubu açıp <em>{notSimilar}</em> seçeneğine dokunun; grup sonraki taramalarda da gösterilmez. Gizlediğiniz grupları {premiumTab} › <em>{showHidden}</em> ile geri getirebilirsiniz."),
            ("Bazı benzer fotoğraflarım bulunmadı.",
             "Benzer fotoğraflar, birbirine birkaç dakika arayla çekilmiş kareler arasında aranır; farklı günlerde çekilmiş benzer kareler gruplanmaz. Kopyalar bölümü yalnızca birebir aynı dosyaları bulur. Yalnızca iCloud'da duran orijinaller analiz edilmez. Yeni fotoğraf çektiyseniz Genel Bakış'ta <em>{rescan}</em> düğmesine dokunun."),
            ("Video küçültme nasıl çalışır?",
             "Videolar HEVC biçiminde HD'ye (720p) küçültülür; HDR videolar HDR kalır. Hiçbir şey silinmeden önce eski ve yeni sürümü karşılaştırırsınız; onayladığınızda yeni sürüm tarih, konum, favori ve albüm bilgileriyle kaydedilir ve orijinal “{recentlyDeleted}”e gider. Ağır çekim ve Sinematik videolar ile orijinali yalnızca iCloud'da olan videolar küçültmeye sunulmaz. <em>{shrinkAll}</em> tüm videoları hazırlar ve tek bir onayla kaydeder."),
            ("Sadece bazı fotoğraflarım taranıyor.",
             "Erişim izni verirken “Erişimi Sınırla”yı seçtiyseniz Cullo yalnızca seçtiğiniz öğeleri görebilir. Tüm arşivi taramak için {photosPrivacyPath} › Cullo bölümünden “Tam Erişim”i seçin."),
            ("Widget'ı nasıl eklerim?",
             "Ana ekranda boş bir alana basılı tutun, Düzenle › Widget Ekle'ye dokunun ve Cullo'yu seçin. Widget boş alanı ve ne kadar temizleyebileceğinizi gösterir; kilit ekranında da kullanılabilir."),
        ],
    ),
    "en": dict(
        name="English",
        premiumTab="Premium", restore="Restore Purchases", manage="Manage Subscription",
        guide="Empty Recently Deleted — guide", showHidden="Show hidden groups",
        notSimilar="Not similar — hide this group", rescan="Rescan", shrinkAll="Shrink all, one by one",
        recentlyDeleted="Recently Deleted", utilities="Utilities",
        subsPath="Settings › [your name] › Subscriptions", photosPrivacyPath="Settings › Privacy & Security › Photos",
        updated="Last updated: November 8, 2026",
        privacy="Privacy Policy", support="Support", languages="Languages",
        p_title="Cullo Privacy Policy",
        p_intro="Cullo is an iOS app that finds duplicate and similar photos, bursts, screenshots and large videos on your iPhone and helps you free up space. This page explains what data the app uses, where it is stored and how.",
        h_collect="Data we collect",
        collect="None. Cullo has no servers, accounts, analytics or advertising tools, and we never track you. Your photos, videos and analysis results never leave your device — we cannot see them. The only exception is when you choose to email us yourself (see below).",
        h_photos="Your photo library",
        photos_read="<strong>Analysis:</strong> When you grant access, Cullo analyzes your photos and videos only on your iPhone: it finds exact duplicates with a file hash (SHA-256), and similar shots, sharpness, open eyes and face quality with Apple's Vision framework. Only files stored on the device are read for analysis; originals kept only in iCloud are not downloaded for it.",
        photos_view="<strong>Viewing:</strong> When you open a photo full screen or play a video whose original is only in iCloud, iOS fetches it from Apple's servers. This is done by Apple, just as in the Photos app — never through our servers.",
        photos_delete="<strong>Deleting:</strong> Cullo never deletes anything on its own. Items you select are moved to “{recentlyDeleted}” only after you confirm and iOS asks once more, and they stay there for 30 days. If iCloud Photos is on, the deletion applies to all your devices signed in to the same Apple Account.",
        photos_shrink="<strong>Shrinking videos:</strong> Shrinking happens on your device. The new version is first prepared as a temporary file; if you accept it, it is saved to your library and the original is moved to “{recentlyDeleted}”. Temporary files you don't accept are deleted.",
        h_device="Data stored on your device",
        dev_results="<strong>Scan results:</strong> The groups from your last scan are stored in the app's own storage as photo identifiers only (no image content), so results appear without rescanning each time. File sizes and quality scores are also cached to speed things up.",
        dev_prefs="<strong>Preferences:</strong> Groups you hide with “Not similar” and the list of videos that couldn't be shrunk are stored on your device.",
        dev_widget="<strong>Widget and statistics:</strong> A storage summary, the space you can clean and your cleaning statistics (numbers of items deleted and space recovered) are kept in the app's shared container so the widget can show them. These are numbers only — no photos or identifiers.",
        dev_quota="<strong>Free quota:</strong> How much you have deleted on the free plan (a single number) is stored in your device's Keychain, so reinstalling the app does not reset the quota. It contains no personal data and never leaves your device.",
        h_feedback="Contacting us by email",
        p_feedback="If you email us, we use your email address and message only to reply and never share them.",
        h_purchases="Purchases",
        purchases="Pro subscriptions are processed by Apple through the App Store. We have no access to your payment information. You can manage or cancel your subscription in {subsPath}.",
        h_delete="Deleting your data",
        delete="Deleting the app removes the scan results, cache, preferences and statistics from your device. The number that records your used free quota stays in the Keychain so the quota isn't reset by reinstalling. You can turn off Cullo's access to your photo library at any time in {photosPrivacyPath}.",
        h_children="Children",
        children="The app does not knowingly collect data from children — it does not collect personal data from anyone.",
        h_changes="Changes",
        changes="If this policy changes, the updated version will be published on this page with a new date.",
        h_contact="Contact",
        p_contact="Questions about privacy: {mail}",
        s_title="Cullo Support",
        s_intro="Have a question, found a bug or have an idea? Write to us — we read every message.",
        s_contact="Email: {mail}. Including your iOS version, iPhone model and a short description of the problem helps us help you faster.",
        h_faq="Frequently asked questions",
        faq=[
            ("What's included in the free plan?",
             "Scanning, every category and the estimate of how much space you can free are free. On the free plan you can delete items one at a time, up to {quota} MB in total; reinstalling the app does not reset this quota. Unlimited deletion, bulk selection and “delete all”, video shrinking and automatic best shot are part of Pro."),
            ("Is there a free trial?",
             "The yearly plan includes a {trial}-day free trial. Unless you cancel at least 24 hours before the trial ends, the subscription starts automatically at the yearly price. Prices are shown in your local currency on the purchase screen in the app."),
            ("How do I manage or cancel my subscription?",
             "In the app, open the {premiumTab} tab and tap <em>{manage}</em>, or go to {subsPath}. Subscriptions renew automatically unless canceled at least 24 hours before the end of the current period."),
            ("I bought Pro but it isn't active.",
             "Tap <em>{restore}</em> in the {premiumTab} tab. Make sure you are signed in with the same Apple Account you used to buy."),
            ("How can I get a refund?",
             "Payments are handled by Apple, so refunds are requested from Apple at <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>."),
            ("I deleted items but my free space didn't grow.",
             "iOS keeps deleted items in “{recentlyDeleted}” for 30 days; the space comes back once that album is emptied. In the Photos app, scroll down to {utilities}, tap “{recentlyDeleted}” and delete all. In the app, {premiumTab} › <em>{guide}</em> walks you through it. Apple only allows you to empty this album yourself."),
            ("What happens if iCloud Photos is on?",
             "An item you delete in Cullo is also removed from your iPad, Mac and iCloud.com signed in to the same Apple Account. With “Optimize iPhone Storage” on, some originals are only in iCloud; deleting them frees iCloud storage, not space on the iPhone. Cullo shows the two amounts separately."),
            ("Photos that aren't similar are in the same group.",
             "Open the group and choose <em>{notSimilar}</em>; it stays hidden in later scans too. You can bring hidden groups back with {premiumTab} › <em>{showHidden}</em>."),
            ("Some of my similar photos weren't found.",
             "Similar photos are looked for among shots taken within a few minutes of each other; similar shots taken on different days aren't grouped. The duplicates section finds byte-identical files only. Originals stored only in iCloud aren't analyzed. If you've taken new photos, tap <em>{rescan}</em> on the Overview tab."),
            ("How does video shrinking work?",
             "Videos are re-encoded to HD (720p) in HEVC; HDR videos stay HDR. You compare the old and new version before anything is deleted; when you accept, the new version is saved with the original's date, location, favorite and albums, and the original goes to “{recentlyDeleted}”. Slo-mo and Cinematic videos, and videos whose original is only in iCloud, aren't offered. <em>{shrinkAll}</em> prepares every video and saves them with a single confirmation."),
            ("Only some of my photos are scanned.",
             "If you chose “Limit Access” when granting permission, Cullo can only see the items you selected. To scan your whole library, choose “Full Access” in {photosPrivacyPath} › Cullo."),
            ("How do I add the widget?",
             "Touch and hold an empty area of your Home Screen, tap Edit › Add Widget and choose Cullo. The widget shows your free space and how much you can clean; it's also available on the Lock Screen."),
        ],
    ),
    "de": dict(
        name="Deutsch",
        premiumTab="Premium", restore="Käufe wiederherstellen", manage="Abo verwalten",
        guide="„Zuletzt gelöscht“ leeren – Anleitung", showHidden="Ausgeblendete Gruppen zeigen",
        notSimilar="Nicht ähnlich – Gruppe ausblenden", rescan="Erneut scannen", shrinkAll="Alle nacheinander verkleinern",
        recentlyDeleted="Zuletzt gelöscht", utilities="Sonstiges",
        subsPath="Einstellungen › [dein Name] › Abonnements", photosPrivacyPath="Einstellungen › Datenschutz & Sicherheit › Fotos",
        updated="Zuletzt aktualisiert: 8. November 2026",
        privacy="Datenschutzerklärung", support="Support", languages="Sprachen",
        p_title="Cullo Datenschutzerklärung",
        p_intro="Cullo ist eine iOS-App, die doppelte und ähnliche Fotos, Serienaufnahmen, Bildschirmfotos und große Videos auf deinem iPhone findet und dir hilft, Speicherplatz freizugeben. Diese Seite erklärt, welche Daten die App verwendet, wo sie gespeichert werden und wie.",
        h_collect="Welche Daten wir erheben",
        collect="Keine. Cullo hat keine Server, keine Konten und keine Analyse- oder Werbetools, und wir tracken dich nie. Deine Fotos, Videos und Analyseergebnisse verlassen nie dein Gerät – wir können sie nicht sehen. Die einzige Ausnahme ist, wenn du uns selbst eine E-Mail schreibst (siehe unten).",
        h_photos="Deine Fotomediathek",
        photos_read="<strong>Analyse:</strong> Wenn du den Zugriff erlaubst, analysiert Cullo deine Fotos und Videos nur auf deinem iPhone: Exakte Duplikate werden per Datei-Hash (SHA-256) gefunden, ähnliche Aufnahmen, Schärfe, offene Augen und Gesichtsqualität mit Apples Vision-Framework. Für die Analyse werden nur Dateien gelesen, die auf dem Gerät liegen; Originale, die nur in iCloud sind, werden dafür nicht geladen.",
        photos_view="<strong>Ansehen:</strong> Wenn du ein Foto im Vollbild öffnest oder ein Video abspielst, dessen Original nur in iCloud liegt, lädt iOS es von Apples Servern. Das übernimmt Apple, genau wie in der Fotos-App – nie über unsere Server.",
        photos_delete="<strong>Löschen:</strong> Cullo löscht nie etwas von sich aus. Ausgewählte Objekte kommen erst nach deiner Bestätigung und einer weiteren Rückfrage von iOS in „{recentlyDeleted}“ und bleiben dort 30 Tage. Ist iCloud-Fotos aktiv, gilt das Löschen für alle Geräte mit demselben Apple Account.",
        photos_shrink="<strong>Videos verkleinern:</strong> Das Verkleinern geschieht auf deinem Gerät. Die neue Version wird zuerst als temporäre Datei erstellt; wenn du sie übernimmst, wird sie in deiner Mediathek gespeichert und das Original kommt in „{recentlyDeleted}“. Nicht übernommene temporäre Dateien werden gelöscht.",
        h_device="Auf deinem Gerät gespeicherte Daten",
        dev_results="<strong>Scan-Ergebnisse:</strong> Die Gruppen deines letzten Scans werden nur als Foto-Kennungen (ohne Bildinhalt) im eigenen Speicher der App abgelegt, damit die Ergebnisse ohne neuen Scan erscheinen. Dateigrößen und Qualitätswerte werden zur Beschleunigung zwischengespeichert.",
        dev_prefs="<strong>Einstellungen:</strong> Gruppen, die du mit „Nicht ähnlich“ ausblendest, und die Liste der Videos, die sich nicht verkleinern ließen, werden auf deinem Gerät gespeichert.",
        dev_widget="<strong>Widget und Statistik:</strong> Eine Speicherübersicht, der aufräumbare Platz und deine Aufräum-Statistik (Anzahl gelöschter Objekte und gewonnener Platz) liegen im gemeinsamen Container der App, damit das Widget sie anzeigen kann. Das sind nur Zahlen – keine Fotos oder Kennungen.",
        dev_quota="<strong>Gratis-Kontingent:</strong> Wie viel du im kostenlosen Plan gelöscht hast (eine einzelne Zahl), wird im Schlüsselbund deines Geräts gespeichert, damit eine Neuinstallation das Kontingent nicht zurücksetzt. Sie enthält keine personenbezogenen Daten und verlässt dein Gerät nie.",
        h_feedback="Kontakt per E-Mail",
        p_feedback="Wenn du uns eine E-Mail schreibst, verwenden wir deine E-Mail-Adresse und Nachricht nur zum Antworten und geben sie nie weiter.",
        h_purchases="Käufe",
        purchases="Pro-Abos werden von Apple über den App Store abgewickelt. Wir haben keinen Zugriff auf deine Zahlungsdaten. Du kannst dein Abo unter {subsPath} verwalten oder kündigen.",
        h_delete="Daten löschen",
        delete="Beim Löschen der App werden Scan-Ergebnisse, Zwischenspeicher, Einstellungen und Statistik von deinem Gerät entfernt. Die Zahl für dein genutztes Gratis-Kontingent bleibt im Schlüsselbund, damit eine Neuinstallation es nicht zurücksetzt. Den Zugriff von Cullo auf deine Fotomediathek kannst du jederzeit unter {photosPrivacyPath} entziehen.",
        h_children="Kinder",
        children="Die App erhebt wissentlich keine Daten von Kindern – sie erhebt von niemandem personenbezogene Daten.",
        h_changes="Änderungen",
        changes="Wenn sich diese Erklärung ändert, wird die neue Fassung mit neuem Datum auf dieser Seite veröffentlicht.",
        h_contact="Kontakt",
        p_contact="Fragen zum Datenschutz: {mail}",
        s_title="Cullo Support",
        s_intro="Du hast eine Frage, einen Fehler gefunden oder eine Idee? Schreib uns – wir lesen jede Nachricht.",
        s_contact="E-Mail: {mail}. Wenn du deine iOS-Version, dein iPhone-Modell und eine kurze Beschreibung des Problems angibst, können wir dir schneller helfen.",
        h_faq="Häufige Fragen",
        faq=[
            ("Was ist im kostenlosen Plan enthalten?",
             "Scannen, alle Kategorien und die Schätzung, wie viel Platz du freigeben kannst, sind kostenlos. Im kostenlosen Plan kannst du Objekte einzeln löschen, insgesamt bis zu {quota} MB; eine Neuinstallation setzt dieses Kontingent nicht zurück. Unbegrenztes Löschen, Mehrfachauswahl und „Alle löschen“, Video-Verkleinerung und automatisches Bestbild sind Teil von Pro."),
            ("Gibt es eine kostenlose Testphase?",
             "Das Jahresabo enthält eine {trial}-tägige kostenlose Testphase. Wenn du nicht mindestens 24 Stunden vor ihrem Ende kündigst, beginnt das Abo automatisch zum Jahrespreis. Die Preise siehst du in deiner Landeswährung auf dem Kaufbildschirm der App."),
            ("Wie verwalte oder kündige ich mein Abo?",
             "Öffne in der App den Tab {premiumTab} und tippe auf <em>{manage}</em>, oder gehe zu {subsPath}. Abos verlängern sich automatisch, wenn sie nicht mindestens 24 Stunden vor Ende des Zeitraums gekündigt werden."),
            ("Ich habe Pro gekauft, aber es ist nicht aktiv.",
             "Tippe im Tab {premiumTab} auf <em>{restore}</em>. Achte darauf, mit demselben Apple Account angemeldet zu sein, mit dem du gekauft hast."),
            ("Wie bekomme ich eine Rückerstattung?",
             "Zahlungen wickelt Apple ab, daher beantragst du Rückerstattungen bei Apple unter <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>."),
            ("Ich habe gelöscht, aber der freie Speicher ist nicht gewachsen.",
             "iOS behält gelöschte Objekte 30 Tage in „{recentlyDeleted}“; der Platz wird frei, sobald dieses Album geleert ist. Scrolle in der Fotos-App zu {utilities}, tippe auf „{recentlyDeleted}“ und lösche alles. In der App zeigt dir {premiumTab} › <em>{guide}</em> die Schritte. Apple erlaubt nur dir selbst, dieses Album zu leeren."),
            ("Was passiert, wenn iCloud-Fotos aktiv ist?",
             "Ein in Cullo gelöschtes Objekt wird auch von iPad, Mac und iCloud.com mit demselben Apple Account entfernt. Mit „iPhone-Speicher optimieren“ liegen manche Originale nur in iCloud; sie zu löschen gibt iCloud-Speicher frei, nicht Platz auf dem iPhone. Cullo zeigt beide Mengen getrennt an."),
            ("Nicht ähnliche Fotos sind in derselben Gruppe.",
             "Öffne die Gruppe und wähle <em>{notSimilar}</em>; sie bleibt auch bei späteren Scans ausgeblendet. Mit {premiumTab} › <em>{showHidden}</em> holst du ausgeblendete Gruppen zurück."),
            ("Einige ähnliche Fotos wurden nicht gefunden.",
             "Ähnliche Fotos werden unter Aufnahmen gesucht, die innerhalb weniger Minuten entstanden sind; ähnliche Aufnahmen von verschiedenen Tagen werden nicht gruppiert. Der Bereich Duplikate findet nur bytegleiche Dateien. Originale, die nur in iCloud liegen, werden nicht analysiert. Wenn du neue Fotos gemacht hast, tippe in der Übersicht auf <em>{rescan}</em>."),
            ("Wie funktioniert das Verkleinern von Videos?",
             "Videos werden in HEVC auf HD (720p) neu kodiert; HDR bleibt HDR. Vor dem Löschen vergleichst du alte und neue Version; wenn du übernimmst, wird die neue Version mit Datum, Ort, Favorit und Alben des Originals gespeichert und das Original kommt in „{recentlyDeleted}“. Zeitlupen- und Kinomodus-Videos sowie Videos, deren Original nur in iCloud liegt, werden nicht angeboten. <em>{shrinkAll}</em> bereitet alle Videos vor und speichert sie mit einer einzigen Bestätigung."),
            ("Es werden nur manche meiner Fotos gescannt.",
             "Wenn du beim Erlauben „Zugriff beschränken“ gewählt hast, sieht Cullo nur die ausgewählten Objekte. Um die ganze Mediathek zu scannen, wähle „Voller Zugriff“ unter {photosPrivacyPath} › Cullo."),
            ("Wie füge ich das Widget hinzu?",
             "Lege den Finger auf eine freie Stelle des Home-Bildschirms, tippe auf Bearbeiten › Widget hinzufügen und wähle Cullo. Das Widget zeigt freien Speicher und aufräumbaren Platz; es ist auch für den Sperrbildschirm verfügbar."),
        ],
    ),
    "es": dict(
        name="Español",
        premiumTab="Premium", restore="Restaurar compras", manage="Gestionar suscripción",
        guide="Vaciar Eliminado: guía", showHidden="Mostrar grupos ocultos",
        notSimilar="No son similares — ocultar grupo", rescan="Volver a analizar", shrinkAll="Reducir todos, uno a uno",
        recentlyDeleted="Eliminado", utilities="Utilidades",
        subsPath="Ajustes › [tu nombre] › Suscripciones", photosPrivacyPath="Ajustes › Privacidad y seguridad › Fotos",
        updated="Última actualización: 8 de noviembre de 2026",
        privacy="Política de privacidad", support="Soporte", languages="Idiomas",
        p_title="Política de privacidad de Cullo",
        p_intro="Cullo es una app para iOS que encuentra fotos duplicadas y similares, ráfagas, capturas de pantalla y vídeos grandes en tu iPhone y te ayuda a liberar espacio. Esta página explica qué datos usa la app, dónde se guardan y cómo.",
        h_collect="Datos que recopilamos",
        collect="Ninguno. Cullo no tiene servidores, cuentas ni herramientas de analítica o publicidad, y nunca te rastreamos. Tus fotos, vídeos y resultados de análisis nunca salen de tu dispositivo; no podemos verlos. La única excepción es si decides escribirnos un correo (ver más abajo).",
        h_photos="Tu fototeca",
        photos_read="<strong>Análisis:</strong> Cuando das acceso, Cullo analiza tus fotos y vídeos solo en tu iPhone: encuentra duplicados exactos con un hash del archivo (SHA-256), y fotos similares, nitidez, ojos abiertos y calidad del rostro con el framework Vision de Apple. Para el análisis solo se leen los archivos guardados en el dispositivo; los originales que están solo en iCloud no se descargan para ello.",
        photos_view="<strong>Visualización:</strong> Cuando abres una foto a pantalla completa o reproduces un vídeo cuyo original está solo en iCloud, iOS lo obtiene de los servidores de Apple. Lo hace Apple, igual que en la app Fotos; nunca a través de nuestros servidores.",
        photos_delete="<strong>Eliminación:</strong> Cullo nunca elimina nada por su cuenta. Los elementos que eliges pasan a “{recentlyDeleted}” solo después de que lo confirmes y de que iOS vuelva a preguntar, y se quedan ahí 30 días. Si Fotos en iCloud está activado, la eliminación se aplica a todos tus dispositivos con el mismo Apple Account.",
        photos_shrink="<strong>Reducir vídeos:</strong> La reducción se hace en tu dispositivo. La nueva versión se prepara primero como archivo temporal; si la aceptas, se guarda en tu fototeca y el original pasa a “{recentlyDeleted}”. Los archivos temporales que no aceptas se eliminan.",
        h_device="Datos guardados en tu dispositivo",
        dev_results="<strong>Resultados del escaneo:</strong> Los grupos de tu último escaneo se guardan en el almacenamiento propio de la app solo como identificadores de fotos (sin contenido de imagen), para que los resultados aparezcan sin volver a escanear. Los tamaños de archivo y las puntuaciones de calidad también se guardan en caché para ir más rápido.",
        dev_prefs="<strong>Preferencias:</strong> Los grupos que ocultas con “No son similares” y la lista de vídeos que no se pudieron reducir se guardan en tu dispositivo.",
        dev_widget="<strong>Widget y estadísticas:</strong> Un resumen del almacenamiento, el espacio que puedes limpiar y tus estadísticas de limpieza (número de elementos eliminados y espacio recuperado) se guardan en el contenedor compartido de la app para que el widget pueda mostrarlos. Son solo números: ni fotos ni identificadores.",
        dev_quota="<strong>Cuota gratuita:</strong> Lo que has eliminado en el plan gratuito (un único número) se guarda en el Llavero de tu dispositivo, para que reinstalar la app no reinicie la cuota. No contiene datos personales y nunca sale de tu dispositivo.",
        h_feedback="Contacto por correo",
        p_feedback="Si nos escribes, usamos tu dirección de correo y tu mensaje solo para responderte y nunca los compartimos.",
        h_purchases="Compras",
        purchases="Apple procesa las suscripciones Pro a través del App Store. No tenemos acceso a tus datos de pago. Puedes gestionar o cancelar tu suscripción en {subsPath}.",
        h_delete="Eliminar tus datos",
        delete="Al eliminar la app se borran de tu dispositivo los resultados del escaneo, la caché, las preferencias y las estadísticas. El número que registra la cuota gratuita usada se queda en el Llavero para que reinstalar no la reinicie. Puedes quitar a Cullo el acceso a tu fototeca en cualquier momento en {photosPrivacyPath}.",
        h_children="Niños",
        children="La app no recopila datos de niños de forma consciente; no recopila datos personales de nadie.",
        h_changes="Cambios",
        changes="Si esta política cambia, la versión actualizada se publicará en esta página con una nueva fecha.",
        h_contact="Contacto",
        p_contact="Preguntas sobre privacidad: {mail}",
        s_title="Soporte de Cullo",
        s_intro="¿Tienes una pregunta, encontraste un error o tienes una idea? Escríbenos: leemos todos los mensajes.",
        s_contact="Correo: {mail}. Si incluyes tu versión de iOS, el modelo de iPhone y una breve descripción del problema, podremos ayudarte más rápido.",
        h_faq="Preguntas frecuentes",
        faq=[
            ("¿Qué incluye el plan gratuito?",
             "El escaneo, todas las categorías y la estimación del espacio que puedes liberar son gratis. En el plan gratuito puedes eliminar elementos de uno en uno, hasta {quota} MB en total; reinstalar la app no reinicia esta cuota. El borrado ilimitado, la selección múltiple y “eliminar todo”, la reducción de vídeos y la mejor foto automática forman parte de Pro."),
            ("¿Hay prueba gratuita?",
             "El plan anual incluye una prueba gratuita de {trial} días. Si no cancelas al menos 24 horas antes de que termine, la suscripción empieza automáticamente con el precio anual. Los precios se muestran en tu moneda local en la pantalla de compra de la app."),
            ("¿Cómo gestiono o cancelo mi suscripción?",
             "En la app, abre la pestaña {premiumTab} y toca <em>{manage}</em>, o ve a {subsPath}. Las suscripciones se renuevan automáticamente salvo que se cancelen al menos 24 horas antes del final del periodo."),
            ("Compré Pro pero no se activó.",
             "Toca <em>{restore}</em> en la pestaña {premiumTab}. Asegúrate de haber iniciado sesión con el mismo Apple Account con el que compraste."),
            ("¿Cómo pido un reembolso?",
             "Apple gestiona los pagos, así que los reembolsos se solicitan a Apple en <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>."),
            ("Eliminé elementos pero el espacio libre no aumentó.",
             "iOS guarda los elementos eliminados en “{recentlyDeleted}” durante 30 días; el espacio vuelve cuando se vacía ese álbum. En la app Fotos, desplázate a {utilities}, toca “{recentlyDeleted}” y elimínalo todo. En la app, {premiumTab} › <em>{guide}</em> te guía paso a paso. Apple solo te permite vaciar este álbum a ti."),
            ("¿Qué pasa si Fotos en iCloud está activado?",
             "Un elemento que eliminas en Cullo también desaparece del iPad, el Mac e iCloud.com con el mismo Apple Account. Con “Optimizar almacenamiento del iPhone”, algunos originales están solo en iCloud; eliminarlos libera almacenamiento de iCloud, no espacio en el iPhone. Cullo muestra las dos cantidades por separado."),
            ("Hay fotos que no se parecen en el mismo grupo.",
             "Abre el grupo y elige <em>{notSimilar}</em>; seguirá oculto en escaneos posteriores. Puedes recuperar los grupos ocultos con {premiumTab} › <em>{showHidden}</em>."),
            ("Algunas fotos similares no aparecieron.",
             "Las fotos similares se buscan entre las tomadas con pocos minutos de diferencia; las fotos parecidas de días distintos no se agrupan. La sección de duplicados solo encuentra archivos idénticos byte a byte. Los originales que están solo en iCloud no se analizan. Si has hecho fotos nuevas, toca <em>{rescan}</em> en Resumen."),
            ("¿Cómo funciona la reducción de vídeos?",
             "Los vídeos se recodifican a HD (720p) en HEVC; el HDR se mantiene. Comparas la versión antigua y la nueva antes de eliminar nada; al aceptar, la nueva se guarda con la fecha, la ubicación, el favorito y los álbumes del original, y el original pasa a “{recentlyDeleted}”. No se ofrecen los vídeos a cámara lenta, en modo Cine ni aquellos cuyo original está solo en iCloud. <em>{shrinkAll}</em> prepara todos los vídeos y los guarda con una sola confirmación."),
            ("Solo se escanean algunas de mis fotos.",
             "Si elegiste “Limitar acceso” al dar permiso, Cullo solo ve los elementos seleccionados. Para escanear toda la fototeca, elige “Acceso total” en {photosPrivacyPath} › Cullo."),
            ("¿Cómo añado el widget?",
             "Mantén pulsada una zona vacía de la pantalla de inicio, toca Editar › Añadir widget y elige Cullo. El widget muestra el espacio libre y cuánto puedes limpiar; también está disponible en la pantalla bloqueada."),
        ],
    ),
}
for _t in L.values():
    _t["quota"] = QUOTA_MB
    _t["trial"] = TRIAL_DAYS

STYLE = """\
  body { font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; max-width: 720px; margin: 0 auto; padding: 24px 16px; color: #1c1c1e; background: #fff; }
  h1 { font-size: 1.6em; } h2 { font-size: 1.2em; margin-top: 1.6em; } h3 { font-size: 1em; margin: 1.4em 0 .2em; }
  nav, footer { font-size: .9em; color: #6e6e73; } nav a, footer a { margin-inline-end: .8em; white-space: nowrap; }
  footer { margin-top: 48px; padding-top: 16px; border-top: 1px solid #ddd; }
  @media (prefers-color-scheme: dark) { body { color: #f2f2f7; background: #000; } a { color: #64b5ff; } nav, footer { color: #98989d; } footer { border-color: #333; } }"""


def fill(t, s):
    return s.format(**t, mail=f'<a href="mailto:{EMAIL}">{EMAIL}</a>')


def page(code, kind, title, body):
    t = L[code]
    other = "support" if kind == "privacy" else "privacy"
    langs = " ".join(
        f'<a href="../{c}/{kind}.html" hreflang="{c}" lang="{c}">{escape(L[c]["name"])}</a>' for c in L if c != code
    )
    alternates = "\n".join(f'<link rel="alternate" hreflang="{c}" href="../{c}/{kind}.html">' for c in L)
    return f"""<!doctype html>
<html lang="{code}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
{alternates}
<style>
{STYLE}
</style>
</head>
<body>

<h1>{escape(title)}</h1>
<p>{t["updated"]}</p>

{body}

<footer>
<p><a href="{other}.html">{t[other]}</a></p>
<p>{t["languages"]}: {langs}</p>
</footer>

</body>
</html>
"""


def privacy(code):
    t = L[code]
    f = lambda s: fill(t, s)
    body = f"""<p>{f(t["p_intro"])}</p>

<h2>{t["h_collect"]}</h2>
<p>{f(t["collect"])}</p>

<h2>{t["h_photos"]}</h2>
<ul>
  <li>{f(t["photos_read"])}</li>
  <li>{f(t["photos_view"])}</li>
  <li>{f(t["photos_delete"])}</li>
  <li>{f(t["photos_shrink"])}</li>
</ul>

<h2>{t["h_device"]}</h2>
<ul>
  <li>{f(t["dev_results"])}</li>
  <li>{f(t["dev_prefs"])}</li>
  <li>{f(t["dev_widget"])}</li>
  <li>{f(t["dev_quota"])}</li>
</ul>

<h2>{t["h_feedback"]}</h2>
<p>{f(t["p_feedback"])}</p>

<h2>{t["h_purchases"]}</h2>
<p>{f(t["purchases"])}</p>

<h2>{t["h_delete"]}</h2>
<p>{f(t["delete"])}</p>

<h2>{t["h_children"]}</h2>
<p>{f(t["children"])}</p>

<h2>{t["h_changes"]}</h2>
<p>{f(t["changes"])}</p>

<h2>{t["h_contact"]}</h2>
<p>{f(t["p_contact"])}</p>"""
    return page(code, "privacy", t["p_title"], body)


def support(code):
    t = L[code]
    f = lambda s: fill(t, s)
    faq = "\n\n".join(f"<h3>{f(q)}</h3>\n<p>{f(a)}</p>" for q, a in t["faq"])
    body = f"""<p>{f(t["s_intro"])}</p>

<h2>{t["h_contact"]}</h2>
<p>{f(t["s_contact"])}</p>

<h2>{t["h_faq"]}</h2>

{faq}"""
    return page(code, "support", t["s_title"], body)


def chooser(kind):
    """cullo/<kind>.html: tarayıcı diline uygun sayfaya yönlendirir, bulamazsa İngilizceye; JS yoksa dil listesi."""
    codes = list(L)
    links = "\n".join(
        f'  <li><a href="{c}/{kind}.html" hreflang="{c}" lang="{c}">{escape(L[c]["name"])} – {escape(L[c][kind])}</a></li>'
        for c in codes
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{APP} – {L["en"][kind]}</title>
<script>
(function () {{
  var codes = {codes!r};
  var prefs = navigator.languages || [navigator.language || "en"];
  for (var i = 0; i < prefs.length; i++) {{
    var p = prefs[i].toLowerCase();
    for (var j = 0; j < codes.length; j++) {{
      var c = codes[j].toLowerCase();
      if (p === c || p.split("-")[0] === c.split("-")[0]) {{ location.replace(codes[j] + "/{kind}.html"); return; }}
    }}
  }}
  location.replace("en/{kind}.html");
}})();
</script>
<style>
{STYLE}
</style>
</head>
<body>
<h1>{APP}</h1>
<ul>
{links}
</ul>
</body>
</html>
"""


if __name__ == "__main__":
    for code in L:
        d = OUT / code
        d.mkdir(parents=True, exist_ok=True)
        (d / "privacy.html").write_text(privacy(code), encoding="utf-8")
        (d / "support.html").write_text(support(code), encoding="utf-8")
    for kind in ("privacy", "support"):
        (OUT / f"{kind}.html").write_text(chooser(kind), encoding="utf-8")
    print(f"{len(L)} dil × 2 sayfa yazıldı → {OUT}")
