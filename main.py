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
NBTExplorer = r'start "" "C:\Program Files (x86)\NBTExplorer\NBTExplorer.exe"'
Notpad = r'start "" "C:\Program Files\Notepad++\notepad++.exe"'
#Optinal end
headers = {
    "Authorization": api,
    "Accept": "application/json",
    'content-type': 'application/json'
}

args = sys.argv

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
if len(args)>=2:
    print(f'Logging into {args[1]}')
    server=servers[int(args[1])]
else:
    print('Pick a server')
    sys.stdout.write('> ')
    server=servers[int(input())]


error = ['Run a command first']

#UUID Function
try:
    UUIDList = json.load(open('uuid.json'))
except:
    UUIDList = dict()

def UUID(uuid,output='print'):
    if output == 'return':
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
    else:
        if uuid.count('-')==4:
            print(f'{uuid}s name is {UUIDList[uuid]}')
        else:
            if uuid in UUIDList.values():
                for u in UUIDList:
                    if UUIDList[u] == uuid:
                        print(f'{uuid}s UUID is {u}')


#Tab complete
tab = dict()
def getTabs(dir):
    global tab
    tab['file'] = []
    tab['dir']  = ['..']
    tab['uuid/name'] = []

    url = pteroUrl+'/api/client/servers/'+server+'/files/list?directory='+dir
    r = requests.get(url,headers=headers,cookies=cookies)
    
    for x in r.json()['data']:
        x=x['attributes']['name']
        if x.count('.'):
            tab['file'].append(x)
        else:
            tab['dir'].append(x)
    for key in UUIDList:
        tab['uuid/name'].append(key)
        tab['uuid/name'].append(UUIDList[key])
    tab['dir'].sort()
    tab['file'].sort()
    tab['uuid/name'].sort()
        
getTabs('')
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
            print(f'({UUID(x[0:36],output="return")}) {x}')
        else:
            print(x)

def download(file):
    url = pteroUrl+'/api/client/servers/'+server+'/files/download?file='+file
    r = requests.get(url,headers=headers,cookies=cookies)
    print(r)
    url = r.json()['attributes']['url']
    r = requests.get(url,headers=headers,cookies=cookies)
    with open(file.split('/')[-1], mode="wb") as fs:
        fs.write(r.content)
    print('Saved to '+file.split('/')[-1])
    error.append(r.text)

def delete(file):
    if areYouSure('Are you sure you want to delete '+file.split('/')[-1]+'\nTHIS CANNOT BE UNDONE!'):
        url = pteroUrl+'/api/client/servers/'+server+'/files/delete'
        data = {"root":file[0:-len(file.split('/')[-1])],"files":[file.split('/')[-1]]}
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
    
def compress(file):
    url = pteroUrl+'/api/client/servers/'+server+'/files/compress'
    data = {"root":file[0:-len(file.split('/')[-1])],"files":[file.split('/')[-1]]}
    r = requests.post(url, headers=headers,json=data,cookies=cookies)
    print(r)
    error.append(r.text)

def decompress(file):
    url = pteroUrl+'/api/client/servers/'+server+'/files/decompress'
    data = {"root":file[0:-len(file.split('/')[-1])],"files":[file.split('/')[-1]]}
    r = requests.post(url, headers=headers,json=data,cookies=cookies)
    print(r)
    error.append(r.text)

def rename(file,newName):
    if areYouSure('Are you sure that you want to rename '+file.split('/')[-1]+' to '+newName):
        url = pteroUrl+'/api/client/servers/'+server+'/files/rename'
        data= {'root': file[0:-len(file.split('/')[-1])],'files':[{'from':file.split('/')[-1],'to':newName}]}
        r = requests.put(url, json=data,headers = headers,cookies=cookies)
        print(r)
        error.append(r.text)
    


def filePrint(file):
    url = pteroUrl+'/api/client/servers/'+server+'/files/contents?file='+file
    r = requests.get(url, json=data,headers = headers,cookies=cookies)
    print(r.text)
    error.append(r.text)

def changeDir(dir):
    global directory
    if dir == '..':
         directory = directory[:-len(directory.split('/')[-1])-1]
    else:
        if dir in tab['dir']:
            if dir.count('.') == 0:
                directory=directory+'/'+dir
                
def fNBTExplorer(file):
    download(file)
    print('Opening NBTExplorer')
    os.system(NBTExplorer+' '+file.split('/')[-1])

def fnotpad(file):
    download(file)
    print('Opening Notpad')
    os.system(Notpad+' '+file.split('/')[-1])
    
def areYouSure(text):
    print(text)
    print('yes/no')
    sys.stdout.write('> ')
    return input().lower() == 'yes'

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def errorPrint():
    for i in error:
        print(str(error.index(i))+': '+str(i))


#Commands
command = dict()
command['ls'] = {'args':['none'],'des': 'Prints all files in diretory.','f':printDir}
command['cd'] = {'args':['dir'],'des': 'Move to the new diretory.','f':changeDir}
command['download'] = {'args':['file'],'des': 'Download the file.','f':download}
command['rename'] = {'args':['file',"New Name"],'des': 'Renames the file.','f':rename}
command['compress'] = {'args':['file'],'des': 'Compresses the file.','f':compress}
command['decompress'] = {'args':['file'],'des': 'Decompresses the file.','f':decompress}
command['NBTExplorer'] = {'args':['file'],'des': 'Opens NBTExploar with the file.','f':fNBTExplorer}
command['print'] = {'args':['file'],'des': 'Prints the data of the file.','f':filePrint}
command['notpad'] = {'args':['file'],'des': 'Opens NBTExploar with the file.','f':fnotpad}
command['uuid'] = {'args':['uuid/name'],'des': 'Returns the UUID or name of a player.','f':UUID}
command['exit'] = {'args':['none'],'des': 'Closes the program.','f':exit}
command['clear'] = {'args':['none'],'des': 'Clears the console.','f':cls}
command['error'] = {'args':['none'],'des': 'Prints all the errors from the response.','f':errorPrint}
command = dict(sorted(command.items()))

def commandHandle(input):
    global directory
    cs = input.split(' ')
    if cs[0] in command:
        for c in cs[1:]:
            try:
                for arg in command[cs[0]]['args']:
                    if not c in tab[arg]:
                        print(f'{c} is not a {arg}')
                        return False
                    elif arg == 'file':
                        cs[cs.index(c)] = directory+'/'+c
            except:
                pass
            
        command[cs[0]]['f'](*cs[1:])
    else:
        print('Unkown command do help for list of all commands')
        
directory=''
while True:
    getTabs(directory)
    input = tabInput('home'+directory+'> ')
    commandHandle(input)
