[app]

title = Погода
package.name = weather
package.domain = com.ferki

source.dir = .
source.main = weather.py
source.include_exts = py,png,jpg,kv,atlas,ttf,json,svg,txt

version = 1.0.0

# ОНОВЛЕНО: Додано cffi та cryptography.
# Це критично важливо для успішної компіляції глибоких залежностей requests (SSL/TLS)
# як Android-рецептів, а не через pip.
requirements = python3,kivy==2.2.1,kivymd==1.1.1,requests,geocoder,cffi,cryptography

# Додайте сюди інші необхідні дозволи, якщо вони є.
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION

android.minapi = 21
android.targetapi = 33
android.api = 33
android.maxsdk = 34

# ВАЖЛИВО: p4a вимагає NDK >= 25
android.ndk = 25b
android.build_tools_version = 34.0.0

# Сучасна конфігурація архітектур
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
