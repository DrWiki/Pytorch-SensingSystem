
import csv
class test:
    def __init__(self):
        self.csvfile_Go = open(f"1.csv", "w")
        self.writer_Go = csv.writer(self.csvfile_Go)
        self.writer_Go.writerow(["Motionnum", "Quat0", "Quat1", "Quat2", "Quat3"])
        # self.writer_Go.writerow(["Motionnum",
        #                     "Quat0", "Quat1", "Quat2", "Quat3",
        #                     "Torque0", "Torque1", "Torque2", "Torque3", "Torque4", "Torque5", "Torque6", "Torque7",
        #                     "Torque8", "Torque9", "Torque10", "Torque11",
        #                     "q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "q11",
        #                     "dq0", "dq1", "dq2", "dq3", "dq4", "dq5", "dq6", "dq7", "dq8", "dq9", "dq10", "dq11"])

        # self.writer_Go.writerows([[1] * 5])



if __name__ == '__main__':
    t = test()
