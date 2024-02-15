import os,requests, sys
pteroUrl = "url"
api = 'ptlc_####'
#From your account

XSRF = 'long string'
#Get from header

session = 'long string2'
#Get from cookies

headers = {
    "Authorization": api,
    "Accept": "application/json",
    "x-xsrf-token": XSRF
}
cookies = {
    'pterodactyl_session':session,
    'XSRF-TOKEN':XSRF
}

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


help = """help: This comand
ls: Show everything in the folder.
cd: Moves folder takes one argument(mods or ..).
download: Takes one argument(elua.txt).
rename: Takes two arguments(badmod.jar badmod.disabledjar).
compress: Takes one argument(mods).
decompress: Takes one argument(mods.tar.gz).
exit: Closes the program.
clear: Clears the console."""



def printfile(dir):
    url = pteroUrl+'/api/client/servers/'+server+'/files/list?directory='+dir
    r = requests.get(url,headers=headers,cookies=cookies)
    for x in r.json()['data']:
        print(x['attributes']['name'])
    print(r)

def download(file,dir):
    url = pteroUrl+'/api/client/servers/'+server+'/files/download?file='+dir+'/'+file
    r = requests.get(url,headers=headers,cookies=cookies)
    print(r)
    url = r.json()['attributes']['url']
    r = requests.get(url,headers=headers,cookies=cookies)
    with open(file, mode="wb") as fs:
        fs.write(r.content)
    print('Saved to '+file)

def delete(file,dir):
    url = pteroUrl+'/api/client/servers/'+server+'/files/delete'
    data = {"root":dir,"files":[file]}
    r = requests.post(url, headers=headers,json=data,cookies=cookies)
    print(r)

def compress(file,dir):
    url = pteroUrl+'/api/client/servers/'+server+'/files/compress'
    data = {"root":dir,"files":[file]}
    r = requests.post(url, headers=headers,json=data,cookies=cookies)
    print(r)

def decompress(file,dir):
    url = pteroUrl+'/api/client/servers/'+server+'/files/decompress'
    data = {"root":dir,"files":[file]}
    r = requests.post(url, headers=headers,json=data,cookies=cookies)
    print(r)

def rename(before,after,dir):
    url = pteroUrl+'/api/client/servers/'+server+'/files/rename'
    data= {'root': dir,'files':[{'from':before,'to':after}]}
    r = requests.put(url, json=data,headers = headers,cookies=cookies)
    print(r)
    print(r.text)
    
def check(name,dir):
    url = pteroUrl+'/api/client/servers/'+server+'/files/list?directory='+dir
    r = requests.get(url,headers=headers,cookies=cookies)
    for x in r.json()['data']:
        if name == x['attributes']['name']:
            return True
    return False

directory=''  
while True:
    sys.stdout.write('home'+directory+'> ')
    command = input()
    split = command.split()
    if split[0] == 'cd':
        if split[1] == '..':
            directory=directory[:-len(directory.split('/')[-1])-1]
        else:
            if check(split[1],directory):
                if split[1].count('.') == 0:
                    directory=directory+'/'+split[1]
                else:
                    print('Directory not file')
            else:
                print('Unkown directory')
    
    elif split[0] == 'ls':
        printfile(directory)
    elif split[0] == 'download':
        if check(split[1],directory):
            download(split[1],directory)
        else:
            print('Unkown file')
    elif split[0] == 'exit':
        exit()
    elif split[0] == 'clear':
        os.system('cls')
    elif split[0] == 'rename':
        if check(split[1],directory):
            if len(split) == 3:
                rename(split[1],split[2],directory)
            else:
                print('Must be two arguments')
        else:
            print('Unkown file')
            
    elif split[0]=='delete':
        if check(split[1],directory):
            delete(split[1],directory)
        else:
            print('Unkown file')
            
    elif split[0]=='compress':
        if check(split[1],directory):
            compress(split[1],directory)
        else:
            print('Unkown file')
            
    elif split[0]=='decompress':
        if check(split[1],directory):
            decompress(split[1],directory)
        else:
            print('Unkown file')
            
    elif split[0] == 'help':
        print(help)
    else:
        print('Unkown command do help for command list')
