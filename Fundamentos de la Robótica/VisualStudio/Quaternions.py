import numpy as np
from math import cos, sin, pi

relations = {"": "", "i": "i", "j": "j", "k": "k" ,
            "ii": "-1", "jj": "-1", "kk": "-1", 
            "ij": "k", "jk": "i", "ki": "j",
            "ji": "-k", "kj": "-i", "ik": "-j"}

def e(x, y, z):
    norm = (x**2 + y**2 + z**2)**(1/2)
    return [(x/norm, "i"), (y/norm, "j"), (z/norm, "k")]

def q(u, angle, conjugate):
    theta = angle/360 * 2*pi
    for coordenate in range(len(u)):
        u[coordenate] = (sin(conjugate * theta/2) * u[coordenate][0], u[coordenate][1])
    return [(cos(conjugate * theta/2), "")] + u

def p(x, y, z):
    return [(x, "i"), (y, "j"), (z, "k")]



def rotar(punto, axis, angle):
    ## punto = tuple(x,y,z)
    ## axis = tuple(x,y,z)
    ## angle in degrees

    def aplicar(Q, P):
        multiplications = []
        for q_value in Q:
            for p_value in P:
                coordenate = relations[q_value[1] + p_value[1]]
                sign = 1
                if "-" in coordenate:
                    sign = -1
                    coordenate = coordenate[1]
                if coordenate == "1":
                    coordenate = ""
                multiplications.append((sign * q_value[0] * p_value[0], coordenate))
        product = []
        used = []
        for v_1 in range(len(multiplications) - 1):
            same = [multiplications[v_1]]
            if multiplications[v_1][1] not in used:
                for v_2 in range(v_1 + 1, len(multiplications)):
                    if multiplications[v_1][1] == multiplications[v_2][1]:
                        same.append(multiplications[v_2])
                used.append(multiplications[v_1][1])
                suma = 0
                for same_coordenates in same:
                    suma += same_coordenates[0]
                product.append((suma, multiplications[v_1][1]))
        return product
    
    multiplications = []
    Q = q(e(*axis), angle, 1)
    P = p(*punto)
    Qc = q(e(*axis), angle, -1)
    QP = aplicar(Q,P)
    QPQc = aplicar(QP,Qc)
    
    return QPQc

## Puede recibir de input vectores en listas, tuples y arrays.
#punto = [0,1,2]
#eje = [0,1,0]
#punto = (0,1,2)
#eje = (0,1,0)
punto = np.array([1,1,1])
eje = np.array([0,0,1])
angulo = 120
punto_rotado = sorted(rotar(punto, eje, angulo), key= lambda x: x[1])

if __name__ == "__main__":
    print(f"Punto: <{punto[0]}, {punto[1]}, {punto[2]}>\n" + \
        f"Eje: <{eje[0]}, {eje[1]}, {eje[2]}>\n" + \
        f"Ángulo: {angulo}°\n" + \
        f"Punto rotado: <{punto_rotado[1][0]}, {punto_rotado[2][0]}, {punto_rotado[3][0]}>")
