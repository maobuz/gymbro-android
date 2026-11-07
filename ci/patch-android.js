// Ritocca il progetto Android generato da Capacitor: permessi e numero di versione.
const fs = require("fs");
const build = process.argv[2] || "1";

const manifestPath = "android/app/src/main/AndroidManifest.xml";
let m = fs.readFileSync(manifestPath, "utf8");
const perms = [
  '<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />',
  '<uses-permission android:name="android.permission.VIBRATE" />',
  '<uses-permission android:name="android.permission.WAKE_LOCK" />',
  '<uses-permission android:name="android.permission.SCHEDULE_EXACT_ALARM" android:maxSdkVersion="32" />',
  '<uses-permission android:name="android.permission.USE_EXACT_ALARM" />'
].filter(p => !m.includes(p.split('"')[1]));
m = m.replace("<application", perms.join("\n    ") + "\n\n    <application");
fs.writeFileSync(manifestPath, m);

const gradlePath = "android/app/build.gradle";
let g = fs.readFileSync(gradlePath, "utf8");
g = g.replace(/versionCode\s+\d+/, "versionCode " + build).replace(/versionName\s+"[^"]*"/, 'versionName "1.' + build + '"');
fs.writeFileSync(gradlePath, g);
console.log("Patch applicata: build " + build + ", permessi aggiunti: " + perms.length);

// Il testo dell'app non deve essere ingrandito una seconda volta dalla dimensione
// caratteri di sistema: la grandezza si sceglie dentro l'app (Schede -> Dimensione del testo).
const activityPath = "android/app/src/main/java/it/maobuz/gymbro/MainActivity.java";
fs.writeFileSync(activityPath, `package it.maobuz.gymbro;

import android.os.Bundle;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (this.bridge != null && this.bridge.getWebView() != null) {
            this.bridge.getWebView().getSettings().setTextZoom(100);
        }
    }
}
`);
console.log("MainActivity: zoom del testo di sistema disattivato");
