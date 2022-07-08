import matplotlib.pyplot as plt
import csv

def arreglar(point_str):
    point_numbers = point_str.split(",")
    return float(point_numbers[0]), float(point_numbers[1])

def graficar_datos(archivo, fn):
    print("\nLoading data...")
    t = []
    Q1 = []
    Q2 = []
    W1 = []
    W2 = []
    A1 = []
    A2 = []
    P_dotX = []
    P_dotY = []
    P_ddotX = []
    P_ddotY = []
    with open(archivo, "r", encoding= "utf-8") as data:
        reader = csv.DictReader(data)
        for state in reader:
            t.append(float(state[fn[0]]))
            q1, q2 = arreglar(state[fn[1]])
            Q1.append(q1)
            Q2.append(q2)
            w1, w2 = arreglar(state[fn[2]])
            W1.append(w1)
            W2.append(w2)
            a1, a2 = arreglar(state[fn[3]])
            A1.append(a1)
            A2.append(a2)
            p_dX, p_dY = arreglar(state[fn[4]])
            P_dotX.append(p_dX)
            P_dotY.append(p_dY)
            p_ddX, p_ddY = arreglar(state[fn[5]])
            P_ddotX.append(p_ddX)
            P_ddotY.append(p_ddY)

    fig1, (axis1, axis2, axis3) = plt.subplots(3)
    print("Drawing Angles v/s time...")    
    fig1.canvas.set_window_title('Angular Movement over Time')
    axis1.plot(t, Q1, label= "q1")
    axis1.plot(t, Q2, label= "q2")
    axis1.set(ylabel= 'q1, q2 [rad]')
    axis1.legend()

    print("Drawing Angular velocity v/s time...")
    axis2.plot(t, W1, label= "w1")
    axis2.plot(t, W2, label= "w2")
    axis2.set(ylabel= 'w1, w2 [rad]')
    axis2.legend()

    print("Drawing Angular acceleration v/s time...")
    axis3.plot(t, A1, label= "a1")
    axis3.plot(t, A2, label= "a2")
    axis3.set(xlabel= 't [s]', ylabel= 'a1, a2 [rad]')
    axis3.legend()

    fig2 = plt.figure()
    ax = fig2.gca(projection='3d')
    print("Drawing Velocity v/s time...")
    ax.plot(P_dotX, P_dotY, t, label='Robot Velocity')
    print("Drawing Acceleration v/s time...")
    ax.plot(P_ddotX, P_ddotY, t, label='Robot Acceleration')
    ax.set_xlabel('x [m/s], [m/s^2]')
    ax.set_ylabel('y [m/s], [m/s^2]')
    ax.set_zlabel('t [s]')
    ax.legend()

    plt.show()