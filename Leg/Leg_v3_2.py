import cv2
import numpy as np
from operator import le
from string import printable
import cv2 as cv
import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import cdist
import time

class Leg:
    def __init__(self, ind, path):
        self.cap = cv2.VideoCapture(ind)
        self.cap.set(cv2.CAP_PROP_EXPOSURE, 70)

        self.index = ind
        self.Origin = None
        self.imgae = None
        self.draw = None
        self.Backg = None
        self.Backg_show = None
        self.is_back_ready = False
        self.Gray = None
        self.bin = None
        self.frame_num = -1
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        self.out_origin_ = cv2.VideoWriter(f'./{path}_origin-{self.index}.mp4', self.fourcc, 20.0,(int(self.cap.get(3)), int(self.cap.get(4))), True)
        self.out_binary_ = cv2.VideoWriter(f'./{path}_binary-{self.index}.mp4', self.fourcc, 20.0,(int(self.cap.get(3)), int(self.cap.get(4))), True)
        self.out_show_ = cv2.VideoWriter(f'./{path}_show-{self.index}.mp4', self.fourcc, 20.0,(int(self.cap.get(3)), int(self.cap.get(4))), True)
        # self.out_display_ = cv2.VideoWriter(f'./{path}_dispaly.mp4', self.fourcc, 20.0,(int(self.cap.get(3)), int(self.cap.get(4))), True)
        self.Points_origin = []
        self.Area_origin = []
        # self.Points_origin = []
        self.Points0 = []
        self.Area0 = []

        self.Area1 = []
        self.Points1 = []
        self.Area_list = []
        self.Points_list = []
        self.kernel_e = np.ones((4, 4), dtype=np.uint8)
        self.kernel_d = np.ones((4, 4), dtype=np.uint8)
        self.t0 = 0

    def read(self):

        hot_t0 = time.time()
        ret, self.Origin = self.cap.read()
        # print(ret)
        if ret == False:
            print(ret)
            self.Origin = None
        else:
            self.imgae = self.Origin.copy()
            self.draw = self.Origin.copy()
        self.out_origin_.write(self.Origin)
        print("Read:",time.time()-hot_t0)

    def resolve_disfeild(self):
        if self.Origin is None:
            return

        self.frame_num = self.frame_num + 1
        hot_t0 = time.time()

        self.Gray = cv.cvtColor(self.imgae, cv.COLOR_BGR2GRAY)
        # gray = cv.convertScaleAbs(gray, alpha=2.5, beta=1)

        _, self.bin = cv.threshold(self.Gray, 16, 255, cv.THRESH_BINARY)
        self.binBGR = cv.cvtColor(self.bin, cv.COLOR_GRAY2BGR)
        self.out_binary_.write(self.binBGR)

        binary = self.bin.copy()
        #binary = cv.erode(binary, self.kernel_e, iterations=1)
        #binary = cv.dilate(binary, self.kernel_d, iterations=1)
        binary = cv.morphologyEx(binary, cv.MORPH_OPEN, self.kernel_e)
        print("Preprocess:",time.time()-hot_t0)

        contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        area = []
        coordinate = []
        selected_con = []


        hot_t0 = time.time()

        for i in range(len(contours)):
            a = cv.contourArea(contours[i])
            # print(a)
            if a < 90:
                continue
            area.append(abs(a))
            M = cv.moments(contours[i])
            cx = M['m10'] / (M['m00'] + 10e-5)
            cy = M['m01'] / (M['m00'] + 10e-5)
            coordinate.append([int(cx), int(cy)])
            selected_con.append(contours[i])
            # temp = 1.00
            # print(type(cx),type(temp))
            cv.circle(self.draw, (int(cx), int(cy)), 3, (255, 0, 0), -1)
            cv.drawContours(self.draw, contours, i, (0, 0, 255), 3)
        print("Visit contours:",time.time()-hot_t0)

        self.Points_list.append(coordinate)
        self.Area_list.append(area)

        if (len(self.Points_list) == 5):
            self.Points1 = self.Points_list.pop(0)
            self.Area1 = self.Area_list.pop(0)
        self.Points0 = coordinate.copy()
        self.Area0 = area.copy()


        # cost = np.ones([len(self.Points0), len(self.Points1)])

        # for i in range(len(self.Points0)):
        #     for j in range(len(self.Points1)):
        #         cost[i, j] = np.sqrt(
        #             (self.Points1[j][0] - self.Points0[i][0]) ** 2 + (self.Points1[j][1] - self.Points0[i][1]) ** 2)
        # row_ind, col_ind = linear_sum_assignment(cost)

        # dist = 0
        '''for x, y in zip(row_ind, col_ind):
            # cv.arrowedLine(self.Backg, self.Points1[y], Points0[x],  (0, 0, 255), 2, 8, 0, 0.5)
            # cv.arrowedLine(self.Backg, Points0[x], self.Points_origin[y], (0, 255, 0), 2, 8, 0, 0.5)
            dist += np.sum(np.square(np.array(self.Points0[x])-np.array(self.Points1[y])))
        dist = dist/(len(self.Points0)+10e-5)
        cv.putText(self.Backg, str(round((1 / (time.time() - self.t0)), 3)) + "Hz", (20, 20), 1, 1.5, (0, 0, 255), 2)'''

        if self.frame_num < 10 and len(coordinate)>30:
            self.Points_origin = coordinate.copy()
            self.Area_origin = area.copy()
        hot_t0 = time.time()

        cost2 = np.ones([len(self.Points0), len(self.Points_origin)])
        '''for i in range(len(self.Points0)):
            for j in range(len(self.Points_origin)):
                cost2[i, j] = np.sqrt(
                    (self.Points_origin[j][0] - self.Points0[i][0]) ** 2 + (self.Points_origin[j][1] - self.Points0[i][1]) ** 2)'''
        array_Points_origin = np.asarray(self.Points_origin)
        array_Points0 = np.asarray(self.Points0)
        cost2 = cdist(array_Points0, array_Points_origin, 'euclidean')
        print("Cal cost:",time.time()-hot_t0)
        hot_t0 = time.time()

        row_ind2, col_ind2 = linear_sum_assignment(cost2)
        print("Match:",time.time()-hot_t0)

        dist_x = 0
        dist_y = 0
        brightness = 0
        max_bright = 0
        maxbright_coord = []
        hot_t0 = time.time()
        self.is_back_ready = False
        self.Backg = cv.cvtColor(binary, cv.COLOR_GRAY2BGR).copy()

        for x, y in zip(row_ind2, col_ind2):
            temp_c = int(50+205*(self.Area0[x]-self.Area_origin[y])/self.Area_origin[y])
            if temp_c > max_bright:
                max_bright = temp_c
            cv.drawContours(self.Backg, selected_con, x, (temp_c, temp_c, 0), -1)
            cv.arrowedLine(self.Backg, self.Points_origin[y], self.Points0[x] , (0, 0, 255), 2, 8, 0, 0.5)
            cv.arrowedLine(self.Backg, self.Points_origin[y], (self.Points0[x][0],self.Points_origin[y][1]) , (0, 255, 0), 2, 8, 0, 0.5)
            cv.arrowedLine(self.Backg, self.Points_origin[y], (self.Points_origin[y][0],self.Points0[x][1]) , (255, 0, 0), 2, 8, 0, 0.5)
            dist_x += self.Points0[x][0] - self.Points_origin[y][0]
            dist_y += self.Points0[x][1] - self.Points_origin[y][1]
            brightness += temp_c * self.Area0[x]
        self.is_back_ready = True
        print("Cal force:",time.time()-hot_t0)

        dist_x = dist_x/55
        dist_y = dist_y/55
        brightness = brightness/(600*800)
        print(f"{self.index}:",str(round((1 / (time.time() - self.t0)), 3)) + "Hz")
        self.t0 = time.time()
        return dist_x, dist_y, brightness, max_bright, self.frame_num

    def predict_force(self):
        pass

    def show(self):
        # if self.Origin is not None:
        #     cv2.imshow(f'Origin_self{str(self.index)}', self.Origin)
        # if self.imgae is not Noe:
        #     cv2.imshow(f'imgae_self{str(self.index)}', self.imgae)
        # if self.draw is not None:
        #     cv2.imshow(f'draw_self{str(self.index)}', self.draw)
        if self.Backg is not None:
            while self.is_back_ready == False:
                time.sleep(0.0000001)
            cv2.imshow(f'Backg_self{str(self.index)}', self.Backg)
        # if self.Gray is not None:
        #      cv2.imshow(f'Gray_self{str(self.index)}', self.Gray)
        # if self.bin is not None:
        #      cv2.imshow(f'bin_self{str(self.index)}', self.bin)
        self.out_show_.write(self.Backg)

