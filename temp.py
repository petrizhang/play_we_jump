import matplotlib.pyplot as plt
import numpy as np
from math import *
from geometry_op import axis_transform as r
from math import sqrt

top_left=[ 929 ,307]
top_right= [1023 ,362]
bottom_left =  [611, 334]
bottom_right = [814, 451]

raw_points = [top_left,top_right,bottom_left,bottom_right]

#x = np.arange(-2000,2000)
#y1 = x/sqrt(3)
#y2 = -x*sqrt(3)+1000
#
## 斜坐标轴
#plt.grid()
#plt.plot(x,y1,'k')
#plt.plot(x,y2,'k')
## 画一个点
#i = 0
#names = ['tl','tr','bl','br']
#for i in range(len(raw_points)):
#    x,y = raw_points[i]
#    plt.plot(x,y,'ko')
#    plt.text(x,y,names[i])
#        
#plt.axis('square')
#plt.gca().invert_yaxis()
#plt.plot(x,y,'r*')
#plt.show()


def kb_Of_line(p1,p2):
    """"""
    x1,y1 = p1
    x2,y2 = p2
    k = (y2-y1)/(x2-x1)
    b =  y1 - k*x1
    return k,b
    
def line_joint(k1,b1,k2,b2):
    # y = k1*x + b1
    # y = k2*x + b2
    # -k1*x + y = b1
    # -k2*x + y = b2
    left = [[k1,1],
     [k2,1]]
    right = [[b1],[b2]]
    return np.linalg.solve(left,right)[:,0]
    
top_k,top_b = kb_of_line(top_left,top_right)
bottom_k,bottom_b = kb_of_line(bottom_left,bottom_right)


print(line_joint(1,1,-1,1))
print(kb_Of_line((-1,0),(0,1)))















