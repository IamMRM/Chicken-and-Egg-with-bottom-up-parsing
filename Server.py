import socket
import sys
import json
import time
from queue import Queue 

port = 10000
maxsize = 32
befferr =Queue(maxsize)
blaa = True
def putInQueue(n):
  befferr.put(n)

def sendToChild(rate,connection,signal):
	msgTosent=""
	for i in range(rate):
		if(befferr.empty()):
			msgTosent+=""
		else:
			msgTosent=msgTosent+befferr.get()
    print('buffer space used is: ',befferr.qsize())
	connection.sendall(str(signal))


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('10.7.53.133', port)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
sock.listen(1)

message ="Message from first file and Lorem Ipsum is simply dummy.$"


print >>sys.stderr, 'waiting for a connection'
connection, client_address = sock.accept()

try:
    print >>sys.stderr, 'connection from', client_address
    rateee =int(raw_input("Enter date rate of client\n"))
    #parent_rate =int(raw_input("Enter date rate of parent\n"))
    end,start=0,0
    buff_occ = 0

    while True:
        if blaa:
            data = connection.recv(5000)
            recvd=json.loads(data.decode('utf-8'))
            msg = recvd['msg']
            rate = recvd['rate']
            if('$' in msg):
                blaa=False
            #print("message length is ",len(msg))
            buff_occ_value = befferr.qsize()+len(msg)-2#(int(rate)/2)
            print("buffer value is ",buff_occ_value)
            signal = 0
            #print('the conditions for checking is ',(maxsize-buff_occ_value))
            #print('The rate of child is ',rate)
            if msg:
        		#rate*=2
        		if rate*2<=(maxsize-buff_occ_value):
        			signal=300#underflow
        		elif rate/2<=(maxsize-buff_occ_value):
        			signal=100#overflow
        		else:
        			signal=(maxsize-buff_occ_value)
        		#print("signal is: ",signal)
        		print("message recieves server: ",msg)
        		map(putInQueue, list(msg))
            sendToChild(2,connection,signal)
            #starting new code

        if(rateee <= len(message)):
            end += rateee
            sliced=message[start:end]
            sent = {'msg':sliced,'rate':rateee}
        else:
            end = len(message)
            sliced = message[start:end]
            sent = {'msg':sliced,'rate':rateee}

        if(end<= len(message)):
            connection.sendall(json.dumps(sent).encode('utf-8'))
            print("sending ", sliced)
            print("\n\t\tAwaiting reply:")
            replyy = connection.recv(5000)
            if(replyy):
                buff_occ = int(replyy)
                #print("buff occupancy: ",buff_occ)
            else:
                buff_occ = 0

            if buff_occ == 100:#buffer extreme overflow
                if rateee != 1:
                    rateee/=2
                print("overflow so rate is ",rateee)
            elif buff_occ == 300:# buffer underflow
                rateee*=2
                print("underflow so rate is ",rateee)
            else:
            	rateee=buff_occ
        time.sleep(1)
        start = end

except:
	print("The rate at which data was being sent was much much greater than server can handle")	
finally:
    print >>sys.stderr, 'closing socket'
    connection.close()