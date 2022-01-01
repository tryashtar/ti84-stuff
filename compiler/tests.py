import os
import compiler

output_files = False

for root, directories, filenames in os.walk('D:/Projects/TI-Basic/Calculator Backups'): 
    for filename in filenames:
        with open(os.path.join(root,filename), "rb") as program:
            original = program.read()
            prgm = compiler.Program(original)
            recompiled = prgm.compile()
            print(f'{filename}: {original == recompiled}')
            if output_files:
                os.makedirs("tests", exist_ok = True)
                with open(os.path.join("tests",filename), "wb") as out:
                    out.write(recompiled)
