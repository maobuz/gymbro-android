# GymBro per Android

Diario di palestra e corsa: schede, serie e pesi, timer di recupero con notifica,
progressi, corsa, e dati Garmin letti da Home Assistant.

## Scaricare l'app
Dal telefono apri:
**https://github.com/maobuz/gymbro-android/releases/latest/download/GymBro.apk**

Installa il file (consenti "Installa app sconosciute" a Chrome; se Play Protect avvisa,
scegli "Installa comunque"). Per aggiornare, scarica e installa di nuovo: i dati restano.

## Dati Garmin
In app: Schede → Home Assistant. Inserisci l'indirizzo (es. Nabu Casa) e un token di
accesso a lunga durata (Home Assistant → Profilo → Sicurezza). Restano solo sul telefono.

## Come si compila
GitHub Actions compila a ogni push su `main` (vedi `.github/workflows/build.yml`)
e pubblica l'APK nelle Release. L'app web è in `www/index.html`.

La chiave in `ci/debug.keystore` serve solo a firmare sempre allo stesso modo,
così gli aggiornamenti si installano sopra la versione precedente.
