# -*- coding:utf-8 -*-
# from mpl_toolkits.mplot3d import axes3d
# import matplotlib.pyplot as plt
# from matplotlib import cm
#
# fig = plt.figure()
# ax = fig.gca(projection='3d')
# X, Y, Z = axes3d.get_test_data(0.05)
# ax.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.3)
# cset = ax.contour(X, Y, Z, zdir='z', offset=-100, cmap=cm.coolwarm)
# cset = ax.contour(X, Y, Z, zdir='x', offset=-40, cmap=cm.coolwarm)
# cset = ax.contour(X, Y, Z, zdir='y', offset=40, cmap=cm.coolwarm)
#
# ax.set_xlabel('X')
# ax.set_xlim(-40, 40)
# ax.set_ylabel('Y')
# ax.set_ylim(-40, 40)
# ax.set_zlabel('Z')
# ax.set_zlim(-100, 100)
#
# plt.show()

# import scipy.misc
# import matplotlib.pyplot as plt
# lena = scipy.misc.lena()
# acopy = lena.copy()
# aview = lena.view()
# plt.subplot(221)
# plt.imshow(lena)
# plt.subplot(222)
# plt.imshow(acopy)
# plt.subplot(223)
# plt.imshow(aview)
# aview.flat=0
# plt.subplot(224)
# plt.imshow(aview)
# plt.show()

#2016-10-30
import numpy as np
from scipy.stats import scoreatpercentile
# data = np.loadtxt(u"E:\\aapl.csv",delimiter=',',usecols=(1,2,3,4,5,6),skiprows=1,unpack=True)#usecols=()参数为那一列，可以写多列
# print "Max method",data.max()
# print "Max function",np.max(data)
# print "Min method",data.min()
# print "Min function",np.min(data)
# print "Mean method ",data.mean()
# print "Mean function",np.mean(data)
# print "Std method",data.std()
# print "Std function",np.std(data)

#2016-11-1
import numpy as np
# A=np.mat("2 4 6;4 2 6;10 -4 18")
# print "A\n", A
# inverse = np.linalg.inv(A)
# print "inverse of A\n",inverse
# print "check\n",A*inverse
# print "Error \n",A*inverse-np.eye(3)#np.eye(3)表示3X3单位矩阵

# A=np.mat("1 -2 1;0 2 -8;-4 5 9")
# print "A\n",A
# b = np.array([0,8,-9])
# print "b\n",b
# x = np.linalg.solve(A,b)#linalg下面的solve()方法是解决现行方程组的解
# print "solution",
# print "check\n",np.dot(A,x)#dot是点乘x

# A=np.mat("3 -2;1 0")
# print "A\n",A
# print "Eigenvalues",np.linalg.eigvals(A)#linalg下面的eigvals是用来求特征值的
# eigenvalues,eigenvectors = np.linalg.eig(A)#eig()函数是求特征值加特征向量
# print "eigenvalues\n",eigenvalues
# print "eigenvectors\n",eigenvectors

#用二项式分布进行博弈
import numpy as np
from matplotlib.pyplot import plot,show
cash = np.arange(10000)
cash[0]=1000
outcome = np.random.binomial(9,0.5,size=len(cash))#nomomial为二项分布P(N)=(nN)pN(1−p)n−N 9 0.5分别对应公式中的n和p n为所有的可能性（范围） p即为每一次的概率 http://blog.csdn.net/lanchunhui/article/details/50172659
for i in range(1,len(cash)):
    if outcome[i]<5:
        cash[i] = cash[i-1]-1
    elif outcome[i]<10:
        cash[i] = cash[i-1]+1
    else:
        raise AssertionError("Unexpected outcome"+outcome)
print outcome.min(),outcome.max()
plot(np.arange(len(cash)), cash)
show()
