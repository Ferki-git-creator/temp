[app]

# Назва програми (відображається під іконкою)
title = Погода

# Унікальний ідентифікатор пакета (змініть на свій)
package.name = weather

# Домен (частина перед package.name)
package.domain = com.ferki

# Шлях до вихідних файлів
source.dir = .

# Головний файл Python
source.main = weather.py

# Версія програми
version = 1.0.0

# Включати розширення файлів
source.include_exts = py,png,jpg,kv,atlas,ttf,json,svg,txt

# Вимоги (бібліотеки Python)
requirements = python3,kivy==2.3.1,kivymd==1.2.0,requests,geocoder,urllib3,certifi,charset-normalizer,idna

# Дозволи Android
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION

# Мінімальна версія Android (5.0)
android.minapi = 21

# Цільова версія Android
android.targetapi = 33

# Версія SDK
# android.sdk = 24  # закоментував, бо викликає проблеми

# Версія NDK (дуже важливо!)
android.ndk = 25b

# Архітектури
android.arch = x86_64

# Орієнтація екрана
orientation = portrait

# Повноекранний режим
fullscreen = 0

# Включити мультітач
android.multitouch_enabled = 1

# Дозволити резервне копіювання
android.allow_backup = true

# Збереження стану при зміні конфігурації
android.retain_state_on_configuration_change = true

# Прийняти ліцензії SDK автоматично
android.accept_sdk_license = true

# Копіювання бібліотек
android.copy_libs = 1

# Сховище
android.storage = shared

# Графічний API
graphics_api = opengl_es2

# Бутстрап (СПРАВЖНЯ ЗМІНА!)
p4a.bootstrap = sdl2

# Точка входу
android.entrypoint = org.kivy.android.PythonActivity

# Версія для збірки
# buildozer android debug
# buildozer android release

# WHITELIST (якщо потрібно)
# android.whitelist =

# BLACKLIST
# android.blacklist =

# Версія Android для бібліотек
android.api = 33

# Перевірка SDK
android.skip_update = False

# Автоматичне оновлення
android.auto_update = True

# Перевірка сертифікатів
android.verify_certificates = True

# Торкнутися файлів
android.touch_sources = weather.py

# Кількість ядер для збірки
# android.num_cores = 4

# Мінімальна версія SDK для запуску
android.min_sdk_version = 21

# Версія build-tools
android.build_tools_version = 34.0.0

# Дозвіл на root
android.allow_root = 1

# Фікс для Android 12+
android.enable_androidx = 1

# Максимальна версія SDK
android.maxsdk = 34

# Дозволити старші версії SDK
android.allow_older_sdk = True

# Пропустити перевірку сховища
android.skip_storage_check = 1

# Фікс для aidl
android.aidl_fix = 1

[p4a]
# Гілка python-for-android
branch = develop

# Додаткові вимоги
extra_requirements = openssl

[buildozer]
# Рівень журналу при збірці
log_level = 2

# Попередження про root (вимкнути для вашої ситуації)
warn_on_root = 0

# Попередження
warnings = 1

# Мінімальна версія buildozer
# min_buildozer_version = 1.5.0

# Дозволити root для buildozer
allow_root = 1

# Кількість потоків для збірки
# jobs = 4

[app:source.exclude_patterns]
# Виключити непотрібні файли
*.pyc
.git
.gitignore
build
bin
__pycache__

[app:android.manifest_extra]
# Додаткові налаштування AndroidManifest.xml
# <uses-feature android:name="android.hardware.location.gps" android:required="false" />
# <uses-feature android:name="android.hardware.location.network" android:required="false" />
# <application android:usesCleartextTraffic="true" />
