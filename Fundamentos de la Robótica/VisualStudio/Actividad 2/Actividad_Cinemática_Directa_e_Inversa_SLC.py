import numpy as np
import pygame       # Load pygame for IO-interfacing 
                    # (keyboard, mouse, joystick, screen, audio)

def R(t):
    theta = t*np.pi/180
    return np.array([[np.cos(theta), -np.sin(theta)], 
                     [np.sin(theta), np.cos(theta)]])

def preguntas_1y2():
    ### P1: 
    P1_2_rotado = R(30 - 90).dot(np.array([0.4,0]))
    P1_1_rotado = R(30).dot(np.array([0.6,0]))
    P1_2_rotado_trasladado = P1_2_rotado + P1_1_rotado
    print("P1:", P1_2_rotado_trasladado)

    ### P2: 
    P2_2_rotado = R(78 + 36).dot(np.array([0.4,0]))
    P2_1_rotado = R(78).dot(np.array([0.6,0]))
    P2_2_rotado_trasladado = P2_2_rotado + P2_1_rotado
    print("P2:", P2_2_rotado_trasladado)

def matrices():
    A = np.array([[1,2,3], [4,5,6], [7,8,9]])
    v = np.array([1,2,3])
    u = np.array([2,5,7])

    print("A*v", A*v)
    print("A.dot(v)", A.dot(v))
    if (np.array([4,30,10])*0.0001 < v*0.001).any():
        print("v*0.0001", np.array([4,30,10])*0.0001 < v*0.001)
    a, b = np.array([v, u])
    print(a)
    print(b)


if __name__ == "__main__": preguntas_1y2()