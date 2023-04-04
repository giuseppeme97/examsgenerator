from setuptools import setup

APP = ['gui.py']
DATA_FILES = []
OPTIONS = {'iconfile': 'exams.icns'}
import os
os.environ['PY2APP_DEBUG'] = '1'

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
