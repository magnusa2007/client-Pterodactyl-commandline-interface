import os,requests, sys, json
from msvcrt import getch
cookies={}

#Setup
cookies['remember_web_######' = 'session0%3D'
#Get from DevTools ^^
api = 'ptlc_key'
#From your account ^^^
pteroUrl = "https://url.com"
#Setup end

#Optinal
NBTExplorer = r'"C:\Program Files (x86)\NBTExplorer\NBTExplorer.exe"'
Notpad = r'"C:\Program Files\Notepad++\notepad++.exe"'
#Optinal end
headers = {
    "Authorization": api,
    "Accept": "application/json",
    'content-type': 'application/json'
}

ASCCI = """
   ___ _ _         _                               
  / __| (_)___ _ _| |_                             
 | (__| | / -_) ' \  _|                            
  \___|_|_\___|_||_\__| 
  ___ _                   _         _        _     
 | _ \ |_ ___ _ _ ___  __| |__ _ __| |_ _  _| |    
 |  _/  _/ -_) '_/ _ \/ _` / _` / _|  _| || | |    
 |_|  \__\___|_| \___/\__,_\__,_\__|\__|\_, |_|    
                                         |__/    
   ___                              _
  / __|___ _ __  _ __  __ _ _ _  __| | (_)_ _  ___ 
 | (__/ _ \ '  \| '  \/ _` | ' \/ _` | | | ' \/ -_)
  \___\___/_|_|_|_|_|_\__,_|_||_\__,_|_|_|_||_\___|
  ___     _            __
 |_ _|_ _| |_ ___ _ _ / _|__ _ __ ___              
  | || ' \  _/ -_) '_|  _/ _` / _/ -_)             
 |___|_||_\__\___|_| |_| \__,_\__\___|             
                                                   
                                                           
Made by MagBot
https://github.com/magnusa2007/client-Pterodactyl-commandline-interface                       
                                                                 """
print(ASCCI)
r=requests.get(pteroUrl,headers=headers,cookies=cookies)
responseCookies = r.cookies.get_dict()

headers['x-xsrf-token'] = responseCookies['XSRF-TOKEN'][:-3]+'='
cookies['pterodactyl_session']=responseCookies['pterodactyl_session']
cookies['XSRF-TOKEN']=responseCookies['XSRF-TOKEN']

r=requests.get(url=pteroUrl+'/api/client',headers=headers,cookies=cookies)
data = r.json()
servers = {}
n=0
for x in data['data']:
    n=n+1
    name = x['attributes']['name']
    print(f'[{n}] {name}')
    servers[n] = x['attributes']['identifier']
print('Pick a server')
sys.stdout.write('> ')
server=servers[int(input())]


error = ['Run a command first']


#Tab complete
def getTabs(dir):
    tab = dict()
    tab['file'] = []
    tab['dir']  = ['..']

    url = pteroUrl+'/api/client/servers/'+server+'/files/list?directory='+dir
    r = requests.get(url,headers=headers,cookies=cookies)
    
    for x in r.json()['data']:
        x=x['attributes']['name']
        if x.count('.'):
            tab['file'].append(x)
        else:
            tab['dir'].append(x)
    tab['dir'].sort()
    tab['file'].sort()
    return tab

tab = getTabs('')

command = dict()
command['ls'] = {'args':['none'],'des': 'Prints all files in diretory.'}
command['cd'] = {'args':['dir'],'des': 'Move to the new diretory.'}
command['download'] = {'args':['file'],'des': 'Download the file.'}
command['rename'] = {'args':['file',"New Name"],'des': 'Download the file.'}
command['compress'] = {'args':['file'],'des': 'Compresses the file.'}
command['decompress'] = {'args':['file'],'des': 'Decompresses the file.'}
command['NBTExplorer'] = {'args':['file'],'des': 'Opens NBTExploar with the file.'}
command['print'] = {'args':['file'],'des': 'Prints the data of the file.'}
command['notpad'] = {'args':['file'],'des': 'Opens NBTExploar with the file.'}
command['exit'] = {'args':['none'],'des': 'Closes the program.'}
command['clear'] = {'args':['none'],'des': 'Clears the console(Windows).'}
command['error'] = {'args':['none'],'des': 'Prints all the errors from the response.'}
command = dict(sorted(command.items()))
history = []

def write(str):
    sys.stdout.write('\033[2K')
    sys.stdout.write(str)
    sys.stdout.flush()
    

    
def tabInput(b):
    index = 0
    line = ''
    sys.stdout.write('\0337')
    while True:
        sys.stdout.write('\0338')
        write(b+line)
        key = str(getch())[2:-1]
        if len(key) == 1:
            line = line+key
            
        elif key == '\\r':
            print()
            history.append(line)
            index = 0
            return line
        
        elif key == '\\x08':
            line = line[0:-1]
        
        elif key == '\\xe0':
                key = str(getch())[2:-1]
                try:
                    if key == 'H': #up
                        index-=1
                        line = history[index%len(history)]
                    elif key == 'P':
                        index+=1
                        line = history[index%len(history)]
                    
                except:
                    pass
                    
        elif key == '\\t':
            try:
                split = line.split()
                if len(split) == 1:
                    for i in command:
                        if i[0:len(split[0])].lower() == split[0].lower():
                            line = i
                else:
                    if split[-1] in tab[command[split[0]]['args'][len(split)-2]]:
                        i = tab[command[split[0]]['args'][len(split)-2]][(tab[command[split[0]]['args'][len(split)-2]].index(split[-1])+1)%len(tab[command[split[0]]['args'][len(split)-2]])]
                        string=''
                        for s in split[0:-1]:
                           string = string+' '+s
                        line = string[1:]+' '+i
                    else:
                        for i in tab[command[split[0]]['args'][len(split)-2]]:
                            if i[0:len(split[-1])].lower() == split[-1].lower():
                                string=''
                                for s in split[0:-1]:
                                   string = string+' '+s
                                line = string[1:]+' '+i
                                break
            except:
                pass

def help(cmds='all'):
    if cmds == 'all':
        for cmd in command:
            print(f'{cmd}:\n  Arguments:\n    {str(command[cmd]["args"])}\n  Description:\n    {command[cmd]["des"]}\n')
    elif cmds in command:
        cmd = cmds
        print(f'{cmd}:\n  Arguments:\n    {str(command[cmd]["args"])}\n  Description:\n    {command[cmd]["des"]}\n')
    else:
        print('Unkown Command')

def printDir():
    for x in tab['dir']:
        print(x)
    for x in tab['file']:
        if x.count('-')==4:
            print(f'({UUID(x[0:36])}) {x}')
        else:
            print(x)

def download(file,dir):
    url = pteroUrl+'/api/client/servers/'+server+'/files/download?file='+dir+'/'+file
    r = requests.get(url,headers=headers,cookies=cookies)
    print(r)
    url = r.json()['attributes']['url']
    r = requests.get(url,headers=headers,cookies=cookies)
    with open(file, mode="wb") as fs:
        fs.write(r.content)
    print('Saved to '+file)
    error.append(r.text)

def delete(file,dir):
    url = pteroUrl+'/api/client/servers/'+server+'/files/delete'
    data = {"root":dir,"files":[file]}
    r = requests.post(url, headers=headers,json=data,cookies=cookies)
    print(r)
    error.append(r.text)
    
def upload(file,dir):
    fs = open(file,'rb').read()
    files = {'file':fs}
    url = pteroUrl+'/api/client/servers/'+server+'/files/upload'
    r=requests.get(url,headers=headers,cookies=cookies)
    print(r)
    url = r.json()['attributes']['url']+dir
    r = requests.post(url,headers=headers,cookies=cookies,files=files)
    print(r)
    error.append(r.text)
    
def compress(file,dir):
    url = pteroUrl+'/api/client/servers/'+server+'/files/compress'
    data = {"root":dir,"files":[file]}
    r = requests.post(url, headers=headers,json=data,cookies=cookies)
    print(r)
    error.append(r.text)

def decompress(file,dir):
    url = pteroUrl+'/api/client/servers/'+server+'/files/decompress'
    data = {"root":dir,"files":[file]}
    r = requests.post(url, headers=headers,json=data,cookies=cookies)
    print(r)
    error.append(r.text)

def rename(before,after,dir):
    url = pteroUrl+'/api/client/servers/'+server+'/files/rename'
    data= {'root': dir,'files':[{'from':before,'to':after}]}
    r = requests.put(url, json=data,headers = headers,cookies=cookies)
    print(r)
    error.append(r.text)
    


def filePrint(file,dir):
    url = pteroUrl+'/api/client/servers/'+server+'/files/contents?file='+dir+'/'+file
    r = requests.get(url, json=data,headers = headers,cookies=cookies)
    print(r.text)
            

def areYouSure(text):
    print(text)
    print('yes/no')
    sys.stdout.write('> ')
    return input().lower() == 'yes'


try:
    UUIDList = json.load(open('uuid.json'))
except:
    UUIDList = dict()

def UUID(uuid):
    if uuid in UUIDList:
        return UUIDList[uuid]
    else:
        r = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}")
        name = r.json()['name']
        UUIDList[uuid] = name
        fs = open("uuid.json", "w")
        json.dump(UUIDList,fs)
        fs.close()
        return name
    
directory=''
while True:
    tab = getTabs(directory)
    input = tabInput('home'+directory+'> ')
    cs = input.split()
    if cs[0] == 'cd':
        if cs[1] == '..':
            directory=directory[:-len(directory.cs('/')[-1])-1]
        else:
            if cs[1] in tab['dir']:
                if cs[1].count('.') == 0:
                    directory=directory+'/'+cs[1]
                else:
                    print('Directory not file')
            else:
                print('Unkown directory')
    
    elif cs[0] == 'ls':
        printDir()
    elif cs[0] == 'download':
        if cs[1] in tab['file']:
            download(cs[1],directory)
        else:
            print('Unkown file')
    elif cs[0] == 'exit':
        exit()
    elif cs[0] == 'clear':
        os.system('cls')
    elif cs[0] == 'rename':
        if cs[1] in tab['file']:
            if len(cs) == 3:
                if areYouSure('Are you sure that you want to rename '+cs[1]):
                    rename(cs[1],cs[2],directory)
            else:
                print('Must be two arguments')
        else:
            print('Unkown file')
            
    elif cs[0]=='delete':
        if cs[1] in tab['file']:
            if areYouSure('Are you sure you want to delete '+cs[1]+'\nTHIS CANNOT BE UNDONE!'):
                delete(cs[1],directory)
        else:
            print('Unkown file')
            
    elif cs[0]=='compress':
        if cs[1] in tab['file']:
            compress(cs[1],directory)
        else:
            print('Unkown file')
            
    elif cs[0]=='upload':
        upload(cs[1],directory)
            
    elif cs[0]=='decompress':
        if cs[1] in tab['files']:
            decompress(cs[1],directory)
        else:
            print('Unkown file')
    elif cs[0]=='NBTExplorer':
        if cs[1] in tab['file']:
            download(cs[1],directory)
            print('Opening NBTExplorer')
            os.system(NBTExplorer+' '+cs[1])
        else:
            print('Unkown file')
    elif cs[0]=='notpad':
        if cs[1] in tab['files']:
            download(cs[1],directory)
            print('Opening Notpad')
            os.system(Notpad+' '+cs[1])
        else:
            print('Unkown file')
    elif cs[0]=='print':
        if cs[1] in tab['file']:
            filePrint(directory,cs[1])
    elif cs[0] == 'help':
        if len(cs) == 1:
            help()
        else:
            help(cs[1])
    elif cs[0] == 'error':
        for i in error:
            print(str(error.index(i))+': '+str(i))
    else:
        print('Unkown command do help for command list')
