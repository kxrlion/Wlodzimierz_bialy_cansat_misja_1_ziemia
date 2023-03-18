from tkinter import *
import serial
import functools
import serial.tools.list_ports
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use("dark_background")
file = open('logs.txt', 'w')

ports = serial.tools.list_ports.comports()
serialObj = serial.Serial()
background_color = "#2b2b2b"
foreground_color = "#ffffff"
c = "0;0;0;0;0;0;0;0;0;0;"
b = 0


def init_com_port(index, win):
    currentPort = str(ports[index])
    comPortVar = str(currentPort.split(' ')[0])
    serialObj.port = comPortVar
    serialObj.baudrate = 115200
    serialObj.open()
    win.destroy()


def choose_com():
    com_chooser_win = Toplevel()
    com_chooser_win.config(bg=background_color)
    for onePort in ports:
        comButton = Button(com_chooser_win, text=onePort, font=('Roboto', '13'),
                           height=1, width=45, bg="#252525",
                           fg=foreground_color, border="0",
                           command=functools.partial(init_com_port, index=ports.index(onePort), win=com_chooser_win))
        comButton.grid(row=ports.index(onePort), column=0, pady=2)


def do_the_funni():
    if serialObj.is_open and serialObj.in_waiting:
        raw = serialObj.readline()
        global c
        c = raw.decode('utf_8')

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
def animate(i):
    graph_data = open('v.txt', 'r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y =line.split(',')
            xs.append(x)
            ys.append(y)

    ax1.clear()
    ax1.plot(xs , ys)

    
    



    style.use('fivethirtyeight')




def chart_show():


    ani = animation.FuncAnimation(fig , animate , interval = 1000)
    plt.show()




def read_the_funni(c):
    g = str(c)
    a = g.split(";")
    global b
    if a[0] != b:
        if a[0] != 0:
            file.write(f"{a[0]};{a[1]};{a[2]};{a[3]};{a[4]};{a[5]};{a[6]};{a[7]};{a[8]};\n")
    b = a[0]
    # time
    if c != "0;0;0;0;0;0;0;0;0;0;":
        text.config(
            text=f"Time: {int(a[0]) // 3600}:{(int(a[0]) % 3600) // 60}:{((int(a[0]) % 3600) % 60) % (24 * 3600)}"
                 f"\nPressure: {a[1]} hPa\n"
                 f"Temp: {a[2]} C\n"
                 f"Longitude: {a[3]}\n"
                 f"Latitude: {a[4]}\n"
                 f"Height: {a[5]}\n"
                 f"Ax: {a[6]}\n"
                 f"Ay: {a[7]}\n"
                 f"Az: {a[8]}\n"
            )
    else:
        text.config(text="No Signal :(")


# main window settings
root = Tk()
root.title("W�odzimierz Bia�y")
root.config(bg=background_color)
root.geometry("340x700+500+300")

choose_com()

# text visuals
text = Label(bg="#252525", fg=foreground_color, text="TEMP", font=("Roboto", 25))
text.pack(side=LEFT, fill=BOTH)

while 1:
    root.update()
    do_the_funni()
    read_the_funni(c)
    #chart_show()

