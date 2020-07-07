from scipy.io import loadmat
from ssc import ssc1,ssc2,ssc
A_three_tank = [[1,1,0],[1,1,1],[0,1,1]]
B_three_tank = [[1,0],[0,0],[0,1]]
assert ssc1(A_three_tank,B_three_tank)==True
assert ssc2(A_three_tank,B_three_tank)==True
print(ssc(A_three_tank,B_three_tank))