import os
import numpy as np
import matplotlib.pyplot as plt
import dataManager as dm

# scale factor to convert time (s) into space (mm)
scaleFactor = 0.5 * 1.2


def centerData(dataArray, scaleFactor, CenterX=None):
    '''
    Function that returns data centered on the max of the diagram.
    CenterX value should be given in the original X scale.
    '''
    Yval = dataArray[1, :]
    Xval = dataArray[0, :] - dataArray[0, -1]
    Xval *= scaleFactor

    if CenterX is None:
        CenterIndex = Yval.argmax()
    else:
        CenterIndex = int(np.argwhere(dataArray[0, :] == CenterX))

    # the scaled numpy array is then centered
    # depending on what side is the longest
    Xcentr = Xval[CenterIndex]

    if CenterIndex < (len(Xval) / 2):
        deltaX = abs(Xcentr - Xval[-1])
    else:
        deltaX = abs(Xcentr - Xval[0])

    Xval += deltaX

    Xval = Xval[0: CenterIndex * 2]
    Yval = Yval[0: CenterIndex * 2]

    return (Xval, Yval)


def plotData(dataDict, scaleFactor, title, centering=None, blocking=True, fileName=None):
    '''
    Plot function. Arguments are the original data dictionary dataDict,
    scaleFactor is the x-axis scaling factor,
    title the graph title,
    centering is a float value for the x-axis value in which center the graph,
    blocking is a bool to make the execution pause when a plot is open,
    fileName if set saves the plot as a .png file in the plots folder with the provided name.
    '''
    # pack the dicitonary data into an numpy matrix
    dataArray = np.array([
        dataDict['ch1'][0],
        dataDict['ch1'][1]
    ])

    Xval, Yval = centerData(
        dataArray, scaleFactor, centering)

    plt.figure()
    plt.plot(Xval, Yval)
    plt.grid()

    plt.title(title)
    plt.xlabel("X [mm]")
    plt.ylabel("Temperature [K]")
    plt.ylim((0, 1600))
    plt.xlim((-12, 12))

    plt.show(block=blocking)
    plt.savefig("plots/" + fileName + ".png")


def subPlotter(plottingTuple):
    plotIndex = [3, 4, 2, 1]
    fig = plt.figure(figsize=(12, 10))
    for index in range(0, 4):
        pTuple = plottingTuple[index]
        dataDict = pTuple[1]
        subtitle = pTuple[0]
        centering = pTuple[2]

        plt.subplot(2, 2, plotIndex[index])

        dataArray = np.array([
            dataDict['ch1'][0],
            dataDict['ch1'][1]
        ])

        Xval, Yval = centerData(
            dataArray, scaleFactor, centering)

        plt.plot(Xval, Yval)
        plt.grid()

        plt.title(subtitle)
        plt.xlabel("X [mm]")
        plt.ylabel("Temperature [K]")
        plt.ylim((0, 1600))
        plt.xlim((-12, 12))

    fig.show()
    fig.savefig("plots/multiPlot.png")


def getMeasures():
    '''
    Loads the .json measures from the data/ folder and packs them with their
    filename inside a list of tuples, with the structure (fileName, dataDict)
    '''
    fileNames = os.listdir("data/")
    titles = [name.strip(".json") for name in os.listdir("data/")]
    measuresList = []

    for i in range(0, len(titles)):
        measuresList.append((titles[i], dm.loadData("data/" + fileNames[i])))

    return measuresList


def getGraphTitle(name):
    '''
    Gives the z position of the sampled data according to the original fileName.
    '''
    if "measure1" in name:
        return "z = +5 mm"
    elif "measure2" in name:
        return "z = +10 mm"
    elif "measure3" in name:
        return "z = +15 mm"
    else:
        return "z = +0 mm"


def main():
    misL = getMeasures()
    structData = []

    # set manually the centering positions for these sampled data
    for name, dataD in misL:
        if name == "measure4_3":
            shift = 84
        elif name == "measure4_4":
            shift = 115
        elif name == "measure6_4":
            shift = 166.50
        else:
            shift = None

        # structure the data in a tuple to be appended in a list
        structData.append(
            ("Temperatura fiamma a " + getGraphTitle(name),
             dataD, shift, name)
        )

    #unpack the tuple and pass the arguments into the plotting function
    subPlotData = []

    for element in structData:
        # print(element[2])
        # plotData(element[1], scaleFactor, element[0],
        #          element[2], blocking=False, fileName=element[3])

        if "measure6_4" in element[3]:
            subPlotData.append(element)
        elif "measure1_2" in element[3]:
            subPlotData.append(element)
        elif "measure2_2" in element[3]:
            subPlotData.append(element)
        elif "measure3_2" in element[3]:
            subPlotData.append(element)

    print(subPlotData)

    subPlotter(tuple(subPlotData))


if __name__ == "__main__":
     main()

# k = 8
# # plotData(misL[k][1], scaleFactor, misL[k][0])
#
#
# dataFiles = os.listdir("data/")
# measure1 = dm.loadData("data/measure4_3.json")
#
# m1ch1 = np.array([
#     measure1['ch1'][0],
#     measure1['ch1'][1]
# ])
#
# Xval, Yval = (m1ch1[0, :], m1ch1[1, :])
#
# # 6_4 : 166.50
# # 4_3 : 84.25
# # 4_4 : 114.85
#
#
# plt.plot(Xval, Yval)
# plt.grid()
# plt.show()
