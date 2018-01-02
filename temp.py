import matplotlib.pyplot as plt
import numpy as np
from math import *
import geometry_op as geo
from math import sqrt

top_left=[ 929 ,307]
top_right= [1023 ,362]
bottom_left =  [611, 334]
bottom_right = [814, 451]

top_left_x,top_left_y = top_left
top_right_x,top_right_y = top_right
bottom_left_x, bottom_left_y = bottom_left
bottom_right_x, bottom_right_y = bottom_right

raw_points = [top_left,top_right,bottom_left,bottom_right]

x = np.arange(-2000,2000)
y1 = x/sqrt(3)
y2 = -x*sqrt(3)+1000

# 斜坐标轴
plt.grid()
plt.plot(x,y1,'k')
plt.plot(x,y2,'k')
# 画一个点
i = 0
names = ['tl','tr','bl','br']
for i in range(len(raw_points)):
    x,y = raw_points[i]
    plt.plot(x,y,'ko')
    plt.text(x,y,names[i])
        
plt.axis('square')
plt.gca().invert_yaxis()
plt.plot(x,y,'r*')

def plot_line(k,b):
    x = np.arange(-1000,1500,10)
    y = x*k + b
    plt.plot(x,y)

joint_x, joint_y = geo.joint((bottom_left_x,bottom_left_y),
                             (top_left_x,top_left_y,top_right_x,top_right_y))
if joint_x < top_left_x:
    top_left_x,top_left_y = joint_x,joint_y
else:
    joint_x, joint_y = geo.joint((top_left_x,top_left_y),
                             (bottom_left_x,bottom_left_y,bottom_right_x,bottom_right_y))
    bottom_left_x,bottom_left_y = joint_x,joint_y
    

joint_x, joint_y = geo.joint((bottom_right_x,bottom_right_y),
                             (top_left_x,top_left_y,top_right_x,top_right_y))

if joint_x > top_right_x:
    top_right_x,top_right_y = joint_x,joint_y
else:
    joint_x, joint_y = geo.joint((top_right_x,top_right_y),
                             (bottom_left_x,bottom_left_y,bottom_right_x,bottom_right_y))
    bottom_right_x,bottom_right_y = joint_x,joint_y
    
    

plt.plot(top_left_x,top_left_y,'y>')
plt.plot(top_right_x,top_right_y,'y>')
plt.plot(bottom_left_x,bottom_left_y,'y>')
plt.plot(bottom_right_x,bottom_right_y,'y>')

plt.show()













