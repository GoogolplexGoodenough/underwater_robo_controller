import socket
import time
import socket
import _thread

class comunicator:
    def __init__(self, host_ip = '192.168.137.2', port = 8008, selfport = 8010, sleep_time = 0.1):
        self.dest = (host_ip, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", selfport))
        self.msg = "0:0:0:0:0"
        self.sleep_time = sleep_time
        _thread.start_new_thread(self.recv_msg, ())

    def set_sleep_time(self, sleep_time):
        self.sleep_time = sleep_time

    def send_msg(self, msg):
        # print(msg)
        self.sock.sendto(msg.encode(), self.dest)
        time.sleep(self.sleep_time)

    #### this function maynot work ...
    def recv_msg(self):
        while 1:
            try:
                msg = self.sock.recvfrom(1024).decode()
                self.msg = msg
                print(msg)
            except:
                pass
    
                        
if __name__ == "__main__":
    c = comunicator()

    # camera 90-180 mid 150
    # while 1:

    for i in range(120, 180, 1):
        # print(i)
        c.send_msg("100:100:100:100:{}".format(str(i).zfill(3)))

        time.sleep(0.1)
        # c.send_msg("100:100:100:100:150")

    for i in range(120, 180, 1):
        # print(i)
        c.send_msg("100:100:100:100:{}".format(str(300 - i).zfill(3)))

        time.sleep(0.1)

