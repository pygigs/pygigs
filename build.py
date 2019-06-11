from jinja2 import Environment, FileSystemLoader
import json
import os
import random

jload = json.load
meminfo = []

def refineData(meminfo):
    memberFiles = [file for file in os.listdir('res/data') if '.json' in file]
    for mem in memberFiles:
        with open('res/data/{}'.format(mem)) as json_file:  
            data = jload(json_file)
            if data['profile-icon'] == 'random':
                pics = [file for file in os.listdir('res/assets/profile')]
                pic = random.choice(pics)
                data['profile-icon'] = pic[:-4]
            meminfo.append(data)

def generate(file_in_templates, outpath, **kwargs):
    template_dir = 'res/templates'
    file_loader = FileSystemLoader(template_dir)
    env = Environment(loader=file_loader)
    template = env.get_template(file_in_templates)

    output = template.render(kwargs)
    print(output, file=open(outpath, 'w', encoding="utf8"))

def genMainPage():
    generate('index.html', 'index.html', append='')

def genMemberPages():
    for info in meminfo:
        try:
            os.mkdir(info['uname'])
        except OSError:
            pass
        generate('member_page.html', info['uname']+'/index.html', info=info, append='../', skills=info['skills'])

def genListing():
    random.shuffle(meminfo)
    generate('list.html', 'list/index.html', append='../', members=meminfo)

def genContact():
    generate('contact.html', 'contact/index.html', append='../')

def genRegister():
    generate('register.html', 'register/index.html', append='../')

refineData(meminfo)
genMainPage()
genListing()
genMemberPages()
genContact()
genRegister()
#with open('res/data/demo.json') as json_file:  
#    data = jload(json_file)

#print(data)

