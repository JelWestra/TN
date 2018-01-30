import numpy as np


__author__ = "Jelle Westra"
__date__ = "30/01/2018"
   


def peakfinder(y, min_peak_height=None, min_peak_distance=None,
               threshold=None, valley=False, plotmode=False):
    
    """ Detects peaks in data by using their amplitude and other features.
    The peakfinder function is based of the findpeaks function in MATLAB.

    Input
    ¯¯¯¯¯¯¯
    y : y-Data.
        1D array-like (array / list / tuple).
        
    min_peak_height : Only detect peaks that are greater.
        number (float / int), default -> lowest data point.
        
    min_peak_distance : minimal distance/datapoints between peaks.
        integer (int), default -> All peaks detected.
        
    threshold : Number of peaks -> takes highest peaks.
        integer (int), default -> all peaks detected.

    valley : When True, the valleys will be detected instead of the peaks.
        True or False (bool), default -> False

    plotmode : When True the data is plotted.
        True or False (bool), default -> False
    
    Return
    ¯¯¯¯¯¯¯¯
    peak : 2D array with peaks in y-data and corresponding x-data.
        Numpy array

    Requirements
    ¯¯¯¯¯¯¯¯¯¯¯¯¯¯
    numpy : only requirement for finding peaks
    
    matplotlib : only if plotmode is enabled

    
    """    
    # Conditions
    y = np.asarray(y) - np.median(y)
    x = np.linspace(0,1,y.size)        
    if (min_peak_height == None):
        min_peak_height = min(y)    
    if valley:
        y = -y

    # Finding all the peaks
    x_result, y_result = [], []
    for i in range(1, y.size - 1):
        if ((y[i-1] < y[i]) & (y[i] > y[i+1]) & (y[i] > min_peak_height)):
            x_result.append(x[i])
            y_result.append(y[i])
    x_result = np.asarray(x_result)
    y_result = np.asarray(y_result)


    # Checking for minimal peak distance
    if (min_peak_distance != None):
        x_mpd_peaks = []
        y_mpd_peaks = []
        for i in range(y_result.size):
            intervalmax = True
            for k in range(0, y.size):
                if (y_result[i] == y[k]) & (x_result[i] == x[k]):
                    center = k
                    break
            a = center - min_peak_distance
            b = center + min_peak_distance
            if (b > y.size):
                b = y.size
            if (a < 0):
                a = 0
            for j in range(a, b):
                if (y_result[i] < y[j]):
                    intervalmax = False
            if (intervalmax):
                x_mpd_peaks.append(x_result[i])
                y_mpd_peaks.append(y_result[i])

        x_result = np.asarray(x_mpd_peaks)
        y_result = np.asarray(y_mpd_peaks)


    # Checking for threshold/number of peaks (chosing highest peaks)       
    if (threshold != None):
        if ((threshold % 1 == 0) & (threshold > 0)):
            if (y_result.size > threshold):
                y_result = np.sort(y_result)
                y_result = y_result[-threshold:]
                x_result = np.zeros(y_result.size)
                for a in range(y_result.size):
                    for b in range(y.size):
                        if (y_result[a] == y[b]):
                            x_result[a] = x[b]
        else:
            return print("Number of peaks needs to be a whole number above 0.")    

    if valley:
        y_result = -y_result
        y = -y

    y = y + np.median(y)

    # Creating plot if plotmode is enabled
    if (plotmode):
        try:
            import matplotlib.pyplot as plt
        except:
            print("Plotmode is only available if matplotlib is installed.")
        plt.plot(x, y, linewidth=1)
        plt.plot(x_result,y_result, "r+", markersize=10)
        plt.show()


    peaks = [x_result, y_result]    
    return peaks



"""  - Example -  """

if (__name__ == "__main__"):
    y = np.sin(2*np.pi*5*np.linspace(0, 1, 200)) + np.random.randn(200)/5 +35
    x = np.linspace(0,1,200)

    peaks_x, peaks_y = peakfinder(y, min_peak_distance=20)
    
    print("X : ", peaks_x)
    print("Y : ", peaks_y)






