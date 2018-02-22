import os
import re

path = './site/src'

os.chdir(path)
files = os.listdir('.')
for name in files:
    if name.endswith(".html"):
        html_content = None
        jsonld_content = None
        with open(name, 'r') as f:
            html_content = f.read()
        mmpid = os.path.basename(name)[:-5]
        jsonld_filename = os.path.join('bioschemas', "{}.json".format(mmpid))
        with open(jsonld_filename, 'r') as f:
            jsonld_content = f.read()
        new_html = re.sub('{content}', jsonld_content, html_content, flags=re.M)
        new_file = "{}_new.html".format(mmpid)
        with open(name, 'w') as f:
            f.writelines(new_html)
