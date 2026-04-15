[app]

# (str) Title of your application
title = Census 2026

# (str) Package name
package.name = census_hamiti_rifi

# (str) Package domain (needed for android packaging)
package.domain = org.nassim

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf

# (list) Application requirements
# تم إضافة كافة المكتبات الموجودة في كودك لضمان التوافق
requirements = python3,kivy==2.3.0,pandas,openpyxl,arabic-reshaper,python-bidi,plyer

# (str) Custom source folders for Path purposes
# source.include_dirs = assets,bin

# (str) Application versioning
version = 1.0

# (list) Permissions
# تم إضافة صلاحيات الكاميرا والتخزين المطلوبة في كودك
android.permissions = CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or external (False)
android.private_storage = True

# (str) Android entry point, default is to use start.py
android.entrypoint = org.kivy.android.PythonActivity

# (list) Pattern to exclude for the search
# android.exclude_src = *.pyc,*/__pycache__/*

# (str) Screen orientation (landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) List of service to declare
# services = NAME:ENTRYPOINT_PY

# (str) Arabic support (Explicitly allowing internal support)
android.accept_sdk_license = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1

# (str) Path to build artifacts (default is ./.buildozer)
# build_dir = ./.buildozer

# (str) Path to bin directory (default is ./bin)
# bin_dir = ./bin
