import ballistic_main as main
import time as timer
import matplotlib
import matplotlib.pyplot as plt

def draw_plot(data_x, data_y, x_name, y_name):
    fig, ax = plt.subplots()
    plt.plot(data_x, data_y)
    ax.set(xlabel=x_name, ylabel=y_name, title='Ballistics')
    ax.grid()
    plt.xlim(left=0)
    plt.ylim(bottom=0, top=plt.xlim()[1])
    plt.show()

start = timer.perf_counter()
aim_trajectory = main.findAngle(25000, 45, -10, 27.5, 0.01, 20)
print("This process took", round(timer.perf_counter()-start, 6), "second(s)")

aim_trajectory.print_data()
main.draw_plot([x[0] for x  in aim_trajectory.pos_points], [x[1] for x in aim_trajectory.pos_points], "Distance (m)", "Altitude (m)")
