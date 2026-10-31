#!/usr/bin/env python3
"""WaterTracker gizlilik ve destek sayfalarını 12 dilde üretir.

Metinleri bu dosyada düzenleyip çalıştırın:  python3 tools/build_watertracker.py
Çıktı: watertracker/<dil>/privacy.html ve watertracker/<dil>/support.html
"""
from html import escape
from pathlib import Path

EMAIL = "appskaplica@gmail.com"
OUT = Path(__file__).resolve().parent.parent / "watertracker"

# Uygulamadaki arayüz etiketleri (Localizable.xcstrings ile aynı) ve iOS menü yolları dile göre `L[...]` içinde.
L = {
    "tr": dict(
        name="Türkçe",
        settings="Ayarlar", manage="Aboneliği yönet", plans="Planları gör", restore="Satın alımları geri yükle",
        sync="Apple Sağlık ile eşitle", reminders="Hatırlatmalar", health="Apple Sağlık",
        subsPath="Ayarlar › [adınız] › Abonelikler", healthPath="Ayarlar › Sağlık › Veri Erişimi ve Aygıtlar",
        notifPath="Ayarlar › Bildirimler",
        updated="Son güncelleme: 31 Ekim 2026",
        privacy="Gizlilik Politikası", support="Destek", languages="Diller",
        p_title="WaterTracker Gizlilik Politikası",
        p_intro="WaterTracker, su tüketiminizi takip etmenize yardımcı olan bir iOS uygulamasıdır. Bu sayfa uygulamanın hangi verileri nasıl kullandığını açıklar.",
        h_collect="Topladığımız veriler",
        collect="Hiçbirini. WaterTracker'ın sunucusu, hesap sistemi, analitik ya da reklam aracı yoktur. Kişisel verileriniz bize veya üçüncü taraflara gönderilmez ve sizi takip etmek için kullanılmaz.",
        h_device="Cihazınızda saklanan veriler",
        dev_logs="<strong>Su kayıtları ve ayarlar</strong> (günlük hedef, bardak boyutu, hatırlatmalar, dil, görünüm, seriler ve başarımlar) yalnızca cihazınızda saklanır; uygulamanın widget'ları ve Canlı Etkinlik ile paylaşılır.",
        dev_health="<strong>{health}:</strong> İzin verirseniz, eklediğiniz su miktarları {health}'a yazılır. Uygulama Sağlık'tan hiçbir veri okumaz. Sağlık verileri reklam veya pazarlama amacıyla kullanılmaz ve kimseyle paylaşılmaz. İzni istediğiniz zaman {healthPath} bölümünden geri alabilirsiniz.",
        dev_notif="<strong>Bildirimler:</strong> Su hatırlatmaları cihazınızda yerel olarak planlanır.",
        h_purchases="Satın almalar",
        purchases="Premium abonelikler Apple tarafından App Store üzerinden işlenir. Ödeme bilgilerinize erişimimiz yoktur. Aboneliğinizi {subsPath} bölümünden yönetebilir veya iptal edebilirsiniz. Satın almalar <a href=\"https://www.apple.com/legal/privacy/\">Apple'ın gizlilik politikasına</a> tabidir.",
        h_delete="Verilerinizi silme",
        delete="Tüm veriler cihazınızda olduğu için uygulamayı silmeniz bunları da kaldırır. {health}'a yazılan kayıtları Sağlık uygulamasından silebilirsiniz.",
        h_children="Çocuklar",
        children="Uygulama çocuklardan bilerek veri toplamaz; zaten hiçbir kullanıcıdan veri toplamaz.",
        h_changes="Değişiklikler",
        changes="Bu politika değişirse güncel hâli yeni tarihiyle bu sayfada yayınlanır.",
        h_contact="İletişim",
        p_contact="Gizlilikle ilgili sorularınız için: {mail}",
        s_title="WaterTracker Destek",
        s_intro="Bir sorunuz, bulduğunuz bir hata ya da bir fikriniz mi var? Bize yazın; her mesajı okuyoruz.",
        s_contact="E-posta: {mail}. iOS sürümünüzü ve sorunu kısaca yazmanız size daha hızlı yardımcı olmamızı sağlar.",
        h_faq="Sık sorulan sorular",
        faq=[
            ("Aboneliğimi nasıl yönetir veya iptal ederim?",
             "Uygulamada {settings} › Premium › {manage} yolunu izleyin ya da {subsPath} bölümüne gidin. Abonelik, dönem bitmeden en az 24 saat önce iptal edilmezse otomatik yenilenir."),
            ("Premium satın aldım ama açılmadı.",
             "{settings} › Premium › {plans} ekranını açıp <em>{restore}</em> düğmesine dokunun. Satın alırken kullandığınız Apple Hesabı ile giriş yaptığınızdan emin olun."),
            ("Nasıl iade alabilirim?",
             "Ödemeleri Apple işlediği için iade talebi Apple'a <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a> adresinden yapılır."),
            ("Su kayıtlarım {health}'da görünmüyor.",
             "Uygulamanın {settings} ekranında <em>{sync}</em> seçeneğini açın, ardından {healthPath} bölümünde WaterTracker'a izin verildiğini kontrol edin."),
            ("Hatırlatma almıyorum.",
             "Uygulamada {settings} › {reminders} bölümünü kontrol edin ve {notifPath} bölümünde WaterTracker bildirimlerine izin verildiğinden emin olun. Etkin bir Odak modu da hatırlatmaları sessize alabilir."),
            ("Widget'ı nasıl eklerim?",
             "Ana ekranda boş bir alana dokunup basılı tutun, Düzenle › Widget Ekle'ye dokunun ve WaterTracker'ı arayın."),
            ("Verilerim yeni iPhone'a taşınır mı?",
             "Verileriniz yalnızca cihazınızda saklanır. Yeni iPhone'u iCloud ya da bilgisayar yedeğinden geri yüklediğinizde veya Hızlı Başlangıç'ı kullandığınızda taşınır."),
        ],
    ),
    "en": dict(
        name="English",
        settings="Settings", manage="Manage subscription", plans="See plans", restore="Restore purchases",
        sync="Sync with Apple Health", reminders="Reminders", health="Apple Health",
        subsPath="Settings › [your name] › Subscriptions", healthPath="Settings › Health › Data Access & Devices",
        notifPath="Settings › Notifications",
        updated="Last updated: October 31, 2026",
        privacy="Privacy Policy", support="Support", languages="Languages",
        p_title="WaterTracker Privacy Policy",
        p_intro="WaterTracker is an iOS app that helps you track how much water you drink. This page explains what data the app uses and how.",
        h_collect="Data we collect",
        collect="None. WaterTracker has no servers, accounts, analytics or advertising tools. Your personal data is never sent to us or to third parties, and it is never used to track you.",
        h_device="Data stored on your device",
        dev_logs="<strong>Water logs and settings</strong> (daily goal, glass size, reminders, language, appearance, streaks and achievements) are stored only on your device and shared with the app's widgets and Live Activity.",
        dev_health="<strong>{health}:</strong> If you grant permission, the water amounts you log are written to {health}. The app does not read any Health data. Health data is never used for advertising or marketing and is never shared. You can revoke access at any time in {healthPath}.",
        dev_notif="<strong>Notifications:</strong> Water reminders are scheduled locally on your device.",
        h_purchases="Purchases",
        purchases="Premium subscriptions are processed by Apple through the App Store. We have no access to your payment information. You can manage or cancel your subscription in {subsPath}. Purchases are subject to <a href=\"https://www.apple.com/legal/privacy/\">Apple's privacy policy</a>.",
        h_delete="Deleting your data",
        delete="Because all data lives on your device, deleting the app removes it. Entries written to {health} can be deleted in the Health app.",
        h_children="Children",
        children="The app does not knowingly collect data from children — it does not collect data from anyone.",
        h_changes="Changes",
        changes="If this policy changes, the updated version will be published on this page with a new date.",
        h_contact="Contact",
        p_contact="Questions about privacy: {mail}",
        s_title="WaterTracker Support",
        s_intro="Have a question, found a bug or have an idea? Write to us — we read every message.",
        s_contact="Email: {mail}. Including your iOS version and a short description of the problem helps us help you faster.",
        h_faq="Frequently asked questions",
        faq=[
            ("How do I manage or cancel my subscription?",
             "In the app, go to {settings} › Premium › {manage}, or open {subsPath}. Subscriptions renew automatically unless canceled at least 24 hours before the end of the current period."),
            ("I bought Premium but it isn't active.",
             "Open {settings} › Premium › {plans} and tap <em>{restore}</em>. Make sure you are signed in with the same Apple Account you used to buy."),
            ("How can I get a refund?",
             "Payments are handled by Apple, so refunds are requested from Apple at <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>."),
            ("My water isn't showing up in {health}.",
             "Turn on <em>{sync}</em> in the app's {settings}, then check that WaterTracker is allowed in {healthPath}."),
            ("I'm not getting reminders.",
             "Check {settings} › {reminders} in the app and make sure notifications for WaterTracker are allowed in {notifPath}. An active Focus can also silence reminders."),
            ("How do I add the widget?",
             "Touch and hold an empty area of your Home Screen, tap Edit › Add Widget, then search for WaterTracker."),
            ("Will my data move to a new iPhone?",
             "Your data is stored only on your device. It moves to a new iPhone when you restore from an iCloud or computer backup, or use Quick Start."),
        ],
    ),
    "de": dict(
        name="Deutsch",
        settings="Einstellungen", manage="Abo verwalten", plans="Pläne ansehen", restore="Käufe wiederherstellen",
        sync="Mit Apple Health synchronisieren", reminders="Erinnerungen", health="Apple Health",
        subsPath="Einstellungen › [dein Name] › Abonnements", healthPath="Einstellungen › Health › Datenzugriff & Geräte",
        notifPath="Einstellungen › Mitteilungen",
        updated="Zuletzt aktualisiert: 31. Oktober 2026",
        privacy="Datenschutzerklärung", support="Support", languages="Sprachen",
        p_title="WaterTracker Datenschutzerklärung",
        p_intro="WaterTracker ist eine iOS-App, mit der du festhältst, wie viel Wasser du trinkst. Diese Seite erklärt, welche Daten die App wie verwendet.",
        h_collect="Welche Daten wir erheben",
        collect="Keine. WaterTracker hat keine Server, keine Konten und keine Analyse- oder Werbetools. Deine personenbezogenen Daten werden weder an uns noch an Dritte gesendet und nie zum Tracking verwendet.",
        h_device="Auf deinem Gerät gespeicherte Daten",
        dev_logs="<strong>Wassereinträge und Einstellungen</strong> (Tagesziel, Glasgröße, Erinnerungen, Sprache, Darstellung, Serien und Erfolge) werden nur auf deinem Gerät gespeichert und mit den Widgets und der Live-Aktivität der App geteilt.",
        dev_health="<strong>{health}:</strong> Wenn du es erlaubst, werden die erfassten Wassermengen in {health} geschrieben. Die App liest keine Health-Daten. Gesundheitsdaten werden nie für Werbung oder Marketing verwendet und nie weitergegeben. Du kannst den Zugriff jederzeit unter {healthPath} widerrufen.",
        dev_notif="<strong>Mitteilungen:</strong> Erinnerungen ans Trinken werden lokal auf deinem Gerät geplant.",
        h_purchases="Käufe",
        purchases="Premium-Abos werden von Apple über den App Store abgewickelt. Wir haben keinen Zugriff auf deine Zahlungsdaten. Du kannst dein Abo unter {subsPath} verwalten oder kündigen. Käufe unterliegen der <a href=\"https://www.apple.com/legal/privacy/\">Datenschutzrichtlinie von Apple</a>.",
        h_delete="Daten löschen",
        delete="Da alle Daten auf deinem Gerät liegen, werden sie beim Löschen der App entfernt. In {health} geschriebene Einträge kannst du in der Health-App löschen.",
        h_children="Kinder",
        children="Die App erhebt wissentlich keine Daten von Kindern – sie erhebt von niemandem Daten.",
        h_changes="Änderungen",
        changes="Wenn sich diese Erklärung ändert, wird die neue Fassung mit neuem Datum auf dieser Seite veröffentlicht.",
        h_contact="Kontakt",
        p_contact="Fragen zum Datenschutz: {mail}",
        s_title="WaterTracker Support",
        s_intro="Du hast eine Frage, einen Fehler gefunden oder eine Idee? Schreib uns – wir lesen jede Nachricht.",
        s_contact="E-Mail: {mail}. Wenn du deine iOS-Version und eine kurze Beschreibung des Problems angibst, können wir dir schneller helfen.",
        h_faq="Häufige Fragen",
        faq=[
            ("Wie verwalte oder kündige ich mein Abo?",
             "Gehe in der App zu {settings} › Premium › {manage} oder öffne {subsPath}. Abos verlängern sich automatisch, wenn sie nicht mindestens 24 Stunden vor Ende des aktuellen Zeitraums gekündigt werden."),
            ("Ich habe Premium gekauft, aber es ist nicht aktiv.",
             "Öffne {settings} › Premium › {plans} und tippe auf <em>{restore}</em>. Achte darauf, mit demselben Apple Account angemeldet zu sein, mit dem du gekauft hast."),
            ("Wie bekomme ich eine Rückerstattung?",
             "Zahlungen wickelt Apple ab, daher beantragst du Rückerstattungen bei Apple unter <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>."),
            ("Mein Wasser erscheint nicht in {health}.",
             "Aktiviere <em>{sync}</em> in den {settings} der App und prüfe dann, ob WaterTracker unter {healthPath} erlaubt ist."),
            ("Ich bekomme keine Erinnerungen.",
             "Prüfe in der App {settings} › {reminders} und stelle sicher, dass Mitteilungen für WaterTracker unter {notifPath} erlaubt sind. Auch ein aktiver Fokus kann Erinnerungen stummschalten."),
            ("Wie füge ich das Widget hinzu?",
             "Lege den Finger auf eine freie Stelle des Home-Bildschirms, tippe auf Bearbeiten › Widget hinzufügen und suche nach WaterTracker."),
            ("Werden meine Daten auf ein neues iPhone übertragen?",
             "Deine Daten werden nur auf deinem Gerät gespeichert. Sie werden übertragen, wenn du das neue iPhone aus einem iCloud- oder Computer-Backup wiederherstellst oder den Schnellstart verwendest."),
        ],
    ),
    "es": dict(
        name="Español",
        settings="Ajustes", manage="Gestionar suscripción", plans="Ver planes", restore="Restaurar compras",
        sync="Sincronizar con Apple Salud", reminders="Recordatorios", health="Apple Salud",
        subsPath="Ajustes › [tu nombre] › Suscripciones", healthPath="Ajustes › Salud › Acceso a datos y dispositivos",
        notifPath="Ajustes › Notificaciones",
        updated="Última actualización: 31 de octubre de 2026",
        privacy="Política de privacidad", support="Soporte", languages="Idiomas",
        p_title="Política de privacidad de WaterTracker",
        p_intro="WaterTracker es una app para iOS que te ayuda a registrar cuánta agua bebes. Esta página explica qué datos usa la app y cómo.",
        h_collect="Datos que recopilamos",
        collect="Ninguno. WaterTracker no tiene servidores, cuentas ni herramientas de analítica o publicidad. Tus datos personales nunca se envían a nosotros ni a terceros, y nunca se usan para rastrearte.",
        h_device="Datos guardados en tu dispositivo",
        dev_logs="<strong>Los registros de agua y los ajustes</strong> (objetivo diario, tamaño del vaso, recordatorios, idioma, apariencia, rachas y logros) se guardan solo en tu dispositivo y se comparten con los widgets y la Actividad en vivo de la app.",
        dev_health="<strong>{health}:</strong> Si das permiso, las cantidades de agua que registras se escriben en {health}. La app no lee ningún dato de Salud. Los datos de salud nunca se usan para publicidad o marketing ni se comparten. Puedes retirar el acceso en cualquier momento en {healthPath}.",
        dev_notif="<strong>Notificaciones:</strong> Los recordatorios para beber agua se programan localmente en tu dispositivo.",
        h_purchases="Compras",
        purchases="Las suscripciones Premium las procesa Apple a través del App Store. No tenemos acceso a tu información de pago. Puedes gestionar o cancelar tu suscripción en {subsPath}. Las compras están sujetas a la <a href=\"https://www.apple.com/legal/privacy/\">política de privacidad de Apple</a>.",
        h_delete="Eliminar tus datos",
        delete="Como todos los datos están en tu dispositivo, al eliminar la app se eliminan también. Los registros escritos en {health} se pueden borrar desde la app Salud.",
        h_children="Menores",
        children="La app no recopila de forma consciente datos de menores; de hecho, no recopila datos de nadie.",
        h_changes="Cambios",
        changes="Si esta política cambia, la versión actualizada se publicará en esta página con una nueva fecha.",
        h_contact="Contacto",
        p_contact="Preguntas sobre privacidad: {mail}",
        s_title="Soporte de WaterTracker",
        s_intro="¿Tienes una pregunta, encontraste un error o tienes una idea? Escríbenos: leemos todos los mensajes.",
        s_contact="Correo: {mail}. Si incluyes tu versión de iOS y una breve descripción del problema, podremos ayudarte más rápido.",
        h_faq="Preguntas frecuentes",
        faq=[
            ("¿Cómo gestiono o cancelo mi suscripción?",
             "En la app, ve a {settings} › Premium › {manage}, o abre {subsPath}. Las suscripciones se renuevan automáticamente salvo que se cancelen al menos 24 horas antes del final del periodo actual."),
            ("Compré Premium pero no está activo.",
             "Abre {settings} › Premium › {plans} y toca <em>{restore}</em>. Asegúrate de haber iniciado sesión con la misma cuenta de Apple que usaste para comprar."),
            ("¿Cómo solicito un reembolso?",
             "Los pagos los gestiona Apple, así que los reembolsos se solicitan a Apple en <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>."),
            ("Mi agua no aparece en {health}.",
             "Activa <em>{sync}</em> en {settings} de la app y comprueba que WaterTracker tenga permiso en {healthPath}."),
            ("No recibo recordatorios.",
             "Revisa {settings} › {reminders} en la app y asegúrate de que las notificaciones de WaterTracker estén permitidas en {notifPath}. Un modo de concentración activo también puede silenciarlos."),
            ("¿Cómo añado el widget?",
             "Mantén pulsada una zona vacía de la pantalla de inicio, toca Editar › Añadir widget y busca WaterTracker."),
            ("¿Mis datos pasarán a un iPhone nuevo?",
             "Tus datos se guardan solo en tu dispositivo. Se transfieren cuando restauras el iPhone nuevo desde una copia de iCloud o del ordenador, o usas Inicio rápido."),
        ],
    ),
    "fr": dict(
        name="Français",
        settings="Réglages", manage="Gérer l’abonnement", plans="Voir les formules", restore="Restaurer les achats",
        sync="Synchroniser avec Apple Santé", reminders="Rappels", health="Apple Santé",
        subsPath="Réglages › [votre nom] › Abonnements", healthPath="Réglages › Santé › Accès aux données et appareils",
        notifPath="Réglages › Notifications",
        updated="Dernière mise à jour : 31 octobre 2026",
        privacy="Politique de confidentialité", support="Assistance", languages="Langues",
        p_title="Politique de confidentialité de WaterTracker",
        p_intro="WaterTracker est une app iOS qui vous aide à suivre la quantité d’eau que vous buvez. Cette page explique quelles données l’app utilise et comment.",
        h_collect="Données que nous collectons",
        collect="Aucune. WaterTracker n’a ni serveur, ni compte, ni outil d’analyse ou de publicité. Vos données personnelles ne nous sont jamais envoyées, ni à des tiers, et ne servent jamais à vous suivre.",
        h_device="Données stockées sur votre appareil",
        dev_logs="<strong>Les relevés d’eau et les réglages</strong> (objectif quotidien, taille du verre, rappels, langue, apparence, séries et succès) sont stockés uniquement sur votre appareil et partagés avec les widgets et l’Activité en direct de l’app.",
        dev_health="<strong>{health} :</strong> si vous l’autorisez, les quantités d’eau saisies sont enregistrées dans {health}. L’app ne lit aucune donnée de Santé. Les données de santé ne sont jamais utilisées à des fins publicitaires ou marketing ni partagées. Vous pouvez retirer l’accès à tout moment dans {healthPath}.",
        dev_notif="<strong>Notifications :</strong> les rappels d’hydratation sont programmés localement sur votre appareil.",
        h_purchases="Achats",
        purchases="Les abonnements Premium sont traités par Apple via l’App Store. Nous n’avons pas accès à vos informations de paiement. Vous pouvez gérer ou résilier votre abonnement dans {subsPath}. Les achats sont soumis à la <a href=\"https://www.apple.com/legal/privacy/\">politique de confidentialité d’Apple</a>.",
        h_delete="Supprimer vos données",
        delete="Toutes les données étant sur votre appareil, supprimer l’app les supprime aussi. Les entrées enregistrées dans {health} peuvent être supprimées dans l’app Santé.",
        h_children="Enfants",
        children="L’app ne collecte pas sciemment de données auprès d’enfants — elle n’en collecte auprès de personne.",
        h_changes="Modifications",
        changes="Si cette politique change, la version mise à jour sera publiée sur cette page avec une nouvelle date.",
        h_contact="Contact",
        p_contact="Questions sur la confidentialité : {mail}",
        s_title="Assistance WaterTracker",
        s_intro="Une question, un bug ou une idée ? Écrivez-nous : nous lisons tous les messages.",
        s_contact="E-mail : {mail}. Indiquer votre version d’iOS et décrire brièvement le problème nous aide à vous répondre plus vite.",
        h_faq="Questions fréquentes",
        faq=[
            ("Comment gérer ou résilier mon abonnement ?",
             "Dans l’app, allez dans {settings} › Premium › {manage}, ou ouvrez {subsPath}. L’abonnement se renouvelle automatiquement s’il n’est pas résilié au moins 24 heures avant la fin de la période en cours."),
            ("J’ai acheté Premium mais il n’est pas actif.",
             "Ouvrez {settings} › Premium › {plans} et touchez <em>{restore}</em>. Vérifiez que vous êtes connecté avec le même compte Apple que lors de l’achat."),
            ("Comment obtenir un remboursement ?",
             "Les paiements sont gérés par Apple : les demandes de remboursement se font auprès d’Apple sur <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>."),
            ("Mon eau n’apparaît pas dans {health}.",
             "Activez <em>{sync}</em> dans les {settings} de l’app, puis vérifiez que WaterTracker est autorisé dans {healthPath}."),
            ("Je ne reçois pas de rappels.",
             "Vérifiez {settings} › {reminders} dans l’app et assurez-vous que les notifications de WaterTracker sont autorisées dans {notifPath}. Un mode de concentration actif peut aussi les masquer."),
            ("Comment ajouter le widget ?",
             "Maintenez le doigt sur une zone vide de l’écran d’accueil, touchez Modifier › Ajouter un widget, puis recherchez WaterTracker."),
            ("Mes données passeront-elles sur un nouvel iPhone ?",
             "Vos données sont stockées uniquement sur votre appareil. Elles sont transférées lorsque vous restaurez le nouvel iPhone depuis une sauvegarde iCloud ou ordinateur, ou utilisez Démarrage rapide."),
        ],
    ),
    "it": dict(
        name="Italiano",
        settings="Impostazioni", manage="Gestisci abbonamento", plans="Vedi i piani", restore="Ripristina acquisti",
        sync="Sincronizza con Apple Salute", reminders="Promemoria", health="Apple Salute",
        subsPath="Impostazioni › [il tuo nome] › Abbonamenti", healthPath="Impostazioni › Salute › Accesso ai dati e dispositivi",
        notifPath="Impostazioni › Notifiche",
        updated="Ultimo aggiornamento: 31 ottobre 2026",
        privacy="Informativa sulla privacy", support="Assistenza", languages="Lingue",
        p_title="Informativa sulla privacy di WaterTracker",
        p_intro="WaterTracker è un’app per iOS che ti aiuta a tenere traccia di quanta acqua bevi. Questa pagina spiega quali dati usa l’app e come.",
        h_collect="Dati che raccogliamo",
        collect="Nessuno. WaterTracker non ha server, account né strumenti di analisi o pubblicità. I tuoi dati personali non vengono mai inviati a noi o a terzi e non vengono mai usati per tracciarti.",
        h_device="Dati salvati sul tuo dispositivo",
        dev_logs="<strong>Registrazioni dell’acqua e impostazioni</strong> (obiettivo giornaliero, dimensione del bicchiere, promemoria, lingua, aspetto, serie e traguardi) sono salvate solo sul tuo dispositivo e condivise con i widget e l’Attività in tempo reale dell’app.",
        dev_health="<strong>{health}:</strong> se lo consenti, le quantità d’acqua registrate vengono scritte in {health}. L’app non legge alcun dato di Salute. I dati sanitari non vengono mai usati per pubblicità o marketing né condivisi. Puoi revocare l’accesso in qualsiasi momento in {healthPath}.",
        dev_notif="<strong>Notifiche:</strong> i promemoria per bere vengono programmati localmente sul tuo dispositivo.",
        h_purchases="Acquisti",
        purchases="Gli abbonamenti Premium sono gestiti da Apple tramite l’App Store. Non abbiamo accesso ai tuoi dati di pagamento. Puoi gestire o annullare l’abbonamento in {subsPath}. Gli acquisti sono soggetti all’<a href=\"https://www.apple.com/legal/privacy/\">informativa sulla privacy di Apple</a>.",
        h_delete="Eliminare i tuoi dati",
        delete="Poiché tutti i dati si trovano sul tuo dispositivo, eliminando l’app vengono rimossi. Le voci scritte in {health} si possono eliminare dall’app Salute.",
        h_children="Minori",
        children="L’app non raccoglie consapevolmente dati di minori: non raccoglie dati di nessuno.",
        h_changes="Modifiche",
        changes="Se questa informativa cambia, la versione aggiornata sarà pubblicata su questa pagina con una nuova data.",
        h_contact="Contatti",
        p_contact="Domande sulla privacy: {mail}",
        s_title="Assistenza WaterTracker",
        s_intro="Hai una domanda, hai trovato un bug o hai un’idea? Scrivici: leggiamo ogni messaggio.",
        s_contact="Email: {mail}. Indicare la versione di iOS e una breve descrizione del problema ci aiuta ad aiutarti più in fretta.",
        h_faq="Domande frequenti",
        faq=[
            ("Come gestisco o annullo l’abbonamento?",
             "Nell’app vai su {settings} › Premium › {manage}, oppure apri {subsPath}. L’abbonamento si rinnova automaticamente se non viene annullato almeno 24 ore prima della fine del periodo in corso."),
            ("Ho acquistato Premium ma non è attivo.",
             "Apri {settings} › Premium › {plans} e tocca <em>{restore}</em>. Assicurati di aver effettuato l’accesso con lo stesso Account Apple usato per l’acquisto."),
            ("Come ottengo un rimborso?",
             "I pagamenti sono gestiti da Apple, quindi i rimborsi si richiedono ad Apple su <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>."),
            ("La mia acqua non compare in {health}.",
             "Attiva <em>{sync}</em> nelle {settings} dell’app, poi verifica che WaterTracker sia autorizzata in {healthPath}."),
            ("Non ricevo i promemoria.",
             "Controlla {settings} › {reminders} nell’app e assicurati che le notifiche di WaterTracker siano consentite in {notifPath}. Anche una modalità Full immersion attiva può silenziarli."),
            ("Come aggiungo il widget?",
             "Tieni premuta un’area vuota della schermata Home, tocca Modifica › Aggiungi widget e cerca WaterTracker."),
            ("I miei dati passeranno a un nuovo iPhone?",
             "I tuoi dati sono salvati solo sul dispositivo. Vengono trasferiti quando ripristini il nuovo iPhone da un backup iCloud o del computer, oppure usi Avvio rapido."),
        ],
    ),
    "pt-BR": dict(
        name="Português (Brasil)",
        settings="Ajustes", manage="Gerenciar assinatura", plans="Ver planos", restore="Restaurar compras",
        sync="Sincronizar com o Apple Saúde", reminders="Lembretes", health="Apple Saúde",
        subsPath="Ajustes › [seu nome] › Assinaturas", healthPath="Ajustes › Saúde › Acesso a Dados e Dispositivos",
        notifPath="Ajustes › Notificações",
        updated="Última atualização: 31 de outubro de 2026",
        privacy="Política de Privacidade", support="Suporte", languages="Idiomas",
        p_title="Política de Privacidade do WaterTracker",
        p_intro="O WaterTracker é um app para iOS que ajuda você a acompanhar quanta água bebe. Esta página explica quais dados o app usa e como.",
        h_collect="Dados que coletamos",
        collect="Nenhum. O WaterTracker não tem servidores, contas nem ferramentas de análise ou publicidade. Seus dados pessoais nunca são enviados para nós ou para terceiros e nunca são usados para rastrear você.",
        h_device="Dados armazenados no seu dispositivo",
        dev_logs="<strong>Registros de água e ajustes</strong> (meta diária, tamanho do copo, lembretes, idioma, aparência, sequências e conquistas) ficam armazenados apenas no seu dispositivo e são compartilhados com os widgets e a Atividade ao Vivo do app.",
        dev_health="<strong>{health}:</strong> se você permitir, as quantidades de água registradas são gravadas no {health}. O app não lê nenhum dado do Saúde. Dados de saúde nunca são usados para publicidade ou marketing nem compartilhados. Você pode revogar o acesso a qualquer momento em {healthPath}.",
        dev_notif="<strong>Notificações:</strong> os lembretes para beber água são agendados localmente no seu dispositivo.",
        h_purchases="Compras",
        purchases="As assinaturas Premium são processadas pela Apple por meio da App Store. Não temos acesso às suas informações de pagamento. Você pode gerenciar ou cancelar sua assinatura em {subsPath}. As compras estão sujeitas à <a href=\"https://www.apple.com/legal/privacy/\">política de privacidade da Apple</a>.",
        h_delete="Apagar seus dados",
        delete="Como todos os dados ficam no seu dispositivo, apagar o app também os remove. Os registros gravados no {health} podem ser apagados no app Saúde.",
        h_children="Crianças",
        children="O app não coleta intencionalmente dados de crianças — ele não coleta dados de ninguém.",
        h_changes="Alterações",
        changes="Se esta política mudar, a versão atualizada será publicada nesta página com uma nova data.",
        h_contact="Contato",
        p_contact="Dúvidas sobre privacidade: {mail}",
        s_title="Suporte do WaterTracker",
        s_intro="Tem uma dúvida, encontrou um erro ou tem uma ideia? Escreva para nós — lemos todas as mensagens.",
        s_contact="E-mail: {mail}. Informar sua versão do iOS e uma breve descrição do problema nos ajuda a responder mais rápido.",
        h_faq="Perguntas frequentes",
        faq=[
            ("Como gerencio ou cancelo minha assinatura?",
             "No app, acesse {settings} › Premium › {manage}, ou abra {subsPath}. A assinatura é renovada automaticamente, a menos que seja cancelada pelo menos 24 horas antes do fim do período atual."),
            ("Comprei o Premium, mas ele não está ativo.",
             "Abra {settings} › Premium › {plans} e toque em <em>{restore}</em>. Verifique se você está conectado com a mesma Conta Apple usada na compra."),
            ("Como peço reembolso?",
             "Os pagamentos são processados pela Apple, então o reembolso é solicitado à Apple em <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>."),
            ("Minha água não aparece no {health}.",
             "Ative <em>{sync}</em> nos {settings} do app e confira se o WaterTracker tem permissão em {healthPath}."),
            ("Não estou recebendo lembretes.",
             "Confira {settings} › {reminders} no app e verifique se as notificações do WaterTracker estão permitidas em {notifPath}. Um modo de Foco ativo também pode silenciá-los."),
            ("Como adiciono o widget?",
             "Toque e mantenha pressionada uma área vazia da Tela de Início, toque em Editar › Adicionar Widget e procure por WaterTracker."),
            ("Meus dados vão para um iPhone novo?",
             "Seus dados ficam apenas no seu dispositivo. Eles são transferidos quando você restaura o iPhone novo a partir de um backup do iCloud ou do computador, ou usa o Início Rápido."),
        ],
    ),
    "ru": dict(
        name="Русский",
        settings="Настройки", manage="Управлять подпиской", plans="Посмотреть планы", restore="Восстановить покупки",
        sync="Синхронизировать с Apple Здоровье", reminders="Напоминания", health="Apple Здоровье",
        subsPath="Настройки › [ваше имя] › Подписки", healthPath="Настройки › Здоровье › Доступ к данным и устройства",
        notifPath="Настройки › Уведомления",
        updated="Последнее обновление: 31 октября 2026 г.",
        privacy="Политика конфиденциальности", support="Поддержка", languages="Языки",
        p_title="Политика конфиденциальности WaterTracker",
        p_intro="WaterTracker — приложение для iOS, которое помогает следить за тем, сколько воды вы пьёте. На этой странице описано, какие данные использует приложение и как.",
        h_collect="Какие данные мы собираем",
        collect="Никаких. У WaterTracker нет серверов, учётных записей, аналитики или рекламных инструментов. Ваши персональные данные никогда не передаются нам или третьим лицам и не используются для отслеживания.",
        h_device="Данные на вашем устройстве",
        dev_logs="<strong>Записи о воде и настройки</strong> (дневная цель, объём стакана, напоминания, язык, оформление, серии и достижения) хранятся только на вашем устройстве и доступны виджетам и Live Activity приложения.",
        dev_health="<strong>{health}:</strong> если вы разрешите, добавленное количество воды записывается в {health}. Приложение не читает никаких данных из «Здоровья». Данные о здоровье никогда не используются для рекламы или маркетинга и никому не передаются. Доступ можно отозвать в любой момент: {healthPath}.",
        dev_notif="<strong>Уведомления:</strong> напоминания о воде планируются локально на вашем устройстве.",
        h_purchases="Покупки",
        purchases="Подписки Premium обрабатывает Apple через App Store. У нас нет доступа к вашим платёжным данным. Управлять подпиской или отменить её можно здесь: {subsPath}. На покупки распространяется <a href=\"https://www.apple.com/legal/privacy/\">политика конфиденциальности Apple</a>.",
        h_delete="Удаление данных",
        delete="Все данные хранятся на вашем устройстве, поэтому при удалении приложения они тоже удаляются. Записи в {health} можно удалить в приложении «Здоровье».",
        h_children="Дети",
        children="Приложение сознательно не собирает данные детей — оно вообще ни у кого не собирает данные.",
        h_changes="Изменения",
        changes="Если политика изменится, новая версия будет опубликована на этой странице с новой датой.",
        h_contact="Контакты",
        p_contact="Вопросы о конфиденциальности: {mail}",
        s_title="Поддержка WaterTracker",
        s_intro="Есть вопрос, нашли ошибку или появилась идея? Напишите нам — мы читаем каждое сообщение.",
        s_contact="Эл. почта: {mail}. Укажите версию iOS и кратко опишите проблему — так мы поможем быстрее.",
        h_faq="Частые вопросы",
        faq=[
            ("Как управлять подпиской или отменить её?",
             "В приложении откройте {settings} › Premium › {manage} или перейдите в {subsPath}. Подписка продлевается автоматически, если не отменить её минимум за 24 часа до окончания текущего периода."),
            ("Я купил Premium, но он не активен.",
             "Откройте {settings} › Premium › {plans} и нажмите <em>{restore}</em>. Убедитесь, что вы вошли в тот же Аккаунт Apple, с которого совершали покупку."),
            ("Как вернуть деньги?",
             "Платежи обрабатывает Apple, поэтому запрос на возврат отправляется в Apple на сайте <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>."),
            ("Вода не появляется в {health}.",
             "Включите <em>{sync}</em> в разделе «{settings}» приложения и проверьте, что WaterTracker разрешён в {healthPath}."),
            ("Не приходят напоминания.",
             "Проверьте {settings} › {reminders} в приложении и убедитесь, что уведомления WaterTracker разрешены в {notifPath}. Включённый режим фокусирования тоже может их заглушать."),
            ("Как добавить виджет?",
             "Нажмите и удерживайте пустое место на экране «Домой», выберите «Изменить» › «Добавить виджет» и найдите WaterTracker."),
            ("Перенесутся ли данные на новый iPhone?",
             "Данные хранятся только на вашем устройстве. Они переносятся, если восстановить новый iPhone из резервной копии iCloud или компьютера либо воспользоваться «Быстрым началом»."),
        ],
    ),
    "ar": dict(
        name="العربية",
        settings="الإعدادات", manage="إدارة الاشتراك", plans="عرض الخطط", restore="استعادة المشتريات",
        sync="المزامنة مع Apple الصحة", reminders="التذكيرات", health="Apple الصحة",
        subsPath="الإعدادات › [اسمك] › الاشتراكات", healthPath="الإعدادات › الصحة › الوصول إلى البيانات والأجهزة",
        notifPath="الإعدادات › الإشعارات",
        updated="آخر تحديث: 31 أكتوبر 2026",
        privacy="سياسة الخصوصية", support="الدعم", languages="اللغات",
        p_title="سياسة خصوصية WaterTracker",
        p_intro="WaterTracker تطبيق لنظام iOS يساعدك على تتبّع كمية الماء التي تشربها. توضح هذه الصفحة البيانات التي يستخدمها التطبيق وكيفية استخدامها.",
        h_collect="البيانات التي نجمعها",
        collect="لا شيء. لا يملك WaterTracker خوادم أو حسابات أو أدوات تحليل أو إعلانات. لا تُرسَل بياناتك الشخصية إلينا أو إلى أي طرف ثالث، ولا تُستخدم أبدًا لتتبّعك.",
        h_device="البيانات المخزّنة على جهازك",
        dev_logs="<strong>سجلات الماء والإعدادات</strong> (الهدف اليومي، حجم الكوب، التذكيرات، اللغة، المظهر، السلاسل والإنجازات) تُخزَّن على جهازك فقط وتُشارَك مع أدوات التطبيق والنشاط المباشر.",
        dev_health="<strong>{health}:</strong> إذا منحت الإذن، تُكتب كميات الماء التي تسجّلها في {health}. لا يقرأ التطبيق أي بيانات من تطبيق الصحة. لا تُستخدم البيانات الصحية للإعلان أو التسويق ولا تُشارَك مع أحد. يمكنك سحب الإذن في أي وقت من {healthPath}.",
        dev_notif="<strong>الإشعارات:</strong> تُجدوَل تذكيرات شرب الماء محليًا على جهازك.",
        h_purchases="المشتريات",
        purchases="تعالج Apple اشتراكات Premium عبر App Store. لا يمكننا الوصول إلى معلومات الدفع الخاصة بك. يمكنك إدارة اشتراكك أو إلغاؤه من {subsPath}. تخضع المشتريات <a href=\"https://www.apple.com/legal/privacy/\">لسياسة خصوصية Apple</a>.",
        h_delete="حذف بياناتك",
        delete="بما أن جميع البيانات موجودة على جهازك، فإن حذف التطبيق يزيلها. يمكنك حذف السجلات المكتوبة في {health} من تطبيق الصحة.",
        h_children="الأطفال",
        children="لا يجمع التطبيق عن علم بيانات من الأطفال، فهو لا يجمع بيانات من أي شخص.",
        h_changes="التغييرات",
        changes="إذا تغيّرت هذه السياسة، فستُنشر النسخة المحدّثة في هذه الصفحة بتاريخ جديد.",
        h_contact="التواصل",
        p_contact="للأسئلة المتعلقة بالخصوصية: {mail}",
        s_title="دعم WaterTracker",
        s_intro="لديك سؤال أو وجدت خطأً أو لديك فكرة؟ راسلنا، فنحن نقرأ كل رسالة.",
        s_contact="البريد الإلكتروني: {mail}. يساعدنا ذكر إصدار iOS ووصف مختصر للمشكلة على مساعدتك بشكل أسرع.",
        h_faq="الأسئلة الشائعة",
        faq=[
            ("كيف أدير اشتراكي أو ألغيه؟",
             "في التطبيق انتقل إلى {settings} › Premium › {manage}، أو افتح {subsPath}. يتجدد الاشتراك تلقائيًا ما لم يُلغَ قبل 24 ساعة على الأقل من نهاية الفترة الحالية."),
            ("اشتريت Premium لكنه غير مفعّل.",
             "افتح {settings} › Premium › {plans} واضغط على <em>{restore}</em>. تأكد من تسجيل الدخول بحساب Apple نفسه الذي استخدمته للشراء."),
            ("كيف أسترد المبلغ؟",
             "تتولى Apple معالجة المدفوعات، لذا يُطلب الاسترداد من Apple عبر <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>."),
            ("لا يظهر الماء في {health}.",
             "فعّل <em>{sync}</em> في {settings} التطبيق، ثم تحقق من السماح لـ WaterTracker في {healthPath}."),
            ("لا تصلني التذكيرات.",
             "تحقق من {settings} › {reminders} في التطبيق، وتأكد من السماح بإشعارات WaterTracker في {notifPath}. قد يؤدي تفعيل وضع التركيز أيضًا إلى كتم التذكيرات."),
            ("كيف أضيف الأداة؟",
             "المس مطولًا مساحة فارغة في الشاشة الرئيسية، ثم اضغط على تعديل › إضافة أداة وابحث عن WaterTracker."),
            ("هل تنتقل بياناتي إلى iPhone جديد؟",
             "تُخزَّن بياناتك على جهازك فقط. تنتقل عند استعادة iPhone الجديد من نسخة iCloud أو الكمبيوتر الاحتياطية، أو عند استخدام البدء السريع."),
        ],
    ),
    "zh-Hans": dict(
        name="简体中文",
        settings="设置", manage="管理订阅", plans="查看方案", restore="恢复购买",
        sync="与 Apple 健康同步", reminders="提醒", health="Apple 健康",
        subsPath="设置 › [你的姓名] › 订阅", healthPath="设置 › 健康 › 数据访问与设备",
        notifPath="设置 › 通知",
        updated="最后更新：2026年10月31日",
        privacy="隐私政策", support="支持", languages="语言",
        p_title="WaterTracker 隐私政策",
        p_intro="WaterTracker 是一款帮助你记录饮水量的 iOS app。本页说明 app 使用哪些数据以及如何使用。",
        h_collect="我们收集的数据",
        collect="不收集任何数据。WaterTracker 没有服务器、账户、分析或广告工具。你的个人数据绝不会发送给我们或任何第三方，也绝不会用于追踪你。",
        h_device="存储在你设备上的数据",
        dev_logs="<strong>饮水记录和设置</strong>（每日目标、杯子容量、提醒、语言、外观、连续记录和成就）仅存储在你的设备上，并与 app 的小组件和实时活动共享。",
        dev_health="<strong>{health}：</strong>如果你授予权限，你记录的饮水量会写入{health}。app 不会读取任何健康数据。健康数据绝不会用于广告或营销，也绝不会与他人共享。你可以随时在“{healthPath}”中撤销访问权限。",
        dev_notif="<strong>通知：</strong>饮水提醒在你的设备上本地安排。",
        h_purchases="购买",
        purchases="Premium 订阅由 Apple 通过 App Store 处理。我们无法访问你的付款信息。你可以在“{subsPath}”中管理或取消订阅。购买受 <a href=\"https://www.apple.com/legal/privacy/\">Apple 隐私政策</a>约束。",
        h_delete="删除你的数据",
        delete="由于所有数据都在你的设备上，删除 app 即会删除这些数据。写入{health}的记录可以在“健康”app 中删除。",
        h_children="儿童",
        children="本 app 不会有意收集儿童的数据——它不收集任何人的数据。",
        h_changes="变更",
        changes="如本政策发生变更，更新后的版本将连同新日期发布在本页面。",
        h_contact="联系我们",
        p_contact="隐私相关问题：{mail}",
        s_title="WaterTracker 支持",
        s_intro="有问题、发现了错误或有好点子？欢迎来信，我们会阅读每一条消息。",
        s_contact="电子邮件：{mail}。附上你的 iOS 版本和问题的简要描述，能帮助我们更快地解决问题。",
        h_faq="常见问题",
        faq=[
            ("如何管理或取消订阅？",
             "在 app 中前往 {settings} › Premium › {manage}，或打开“{subsPath}”。除非在当前周期结束前至少 24 小时取消，否则订阅会自动续订。"),
            ("我购买了 Premium，但没有生效。",
             "打开 {settings} › Premium › {plans}，然后轻点<em>{restore}</em>。请确认你登录的是购买时使用的同一个 Apple 账户。"),
            ("如何申请退款？",
             "付款由 Apple 处理，因此请前往 <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a> 向 Apple 申请退款。"),
            ("饮水记录没有出现在{health}中。",
             "在 app 的{settings}中打开<em>{sync}</em>，然后在“{healthPath}”中确认已允许 WaterTracker。"),
            ("我收不到提醒。",
             "检查 app 中的 {settings} › {reminders}，并确认在“{notifPath}”中已允许 WaterTracker 的通知。开启的专注模式也可能使提醒静音。"),
            ("如何添加小组件？",
             "按住主屏幕的空白区域，轻点“编辑” › “添加小组件”，然后搜索 WaterTracker。"),
            ("我的数据会转移到新 iPhone 吗？",
             "你的数据仅存储在你的设备上。当你通过 iCloud 或电脑备份恢复新 iPhone，或使用“快速开始”时，数据会一并转移。"),
        ],
    ),
    "ja": dict(
        name="日本語",
        settings="設定", manage="サブスクリプションを管理", plans="プランを見る", restore="購入を復元",
        sync="Apple ヘルスケアと同期", reminders="リマインダー", health="Apple ヘルスケア",
        subsPath="設定 › [ユーザ名] › サブスクリプション", healthPath="設定 › ヘルスケア › データアクセスとデバイス",
        notifPath="設定 › 通知",
        updated="最終更新日：2026年10月31日",
        privacy="プライバシーポリシー", support="サポート", languages="言語",
        p_title="WaterTracker プライバシーポリシー",
        p_intro="WaterTracker は、飲んだ水の量を記録できる iOS アプリです。このページでは、アプリがどのデータをどのように使用するかを説明します。",
        h_collect="収集するデータ",
        collect="ありません。WaterTracker にはサーバ、アカウント、分析ツール、広告ツールはありません。お客様の個人データが当方や第三者に送信されることはなく、トラッキングに使われることもありません。",
        h_device="デバイスに保存されるデータ",
        dev_logs="<strong>水の記録と設定</strong>（1日の目標、グラスの容量、リマインダー、言語、外観、連続記録と実績）はお使いのデバイスにのみ保存され、アプリのウィジェットとライブアクティビティで共有されます。",
        dev_health="<strong>{health}：</strong>許可した場合、記録した水の量が{health}に書き込まれます。アプリがヘルスケアのデータを読み取ることはありません。ヘルスケアデータが広告やマーケティングに使われたり、共有されたりすることはありません。アクセスはいつでも「{healthPath}」で取り消せます。",
        dev_notif="<strong>通知：</strong>水分補給のリマインダーはデバイス上でローカルに設定されます。",
        h_purchases="購入",
        purchases="Premium サブスクリプションは App Store を通じて Apple が処理します。当方がお支払い情報にアクセスすることはありません。サブスクリプションの管理や解約は「{subsPath}」で行えます。購入には <a href=\"https://www.apple.com/legal/privacy/\">Apple のプライバシーポリシー</a>が適用されます。",
        h_delete="データの削除",
        delete="すべてのデータはデバイス上にあるため、アプリを削除するとデータも削除されます。{health}に書き込まれた記録はヘルスケア App で削除できます。",
        h_children="お子様",
        children="本アプリが故意にお子様からデータを収集することはありません。そもそも誰からもデータを収集しません。",
        h_changes="変更",
        changes="本ポリシーを変更した場合は、更新版を新しい日付とともにこのページに掲載します。",
        h_contact="お問い合わせ",
        p_contact="プライバシーに関するご質問：{mail}",
        s_title="WaterTracker サポート",
        s_intro="ご質問、不具合の報告、アイデアなどがあればお気軽にご連絡ください。すべてのメッセージに目を通しています。",
        s_contact="メール：{mail}。iOS のバージョンと問題の簡単な説明を添えていただくと、より早く対応できます。",
        h_faq="よくある質問",
        faq=[
            ("サブスクリプションの管理や解約はどうすればいいですか？",
             "アプリで {settings} › Premium › {manage} を開くか、「{subsPath}」を開いてください。現在の期間が終了する24時間前までに解約しない限り、サブスクリプションは自動更新されます。"),
            ("Premium を購入したのに有効になりません。",
             "{settings} › Premium › {plans} を開き、<em>{restore}</em>をタップしてください。購入時と同じ Apple アカウントでサインインしていることを確認してください。"),
            ("返金を受けるには？",
             "お支払いは Apple が処理しているため、返金は <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a> から Apple にリクエストしてください。"),
            ("{health}に水の記録が表示されません。",
             "アプリの{settings}で<em>{sync}</em>をオンにし、「{healthPath}」で WaterTracker が許可されているか確認してください。"),
            ("リマインダーが届きません。",
             "アプリの {settings} › {reminders} を確認し、「{notifPath}」で WaterTracker の通知が許可されていることを確認してください。集中モードがオンの場合もリマインダーが届かないことがあります。"),
            ("ウィジェットを追加するには？",
             "ホーム画面の空いている場所を長押しし、「編集」›「ウィジェットを追加」をタップして WaterTracker を検索してください。"),
            ("新しい iPhone にデータは移行されますか？",
             "データはお使いのデバイスにのみ保存されます。新しい iPhone を iCloud やコンピュータのバックアップから復元するか、クイックスタートを使用すると移行されます。"),
        ],
    ),
    "ko": dict(
        name="한국어",
        settings="설정", manage="구독 관리", plans="플랜 보기", restore="구매 복원",
        sync="Apple 건강과 동기화", reminders="알림", health="Apple 건강",
        subsPath="설정 › [사용자 이름] › 구독", healthPath="설정 › 건강 › 데이터 접근 및 기기",
        notifPath="설정 › 알림",
        updated="최종 업데이트: 2026년 10월 31일",
        privacy="개인정보 처리방침", support="지원", languages="언어",
        p_title="WaterTracker 개인정보 처리방침",
        p_intro="WaterTracker는 마신 물의 양을 기록하도록 도와주는 iOS 앱입니다. 이 페이지에서는 앱이 어떤 데이터를 어떻게 사용하는지 설명합니다.",
        h_collect="수집하는 데이터",
        collect="없습니다. WaterTracker에는 서버, 계정, 분석 도구나 광고 도구가 없습니다. 개인 데이터는 저희나 제3자에게 전송되지 않으며 사용자를 추적하는 데 사용되지 않습니다.",
        h_device="기기에 저장되는 데이터",
        dev_logs="<strong>물 기록과 설정</strong>(하루 목표, 컵 용량, 알림, 언어, 화면 모드, 연속 기록과 업적)은 기기에만 저장되며 앱의 위젯 및 실시간 현황과 공유됩니다.",
        dev_health="<strong>{health}:</strong> 권한을 허용하면 기록한 물의 양이 {health}에 저장됩니다. 앱은 건강 데이터를 읽지 않습니다. 건강 데이터는 광고나 마케팅에 사용되지 않으며 누구와도 공유되지 않습니다. 언제든지 {healthPath}에서 접근 권한을 철회할 수 있습니다.",
        dev_notif="<strong>알림:</strong> 물 마시기 알림은 기기에서 로컬로 예약됩니다.",
        h_purchases="구입",
        purchases="Premium 구독은 App Store를 통해 Apple이 처리합니다. 저희는 결제 정보에 접근할 수 없습니다. {subsPath}에서 구독을 관리하거나 취소할 수 있습니다. 구입에는 <a href=\"https://www.apple.com/legal/privacy/\">Apple의 개인정보 처리방침</a>이 적용됩니다.",
        h_delete="데이터 삭제",
        delete="모든 데이터가 기기에 있으므로 앱을 삭제하면 데이터도 삭제됩니다. {health}에 저장된 기록은 건강 앱에서 삭제할 수 있습니다.",
        h_children="아동",
        children="앱은 아동의 데이터를 고의로 수집하지 않으며, 어떤 사용자의 데이터도 수집하지 않습니다.",
        h_changes="변경 사항",
        changes="이 방침이 변경되면 새 날짜와 함께 업데이트된 내용을 이 페이지에 게시합니다.",
        h_contact="문의",
        p_contact="개인정보 관련 문의: {mail}",
        s_title="WaterTracker 지원",
        s_intro="궁금한 점이나 발견한 버그, 아이디어가 있으신가요? 메일을 보내 주세요. 모든 메시지를 읽고 있습니다.",
        s_contact="이메일: {mail}. iOS 버전과 문제에 대한 간단한 설명을 함께 보내 주시면 더 빠르게 도와드릴 수 있습니다.",
        h_faq="자주 묻는 질문",
        faq=[
            ("구독을 관리하거나 취소하려면 어떻게 하나요?",
             "앱에서 {settings} › Premium › {manage}로 이동하거나 {subsPath}을(를) 여세요. 현재 기간이 끝나기 최소 24시간 전에 취소하지 않으면 구독이 자동으로 갱신됩니다."),
            ("Premium을 구입했는데 활성화되지 않았어요.",
             "{settings} › Premium › {plans}을(를) 열고 <em>{restore}</em>을(를) 탭하세요. 구입할 때 사용한 것과 같은 Apple 계정으로 로그인했는지 확인하세요."),
            ("환불은 어떻게 받나요?",
             "결제는 Apple이 처리하므로 <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>에서 Apple에 환불을 요청하세요."),
            ("{health}에 물 기록이 표시되지 않아요.",
             "앱의 {settings}에서 <em>{sync}</em>을(를) 켠 다음, {healthPath}에서 WaterTracker가 허용되어 있는지 확인하세요."),
            ("알림이 오지 않아요.",
             "앱의 {settings} › {reminders}을(를) 확인하고 {notifPath}에서 WaterTracker 알림이 허용되어 있는지 확인하세요. 집중 모드가 켜져 있어도 알림이 울리지 않을 수 있습니다."),
            ("위젯은 어떻게 추가하나요?",
             "홈 화면의 빈 곳을 길게 누른 다음 편집 › 위젯 추가를 탭하고 WaterTracker를 검색하세요."),
            ("새 iPhone으로 데이터가 옮겨지나요?",
             "데이터는 기기에만 저장됩니다. 새 iPhone을 iCloud 또는 컴퓨터 백업에서 복원하거나 빠른 시작을 사용하면 함께 옮겨집니다."),
        ],
    ),
}

STYLE = """\
  body { font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; max-width: 720px; margin: 0 auto; padding: 24px 16px; color: #1c1c1e; background: #fff; }
  h1 { font-size: 1.6em; } h2 { font-size: 1.2em; margin-top: 1.6em; } h3 { font-size: 1em; margin: 1.4em 0 .2em; }
  nav, footer { font-size: .9em; color: #6e6e73; } nav a, footer a { margin-inline-end: .8em; white-space: nowrap; }
  footer { margin-top: 48px; padding-top: 16px; border-top: 1px solid #ddd; }
  @media (prefers-color-scheme: dark) { body { color: #f2f2f7; background: #000; } a { color: #64b5ff; } nav, footer { color: #98989d; } footer { border-color: #333; } }"""


def page(code, kind, title, body):
    t = L[code]
    other = "support" if kind == "privacy" else "privacy"
    langs = " ".join(
        f'<a href="../{c}/{kind}.html" hreflang="{c}" lang="{c}">{escape(L[c]["name"])}</a>' for c in L if c != code
    )
    alternates = "\n".join(f'<link rel="alternate" hreflang="{c}" href="../{c}/{kind}.html">' for c in L)
    direction = ' dir="rtl"' if code == "ar" else ""
    return f"""<!doctype html>
<html lang="{code}"{direction}>
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
    f = lambda s: s.format(**t, mail=f'<a href="mailto:{EMAIL}">{EMAIL}</a>')
    body = f"""<p>{f(t["p_intro"])}</p>

<h2>{t["h_collect"]}</h2>
<p>{f(t["collect"])}</p>

<h2>{t["h_device"]}</h2>
<ul>
  <li>{f(t["dev_logs"])}</li>
  <li>{f(t["dev_health"])}</li>
  <li>{f(t["dev_notif"])}</li>
</ul>

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
    f = lambda s: s.format(**t, mail=f'<a href="mailto:{EMAIL}">{EMAIL}</a>')
    faq = "\n\n".join(f"<h3>{f(q)}</h3>\n<p>{f(a)}</p>" for q, a in t["faq"])
    body = f"""<p>{f(t["s_intro"])}</p>

<h2>{t["h_contact"]}</h2>
<p>{f(t["s_contact"])}</p>

<h2>{t["h_faq"]}</h2>

{faq}"""
    return page(code, "support", t["s_title"], body)


def chooser(kind):
    """watertracker/<kind>.html: tarayıcı diline uygun sayfaya yönlendirir, bulamazsa İngilizceye; JS yoksa dil listesi."""
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
<title>WaterTracker – {L["en"][kind]}</title>
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
<h1>WaterTracker</h1>
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
