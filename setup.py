import cx_Freeze

executables=[cx_Freeze.Executable('PyCarGame.py',targetName='ABitRacey01')]
includeFiles=['images','soundeffects']

build_options={'include_files':includeFiles}
dist_options={'initial_target_dir':'C:\\'}

cx_Freeze.setup(
    name='A Bit Racey',
    options={'build_exe':build_options,
             'bdist_msi':dist_options},
    executables=executables,
    version='1.0'
    )
