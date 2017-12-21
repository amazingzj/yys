
import threading,time
import socket
import MySQLdb as mysql



s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('0.0.0.0',9998))
s.listen(5)
print 'waitting for connection.'


db = mysql.connect(user="root",passwd="zhongjun",host="localhost",db="yumu")
db.autocommit(True)
cur = db.cursor()
print 'mysql database connection.'



def tcplink(sock,addr):
    print "Accept new conncetion from %s:%s" % addr
   # sock.send('ok\n')
    l = []
    global result
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
        data_processing(data)
        print mode
        print ip
        print code
        if int(mode) == 1:
            sql = 'delete from ipcode where code=%s'%(str(code))
            print sql
            try:
                cur.execute(sql)
            except:
                db.rollback()
            sql = 'insert into ipcode (ip ,code) value (%s,%s)'%(str(ip),str(code))
            print sql
            try:
                cur.execute(sql)
            except:
                db.rollback()

        if int(mode) == 2:
            sql = "SELECT * FROM ipcode where ip=%s and code=%s" %(str(ip), str(code))
            print sql
            try:
                cur.execute(sql)
                result = cur.fetchall()
                print result
            except:
                print "Error: unable to fecth data"

            if result == ():
                sock.send(b'0')
            else:
                sock.send(b'1')

        if int(mode) == 9:
            sql = 'delete from ipcode where code=%s'%(str(code))
            print sql
            try:
                cur.execute(sql)
            except:
                db.rollback()

    sock.close()
    #print l
    print 'Connection from %s:%s closed' % addr


def data_processing(data):
    global mode, ip, code
    mode = data.split('-')[0]
    ip = data.split('-')[1]
    code = data.split('-')[2]
    return mode, ip, code


while True:
    sock, addr = s.accept()
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()

