import os,requests, json, sys
headers = json.load(open('headers.json'))
cookies = json.load(open('cookies.json'))

help = """help: This command
ls: Show everything in the folder
cd: Moves folder takes on argument(mods or ..)
download: Takes one argument(elua.txt)
rename: Takes two arguments(badmod.jar badmod.disabledjar)
exit: Closes the program
clear: Clears the console"""



def printfile(dir):
    url = 'https://console.moeat.net/api/client/servers/821ae3ad-4355-4e79-b31f-9ff1ccd23d77/files/list?directory='+dir
    r = requests.get(url,cookies=cookies)
    j = json.loads(r.text)
    for x in j['data']:
        print(x['attributes']['name'])
    print(r)

def download(file):
    url = 'https://console.moeat.net/api/client/servers/821ae3ad-4355-4e79-b31f-9ff1ccd23d77/files/contents?file='+file
    r = requests.get(url,cookies=cookies)
    print(r)
    fs = open(file.split('/')[-1],'w')
    fs.write(r.text)
    fs.close()
    print('Saved to '+file.split('/')[-1])

def rename(before,after,dir):
    url = 'https://console.moeat.net/api/client/servers/821ae3ad-4355-4e79-b31f-9ff1ccd23d77/files/rename'
    data= {'root': dir,'files':[{'from':before,'to':after}]}
    r = requests.put(url,cookies=cookies, json=data,headers = headers)
    print(r)

directory=''  
printfile(directory)
while True:
    sys.stdout.write(directory+'> ')
    command = input()
    split = command.split()
    if split[0] == 'cd':
        if split[1] == '..':
            directory=directory[:-len(directory.split('/')[-1])-1]
        else:
            directory=directory+'/'+split[1]
    
    elif split[0] == 'ls':
        printfile(directory)
    elif split[0] == 'download':
        download(directory+'/'+split[1])
    elif split[0] == 'exit':
        exit()
    elif split[0] == 'clear':
        os.system('cls')
    elif split[0] == 'rename':
        rename(split[1],split[2],directory)
    elif split[0] == 'help':
        print(help)
    else:
        print('Unkown command do help for command list')