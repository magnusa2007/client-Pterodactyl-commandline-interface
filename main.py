import os,requests, json, sys
pteroUrl = ''
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
    url = pteroUrl+'/files/list?directory='+dir
    r = requests.get(url,cookies=cookies)
    j = json.loads(r.text)
    for x in j['data']:
        print(x['attributes']['name'])
    print(r)

def download(file):
    url = pteroUrl+'/files/contents?file='+file
    r = requests.get(url,cookies=cookies)
    print(r)
    fs = open(file.split('/')[-1],'w')
    fs.write(r.text)
    fs.close()
    print('Saved to '+file.split('/')[-1])

def rename(before,after,dir):
    url = pteroUrl+'/files/rename'
    data= {'root': dir,'files':[{'from':before,'to':after}]}
    r = requests.put(url,cookies=cookies, json=data,headers = headers)
    print(r)
    
def check(name,dir):
    url = pteroUrl+'/files/list?directory='+dir
    r = requests.get(url,cookies=cookies)
    j = json.loads(r.text)
    for x in j['data']:
        if name == x['attributes']['name']:
            return True
    return False

directory=''  
while True:
    sys.stdout.write(directory+'> ')
    command = input()
    split = command.split()
    if split[0] == 'cd':
        if split[1] == '..':
            directory=directory[:-len(directory.split('/')[-1])-1]
        else:
            if check(split[1],directory):
                directory=directory+'/'+split[1]
            else:
                print('Unkown directory')
    
    elif split[0] == 'ls':
        printfile(directory)
    elif split[0] == 'download':
        if check(split[1],directory):
            download(directory+'/'+split[1])
        else:
            print('Unkown file')
    elif split[0] == 'exit':
        exit()
    elif split[0] == 'clear':
        os.system('cls')
    elif split[0] == 'rename':
        if check(split[1],directory):
            if len(split) == 2:
                rename(split[1],split[2],directory)
            else:
                print('Must be two arguments')
        else:
            print('Unkown file')
    elif split[0] == 'help':
        print(help)
    else:
        print('Unkown command do help for command list')