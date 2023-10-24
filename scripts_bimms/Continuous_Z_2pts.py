"""

"""
from tabnanny import verbose
import bimms as bm
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
from pyqtgraph.Qt import QtWidgets
import pyqtgraph as pg
import time as t
import keyboard 
import csv
import pandas as pd



freq = 10000
n_pts = 1
i_amp = 0.005 #in mA
settling_time = 0.00001
NPeriods = 8
amp = 0.01             		 #amplitude (V)

differential = False
two_wires = True             #A CHANGER 
post_filtering = False

gain_current = 20
gain_voltage = gain_current

time_span = 1500             #in s 
refresh_time = 0.01       #in s

#filename and output dir
now = datetime.now()
time = now.strftime("%H_%M_%S")
current_date = now.strftime("%d_%m_%Y")
data_path = "data"
folder_name = data_path + "/data_"+current_date
if not os.path.exists(data_path):
    os.mkdir(data_path)
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

freq_label = str(int(freq/1000)) + 'khz'
output_file_name = folder_name+"/continuous_Z_"+freq_label+'_' + time 

app = QtWidgets.QApplication([]) 
win = pg.GraphicsLayoutWidget(title="Continuous Impedance")
p = win.addPlot(row=0, col=0)     # creates a window)                                               # creates empty space for the plot in the window
curve = p.plot()                                               # create an empty "plot" (a curve to plot)
p2 = win.addPlot(row=1, col=0)
curve2 = p2.plot()
p.setLogMode(x=False, y=True)
win.show()

#time_span = int(time_span/refresh_time)                              # width of the window displaying the curve
Data1 = np.linspace(0,0,time_span)                                 # create array that will contain the relevant time series    
Data2 = np.linspace(0,0,time_span)                                 # create array that will contain the relevant time series  
Time = np.linspace(0,0,time_span)*refresh_time 

ptr = -time_span                                                # set first x position


data = 0
data_buffer = []
data_buffer_phase = []
buffer_size = 1000
buffer_idx = 0
n_data = 0

time_idx = 0
def update():
    global curve, ptr, Data1,Data2,data,phase,time_idx    
    Data1[:-1] = Data1[1:]                        # shift data in the temporal mean 1 sample left
    Data1[-1] = float(data)                   # vector containing the instantaneous values  
    Data2[:-1] = Data2[1:]                        # shift data in the temporal mean 1 sample left
    Data2[-1] = float(phase)                   # vector containing the instantaneous values 
    Time[:-1] = Time[1:]                        # shift data in the temporal mean 1 sample left
    Time[-1] = float(time_idx)                   # vector containing the instantaneous values      
    ptr += 1                                # update x position for displaying the curve
    curve.setData(Data1)                       # set the curve with this data
    curve.setPos(ptr,0)                     # set x position in the graph to 0
    curve2.setData(Data2)                       # set the curve with this data
    curve2.setPos(ptr,0)                     # set x position in the graph to 0
    QtWidgets.QApplication.processEvents()  # you MUST process the plot now

def record_data():
    global buffer_idx,buffer_size,data_buffer,data,data_buffer_phase,phase,n_data
    if (buffer_idx<buffer_size):
        buffer_idx = buffer_idx +1
        data_buffer.append(data)
        data_buffer_phase.append(phase)
    else:
        n_data = n_data + buffer_size
        file_path = "csv/foo.csv"
        data_file = np.asarray([data_buffer,data_buffer_phase])
        data_file = np.transpose(data_file)

        with open(file_path,'a') as csvfile:
            np.savetxt(csvfile, data_file, delimiter=",")

        data_buffer = []
        data_buffer_phase = []
        buffer_idx = 0

def stop_recording():
    pg.QtWidgets.QApplication.exec_() 
    quit()

BS = bm.BIMMS()
BS.keep_on()
BS.set_potentiostat_EIS_config(differential=differential, two_wires = two_wires, coupling = 'DC',voltage_gain=gain_voltage,current_gain=gain_current)


if (differential):
    amp = amp/BS.Gain_Voltage_DIFF
    offset = amp/BS.Gain_Voltage_DIFF
else :
    amp = amp/BS.Gain_Voltage_SE
    offset = amp/BS.Gain_Voltage_SE

BS.interface.configure_network_analyser()
Vrange_CH1 = amp * 1.5
offset_CH1 = amp * 1.5

with open('foo.csv', 'w', newline='') as outcsv:
    writer = csv.writer(outcsv)
    writer.writerow(["magnitude", "phase"])

print('press q to quit')


start_time = t.time()
while True: 
    t1 = t.time()
    gain, phase, gain_ch1 = BS.interface.single_frequency_gain_phase(freq,dB = False, settling_time=settling_time,
	amp = amp, offset = 0.0, Nperiods = NPeriods,Vrange_CH1 = 1.0,Vrange_CH2 = 1.0, 
	offset_CH1 = 0.0,offset_CH2 = 0.0, verbose = False)
    t2 = t.time()
    print(t2 - t1 - NPeriods/freq)
    print(t2 - t1)
    data = gain*BS.Gain_TIA
    phase = (180.*phase/np.pi)-180
    time_idx = time_idx + refresh_time
    update()
    record_data()


    try:  
        if keyboard.is_pressed('q'):  
            dumped_q = input('')
            break  
    except:
        break

    #t.sleep(refresh_time)
    
BS.close()

elasped_time = t.time() - start_time
file_path = "foo.csv"

n_data = n_data + len(data_buffer)
time_array = np.linspace(0,elasped_time,num = n_data)
data_file = np.asarray([data_buffer,data_buffer_phase])
data_file = np.transpose(data_file)

with open(file_path,'a') as csvfile:
    np.savetxt(csvfile, data_file, delimiter=",")


win.close()
pg.QtWidgets.QApplication.closeAllWindows()


info = input('Add info on file name:')
info = str(info)
info = info.replace(" ","_")

if (info):
    output_file_name = output_file_name +'_'+ info + ".csv"
else:
    output_file_name = output_file_name + ".csv"

df = pd.read_csv("foo.csv")
df["time"] = time_array
df.to_csv(output_file_name, index=False)
os.remove("foo.csv")