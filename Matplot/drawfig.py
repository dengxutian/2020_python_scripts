import matplotlib.pyplot as plt
import numpy as np
import math

#四元数转旋转矩阵
def quaternions2matrix(w, x, y, z):
    return np.array([
        [1-2*y*y-2*z*z, 2*x*y-2*z*w, 2*x*z+2*y*w], 
        [2*x*y+2*z*w, 1-2*x*x-2*z*z, 2*y*z-2*x*w], 
        [2*x*z-2*y*w, 2*y*z+2*x*w, 1-2*x*x-2*y*y]])

dataset = np.loadtxt('/home/dxt/Ultrasound/Data_Opt/sample_set.txt', dtype=np.float32)
pi = 3.14158365352208978
width_factor = 0.5 #调节线宽
a = plt.axes(projection='3d')
x = np.linspace(-1, 1)
y = (1-x**2)**0.5
a.plot3D(x, y, 0, 'gray')
a.plot3D(x, -y, 0, 'gray')

#画平面的圆
delta_range = np.arange(-1, 1 + 0.05, 0.05)*pi
for delta in delta_range:
    z = math.sin(delta)
    r = math.sqrt(1-z**2)
    x=np.linspace(-r, r)
    y = (r**2-x**2)**0.5
    a.plot3D(x, y, z, 'gray', linewidth = width_factor)
    a.plot3D(x, -y, z, 'gray', linewidth = width_factor)

#画纵向的圆
y = np.linspace(-1, 1)
z = (1-x**2)**0.5
x = np.zeros_like(y)
dots = np.array([x, y, z]).T
belta_range = np.arange(-1, 1, 0.05)*2*pi
for belta in belta_range:
    rotate_matrix = np.array([[math.cos(belta), -math.sin(belta), 0], [-math.sin(belta), math.cos(belta), 0], [0, 0, 1]])
    dots_ = np.dot(dots, rotate_matrix)
    a.plot3D(dots_[:,0], dots_[:,1], dots_[:,2], 'gray', linewidth = width_factor)
    a.plot3D(dots_[:,0], dots_[:,1], -dots_[:,2], 'gray', linewidth = width_factor)


#画出数据
dotset = np.empty(shape = (1,3))
for loop in range(dataset.shape[0]):
    dot_to_draw = np.array([0, 0, 1])
    dot_to_draw = np.dot(quaternions2matrix(dataset[loop,0], dataset[loop,1], dataset[loop,2], dataset[loop,3]), dot_to_draw)
    dotset = np.r_[dotset, np.array([dot_to_draw])]
dotset = dotset[1:dotset.shape[0], :]
a.plot3D(dotset[:,0], dotset[:,1], dotset[:,2], 'red', linewidth = width_factor)

# x = np.linspace(-1.5, 1.5)
# a.plot3D(x, np.zeros_like(x), np.zeros_like(x), 'gray', linewidth = width_factor*2)
# a.plot3D(np.zeros_like(x), x, np.zeros_like(x), 'gray', linewidth = width_factor*2)
# a.plot3D(np.zeros_like(x), np.zeros_like(x), x, 'gray', linewidth = width_factor*2)


a.quiver(0, 0, 0, 1, 0, 0, length=2, label='x')
a.quiver(0, 0, 0, 0, 1, 0, length=2)
a.quiver(0, 0, 0, 0, 0, 1, length=2)
a.text = (0, 0, 0, 1)

# plt.axis('off')
# a.view_init(90, 0)
plt.show()
# plt.savefig('test.jpg', dpi=1000)
