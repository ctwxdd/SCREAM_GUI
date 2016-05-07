#import visa

class lockinAmp():
    
    v_max = +12
    v_min = -12

    def __init__(self):

        # self.rm = visa.ResourceManager()
        # #Depending on instrument GPIB address
        # self.sr = self.rm.open_resource('GPIB::10') #SR7265 GPIB address 10
        # #Execute something with SR7265
        # print(self.sr.query("ID"))
        # self.amplitude = 1.5
        # self.frequency = 2000

        # self.amp_set = self.amplitude*1000000 #conversion based on original setting
        # self.freq_set = self.frequency*1000 #conversion based on original setting
        # self.sr.write("OA %d" %self.amp_set)
        # self.sr.write("OF %d" %self.freq_set)

        # self.sr.write("SEN23")
        # self.sr.write("TC10")

        # self.sr.write("DAC1 0")
        print ("intitialized")


    def __str__(self):
        return "initialized"


    def ouputSignal(self, amp, freq):
    #Output signal
        # self.amplitude = amp #Oscillator output Vrms from 0 to 5V
        # self.frequency = freq #Oscillator output frequency from 0 to 250kHz
        # self.amp_set = self.amplitude*1000000 #conversion based on original setting
        # self.freq_set = self.frequency*1000 #conversion based on original setting
        # self.sr.write("OA %d" %self.amp_set)
        # self.sr.write("OF %d" %self.freq_set)
        print ("outputSignal")
    #Sensing setting
    def sensitivity(self, mode):
        #Sensing range
        # self.sr.write("SEN%d" %mode)
        # print("SEN%d" %mode)
        print ("sensitivity")

    def timeConst(self, mode):
    #Time constant
       # self.sr.write("TC%d" %mode)
        #print("TC%d" %mode)
        print("timeConst")
    def acGain(self, mode):
    #AC Gain
#       self.sr.write("ACGAIN1")
        print("ACGAIN1")

    #DAC output (Digital to Analog Converter)
    def dacOutput(self, vol):

        dac_amplitude = vol #DAC output DC voltage from -12V to 12V
        dac_step = 0.1 #DAC output step in volts
        dac_amp_set = dac_amplitude*1000 #conversion based on original setting
        dac_step_set = dac_step*1000 #conversion based on original setting
        dac_i = 0 #sweep from zero

        while dac_i <= dac_amp_set:
            #self.sr.write("DAC1 %d" %dac_i)
            dac_i+=dac_step_set
        #print(type(vol))
        if (vol <=12 and vol >= -12) :
            H_e=vol*float(56.953)
            H_c=vol*float(23.833)
        #print("The magnetic fild at Edge is %.2lf (Oe)." %H_e)
        #print("The magnetic fild at cenber is %.2lf (Oe)" %H_c)

            msg = "DAC output has been set to "+str(vol)+"(V)."
            return msg
        else:
            return "Out of limit."
	
#Measurement readout
# print("----Readout from Signal Recovery 7265----\n")
# print("X (V):",sr.query("X."))
# print("Y (V):",sr.query("Y."))
# print("R (V):",sr.query("MAG."))
# print("Phase (Deg):",sr.query("PHA."))
# print("OSC_Frequency (Hz):",sr.query("FRQ."))
#print(sr.query("MP."))

#Output readout from Keithley2000
# keith.write("CONFigure:VOLTage:AC")
# print("----Readout from Keithley 2000----\n")
# print("OSC_Amplitude (V):",keith.query(":READ?"))
# keith.write("CONFigure:FREQuency")
# print("OSC_Frequency (Hz):",keith.query(":READ?"))

#Prevent windows close
# input("Press Enter to close the program")
