import os
import sys
import json
import matplotlib.pyplot as plt

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

def sliceData(data, sampleId, t0, tf):
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

def saveData(sample, sampleID):
    '''
    Dumps the sample dictionary data into a .json file
    so it can be opened again
    '''
    with open("sample{}.json".format(sampleID), 'w') as fp:
        json.dump(sample, fp, indent=4)

def loadData(jsonFile):
    '''
    Loads saved sample data from a .json file.
    Argument must be a string containing the filename.
    '''
    try:
        with open(jsonFile, 'r') as fp:
            data = json.load(fp)
        return data
    except OSError:
        print("Cannot find file " + jsonFile)


def loadRawData(numberOfSamples):
    '''
    Returns a dictionary of the loaded data, whose
    stucture is as follows:
    { sample: { ch1: [t, d], ...}, ... }
    '''

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

    return data

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
    plt.show(block=False)
    plt.pause(10)


data = loadRawData(6)
sample1 = sliceData(data, 1, 80, 115)
saveData(sample1, 1)

dSample1 = loadData("sample1.json")
makePlot(dSample1)

# first graph
# makePlot(data['sample1'], 80, 115)

# second graph
# makePlot(data['sample2'], 94, 127)

# third graph
# makePlot(data['sample3'],87, 123)
