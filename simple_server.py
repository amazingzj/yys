import threading,time
import socket

s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('0.0.0.0',9998))
s.listen(5)
print 'waitting for connection.'

def tcplink(sock,addr):
    print "Accept new conncetion from %s:%s" % addr
    sock.send('Wellcome')
    l = []
    while True:
        data = sock.recv(1024)
        print data
        time.sleep(1)

        try:
            pass
        except None, data:
            continue

        if data == 'exit' or not data:
            break
        else:
            l.append(data)

        sock.send('HELLO, %s   ' % data)
    sock.close()
    print l
    print 'Connection from %s:%s closed' % addr


while True:
    sock,addr = s.accept()
    t = threading.Thread(target=tcplink,args=(sock,addr))
    t.start()
