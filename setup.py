import cx_Freeze
import os

os.environ['TCL_LIBRARY'] = r'C:\Users\xtrar\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\xtrar\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6'

executables = [cx_Freeze.Executable(
    "game.py",
    icon = "cmicon.ico")]

cx_Freeze.setup(
    name="TicTacTrivia",
    options={"build_exe":{"packages":["pygame"],
                          "include_files":["50animequestions.csv",
                                           "50videogamequestions.csv",
                                           "dupecheck.txt",
                                           ]}},
    executables = executables
)