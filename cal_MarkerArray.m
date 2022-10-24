%% 说明
% 坐标求算的话也用程序计算，内球壳直径r0, 
% 点之间的直线距离d, 第i圈的点的阵列数量，si

clear
clc
close all
%% 参数设定
r0 = 17.5;        % in mm
d = 3;          % in mm
s1=1; % 第1圈数量
s2=6;
s3=12;
s4=16;
s5=20; % 第5圈数量
s = [s1,s2,s3,s4,s5];

%% 思路
% 直接先用球坐标系，求出每个点的球坐标
% r: 球的半径
% phi: 360 deg 等分成si份 （赤道）
% theta: 利用三角形关系，余弦定理 （经线）
% 然后将球坐标转换成直角坐标: sph2cart函数

%% 计算r,phi,theta，并转成直角坐标系
% r坐标
r_in = r0;      % 球壳内半径，其实就是每个阵列的r坐标
r = r0*ones(1, sum(s));   % 做成行向量

% theta: 计算每一圈阵列的theta坐标（rad）
% a = b = r_in, c = d
delta_theta = cal_deg_cosine_theorem(r_in, r_in, d);    % in rad
theta1 = pi/2 * ones(1, s1);
theta2 = (pi/2 - delta_theta) * ones(1, s2);
theta3 = (pi/2 - 2*delta_theta) * ones(1, s3);
theta4 = (pi/2 - 3*delta_theta) * ones(1, s4);
theta5 = (pi/2 - 4*delta_theta) * ones(1, s5);
theta = [theta1, theta2, theta3, theta4, theta5];   % 做成行向量

% phi坐标: 计算每一圈阵列的phi坐标（rad）
eps0 = 0.0001;  % 一个极小值，消除2*pi这一点
phi1 = pi/2 : 2*pi/s1 : 2*pi+pi/2-eps0;
phi2 = pi/2 : 2*pi/s2 : 2*pi+pi/2-eps0;
phi3 = pi/2 : 2*pi/s3 : 2*pi+pi/2-eps0;
phi4 = pi/2 : 2*pi/s4 : 2*pi+pi/2-eps0;
phi5 = pi/2 : 2*pi/s5 : 2*pi+pi/2-eps0;
phi = [phi1, phi2, phi3, phi4, phi5];   % 做成行向量

% 将球坐标系转换为直角坐标系
[x, y, z] = sph2cart(phi, theta, r);

%% 输出xyz坐标（直角坐标）
% 输出阵列的x, y, z值
% x, y, z

% % 将x, y, z轴的值写入txt文档中
% fid1=fopen('xyz.txt','w');%写入文件路径
% % 第一行：
% fprintf(fid1,'x(mm)\ty(mm)\tz(mm)\n');
% 
% % 输出直角坐标
% for ii = 1:length(x)
%     fprintf(fid1, '%.4f\t%.4f\t%.4f\n', x(ii), y(ii),z(ii));
% end

% 将x, y, z轴的值写入csv文档中
% Create a csv file
fid=fopen('result_xyz.csv','w');
if fid<0
	errordlg('File creation failed','Error');
end
% Write the data
str=["x(mm)","y(mm)","z(mm)"];
fprintf(fid, '%s,%s,%s\n', str(1), str(2), str(3));
for ii = 1:length(x)
	fprintf(fid,'%.4f,%.4f,%.4f\n', x(ii), y(ii), z(ii));
end
fclose(fid);

% 输出球坐标
% 如果需要输出阵列中每个点的球坐标，我马上写。代码原理和上面相同。
%% 作图：plot3
% 画出阵列
plot3(x, y, z, 'ro', LineWidth=2);
hold on

% 画出半球
[x_s, y_s, z_s] = sphere(50);
% sphere的参数就是有多少个面，这个可以调。如果要这个圆更圆滑，那就调大一点。

x_s = r_in * x_s;
y_s = r_in * y_s;

z_s(find(z_s < 0)) = 0; % 只要上半球
z_s = r_in * z_s;
surf(x_s, y_s, z_s) % 画出半球
alpha(0.1)

% 图像设置
axis([-r_in, r_in, -r_in, r_in, 0, r_in])
xlabel('x/mm');
ylabel('y/mm');
zlabel('z/mm');
title('传感器阵列图')
%% 自定义函数：通过余弦定理计算角度
function angle_c_rad = cal_deg_cosine_theorem(a, b, c)   % 返回值的单位是rad（弧度）
    cos_angle_c = (a.^2 + b.^2 - c.^2) ./ (2.*a.*b);
    angle_c_rad = acos(cos_angle_c);
end
