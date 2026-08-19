from setuptools import setup

APP = ['main.py']
# Tell py2app to include your audio files in the app bundle
DATA_FILES = [
    'bounce_wall.wav', 
    'bounce_paddle.wav', 
    'freeze.wav', 
    'trockey_bgm.mp3'
]
OPTIONS = {
    'iconfile': 'app_icon.icns', # The Action will generate this from your PNG
    'packages': ['pygame', 'turtle']
}

setup(
    app=APP,
    name='Trockey 4K',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)