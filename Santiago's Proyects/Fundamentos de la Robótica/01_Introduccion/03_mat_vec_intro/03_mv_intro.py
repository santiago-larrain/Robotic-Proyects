#------------------------------------------------------------------------------#
# 03_mv_intro.py
# Introduction to basic matrix and vector operations.
# This code shows basic vector and matrix operations that can be performed
# in Python, similar to those of Matlab.
#
# For a complete list of tuple/array/vector/matrix operations see:
# http://docs.scipy.org/doc/numpy-dev/user/numpy-for-matlab-users.html
# http://docs.scipy.org/doc/numpy/reference/routines.math.html
# http://docs.scipy.org/doc/numpy/reference/generated/numpy.reshape.html
# http://docs.scipy.org/doc/numpy/reference/generated/numpy.sum.html#numpy.sum
#
# Miguel Torres Torriti (c) 2016.07.01
#------------------------------------------------------------------------------#

#import numpy as np
from numpy import *
#from scipy.integrate import odeint
#import matplotlib.pyplot as plt


# http://stackoverflow.com/questions/1534504/convert-variable-name-to-string
# Does not work when importing numpy using *, because the original eval definition gets changed.
def print_var_name(variable):
    for name in globals():
        if eval(name) == variable:
            #print(name)
            print(name,'\b:\n',variable)
            #return name

def pprint(variable): #pretty print
    print_var_name(variable)
    
def clear(j):
    print(' \n' * j)

#------------------------------------------------------------------------------#    
clear(100)
print("\n --- Basic arrays and matrices and operations ---")    

p0=(1,0,0) # Defining a tuple
print("p0 is a tuple:\n", p0)

M1 = array([[.6,.3,0],  # first row
              [.4,.7,0],  # second row
              [ 0, 0,1]]) # third row
print("M1:\n", M1)
print("M1[:,1:2]:\n", M1[:,1:2])

v1 = dot(M1,p0) # Multiplying a matrix times a tuple
                  # yields a column vector of 'array' type.

print("v1 = M1*p0:\n", v1)

v2 = dot(M1,v1) # Multiplying a matrix times a vector or 'array' type
                  # yields a column vector of 'array' type.
                  
print("v2 = M1*v1:\n", v2)

v3 = v1*v2
print("v3 = v1.*v2 (element-wise multiplication):\n", v3)

v4 = v1+v2
print("v4 = v1+v2:\n", v4)

s1 = sum(M1)
print("s1 = sum(M1):\n", s1)

s2 = sum(v2)
print("s2 = sum(v2):\n", s2)

v5 = v1/s1;
print("v4 = v1/s1:\n", v5)

input("Press a key to continue...\n")

#------------------------------------------------------------------------------#
clear(100)
print("\n --- Array/matrix concatenation ---")

v6 = r_[v1,v2]   # Concatenate the rows of v1 followed by the rows of v2
print("v6 = [v1; v2]:\n", v6)

M2 = c_[M1,c_[v1,v2]] # Concatenate the columns of M1 followed by the 
                      # the concatenation of the columns of v1 and v2
                      # to create a larger matrix.

print("M2 = [M1 v1 v2]:\n", M2)

v7 = array(reshape(v1,(3,1)))
print("v7 = array(reshape(v1,(3,1))):\n", v7)

M3 = v7
v8 = reshape(v2,(3,1))
print("v8 = reshape(v2,(3,1)):\n", v8)

M3 = append(M3,v8,axis=1)
print("M3 = append(v6,v7,axis=1):\n", M3)

v9 = reshape(v3,(3,1))
print("v9 = reshape(v3,(3,1)):\n", v9)

M3 = append(M3,v9,axis=1)
print("M3 = append(M3,v8,axis=1):\n", M3)

M4 = c_[c_[v7,v8],v9]
print("M4 = c_[c_[v7,v8],v9]:\n", M4)

M5 = c_[c_[v1,v2],v3]
print("M5 = c_[c_[v1,v2],v3]:\n", M5)
print("M5 was built in less steps than M3... try not to use reshape+append!")

input("Press a key to continue...\n")

#------------------------------------------------------------------------------#
clear(100)
print("\n--- Some useful arrays and matrices---")

ones3x4 = ones((3,4))*7;
print("ones3x4:\n", ones3x4)

ones4x1 = ones(4)/2;
print("ones4x1:\n", ones4x1)

eye3 = eye(3)/5;
print("eye3:\n", eye3)

input("Press a key to continue...\n")

#------------------------------------------------------------------------------#
clear(100)
print("\n--- Some linear algebra and other operations ---")

M1inv = linalg.inv(M1)
print("M1inv:\n", M1inv)

II3 = M1.dot(M1inv)
print("II3 = M1*M1^{-1}:\n", II3) 

v1norm2 = linalg.norm(v1)**2
print("|v1|^2:\n", v1norm2) 

input("Press a key to continue...\n")

#------------------------------------------------------------------------------#
clear(100)
print("\n--- Stack of matrices ---")

matrix_stack=zeros((6,3,3),order='F') # Stack of 6 matrices 3x3. 
matrix_stack[2,:,:] = M5
matrix_stack[3,:,:] = eye3
print("matrix_stack[:,:,:]:\n", matrix_stack)

print("matrix_stack[:,:,0]\n", matrix_stack[:,:,0])
