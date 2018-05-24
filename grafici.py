import os
import sys
import numpy as np
import matplotlib.pyplot as plt

root = os.getcwd() # base directory
numberOfSamples = 6 # total number of sampling procedures


def getDataFile(sampleId, channelId):
    '''
    Simple function that returns the pointer to a file
    containing the channelId-th data from the sampleId-th
    experimental sampling
    '''
    
    folderName = "Th.C. 0000" + str(sampleId)
    fileName = "CH" + str(channelId) + "_0" + str(channelId) + "h.txt"
    
    fileDir = root + "/Group 5/" + folderName + "/" + fileName
    try:
        return open(fileDir, 'r')
    except OSError:
        print("Cannot find file: " + fileName)

def makePlot(sampleId, t0=0, tf=None):
    '''
    Function to produce plots.
    It's possible to specify
    an initial time and final time of sampling if 
    desired. Otherwise it defaults to all the available
    timesteps.
    '''


    plt.subplot(2,1,1)
    ch = data['sample' + str(sampleId)]['ch1']
    
    if tf is not None:
        b = ch[0].index(float(t0))
        e = ch[0].index(float(tf))

        t = ch[0][b:e]
        d = ch[1][b:e]
    else:
        t = ch[0]
        d = ch[1]


    plt.plot(t, d)
    plt.grid()
    plt.xlabel('Time [s]')
    plt.ylabel('Temperature [K]')

    plt.subplot(2,1,2)
    ch = data['sample' + str(sampleId)]['ch2']

    if tf is not None:
        b = ch[0].index(float(t0))
        e = ch[0].index(float(tf))

        t = ch[0][b:e]
        d = ch[1][b:e]
    else:
        t = ch[0]
        d = ch[1]

    plt.plot(t, d)
    plt.grid()
    plt.show(block=False)
    plt.pause(10)



# create an empty dictionary whose keys are strings "sample#"
# and their values are currently empty lists

data = dict([("sample" + str(a), []) for a in range(1, numberOfSamples)])

for sampleId in range(1, numberOfSamples + 1):
    ch = {'ch1': [], 'ch2':[]}

    for chanId in range(1, 3):
        t = []
        d = []

        for line in getDataFile(sampleId, chanId):

            temp = line.split('\t')
            temp[1] = temp[1].replace('\r\n','')

            t.append(float(temp[0]))
            d.append(float(temp[1]))
        
        ch['ch' + str(chanId)] = [t, d]
    
    data['sample' + str(sampleId)] = ch

ch1 = data['sample1']['ch1']

makePlot(6)
