from tkinter import *
from tkinter import ttk
import tkinter 
import pylab
from pylab import *
import os
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib
import math
import numpy
from keithley import Keithley
from LockinAmp import lockinAmp
import time

Ta=0.01
fa=1.0/Ta
fcos=3.5

Konstant=cos(2*pi*fcos*Ta)
T0=1.0
T1=Konstant

def measureNext():
    
    global values_x, values_y, result
    values_y=[]
    values_x=[]
    result=[]
    i=float(entry_interval.get())
    n=int(entry_number.get())
    t=0

    if func == '':
        listbox_l.insert('end',"Please select measurement mode.")
        
    else:
        keith=Keithley(func)
        
        while t <= i*n :
            time.sleep(i/1000)
            result=keith.mesasureOnce()
            values_y.append(result[0])
            values_x.append(t)
            
            listbox_l.insert('end', result)
            t+=i

    min_v = min(values_y)
    max_v = max(values_y)

    ax.axis([0, i*n, min_v-float(min_v)/2, max_v+float(max_v)/2])
    #
    scat=ax.scatter(values_x, values_y, s=50, alpha=0.5)
    canvas.draw()
    scat.remove()
    listbox_l.insert('end',"Finished")


#   Tnext=((Konstant*T1)*2)-T0 
#   if len(values)%100>70:
#     values.append(random()*2-1)
#   else:
#     values.append(Tnext)
#   T0=T1
#   T1=Tnext

#   


# def RealtimePloter():

#   global values,wScale,wScale2
#   NumberSamples=min(len(values),wScale.get())
#   CurrentXAxis=pylab.arange(len(values)-NumberSamples,len(values),1)
#   line1[0].set_data(CurrentXAxis,pylab.array(values[-NumberSamples:]))
#   ax.axis([CurrentXAxis.min(),CurrentXAxis.max(),-1.5,1.5])
#   canvas.draw()
#   frame.after(25,RealtimePloter)



def optionMethod(val):

    global func 
    func = value.get()
    #print(func)

def measureMethod():

    global result

    if func == '':
        listbox_l.insert('end',"Please select measurement mode.")
        
    else:
        keith=Keithley()
        #set inteval and number if input is digit 
        if entry_interval.get().isdigit():
            keith.interval_in_ms = int(entry_interval.get())

        if entry_number.get().isdigit():
            keith.number_of_recordigns = int(entry_number.get())

        keith.func=func
        #self.outputField.delete(0, 200)
        keith.messurement()

        result = keith.result
        #self.outputField.insert(0, self.e.average)
        for i in result:
            listbox_l.insert('end',i)
            

        ax.scatter(range(0,len(result),1), result, s=100, alpha=0.5)
        canvas.draw()
        listbox_l.insert('end', func+" measurement is completed.")

    listbox_l.see(END)

def saveMethod():

    global result

    if result == ['']:
        listbox_l.insert('end', "No Data can save.")
        listbox_l.see(END)

    else:

        f =  filedialog.asksaveasfile(mode='w', defaultextension=".txt")

        f.write(func+":\n\n")
        cnt=1
        #output all data 
        for a in result:
           f.write("#"+str(cnt)+" "+str(a)+"\n")
           cnt +=1

        #output the average
        #f.write("\nAverage : " +  str(e.average)+ "\n")
        f.closed

        listbox_l.insert('end', "The Measurement Data is saved.")
        listbox_l.see(END)

def outputMethod():
    
    if entry_output.get().replace('.','').replace('-','').isdigit() :
        #print(entry_output.get())
        amp = lockinAmp()
        msg = amp.dacOutput(double(entry_output.get()))

        listbox_l.insert('end', msg)
        listbox_l.see(END)
    else:
        listbox_l.insert('end', "\""+entry_output.get()+"\" is not a valid ouput value.")
        listbox_l.see(END)

def clearMethod():
    print("clear all")

#****************************************************************#

root = Tk()
func=''
result=['']
values_y=[]
values_x=[]
#set up plot 


fig = pylab.figure(1)

ax = fig.add_subplot(111)
ax.grid(True)
ax.set_title("Realtime Waveform Plot")
ax.set_xlabel("Time")
ax.set_ylabel("Amplitude")
ax.axis([0,10,0,10])
scat=ax.scatter(0, 0, s=50, alpha=0.5)

# x=numpy.linspace(0.2,10,100)
# ax.plot(x,1/x)
# ax.plot(x,numpy.log(x))
# # ax.set_aspect('equal')
# ax.axis([-10,100,-1.5,1.5])
ax.grid(True)
ax.axvline(0, color='k')
ax.axhline(0, color='k')

content = ttk.Frame(root, padding=(3,3,12,12))

#plotting area 
frame = ttk.Frame(content, borderwidth=0, relief="sunken",padding=(3,3,12,12))
frame_setting = ttk.Frame(content)
frame_information = ttk.Frame(content, padding = (3,3,12,12)) 
frame_buttomArea = ttk.Frame(content)


value = tkinter.StringVar()
mode = ["    ","Resistance","FResistance", "Voltage", "Voltage:AC","Current","Current:AC","Frequency","Temperature"]

option_mode = ttk.OptionMenu(frame_setting, value, *mode, command = optionMethod)

listbox_l = Listbox(frame_information,height=5)
scrollbar_s = ttk.Scrollbar(frame_information, orient=VERTICAL, command=listbox_l.yview)

label_mode = ttk.Label(frame_setting, text="Mode:")
label_interval = ttk.Label(frame_setting, text="Interval:") 
label_number = ttk.Label(frame_setting, text="Number:")
label_output = ttk.Label(frame_setting, text="Output:")

entry_number = ttk.Entry(frame_setting); entry_number.insert(0,"10")
entry_interval = ttk.Entry(frame_setting);entry_interval.insert(0,"500")
entry_output = ttk.Entry(frame_setting); entry_output.insert(0,"0")

#button_measure = ttk.Button(frame_buttomArea, text ="Measure", command = measureMethod)
button_measure = ttk.Button(frame_buttomArea, text ="Measure", command = measureNext)
button_save  = ttk.Button(frame_buttomArea, text="Save", command = saveMethod)
button_cancel = ttk.Button(frame_buttomArea, text="Cancel")
button_output = ttk.Button(frame_buttomArea, text="Output", command = outputMethod)
button_clear = ttk.Button(frame_buttomArea, text="Clear", command = clearMethod)

#draw plot 
canvas = FigureCanvasTkAgg(fig, frame)
canvas.get_tk_widget().grid(row=0, column =0, pady =0, padx =0,sticky='nsew')
content.grid(column=0, row=0, sticky=(N, S, E, W))
frame.grid(column=0, row=0, columnspan=3, rowspan=20, sticky=(N, S, E, W))


frame_setting.grid(column=3, row=0, columnspan=2, rowspan=20, sticky=(N, S, E, W))
label_mode.grid(column=0, row=1, columnspan=2, sticky=(N, W), padx=5)
option_mode.grid(column=0, row=2, columnspan=2, sticky=(N, W), padx=5)
label_interval.grid(column=0, row=3, columnspan=2, sticky=(N, W), padx=5)
entry_interval.grid(column=0, row=4, columnspan=2, sticky=(N, W), padx=5)
label_number.grid(column=0, row=5, columnspan=2, sticky=(N, W), padx=5)
entry_number.grid(column=0, row=6, columnspan=2, sticky=(N, W), padx=5)
label_output.grid(column=0, row=7, columnspan=2, sticky=(N, W), padx=5)
entry_output.grid(column=0, row=8, columnspan=2, sticky=(N, W), padx=5)

#wScale = Tkinter.Scale(master=root,label="View Width:", from_=3, to=1000,sliderlength=30,length=ax.patch.get_window_extent().width, orient=Tkinter.HORIZONTAL)
#wScale2 = Tkinter.Scale(master=root,label="Generation Speed:", from_=1, to=200,sliderlength=30,length=ax.patch.get_window_extent().width, orient=Tkinter.HORIZONTAL)
#wScale.set(100)
#wScale2.set(wScale2['to']-10)


frame_information.grid(column=0, row=25,columnspan=3,sticky=(N,W,E,S))

listbox_l.grid(column=0, row=0,columnspan=3,sticky=(N,W,E,S))
scrollbar_s.grid(column=1, row=0, sticky=(N,S))

listbox_l['yscrollcommand'] = scrollbar_s.set

frame_information.grid_columnconfigure(0, weight=1)
frame_information.grid_rowconfigure(0, weight=1)



frame_buttomArea.grid(column =3, row=25,columnspan=2,sticky=(N, S, E, W))

button_output.grid(column=0, row=0,columnspan = 2,sticky=(N, S, E, W))
button_measure.grid(column =0, row=1, columnspan = 2,sticky=(N, S, E, W))
button_clear.grid(column = 0, row = 2, columnspan = 2, sticky=(N,S,E,W))
button_save.grid(column=0, row=3,columnspan = 1,sticky=(N, S, E, W))
button_cancel.grid(column=1, row=3,columnspan = 1,sticky=(N, S, E, W))


root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

content.columnconfigure(0, weight=3)
content.columnconfigure(1, weight=3)
content.columnconfigure(2, weight=3)
content.columnconfigure(3, weight=1)
content.columnconfigure(4, weight=1)
content.rowconfigure(1, weight=1)

# frame.after(100,SinwaveformGenerator)
# frame.after(100,RealtimePloter)
root.mainloop()
