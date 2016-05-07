from tkinter import *
from tkinter import ttk
import tkinter
from tkinter import filedialog
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import pylab
from pylab import *
import math
import numpy
from keithley import Keithley
from LockinAmp import lockinAmp
import time
import multiprocessing

root = Tk()

def main():

    global result, func, qx, qy

    qx = multiprocessing.Queue()
    qy = multiprocessing.Queue()

    func=''
    result=['']
    values_y=[]
    values_x=[]

    createWidgit()

    root.protocol('WM_DELETE_WINDOW', quit) 
    root.mainloop()

#************************Main End Here***************************#

def updateplot():

    global ax, frame, qx, qy

    try:

        x=qx.get_nowait()
        y=qy.get_nowait()
        #print ("%s" %time.ctime(time.time()*1000))
        if y != 'Q':
            ax.scatter(x, y, s=50, alpha=0.5)
            canvas.draw()
            frame.after(1,updateplot)

        else:
            #canvas.draw()
            print ("done")
    except:
        #print ("empty")
        frame.after(1,updateplot)

def measureMethod( _inteval, _number, _output):
    
    global values_x, values_y, result, keith, qx, qy
    
    i=float(_inteval)
    n=int(_number)
    ax.clear()
    ax.grid(True)
    ax.set_title("Realtime Waveform Plot")
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude")
    ax.axis([0, i*n,-10,10])
    #ax.axis('auto')

 

    #check if func is empty

    if func == '':

        listbox_l.insert('end',"Please select measurement mode.")
        
    else:



        k=i*n
        process1 = multiprocessing.Process(target = measureUpdate, args = (i,k,func,qx,qy,))
        process1.start()
        updateplot()

        listbox_l.insert('end',"Measurement finished")
    listbox_l.see(END)

def measureUpdate(i,lim, f, qx, qy):

    keith=Keithley(f)
    t=0
    #t0=time.time()*1000
    print("Start to query data")
    while t <= lim :
        #print (time.time()*1000-t0)
        #print ("%.2f" %float(time.time()*1000-t0))
        tmp = keith.measureOnce()
        qy.put(tmp[1])
        qx.put(t)
        #print(tmp[1])
        time.sleep(i/1000)
        t+=i
    print("Mesaurement completed")
    qy.put('Q')
    qx.put('Q')


#################################################

# def measureMethod( _inteval, _number, _output):
    
#     global values_x, values_y, result

#     values_y=[]
#     values_x=[]
#     result=[]

#     i=float(_inteval)
#     n=int(_number)
    
#     t=0
    

#     ax.clear()
#     ax.grid(True)
#     ax.set_title("Realtime Waveform Plot")
#     ax.set_xlabel("Time")
#     ax.set_ylabel("Amplitude")
#     ax.axis([0, i*n, -10, 10])



#     #check if func is empty

#     if func == '':

#         listbox_l.insert('end',"Please select measurement mode.")
        
#     else:

#         keith=Keithley(func)

#         #ramp
#         amp = lockinAmp()
#         step = double(_output)/n
#         a=0.0
        
#         while t <= i*n :

#             amp.dacOutput(a)
#             time.sleep(i/1000)
#             tmp=keith.measureOnce()
#             result.append(tmp[1])
#             values_y.append(tmp[1])
#             values_x.append(t)
#             ax.scatter(values_x[-1], values_y[-1], s=50, alpha=0.5)
#             canvas.draw()
#             listbox_l.insert('end', tmp)
#             t+=i
#             a+=step
        

#         #scat=ax.scatter(values_x, values_y, s=50, alpha=0.5)
#         #canvas.draw()

#         listbox_l.insert('end',"Measurement finished")
#     listbox_l.see(END)


def optionMethod(val):

    global func 

    func = val

    print(func)

# def measureMethod():

#     global result

#     if func == '':
#         listbox_l.insert('end',"Please select measurement mode.")
        
#     else:

#         keith=Keithley()
#         #set inteval and number if input is digit 
#         if entry_interval.get().isdigit():
#             keith.interval_in_ms = int(entry_interval.get())

#         if entry_number.get().isdigit():
#             keith.number_of_recordigns = int(entry_number.get())

#         keith.func=func
#         #self.outputField.delete(0, 200)
#         keith.messurement()

#         result = keith.result
#         #self.outputField.insert(0, self.e.average)
#         for i in result:
#             listbox_l.insert('end',i)
            

#         ax.scatter(range(0,len(result),1), result, s=100, alpha=0.5)
#         canvas.draw()
#         listbox_l.insert('end', func+" measurement is completed.")

#     listbox_l.see(END)

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

        f.closed

        listbox_l.insert('end', "The Measurement Data is saved.")
        listbox_l.see(END)

def outputMethod(_output):
    
    if _output.replace('.','').replace('-','').isdigit() :
        #print(entry_output.get())
        amp = lockinAmp()
        msg = amp.dacOutput(double(_output))

        listbox_l.insert('end', "Output has been set to %s" %str(_output))
        listbox_l.see(END)
    else:
        listbox_l.insert('end', "\""+_output+"\" is not a valid ouput value.")
        listbox_l.see(END)

def clearMethod():
    ax.clear()
    ax.grid(True)
    ax.set_title("Realtime Waveform Plot")
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude")
    ax.axis([0, 10, 0, 10])
    
    canvas.draw()
    listbox_l.delete(0, END)
    
    print("clear all")

def quitMethod():

    global root

    root.quit()

def createWidgit():

    global ax, canvas, listbox_l, result, func, frame

    fig = pylab.figure(1)

    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.set_title("Realtime Waveform Plot")
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude")
    ax.axis([0,10,0,10])
    #ax.autoscale(enable=True, axis='x', tight=True)


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
    #button_measure = ttk.Button(frame_buttomArea, text ="Measure", command = lambda : measureMethod(entry_interval.get(), entry_number.get(), entry_output.get()))
    button_measure = ttk.Button(frame_buttomArea, text ="Measure", command = lambda : measureMethod(entry_interval.get(), entry_number.get(), entry_output.get()))

    button_save  = ttk.Button(frame_buttomArea, text="Save", command = saveMethod)
    button_quit = ttk.Button(frame_buttomArea, text="Quit", command = quitMethod)
    button_output = ttk.Button(frame_buttomArea, text="Output", command = lambda : outputMethod(entry_output.get()))
    button_clear = ttk.Button(frame_buttomArea, text="Clear", command = clearMethod)

    #Attatch Plot 
    canvas = FigureCanvasTkAgg(fig, frame)
    canvas.get_tk_widget().grid(row=0, column =0, pady =0, padx =0,sticky='nsew')
    content.grid(column=0, row=0, sticky=(N, S, E, W))
    frame.grid(column=0, row=0, columnspan=3, rowspan=20, sticky=(N, S, E, W))


    frame_setting.grid(column=3, row=0, columnspan=2, rowspan=20, sticky=(N, S, E, W))

    #Frame setting grid
    label_mode.grid(column=0, row=1, columnspan=2, sticky=(N, W), padx=5)
    option_mode.grid(column=0, row=2, columnspan=2, sticky=(N, W), padx=5)
    label_interval.grid(column=0, row=3, columnspan=2, sticky=(N, W), padx=5)
    entry_interval.grid(column=0, row=4, columnspan=2, sticky=(N, W), padx=5)
    label_number.grid(column=0, row=5, columnspan=2, sticky=(N, W), padx=5)
    entry_number.grid(column=0, row=6, columnspan=2, sticky=(N, W), padx=5)
    label_output.grid(column=0, row=7, columnspan=2, sticky=(N, W), padx=5)
    entry_output.grid(column=0, row=8, columnspan=2, sticky=(N, W), padx=5)


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
    button_quit.grid(column=1, row=3,columnspan = 1,sticky=(N, S, E, W))


    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    content.columnconfigure(0, weight=3)
    content.columnconfigure(1, weight=3)
    content.columnconfigure(2, weight=3)
    content.columnconfigure(3, weight=1)
    content.columnconfigure(4, weight=1)
    content.rowconfigure(1, weight=1)

if __name__ == '__main__':
    main()





