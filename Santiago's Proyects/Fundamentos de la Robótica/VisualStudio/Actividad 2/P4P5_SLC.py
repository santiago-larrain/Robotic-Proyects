import numpy as np

def R(t):
    theta = t*np.pi/180
    return np.array([[np.cos(theta), -np.sin(theta)], 
                     [np.sin(theta), np.cos(theta)]])
                

#    P1_rotado = R(a1).dot(l1)
#    P2_rotado = R(a1 + a2).dot(l2)

def angulos_optimos(p_optimo, l_base, q_inicial):
    ## p_optimo = [p*_x, p*_y]
    ## l_base = (l1, l2)
    ## q_inicial = [q1, q2]

    def J_q(q_0):
        t_1 = q_0[0] * np.pi / 180
        t_2 = q_0[1] * np.pi / 180
        return np.array([[-l1*np.sin(t_1) - l2*np.sin(t_1 + t_2), -l2*np.sin(t_1 + t_2)],
                         [l1*np.cos(t_1) + l2*np.cos(t_1 + t_2), l2*np.cos(t_1 + t_2)]])


    epsilon = 1e-10
    l1, l2 = l_base
    q_viejo = q_inicial
    t1 = q_viejo[0] * np.pi / 180
    t2 = q_viejo[1] * np.pi / 180
    p_actual = np.array([l1*np.cos(t1) + l2*np.cos(t1 + t2),
                         l1*np.sin(t1) + l2*np.sin(t1 + t2)])
    #print(f"p: {p_actual}\nq: {q_viejo}\n-------------")

    q_nuevo = q_viejo + np.linalg.pinv(J_q(q_viejo)).dot(p_optimo - p_actual)
    
    while ((p_optimo - p_actual) > epsilon).any() and \
          ((q_nuevo - q_viejo) > epsilon).any():
        
        q_viejo = q_nuevo
        
        t1 = q_viejo[0] * np.pi / 180
        t2 = q_viejo[1] * np.pi / 180
        p_actual = np.array([l1*np.cos(t1) + l2*np.cos(t1 + t2),
                         l1*np.sin(t1) + l2*np.sin(t1 + t2)])
        
        q_nuevo = q_viejo + np.linalg.pinv(J_q(q_viejo)).dot(p_optimo - p_actual)

    return q_nuevo

def pregunta_4():
    Q = angulos_optimos(np.array([0, 0.5]), (0.6, 0.4), np.array([-25,25]))
    P2_rotado = R(Q[0] + Q[1]).dot(np.array([0.4,0]))
    P1_rotado = R(Q[0]).dot(np.array([0.6,0]))
    P = P1_rotado + P2_rotado
    print(f"q = {Q}\np = {P}")

def pregunta_5():
    Q = angulos_optimos(np.array([0.424, 0.824]), (0.6, 0.4), np.array([44, 46]))
    P2_rotado = R(Q[0] + Q[1]).dot(np.array([0.4,0]))
    P1_rotado = R(Q[0]).dot(np.array([0.6,0]))
    P = P1_rotado + P2_rotado
    print(f"q = {Q}\np = {P}")

if __name__ == "__main__":
    #pregunta_4()
    pregunta_5()