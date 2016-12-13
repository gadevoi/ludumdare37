import cx_Freeze

executables = [cx_Freeze.Executable("game.py")]

cx_Freeze.setup(
    name="Garden of Eden",
    options={"build_exe": {"packages":["pygame", "pygame.freetype", "numpy", "random", "copy", "math"],
                           "include_files":["bg.png", "stars.png", "CrimsonText-Regular.ttf", "dead.png", "rad.png", "marsbound.mp3"]}},
    executables = executables

    )
