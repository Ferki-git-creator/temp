[app]

title = Погода
package.name = weather
package.domain = com.ferki

source.dir = .
source.main = weather.py
source.include_exts = py,png,jpg,kv,atlas,ttf,json,svg,txt

version = 1.0.0

# ВСІ твої залежності без урізання функціоналу:
requirements = python3,kivy==2.2.1,kivymd==1.1.1,requests,geocoder,urllib3,certifi,charset-normalizer,idna,libffi==3.4.2

android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION

android.minapi = 21
android.targetapi = 33
android.api = 33
android.maxsdk = 34

# ВАЖЛИВО: NDK >= 25 (p4a вимагає мінімум 25). 
android.ndk = 25b
android.build_tools_version = 34.0.0

# Використовуємо сучасний ключ (не deprecated)
android.archs = arm64-v8a

graphics_api = opengl_es2
orientation = portrait
fullscreen = 0
android.multitouch_enabled = 1

android.allow_root = 1
android.enable_androidx = 1

android.copy_libs = 1
android.storage = shared
android.skip_storage_check = 1

android.aidl_fix = 1
android.accept_sdk_license = true
android.auto_update = true
android.verify_certificates = true

p4a.bootstrap = sdl2
android.entrypoint = org.kivy.android.PythonActivity
android.touch_sources = weather.py

[p4a]
branch = stable
extra_requirements = openssl

[buildozer]
log_level = 2
warn_on_root = 0
warnings = 1
allow_root = 1

[app:source.exclude_patterns]
*.pyc
.git
.gitignore
build
bin
__pycache__

[app:android.manifest_extra]
# <uses-feature android:name="android.hardware.location.gps" android:required="false" />
# <uses-feature android:name="android.hardware.location.network" android:required="false" />
# <application android:usesCleartextTraffic="true" />
