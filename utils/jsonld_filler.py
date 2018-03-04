import os
import re

path = '../site/src'
template_format = ".template.html"
os.chdir(path)
files = os.listdir('.')
for name in files:
    if name.endswith(template_format):
        html_content = None
        jsonld_content = None
        with open(name, 'r', encoding="UTF-8") as f:
            html_content = f.read()
        mmpid = os.path.basename(name).replace(template_format, "")
        jsonld_filename = os.path.join('bioschemas', "{}.json".format(mmpid))
        with open(jsonld_filename, 'r') as f:
            jsonld_content = f.read()
        new_html = re.sub('{content}', jsonld_content, html_content, flags=re.M)
        new_file = "{}.html".format(mmpid)
        with open(new_file, 'w', encoding="UTF-8") as f:
            f.writelines(new_html)
