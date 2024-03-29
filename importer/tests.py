import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../compiler'))
import compiler

output_files = True

here = os.path.dirname(os.path.abspath(__file__))
for root, directories, filenames in os.walk('/d/Projects/TI-Basic'): 
    for filename in filenames:
        with open(os.path.join(root,filename), "rb") as program:
            original = program.read()
        prgm = compiler.load_program(original)
        recompiled = prgm.compile()
        print(f'{filename}: {original == recompiled}')
        if output_files:
            os.makedirs(os.path.join(here, "tests"), exist_ok = True)
            with open(os.path.join(here, "tests", filename), "wb") as out:
                out.write(recompiled)
            with open(os.path.join(here, "tests", os.path.splitext(filename)[0]+'.txt'), "w", encoding="utf-8") as out:
                out.write(prgm.code)
