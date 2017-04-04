import cx_Freeze;

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="PotHoles",
    options={"build_exe":{"packages":["pygame"],
                          "include_files":["card.png","Impact.TTF","Comic.TTF"]}},
    executables =   executables
    
    )
