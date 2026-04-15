[app]
title = Census 2026
package.name = census.hamiti.rifi
package.domain = org.nassim
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 1.0

# المكتبات المطلوبة بناءً على كودك
requirements = python3,kivy,pandas,openpyxl,arabic-reshaper,python-bidi,plyer

orientation = portrait
fullscreen = 0
android.permissions = CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1

