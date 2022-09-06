import sys
from PyQt5.QtWidgets import QApplication
from Simulador.display import Display
from Simulador.objects import Car, Ball, Arc
from coms import BTComs, SimComs
from controller import Controller
from task_manager import TaskManager
from vision import Vision
import numpy as np

if __name__ == "__main__":
    simulation = False

    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook
    app = QApplication([])

    if simulation:
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

    else:
        # Vision for real deal
        vision = Vision(nCam= 0, app= app)

        # Comms
        coms = BTComs()
        
    
    ##########################
    # --- Create classes --- #
    ##########################

    # Controller
    controller = Controller()

    # Task Manager
    task_manager = TaskManager()

    # --- Connections ---

    # Manage keyboard input
    if simulation:
        # Connect keboard
        display.keyboard_signal.connect(
            task_manager.manage_keyboard
        )
        # Set speed via signals (not BT)
        coms.send_message_signal.connect(
            robot.set_speed
        )
    else:
        vision.keyboard_signal.connect(
            task_manager.manage_keyboard
        )

    # Update message from controller to coms
    controller.update_message_signal.connect(
        coms.set_message
    )

    # --- Task Manager ---
    # set manual drive
    task_manager.manual_drive_signal.connect(
        controller.set_manual_drive
    )
    # set task for automatic drive
    task_manager.task_signal.connect(
        controller.set_task
    )
    # Toggle On/Off coms
    task_manager.toggle_OnOff_coms_signal.connect(
        coms.toggle_OnOff
    )


    # --- Start program ---
    task_manager.restart_signal.connect(
        controller.restart
    )
    task_manager.restart_signal.connect(
        coms.restart
    )

    if simulation:
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
    if simulation:
        task_manager.end_signal.connect(
            robot.end
        )
        task_manager.end_signal.connect(
            display.end
        )
    else:
        task_manager.end_signal.connect(
            vision.end
        )

    # --- Initialize program ---
    if simulation:
        display.restart()
        # --- Initialize QApp ---
        app.exec_()
    else:
        vision.thread.start()
    # --- Initialize QApp ---
    app.exec_()