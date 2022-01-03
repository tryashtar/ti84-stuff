import os
import yaml
import compiler

here = os.path.dirname(os.path.abspath(__file__))
for root, directories, filenames in os.walk(os.path.join(here, '..', 'projects')): 
    for filename in filenames:
        parts = os.path.splitext(filename)
        if parts[1] == '.txt':
            with open(os.path.join(root,filename), 'r', encoding='utf8') as file:
                code = file.read()
            with open(os.path.join(root,'metadata.yaml'), 'r', encoding='utf8') as file:
                meta = yaml.safe_load(file.read())
            prgm = compiler.Program(meta['name'], meta['comment'], code, int(meta['version']))
            compiled = prgm.compile()
            destination = os.path.join(root, parts[0]+'.8xp')
            if os.path.exists(destination):
                with open(destination, 'rb') as file:
                    existing = file.read()
                if existing != compiled:
                    print(f'changed {parts[0]}')
            else:
                print(f'new {parts[0]}')
            with open(destination, 'wb') as file:
                file.write(compiled)
