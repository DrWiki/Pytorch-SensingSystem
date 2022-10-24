import socket
import struct
import stop
import os


class UdpLogic:
    def __init__(self, topic, name):
        self.udp_socket = None
        self.udp_sever_th = None
        self.udp_port1 = 19999
        self.udp_ip1 = "127.0.0.1"
        self.link = False
        self.folder_Go = f"./Syn_GoLog_UDP/{topic}"
        self.topic = topic
        self.name = name
        # 判断结果
        if not os.path.exists(self.folder_Go):
            os.makedirs(self.folder_Go)
            print("OK_UDP_folder")

    def data_split(self,msg):
        Go_data = struct.unpack("<i"+"f"*40, msg)
        # print(Go_data)
        return Go_data

    def udp_server_start(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            address = ('', self.udp_port1)
            self.udp_socket.bind(address)
            self.link = True
        except Exception as ret:
            print('请检查端口号\n')

    def udp_close(self):
        try:
            stop.stop_thread(self.udp_sever_th)
        except Exception:
            pass

        try:
            self.udp_socket.close()
            if self.link is True:
                msg = '已断开网络\n'
                self.signal_write_msg.emit(msg)
        except Exception as ret:
            pass
        self.link = False

if __name__ == '__main__':
    myudp = UdpLogic()
    myudp.udp_server_start()

