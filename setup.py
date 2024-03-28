from setuptools import setup

APP = ['gui.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'plist': {
        'iconfile': 'exam.icns',
        'CFBundleName': 'ExamsGenerator',
        'CFBundleDisplayName': 'ExamsGenerator',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleIdentifier': 'com.examsgenerator.giuseppe',
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': 'True',
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
