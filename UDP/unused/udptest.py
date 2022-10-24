#!/usr/bin/env python
import socket
address=('192.168.3.18',19999)
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(address)
while 1:
	data,addr=s.recvfrom(2048)
	if not data:
		break
	print ("got data from",addr)
	print (data)
s.close()
# ————————————————
# 版权声明：本文为CSDN博主「零丁若叹」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/u011608357/article/details/19776405