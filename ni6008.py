#Importing the wrapper for the daqmx configured
import nidaqmx as nqmx 
 
import matplotlib.pyplot as plt
plt.ion() # For real time plotting
import csv 
import datetime as dt

# libraries for Configuring the timing properties of the nidaqmx.task class
from nidaqmx.constants import LineGrouping
from nidaqmx.constants import Edge
from nidaqmx.constants import AcquisitionType

#drawnow to make figures
from drawnow import *  


def make_figure():
    plt.xticks(rotation=70)
    
    """ Takes the set of voltages inputs and plots it in real time"""
    
    plt.title('Voltage at 10kHz Sampling Rate Over a Period of Time')
    plt.ylabel('Voltage Values')
    plt.plot(x,voltages,'r-')



x=[] 
voltages=[]

# Column names for the csv file 
headerList = ['Interval', 'Voltage Value at 10Khz sampling Rate']
  


interval=0  #Initializing the counter/interval

#Csv file Creation along with plotting values in real time simultaneously
with open("VoltageReadings.csv",'r+') as file: 
    file.truncate(0)
    writer = csv.DictWriter(file, fieldnames=headerList)  #Creating a DictWriter  
    writer.writeheader()


    with nqmx.Task() as task:
        
        #Adding the voltage channel from the device configured(name=Dev1,channel=ai0)
        task.ai_channels.add_ai_voltage_chan("Dev1/ai0") 
        
        #Converting 10khz=10000 cycles/second
        task.timing.cfg_samp_clk_timing(rate=10000,samps_per_chan=10) #rate specifies the sampling rate(samples per channel per second).
    
        while interval<100: 
            #This is a random interval set now to avoid infinite loops.Incase if we want to continuously plot
            #the data over a longer period until the user stops the readings 
            #then we can make it an continuous loop by setting (while:True) or by increasing the interval value
            
            data=task.read() #Collecting the voltage from the NI 6008 simulator
            
            
            #Appending the value to a list for plotting
            voltages.append(data)
            time=dt.datetime.now().strftime('%H:%M:%S')
            x.append(time)
            
            #Writing the values on a real time to the csv file
            writer.writerow({'Interval':time,'Voltage Value at 10Khz sampling Rate':data}) 
            
            #Calling the drawnow Function to plot values in Real Time           
            drawnow(make_figure) 
            
            plt.pause(0.0001)
            interval+=1 #Updating the count
            
        print("CSV FILE CREATION COMPLETE!")
       
        
    
    
        