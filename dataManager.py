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

def saveData(sample, nameFile):
    '''
    Dumps the sample dictionary data into a .json file
    so it can be opened again
    '''
    with open(nameFile, 'w') as fp:
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

def processData(dataDict, sliceDataList, fileName):
    '''
    Processes the raw data dictionary and saves into a .json file the
    processed data following the instructions from the sliceDataList.
    sliceDataList = [
        integer value of the Nth of sample campaign
        (tuple with the n's samples of the meaurement campaign),
        (tuple with the beginning and end time for slicing),
        ...
    ]
    '''
    sampleId = sliceDataList.pop(0)
    indexes = sliceDataList.pop(0)

    for i in range(0, len(indexes)):
        outData = sliceData(dataDict, sampleId, sliceDataList[i][0], sliceDataList[i][1])
        saveData(outData, fileName + "{}_{}.json".format(sampleId, indexes[i]))

def makePlot(sampleDict, t0=0, tf=None, blocking=True, nameFile=None):
    '''
    Function to produce plots by passing a sample dictionary.
    It's possible to specify an initial time and
    final time of sampling if desired. Otherwise it defaults
    to all the available timesteps.
    '''

    plt.figure()
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
    plt.show(block=blocking)
    if nameFile is not None:
        nameFile = nameFile.strip(".json")
        plt.savefig(nameFile + ".png")

def main():
    data = loadRawData(6)

    slice1 = [
        1,
        (2, 3),
        (37, 75),
        (75, 114)
    ]

    slice2 = [
        2,
        (2, 3),
        (47, 86),
        (91,130)
    ]

    slice3 = [
        3,
        (2, 3),
        (46, 82),
        (82, 122)
    ]

    slice4 = [
        4,
        (3, 4),
        (67, 100),
        (100, 131)
    ]

    slice5 = [
        5,
        (2, 3),
        (60, 100),
        (100, 132)
    ]

    slice6 = [
        6,
        (4,),
        (150, 183)
    ]

    processList = [slice1, slice2, slice3, slice4, slice5, slice6]

    os.chdir("data")
    for sliceL in processList:
        processData(data, sliceL, "measure")

    os.chdir("..")
    dataFiles = os.listdir("data")
    print(os.getcwd())
    for dataF in dataFiles:
        d = loadData("data/" + dataF)
        makePlot(d, blocking=False, nameFile="plots/" + dataF)




if __name__ == "__main__":
    main()
