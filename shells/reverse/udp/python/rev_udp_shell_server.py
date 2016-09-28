import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port, check if the port is open in possible fw first..
server_address = ('0.0.0.0', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

while True:
    print >>sys.stderr, '\nwaiting to receive message'
    data, address = sock.recvfrom(4096)
    print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
    #print >>sys.stderr, data
    print data
    data, address = sock.recvfrom(4096)
    command = raw_input (data)
    #print 'Sending: ', command
    sent = sock.sendto(command, address)
    print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)
