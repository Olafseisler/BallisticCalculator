import ballistic_main as main
import time as timer
import matplotlib
import matplotlib.pyplot as plt
from tkinter import *


def open_window():
    root = Tk()
    label = Label(root, text="Ballistic Calculator")
    label.pack()
    root.geometry("400x400")

    Label(root, text='First Name')
    e1 = Entry(root)
    root.mainloop()


def draw_plot(data_x, data_y, x_name, y_name):
    fig, ax = plt.subplots()
    plt.plot(data_x, data_y)
    ax.set(xlabel=x_name, ylabel=y_name, title='Ballistics')
    ax.grid()
    #plt.xlim(left=0)
    #plt.ylim(bottom=0, top=plt.xlim()[1])


def calculate_angle():
    start = timer.perf_counter()
    aim_trajectory = main.find_angle(25000, 45, -10, 27.5, 0.01, 20)
    print("This process took", round(timer.perf_counter() - start, 6), "second(s)")

    aim_trajectory.print_data()
    open_window()
    draw_plot([x[0] for x in aim_trajectory.pos_points], [x[1] for x in aim_trajectory.pos_points], "Distance (m)",
              "Altitude (m)")


def test_range(angle_rng: tuple):
    ranges_list = []
    for angle in range(angle_rng[0], angle_rng[1]):
        aim_trajectory = main.calculate_trajectory(angle, main.v, main.x, main.y, main.p,
        main.C, main.A, main.m, main.g, main.timestep, main.time)

        ranges_list.append((angle, aim_trajectory.d_final()))
    #print(*ranges_list, sep="\n")
    draw_plot([point[0] for point in ranges_list], [point[1] for point in ranges_list], "Angle (degrees)",
              "Distance (m)")


#test_range((1, 90))
calculate_angle()

plt.show()
