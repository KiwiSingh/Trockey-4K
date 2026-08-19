from setuptools import setup

APP = ['main.py']
DATA_FILES = [
    'bounce_wall.wav', 
    'bounce_paddle.wav', 
    'freeze.wav', 
    'trockey_bgm.mp3',
    'NotoSansJP-Regular.ttf',
    'NotoSansDevanagari-Regular.ttf'
]
OPTIONS = {
    'iconfile': 'app_icon.icns', 
    'packages': ['pygame', 'turtle', 'pyglet']
}

setup(
    app=APP,
    name='Trockey 4K',
    version='2.0.0',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)