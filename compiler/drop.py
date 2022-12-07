import sys
import os
import datetime
import yaml
import compiler

if len(sys.argv) < 2:
  print('Drag a file to compile or decompile it')
  exit()

for path in sys.argv[1:]:
  if not os.path.exists(path):
    print(f'File not found: {path}')
    continue
  with open(path, 'rb') as file:
    data = file.read()
    name = os.path.splitext(path)[0]
    meta_path = os.path.join(os.path.dirname(path), 'metadata.yaml')
    if data.startswith('**TI83F*'.encode('ascii')):
      print(data)
      prgm = compiler.load_program(data)
      with open(os.path.join(os.path.dirname(path), name + '.txt'), 'w', encoding='utf8') as result:
        result.write(prgm.code)
      with open(meta_path, 'w', encoding='utf8') as meta:
        metadata = {'name': prgm.name, 'comment': prgm.comment, 'version': prgm.version}
        yaml.dump(metadata, meta, default_flow_style=False)
    else:
      if os.path.exists(meta_path):
        with open(meta_path, 'r', encoding='utf8') as meta:
          metadata = yaml.safe_load(meta.read())
          prgm_name = metadata['name']
          comment = metadata['comment']
          version = metadata['version']
      else:
        prgm_name = name
        comment = f'Compiled {datetime.datetime.now().date().isoformat()}'
        version = 1
      prgm = compiler.Program(name=prgm_name, comment=comment, code=data.decode('utf8'), version=version)
      with open(os.path.join(os.path.dirname(path), name + '.8xp'), 'wb') as result:
        result.write(prgm.compile())
