#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 17:33:13 2019

@author: andreunsal
"""

# Necessary libraries with subroutines and functions
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as it
import scipy.signal as signal
from mpl_toolkits import mplot3d 

class MetaMotionAccelerationAnalyzer():
    
    def DataPreparation(self, filename):
    
        # Variable preparation, print analysis to console
        print('\n *** FILE METRICS ***')
        print(filename, 'is being analyzed')
        allData = pd.read_csv(filename)
        xAcc = allData.loc[:, 'x-axis (g)'].values
        yAcc = allData.loc[:, 'y-axis (g)'].values
        zAcc = allData.loc[:, 'z-axis (g)'].values
        time = allData.loc[:, 'elapsed (s)'].values
        timeMin = time / 60 # convert to minutes
        
        # Check file size, sample count, and time samples
        fileStats = os.stat(filename)
        fileSize = fileStats.st_size/(1e6) # file size in MB
        print('Data Size:', '%.2f' %fileSize, 'MB')
        print('Samples:', len(allData))
        print('Time elapsed:', time[-1], 's')
        
        # Prepare a dictionary, DataSet, to initialize data storage
        DataSet = {
                    "File Size (MB)": fileSize,
                    "Time (s)": time[-1],
                    "Time (min)": timeMin[-1],
                    "Time (all)": time,
                    "Sample Count": len(allData),
                    "X Accel. (g)": xAcc,
                    "Y Accel. (g)": yAcc,
                    "Z Accel. (g)": zAcc 
                   }
        
        return(DataSet)
        
    def RawSignalPlotter(self, DataSet):
    
        # Variables retrieved from DataSet
        time = DataSet["Time (all)"]
        xAcc = DataSet["X Accel. (g)"]
        yAcc = DataSet["Y Accel. (g)"]
        zAcc = DataSet["Z Accel. (g)"]
        
        # Plotting raw X acceleration
        plt.figure(figsize = (10, 6))
        plt.plot(time, xAcc, label = "X", color = 'r', linewidth = 2.25)
        plt.title("Raw Acceleration in X Domain")
        plt.ylabel("Acceleration (g)")
        plt.xlabel("Time (s)")
        plt.grid()
        plt.xlim()
        plt.ylim()
        plt.show()
        
        # Plotting raw Y acceleration
        plt.figure(figsize = (10, 6))
        plt.plot(time, yAcc, label = "Y", color = 'g', linewidth = 2.25)
        plt.title("Raw Acceleration in Y Domain")
        plt.ylabel("Acceleration (g)")
        plt.xlabel("Time (s)")
        plt.grid()
        plt.xlim()
        plt.ylim()
        plt.show()
        
        # Plotting raw Z acceleration
        plt.figure(figsize = (10, 6))
        plt.plot(time, zAcc, label = "Z", color = 'b', linewidth = 2.25)
        plt.title("Raw Acceleration in Z Domain")
        plt.ylabel("Acceleration (g)")
        plt.xlabel("Time (s)")
        plt.grid()
        plt.xlim()
        plt.ylim()
        plt.show()
        
        # Plotting X, Y, Z accelerations together
        plt.figure(figsize = (10, 6))
        plt.plot(time, xAcc, label = "X", color = 'r', linewidth = 2.25, alpha = 0.55)
        plt.plot(time, yAcc, label = "Y", color = 'g', linewidth = 2.25, alpha = 0.55)
        plt.plot(time, zAcc, label = "Z", color = 'b', linewidth = 2.25, alpha = 0.55)
        plt.title("Raw Accelerations in X, Y, Z Domains")
        plt.legend(loc = "upper left")
        plt.grid()
        plt.xlabel("Time (s)")
        plt.ylabel("Acceleration (g)")
        plt.xlim()
        plt.ylim()
        plt.show()
        
        return
    
    def Denoiser(self, DataSet):
    
        # Variable initialization
        xAcc = DataSet["X Accel. (g)"]
        yAcc = DataSet["Y Accel. (g)"]
        zAcc = DataSet["Z Accel. (g)"]
        xAcc_ = DataSet["X Accel. (g)"]
        yAcc_ = DataSet["Y Accel. (g)"]
        zAcc_ = DataSet["Z Accel. (g)"]
        time = DataSet["Time (all)"]
        
        # Setting up Butterworth lowpass filter (windowing average function)
        N = 2 # Filter order
        Wn = 0.4 # Cutoff frequency 0 < Wn < 1
        B, A = signal.butter(N, Wn, output = "ba")
        
        # Apply filter and plot X signal
        xMean = []
        for i in range(len(xAcc_)):
            xMean.append(np.mean(xAcc_))
        xAcc_ = signal.filtfilt(B, A, xAcc_)
        plt.figure(figsize = (10, 6))
        plt.plot(time, xAcc_, label = "smooth", linewidth = 2.25)
        plt.plot(time, xAcc, label = "raw", linewidth = 1.5, alpha = 0.5, color = "r")
        #plt.plot(time, xMean, label = "avg offset", linewidth = 2, color = "black")
        plt.legend(loc = "upper left")
        plt.grid()
        plt.xlabel("Time (s)")
        plt.ylabel("Acceleration (g)")
        plt.title("Denoised X Acceleration")
        plt.show()
        #print("Current Offset:", xMean[0]) # Average offset, not useful
        
        # Appending to new dictionary entry
        DataSet["Denoised X Accel. (g)"] = xAcc_
        
        # Apply filter and plot Y signal
        yMean = []
        for i in range(len(yAcc_)):
            yMean.append(np.mean(yAcc_))
        yAcc_ = signal.filtfilt(B, A, yAcc_)
        plt.figure(figsize = (10, 6))
        plt.plot(time, yAcc_, label = "smooth", linewidth = 2.25)
        #plt.plot(time, yMean, label = "avg offset", linewidth = 2, color = "black")
        plt.plot(time, yAcc, label = "raw", linewidth = 1.5, alpha = 0.5, color = "g")
        plt.legend(loc = "upper left")
        plt.grid()
        plt.xlabel("Time (s)")
        plt.ylabel("Acceleration (g)")
        plt.title("Denoised Y Acceleration")
        plt.show()
        #print("Current Offset:", yMean[0]) # Average offset, not useful
        
        # Appending to new dictionary entry
        DataSet["Denoised Y Accel. (g)"] = yAcc_
        
        # Apply filter and plot Z signal
        zMean = []
        for i in range(len(zAcc_)):
            zMean.append(np.mean(zAcc_))
        zAcc_ = signal.filtfilt(B, A, zAcc_)
        plt.figure(figsize = (10, 6))
        plt.plot(time, zAcc_, label = "smooth", linewidth = 2.25)
        plt.plot(time, zAcc, label = "raw", linewidth = 1.5, alpha = 0.5, color = "b")
        #plt.plot(time, zMean, label = "avg offset", linewidth = 2, color = "black")
        plt.legend(loc = "upper left")
        plt.grid()
        plt.xlabel("Time (s)")
        plt.ylabel("Acceleration (g)")
        plt.title("Denoised Z Acceleration")
        plt.show()
        #print("Current Offset:", zMean[0]) # Average offset, not useful
        
        # Appending to new dictionary entry
        DataSet["Denoised Z Accel. (g)"] = zAcc_
        
        return(DataSet)
        
    def OffsetRemover(self, DataSet):
    
        # Variable extraction
        xAcc = DataSet["Denoised X Accel. (g)"]
        yAcc = DataSet["Denoised Y Accel. (g)"]
        zAcc = DataSet["Denoised Z Accel. (g)"]
        
        xsMean = np.mean(xAcc[:200])
        ysMean = np.mean(yAcc[:200])
        zsMean = np.mean(zAcc[:200])
        
        print("Offset first 200 samples X:", "%.4f", xsMean)
        print("Offset first 200 samples Y:", "%.4f", ysMean)
        print("Offset first 200 samples Z:", "%.4f", (1-zsMean))
        
        DataSet["Offset X"] = xsMean
        DataSet["Offset Y"] = ysMean
        DataSet["Offset Z"] = zsMean
        
        xAcc = xAcc - xsMean
        yAcc = yAcc - ysMean
        zAcc = zAcc - zsMean
        
        """
        # Mean value calculations
        xMean = np.mean(xAcc)
        yMean = np.mean(yAcc)
        zMean = np.mean(zAcc)
        
        # Printing offset values
        print("Offset X:", '%.6f' %xMean)
        print("Offset Y:", '%.6f' %yMean)
        print("Offset Z:", '%.6f' %(1-zMean)) # Z is constant at +1
        
        # Adding new dictionary entries
        DataSet["Offset X"] = xMean
        DataSet["Offset Y"] = yMean
        DataSet["Offset Z"] = zMean
        
        # Removing offsets from the signal
        xAcc = xAcc - xMean
        yAcc = yAcc - yMean
        zAcc = zAcc - zMean
        """
        

        # Adding the signals as new entries to the dictionary
        DataSet["Denoised + Offset Removed X Accel. (g)"] = xAcc
        DataSet["Denoised + Offset Removed Y Accel. (g)"] = yAcc
        DataSet["Denoised + Offset Removed Z Accel. (g)"] = zAcc
        
        return(DataSet)
        
    def AdjustedSignalPlotter(self, DataSet):
    
        # Variable extraction
        time = DataSet["Time (all)"]
        xAcc = DataSet["Denoised + Offset Removed X Accel. (g)"]
        yAcc = DataSet["Denoised + Offset Removed Y Accel. (g)"]
        zAcc = DataSet["Denoised + Offset Removed Z Accel. (g)"]
        
        # Means of first 200 samples
        xsMean = np.mean(xAcc[:200])
        ysMean = np.mean(yAcc[:200])
        zsMean = np.mean(zAcc[:200])
        
        # Plot X acceleration
        xMean = []
        for i in range(len(xAcc)):
            xMean.append(np.mean(xAcc))
        plt.figure(figsize = (10, 6))
        plt.plot(time, xAcc, color = 'r', label = 'new signal', linewidth = 2.5)
        #plt.plot(time, xMean, color = 'black', label = 'corrected offset', linewidth = 2.5)
        plt.title("Noise and Offset Calibrated: X Acceleration")
        plt.xlabel("Time (s)")
        plt.ylabel("Acceleration (g)")
        plt.grid()
        plt.xlim()
        plt.ylim()
        plt.legend(loc = 'upper left')
        plt.show()
        print("Updated Offset first 200 samples:", xsMean)
        
        # Plot Y acceleration
        yMean = []
        for i in range(len(yAcc)):
            yMean.append(np.mean(yAcc))
        plt.figure(figsize = (10, 6))
        plt.plot(time, yAcc, color = 'g', label = 'new signal', linewidth = 2.5)
        #plt.plot(time, yMean, color = 'black', label = 'corrected offset', linewidth = 2.5)
        plt.title("Noise and Offset Calibrated: Y Acceleration")
        plt.xlabel("Time (s)")
        plt.ylabel("Acceleration (g)")
        plt.grid()
        plt.xlim()
        plt.ylim()
        plt.legend(loc = 'upper left')
        plt.show()
        print("Updated Offset first 200 samples:", ysMean)
        
        # Plot Z acceleration
        zMean = []
        for i in range(len(zAcc)):
            zMean.append(np.mean(zAcc))
        plt.figure(figsize = (10, 6))
        plt.plot(time, zAcc, color = 'b', label = 'new signal', linewidth = 2.5)
        #plt.plot(time, zMean, color = 'black', label = 'corrected offset', linewidth = 2.5)
        plt.title("Noise and Offset Calibrated: Z Acceleration")
        plt.xlabel("Time (s)")
        plt.ylabel("Acceleration (g)")
        plt.grid()
        plt.xlim()
        plt.ylim()
        plt.legend(loc = 'upper left')
        plt.show()
        print("Updated Offset first 200 samples:", zsMean)
        
        return(DataSet)
        
    def Integrator(self, DataSet):
    
        # Variable extraction
        xAcc = DataSet["Denoised + Offset Removed X Accel. (g)"]
        yAcc = DataSet["Denoised + Offset Removed Y Accel. (g)"]
        zAcc = DataSet["Denoised + Offset Removed Z Accel. (g)"]
        time = DataSet["Time (all)"]
        
        # Integrating acceleration vectors, producing velocities
        xVel = it.cumtrapz(xAcc, time)
        yVel = it.cumtrapz(yAcc, time)
        zVel = it.cumtrapz(zAcc, time)
        
        # Plotting Velocities in X, Y, and Z
        time = np.resize(time, time.size - 1)
        plt.figure(figsize = (10, 6))
        plt.plot(time, xVel, linewidth = 2.25, alpha = 0.6, label = 'x', color = 'r')
        plt.plot(time, yVel, linewidth = 2.25, alpha = 0.6, label = 'y', color = 'g')
        plt.plot(time, zVel, linewidth = 2.25, alpha = 0.6, label = 'z', color = 'b')
        plt.title("Velocities in X, Y, and Z")
        plt.xlabel("Time (s)")
        plt.ylabel("Velocity (m/s)")
        plt.grid()
        plt.xlim()
        plt.ylim()
        plt.legend(loc = 'upper left')
        plt.show()
        
        # Adding new dictionary entries
        DataSet["X Velocity"] = xVel
        DataSet["Y Velocity"] = yVel
        DataSet["Z Velocity"] = zVel
        
        # Integrating the velocity vectors
        xLoc = it.cumtrapz(xVel, time)
        yLoc = it.cumtrapz(yVel, time)
        zLoc = it.cumtrapz(zVel, time)
        
        # 3D Trajectory Plotting
        plt.figure(num=None, figsize=(10, 8), dpi=80, facecolor='w', edgecolor='k')
        ax = plt.axes(projection = '3d')
        ax.plot3D(xLoc, yLoc, zLoc, 'purple', label = 'Trajectory', linewidth = 4)
        ax.set_xlabel('X DISTANCE [M]', fontsize = 12)
        ax.set_ylabel('Y DISTANCE [M]', fontsize = 12)
        ax.set_zlabel('Z DISTANCE [M]', fontsize = 12)
        plt.legend(loc = 'upper left')
        plt.title('Location Trajectory')
        plt.show()
        
        # Adding new dictionary entries
        DataSet["X Trajectory"] = xLoc
        DataSet["Y Trajectory"] = yLoc
        DataSet["Z Trajectory"] = zLoc
        
        return(DataSet)
        
def Main():
    
    print("THIS IS AN ANALYZER DESIGNED FOR DATAFRAMES GENERATED BY METAMOTIONR 3AXIS ACCELEROMOTERS ")
    print("THE ANALYSES REQUIRE THAT ANY TESTS PERFORMED HAVE 1-2S OF STATIONARY DATA BEFORE EXPERIMENT BEGINS ")
    filename = "Semester 2 +x Test1 800Hz +- 4Gs Jan 29 2019.csv"    
    
    analyzer = MetaMotionAccelerationAnalyzer() # MetaMotionAccelerationAnalyzer instance called analyzer
    
    DataSet = analyzer.DataPreparation(filename)
    #print(DataSet) # debugging and validation
    
    analyzer.RawSignalPlotter(DataSet)
    
    DataSet = analyzer.Denoiser(DataSet)
    
    DataSet = analyzer.OffsetRemover(DataSet)
    
    DataSet = analyzer.AdjustedSignalPlotter(DataSet)
    
    DataSet = analyzer.Integrator(DataSet)
    
    return
    
if __name__ == "__main__":
    Main()
    
filename = "Semester 2 Stationary 800Hz +- 4G Jan 29 2019.csv"
allData = pd.read_csv(filename)
    
    