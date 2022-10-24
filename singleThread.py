import Leg.Leg_v3_2 as Leg
import cv2
import time
from threading import Thread
from visdom import Visdom
import csv
import os
import UDP.UDP as UDP

use_show = False
use_visdom = False
use_UDP = False


topic = "LS_Hybrid" # Yaw, Pitch, Roll, Hybrid
folder = f"./log/{topic}"
# 判断结果
if not os.path.exists(folder):
    os.makedirs(folder)
    print("OK_folder")

name = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())

if use_UDP:
    Get_Go = UDP.UdpLogic(topic, name)
    Get_Go.udp_server_start()

if use_visdom:
    vis = Visdom(env=topic)
    vis.line([[0., 0., 0., 0.]], [0.], win='mean_dist_x',
             opts=dict(title='mean_dist_x', legend=['leg0', 'leg1', 'leg2', 'leg3']))
    vis.line([[0., 0., 0., 0.]], [0.], win='mean_dist_y',
             opts=dict(title='mean_dist_y', legend=['leg0', 'leg1', 'leg2', 'leg3']))
    vis.line([[0., 0., 0., 0.]], [0.], win='mean_brightness',
             opts=dict(title='mean_brightness', legend=['leg0', 'leg1', 'leg2', 'leg3']))
    vis.line([[0., 0., 0., 0.]], [0.], win='max_brightness',
             opts=dict(title='max_brightness', legend=['leg0', 'leg1', 'leg2', 'leg3']))
    distx_list = [0, 0, 0, 0]
    disty_list = [0, 0, 0, 0]
    brightness_list = [0, 0, 0, 0]
    max_brightness_list = [0, 0, 0, 0]
    frame_num = [0, 0, 0, 0]

folder_video = f"./video/{topic}/{name}"

Legs = [Leg.Leg(0, folder_video)]
flag = True
leg_dex = [0]

def show():
    global flag, leg_dex
    while flag:
        for i in leg_dex:
            Legs[i].show()
        keyboard = cv2.waitKey(1)
        if keyboard == 27:
            flag = False

def Legthread(i):
    global flag, leg_dex,distx_list, disty_list, brightness_list, max_brightness_list, frame_num
    ##save data as csv
    csvfile = open(f"{folder}/Leg_" + str(i) + f"_{name}.csv", "w")
    writer = csv.writer(csvfile)
    writer.writerow(["frame_num", "dist_x", "dist_y", "brightness", "max_bright"])
    while flag:
        t = time.time()
        Legs[i].read()
        distx_list[i], disty_list[i], brightness_list[i], max_brightness_list[i], frame_num[i] = Legs[i].resolve_disfeild()
        #先写入columns_name
        #写入多行用writerows
        writer.writerows([[frame_num[i], distx_list[i], disty_list[i], brightness_list[i], max_brightness_list[i]]])
        print("Whole:",time.time()-t)

def visdom_show():
    global flag, dist_x, dist_y, brightness, max_bright
    local_num = 0
    while flag:
        vis.line([distx_list], [local_num], win='mean_dist_x', update='append')
        vis.line([disty_list], [local_num], win='mean_dist_y', update='append')
        vis.line([brightness_list], [local_num], win='mean_brightness', update='append')
        vis.line([max_brightness_list], [local_num], win='max_brightness', update='append')
        local_num = local_num + 1
        time.sleep(0.0000001)
    # Get_Go.udp_close()

def UDP_save():
    global flag

    Get_Go.csvfile_Go = open(f"{Get_Go.folder_Go}/Go_{Get_Go.name}.csv", "w")
    Get_Go.writer_Go = csv.writer(Get_Go.csvfile_Go)
    # Get_Go.writer_Go.writerow(["Motionnum","Quat0", "Quat1", "Quat2", "Quat3"])
    Get_Go.writer_Go.writerow(["Motionnum",
                             "Quat0", "Quat1", "Quat2", "Quat3",
                             "Torque0", "Torque1", "Torque2", "Torque3", "Torque4", "Torque5", "Torque6", "Torque7",
                             "Torque8", "Torque9", "Torque10", "Torque11",
                             "q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "q11",
                             "dq0", "dq1", "dq2", "dq3", "dq4", "dq5", "dq6", "dq7", "dq8", "dq9", "dq10", "dq11"])
    # Get_Go.writer_Go.writerows([[1] * 40])
    Get_Go.udp_socket.setblocking(False)
    while flag:
        # print("-----------------")
        try:
            recv_msg, recv_addr = Get_Go.udp_socket.recvfrom(164)
        except Exception as ret:
            pass
        else:
            # print(recv_msg, type(recv_msg),len(recv_msg))
            Get_Go.data_split(recv_msg)
            Go_data = Get_Go.data_split(recv_msg)
            Get_Go.writer_Go.writerows([list(Go_data)])

        # a, b, c, d, e, f,_,_ = struct.unpack('<ffffffcc', recv_msg)
        # print(a,b,c,d,e,f)
        # msg = recv_msg.decode('utf-8')
        # time.sleep(0.005)

if __name__ == '__main__':
    Tshow = Thread(target=show, name='show')
    Tvis = Thread(target=visdom_show, name='vis')
    TUDP = Thread(target=UDP_save, name='UDP_save')
    Tlegs = [Thread(target=Legthread, name='Legthread'+str(i), args=(i,)) for i in leg_dex]


    Tshow.start()
    if use_visdom: Tvis.start()
    if use_UDP: TUDP.start()
    [Tlegs[i].start() for i in leg_dex]


    [Tlegs[i].join() for i in leg_dex]
    Tshow.join()
    if use_visdom: Tvis.join()
    if use_UDP: TUDP.join()
