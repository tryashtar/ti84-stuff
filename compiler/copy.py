import os
import yaml
import datetime
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
        nice_item = item.replace("_theta_", "")
        print(item)
        for folder in folders:
            file = os.path.join(folder, item + ".8xp")
            if os.path.exists(file):
                dest = os.path.join(cat_folder, nice_item)
                os.makedirs(dest, exist_ok = True)
                with open(file, "rb") as code:
                    prgm = compiler.Program(code.read())
                prgm.archived = False
                with open(os.path.join(dest, nice_item + ".txt"), "w", encoding="utf8") as src:
                    src.write(prgm.code)
                with open(os.path.join(dest, "metadata.yaml"), "w", encoding="utf8") as meta:
                    data = {'name': prgm.name, 'comment': prgm.comment, 'version': prgm.version}
                    yaml.dump(data, meta, default_flow_style=False)
                with open(os.path.join(dest, nice_item + ".8xp"), "wb") as code:
                    code.write(prgm.compile())
                readme = os.path.join(dest, "README.md")
                if not os.path.exists(readme):
                    open(readme, "a").close()
                break
