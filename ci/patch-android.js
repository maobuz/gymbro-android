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
const appId = JSON.parse(fs.readFileSync("capacitor.config.json", "utf8")).appId;
const activityPath = "android/app/src/main/java/" + appId.split(".").join("/") + "/MainActivity.java";
fs.writeFileSync(activityPath, `package ${appId};

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

// Firma sempre con la chiave del repository, così ogni nuovo APK si installa sopra il precedente.
let g2 = fs.readFileSync(gradlePath, "utf8");
if (!g2.includes("ci/debug.keystore")) {
  g2 = g2.replace(/android\s*\{/, `android {
    signingConfigs {
        debug {
            storeFile file("\${rootDir}/../ci/debug.keystore")
            storePassword "android"
            keyAlias "androiddebugkey"
            keyPassword "android"
        }
    }`);
  fs.writeFileSync(gradlePath, g2);
}
console.log("Firma: chiave fissa da ci/debug.keystore");
