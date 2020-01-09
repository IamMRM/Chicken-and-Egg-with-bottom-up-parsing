import socket
import sys
import time
import json
from queue import Queue
port = 10000
maxsize = 32
befferr =Queue(maxsize)

blaa= True
def putInQueue(n):
  befferr.put(n)

def sendToChild(rate,sock,signal):
    msgTosent=""
    for i in range(rate):
        if(befferr.empty()):
            msgTosent+=""
        else:
            msgTosent=msgTosent+befferr.get()
    #print('buffer space used is: ',befferr.qsize())
    sock.sendall(str(signal))

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('10.7.53.133', port)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)
message ="Muhammad Roshan, MIT graduate persuing his career in Computer Science currently working with the collaboration of Tesla in Google.$"
try:
    #here division means rate
    rate =int(raw_input("Enter date rate\n"))
    #parent_rate =int(raw_input("Enter date rate of parent\n"))
    # n = len(message)/division
    # count = len(message) - n*division
    end,start=0,0
    buff_occ = 0

    while True:
        if(rate <= len(message)):
            end += rate
            sliced=message[start:end]
            sent = {'msg':sliced,'rate':rate}
        else:
            end = len(message)
            sliced = message[start:end]
            sent = {'msg':sliced,'rate':rate}

        

        if(end<= len(message)):
            sock.sendall(json.dumps(sent).encode('utf-8'))
            print("sending ", sliced)
            print("\n\t\tAwaiting reply:")
            replyy = sock.recv(5000)
            if(replyy):
                buff_occ = int(replyy)
                #print("buff occupancy: ",buff_occ)
            else:
                buff_occ = 0

            if buff_occ == 100:#buffer extreme overflow
                if rate != 1:
                    rate/=2
                print("overflow so rate is ",rate)
            elif buff_occ == 300:# buffer underflow
                rate*=2
                print("underflow so rate is ",rate)
            else:
            	rate= buff_occ
        #print("The rate is: ",rate)
        time.sleep(1)
        start = end

        #starting new code
        if blaa:
            data = sock.recv(5000)
            recvd=json.loads(data.decode('utf-8'))
            msg = recvd['msg']
            rateee = recvd['rate']
            if('$' in msg):
                blaa=False

            buff_occ_value = befferr.qsize()+len(msg)-2#(int(rate)/2)
            print("Buffer value is ",buff_occ_value)
            signal = 0
            if msg:
                #rateee*=2
                if rateee*2<=(maxsize-buff_occ_value):
                    signal=300#underflow
                elif rateee/2<=(maxsize-buff_occ_value):
                    signal=100#overflow
                else:
                	signal=(maxsize-buff_occ_value)#jo ha woh ha
                print("message recieves server: ",msg)
                map(putInQueue, list(msg))
            sendToChild(2,sock,signal)

except:
	print("Couldnot run the program due to connection issues.")
finally:
    print >>sys.stderr, 'closing socket'
    sock.close()