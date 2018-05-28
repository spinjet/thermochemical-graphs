import os
import sys
import numpy as np
import matplotlib.pyplot as plt

numberOfSamples = 6 # total number of sampling procedures


def getDataFile(sampleId, channelId):
    '''
    Simple function that returns the pointer to a file
    containing the channelId-th data from the sampleId-th
    experimental sampling
    '''

    folderName = "Th.C. 0000" + str(sampleId)
    fileName = "CH" + str(channelId) + "_0" + str(channelId) + "h.txt"

    fileDir = "Group 5/" + folderName + "/" + fileName
    try:
        return open(fileDir, 'r')
    except OSError:
        print("Cannot find file: " + fileName)

def sliceData(sampleId, t0, tf):
    '''
    Function to slice a sample given an initial time t0
    and a final time tf. Returns a dictionary of the
    sample with the sliced data.
    '''
    slicedData = {'ch1':[], 'ch2':[]}

    for k, ch in data['sample' + str(sampleId)].items():

        # begin and end positions
        b = ch[0].index(float(t0))
        e = ch[0].index(float(tf))

        t = ch[0][b:e]
        d = ch[1][b:e]

        slicedData[k] = [t, d]

    return slicedData



def makePlot(sampleDict, t0=0, tf=None):
    '''
    Function to produce plots by passing a sample dictionary.
    It's possible to specify an initial time and
    final time of sampling if desired. Otherwise it defaults
    to all the available timesteps.
    '''


    plt.subplot(2,1,1)
    # ch = data['sample' + str(sampleId)]['ch1']
    ch = sampleDict['ch1']

    maxTemp = np.ones(len(ch[0]))

    if tf is not None:
        b = ch[0].index(float(t0))
        e = ch[0].index(float(tf))

        t = ch[0][b:e]
        d = ch[1][b:e]
    else:
        t = ch[0]
        d = ch[1]


    plt.plot(t, d, t, 1500 * maxTemp)
    plt.grid()
    plt.xlabel('Time [s]')
    plt.ylabel('Temperature [K]')

    plt.subplot(2,1,2)
    #ch = data['sample' + str(sampleId)]['ch2']
    ch = sampleDict['ch2']

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
    plt.ylabel('Pulses')
    plt.show()



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

#sample1 = sliceData(1, 80, 115)

makePlot(data['sample6'])

# first graph
# makePlot(data['sample1'], 80, 115)

# second graph
# makePlot(data['sample2'], 94, 127)

# third graph
# makePlot(data['sample3'],87, 123)
