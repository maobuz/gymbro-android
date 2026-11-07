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
