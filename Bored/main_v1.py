import sys
from PyQt5.QtWidgets import QApplication
from Simulador.display import Display
from Simulador.objects import Car, Ball, Arc
from coms import BTComs, SimComs
from controller import Controller
from task_manager import TaskManager
import numpy as np

if __name__ == "__main__":
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook
    app = QApplication([])


    # --- Create classes ---
    # Display class for simulation
    display = Display(app)

    # Create and add main car
    scale = display.p("SCALE")

    back = np.array([display.p("WINDOW_WIDTH")//2 - 10, display.p("WINDOW_LENGHT")//2])
    front = np.array([display.p("WINDOW_WIDTH")//2, display.p("WINDOW_LENGHT")//2])
    robot = Car(back, front, scale)
    display.cars.append(robot)


    # Comms
    coms = SimComs()

    # Controller
    controller = Controller()

    # Task Manager
    task_manager = TaskManager()

    # --- Connections ---

    # Manage keyboard input
    display.keyboard_signal.connect(
        task_manager.manage_keyboard
    )
    # Update message
    controller.update_message_signal.connect(
        coms.set_message
    )

    # --- Task Manager ---
    # toggle automatic/manual drive
    task_manager.speed_controller_signal.connect(
        controller.toggle_controller
    )
    # set manual speed
    task_manager.set_speed_signal.connect(
        coms.set_message
    )
    # Toggle On/Off coms
    task_manager.toggle_OnOff_coms_signal.connect(
        coms.toggle_OnOff
    )

    # --- Only for simulations ---
    coms.send_message_signal.connect(
        robot.set_speed
    )


    # --- Start program ---
    task_manager.restart_signal.connect(
        controller.restart
    )
    task_manager.restart_signal.connect(
        coms.restart
    )
    task_manager.restart_signal.connect(
        robot.restart
    )

    # --- End program ---
    task_manager.end_signal.connect(
        controller.end
    )
    task_manager.end_signal.connect(
        coms.end
    )
    task_manager.end_signal.connect(
        robot.end
    )
    task_manager.end_signal.connect(
        display.end
    )

    # --- Initialize program ---
    display.restart()

    # --- Initialize QApp ---
    app.exec_()