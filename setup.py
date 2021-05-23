from distutils.core import setup
import py2exe

setup(console=['parser.py'], 
options={'py2exe': {"includes": ["lxml._elementpath"]}})
