[app]

title = Погода
package.name = weather
package.domain = com.ferki

source.dir = .
source.main = weather.py
source.include_exts = py,png,jpg,kv,atlas,ttf,json,svg,txt

version = 1.0.0

# ОНОВЛЕНО: Повний список залежностей для requests/cryptography
requirements = python3,kivy==2.2.1,kivymd==1.1.1,requests,geocoder,cffi,cryptography,openssl,hostpython3,setuptools,six,certifi,idna,charset-normalizer

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


# >>>>>> КРИТИЧНЕ ВИПРАВЛЕННЯ ДЛЯ ЛОГІВ ТА КОМПІЛЯЦІЇ <<<<<<<
# 1. log_level = 2: Увімкне повний детальний лог, як вимагає Buildozer.
# 2. p4a.ndk_api = 33: Виправить проблему лінкеру (link error) з OpenSSL/Cryptography.
log_level = 0
p4a.ndk_target_api = 33
p4a.ndk_api = 33
