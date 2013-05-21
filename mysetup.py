from distutils.core import setup
import py2exe

setup(windows=["Eat_What.pyw",{"script":"Eat_What.pyw","icon_resources":\
                              [(1,"icon\\eat.ico")]}],\
      data_files=[("data",["data\\data.txt","data\\Config.txt"])\
                  ,("icon",["icon\\eat.ico"])])
