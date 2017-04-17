from numpy import *
import matplotlib.pyplot as plt

############ SQUARE WAVE GENERATOR ############
# USES SIN WAVE TO ESTIMATE IF TOP OR BOTTOM LINE WILL BE DRAWN
# SIN VALUE ABOVE VERTICAL MID POINT ADDS HIGH CONSTANT VALUE
# SIN VALUE BELOW VERTICAL MID POINT ADDS LOW CONSTANT VALUE
def square_wave_generator(t1, t2, C1, C2, D, C, R, t):    
    A = (C1-C2)/2.0 #Calculate the amplitude of the wave
    B = 2.0*pi/(t2-t1) #B is equal to 2Pi/period
    square_wave = zeros(R) #Generate empty matrix of resolution length
    for i in range(0, R):
        if A*sin(B*t[i] - 2.0*C) + D >= D:
            square_wave[i] = C1 + D
        else:
            square_wave[i] = C2 + D
    return square_wave    

############ Cross_correlation_function ############
#Finds the correlation by shifting the signal for every N of the signal length fs.
#Normalizes the signal so correlation is between -1 and 1. Returns an array of 
#values between -1 and 1 over the time-axis.
def normalized_cross_correlation(signal1, signal2, Fs):
    signal_1_energy = 0.0
    signal_2_energy = 0.0
    scaling_factor = 0.0
    # Scaling values 
    for i in range(Fs):
        signal_1_energy += signal1[i]**2 #Energy of signal 1
        signal_2_energy += signal2[i]**2 #Energy of signal 2
        scaling_factor = sqrt(signal_1_energy*signal_2_energy) #Calculate total scaling factor
    for j in range(Fs):
        correlation = 0.0 #Reset correlation 
        signal2_lag_compensated = roll(signal2, j) #Switch the array one place to the right, last value becomes the first
        for k in range(Fs):
            correlation += signal1[k]*signal2_lag_compensated[k]/scaling_factor #Add up all the values to get correlation for this point
        correlation_array[j] = correlation
    return correlation_array

############ Convolution-function ############
#Convolves two signals, over the whole signal length fs.
#Does this by revolving mirroring the second signal backwards, and 
#multiplying with the other signal from -fs/2 to fs/2. 
def convolution(signal1, signal2, Fs):
    signal2_rev = list(reversed(signal2))
    for l in range(Fs):
        convolution = 0.0
        signal2_lag_compensated = roll(signal2_rev, l-(Fs/2)) #Switch the array one place to the right, last value becomes the first
        for m in range(Fs):
            convolution += signal1[m]*signal2_lag_compensated[m]
        convolution_array[l] = convolution
    return convolution_array
    
############ PARAMETERS ############

fs = 1000 #Data points, or resolution of square waves to be created
    
tStart = 0 #Start of timeline
tEnd = 2*pi #End of timeline

V1 = 1.0 #highest square wave amplitude
V2 = -1.0 #lowest square wave amplitude

vShift = 0.0 #Vertical shift

hShift = -0.5*pi #horizontal shift

ta = 0.0 # beginning of signal
tb = pi # Length of signal = tb-ta.

time = linspace(tStart, tEnd - (1.0/fs), fs) #Generate timeline
wave = square_wave_generator(ta, tb, V1, V2, vShift, 0, fs, time) #Generate centered square wave
wave_delayed = square_wave_generator(ta, tb, V1, V2, vShift, hShift, fs, time) #Generate shifted wave

############ GET CORRELATION ############
correlation_array = zeros(fs) #Generate empty array
correlation_array = normalized_cross_correlation(wave, wave_delayed, fs) #Fill with values

############ GET CONVOLUTION ############
convolution_array = zeros(fs) #Generate emtpy array
convolution_array = convolution(wave, wave_delayed, fs) #Fill with values

############ PLOTTING ############
plt.subplot(311)
plt.plot(time, wave, color = 'green', label = 'Regular signal') #Plot first signal
plt.plot(time, wave_delayed, color = 'red', label = 'Delayed signal') #Plot delayed signal
plt.ylim([-1.5, 1.5])
plt.ylabel('Amplitude')
plt.xlabel('Time')
plt.tight_layout()
plt.legend()

plt.subplot(312)
plt.plot(time, correlation_array, label = 'Correlation') #Plot correlation
plt.ylim([-1.5, 1.5])
plt.ylabel('Correlation')
plt.xlabel('Time')
plt.legend()

plt.subplot(313)
plt.plot(convolution_array, label = 'Convolution') #Plot convolution
plt.ylabel('Convolved value')
plt.xlabel('Data points')
plt.legend()
