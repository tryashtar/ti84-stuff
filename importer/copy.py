import os
import yaml
import datetime
import sys
sys.path.append('../compiler')
import compiler

here = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(here, "copy.yaml"), "r") as file:
    data = yaml.safe_load(file.read())

project_folder = "D:/Projects/TI-Basic"
folders = [os.path.join(project_folder, x) for x in os.listdir(project_folder) if os.path.isdir(os.path.join(project_folder, x))]
folders.sort(key = lambda x: datetime.datetime.strptime(os.path.basename(x), "%Y.%m.%d"), reverse = True)

for category, items in data.items():
    cat_folder = os.path.join(here, '..', 'projects', category)
    for item in items:
        if type(item) is str:
            item = {'name':item}
        name = item['name']
        prgm_name = None
        nice_name = name.replace("_theta_", "")
        if 'rename' in item:
            nice_name = item['rename']
            prgm_name = nice_name
        print(nice_name)
        for folder in folders:
            file = os.path.join(folder, name + ".8xp")
            if os.path.exists(file):
                dest = os.path.join(cat_folder, nice_name)
                os.makedirs(dest, exist_ok = True)
                with open(file, "rb") as code:
                    prgm = compiler.load_program(code.read())
                prgm.archived = False
                if prgm_name is not None:
                    prgm.name = prgm_name
                if 'remove' in item:
                    lines = prgm.code.splitlines()
                    remove = item['remove']
                    remove.sort()
                    for i, r in enumerate(remove):
                        del lines[r-i]
                    prgm.code = '\n'.join(lines)
                with open(os.path.join(dest, nice_name + ".txt"), "w", encoding="utf8") as src:
                    src.write(prgm.code)
                with open(os.path.join(dest, "metadata.yaml"), "w", encoding="utf8") as meta:
                    data = {'name': prgm.name, 'comment': prgm.comment, 'version': prgm.version}
                    yaml.dump(data, meta, default_flow_style=False)
                with open(os.path.join(dest, nice_name + ".8xp"), "wb") as code:
                    code.write(prgm.compile())
                readme = os.path.join(dest, "README.md")
                if not os.path.exists(readme):
                    open(readme, "a").close()
                break
