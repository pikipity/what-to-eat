from distutils.core import setup
import py2exe

setup(windows=["Eat_What.py",{"script":"Eat_What.py","icon_resources":[(1,"icon\\eat.ico")]}],\
      data_files=[("data",["data\\set.txt"]),("icon",["icon\\eat.ico"])])
