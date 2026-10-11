[app]

title = Rubika Channel Manager
package.name = rubikaleavemanager
package.domain = org.example
source.dir = .
source.include_exts = py,db,png,jpg,kv
version = 1.0.0

requirements = python3,kivy,rubpy==7.3.5

orientation = portrait
fullscreen = 0

android.permissions = INTERNET

android.api = 33
android.minapi = 23
android.archs = arm64-v8a

[buildozer]

log_level = 2
warn_on_root = 1
