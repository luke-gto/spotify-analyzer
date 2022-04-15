import sys

from cx_Freeze import Executable, setup

try:
    from cx_Freeze.hooks import get_qt_plugins_paths
except ImportError:
    include_files = []
else:
    include_files = get_qt_plugins_paths("PyQt5", "platforms")

base=None

if sys.platform == 'Win32':
    base='Win32GUI'

build_exe_options = {
    "excludes": ["tkinter"],
    "include_files": include_files,
}

bdist_mac_options = {
    "bundle_name": "Test",
}

bdist_dmg_options = {
    "volume_label": "TEST",
}

executables = [Executable("main.py", base=base, target_name="Spotify_Analyzer.exe", icon="resources/images/icon.png", shortcutName="Spotify Analyzer", shortcutDir="DesktopFolder")]

setup(
    name="Spotify Analyzer",
    version="0.0.1",
    description="A buggy Spotify userdata retriever",
    options={
        "build_exe": build_exe_options,
        "bdist_mac": bdist_mac_options,
        "bdist_dmg": bdist_dmg_options,
    },
    executables=executables,
)
