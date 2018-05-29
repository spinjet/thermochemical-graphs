import os
import numpy as np
import matplotlib.pyplot as plt
import dataManager as dm

# scale factor to convert time (s) into space (mm)
scaleFactor = 0.5 * 1.2


def centerData(dataArray, scaleFactor, CenterX=None):
    '''
    Function that returns data centered on the max of the diagram.
    CenterX value should be given in the original X scale
    '''
    Yval = dataArray[1, :]
    Xval = dataArray[0, :] - dataArray[0, -1]
    Xval *= scaleFactor

    if CenterX is None:
        CenterIndex = Yval.argmax()
    else:
        CenterIndex = int(np.argwhere(dataArray[0, :] == CenterX))

    Xcentr = Xval[CenterIndex]
    deltaX = abs(Xcentr - Xval[-1])
    Xval += deltaX

    Xval = Xval[0: CenterIndex * 2]
    Yval = Yval[0: CenterIndex * 2]

    return (Xval, Yval)


def plotData(dataDict, scaleFactor, name, centering=None):

    dataArray = np.array([
        dataDict['ch1'][0],
        dataDict['ch1'][1]
    ])

    Xval, Yval = centerData(
        dataArray, scaleFactor, centering)

    plt.figure()
    plt.plot(Xval, Yval)
    plt.grid()

    plt.title(name)
    plt.xlabel("Position [mm]")
    plt.ylabel("Temperature [K]")
    plt.ylim((0, 1600))

    plt.show()


def getMeasures():
    fileNames = os.listdir("data/")
    titles = [name.strip(".json") for name in os.listdir("data/")]
    measuresList = []

    for i in range(0, len(titles)):
        measuresList.append([titles[i], dm.loadData("data/" + fileNames[i])])

    return measuresList


misL = getMeasures()
k = 8
# plotData(misL[k][1], scaleFactor, misL[k][0])


dataFiles = os.listdir("data/")
measure1 = dm.loadData("data/measure5_2.json")

m1ch1 = np.array([
    measure1['ch1'][0],
    measure1['ch1'][1]
])

Xval, Yval = (m1ch1[0, :], m1ch1[1, :])

# 6_4 : 166.50
# 4_3 : 84.25
# 4_4 : 114.85


plt.plot(Xval, Yval)
plt.grid()
plt.show()
