import matplotlib.pyplot as plt
import MineSweeper1 as ms1
import MineSweeper2 as ms2
import MineSweeper3 as ms3


# Compare Agent 1 and Agent2
def comparison2(sizes, minedensities, iterations):
    sizeData = {}
    for size in sizes:
        minedensitydata = {}
        for minedensity in minedensities:
            scorefor1 = 0
            time1 = 0
            scorefor2 = 0
            time2 = 0
            for iter in range(iterations):
                agent1 = ms1.MineSweeperPlay(size, minedensity, "A")
                result1 = agent1.letsplay()

                scorefor1 = scorefor1 + result1[1] / result1[0]
                time1 = time1 + result1[3] / (10 ** 3)
                agent2 = ms2.MineSweeper2Play(size, minedensity, "A")
                result2 = agent2.letsplay()
                scorefor2 = scorefor2 + result2[1] / result2[0]
                time2 = time2 + result2[3] / (10 ** 3)
            minedensitydata[minedensity] = {"Basic": [round(scorefor1 / iterations, 3), round(time1 / iterations, 2)],
                                            "KnowledgeBased": [round(scorefor2 / iterations, 3),
                                                               round(time2 / iterations, 2)]}
        sizeData[size] = minedensitydata
    return sizeData


# Compare Agent 1,Agent2, Agent3 and Agent4
def comparison4(sizes, minedensities, iterations):
    print("Compare2")
    sizeData = {}
    for size in sizes:
        minedensitydata = {}
        for minedensity in minedensities:
            scorefor1 = 0
            time1 = 0
            scorefor2 = 0
            time2 = 0
            scorefor3 = 0
            time3 = 0
            scorefor4 = 0
            time4 = 0
            for iter in range(iterations):
                agent1 = ms1.MineSweeperPlay(size, minedensity, "A")
                result1 = agent1.letsplay()
                scorefor1 = scorefor1 + result1[1] / result1[0]
                time1 = time1 + result1[3] / (10 ** 3)
                agent2 = ms2.MineSweeper2Play(size, minedensity, "A")
                result2 = agent2.letsplay()
                scorefor2 = scorefor2 + result2[1] / result2[0]
                time2 = time2 + result2[3] / (10 ** 3)
                agent3 = ms3.MineSweeper3Play(size, minedensity, "P", "A")
                result3 = agent3.letsplay()
                scorefor3 = scorefor3 + result3[1] / result3[0]
                time3 = time3 + result3[3] / (10 ** 3)
                agent4 = ms3.MineSweeper3Play(size, minedensity, "IP", "A")
                result4 = agent4.letsplay()
                scorefor4 = scorefor4 + result4[1] / result4[0]
                time4 = time4 + result4[3] / (10 ** 3)
            minedensitydata[minedensity] = {"Basic": [round(scorefor1 / iterations, 3), round(time1 / iterations, 2)],
                                            "KnowledgeBased": [round(scorefor2 / iterations, 3),
                                                               round(time2 / iterations, 2)],
                                            "Probabilistic": [round(scorefor3 / iterations, 3),
                                                              round(time3 / iterations, 2)],
                                            "Improved Probabilistic": [round(scorefor4 / iterations, 3),
                                                                       round(time4 / iterations, 2)]
                                            }
        sizeData[size] = minedensitydata
    return sizeData


# Plot data
def disp_data(data, varnames, xlable, ylabel, title, index):
    """
    This method is used to visualize data by displaying the graph
    :param index: 0 for score and 1 for time
    :param data: data to be plotted
    :param varnames: variables to be plotted
    :param xlable: x label
    :param ylabel: y label
    :param title: title
    """
    print("display")
    fig = plt.figure()  # Initializing figure
    ax1 = fig.add_subplot()
    ax1.set_xlabel(xlable)
    ax1.set_ylabel(ylabel)
    ax1.set_title(title)
    datakeys = list(data.keys())

    for var in varnames:
        toplot = list(map(lambda key: data.get(key).get(var)[index], data.keys()))
        ax1.plot(datakeys, toplot, label=var)
    ax1.legend(title="Agent")
    ax1.grid(True)


# Extract dicionary to be plotted
def reducedata(data, sizes, minedensities):
    dataToPlot = {}
    if len(sizes) == 1:
        dataToPlot = data.get(sizes[0])
    else:
        for key in data.keys():
            temp = data.get(key).get(minedensities[0])
            dataToPlot.update({key: temp})
    return dataToPlot


# Generate and Plot data for given sizes and mine density
def plotdata():
    s1 = [20, 30, 40, 50, 60]
    m1 = [0.4]
    s2 = [50]
    m2 = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
    s3 = [8, 10, 12, 15, 17]
    s4 = [12]
    iter = 10

    data1 = comparison2(s1, m1, iter)
    data1 = reducedata(data1, s1, m1)
    disp_data(data1, ["Basic", "KnowledgeBased"], "Sizes", "Score",
              "Size vs Score for mine density 0.4", 0)
    disp_data(data1, ["Basic", "KnowledgeBased"], "Sizes", "Time(ms)",
              "Size vs time for mine density 0.4", 1)

    data2 = comparison2(s2, m2, iter)
    data2 = reducedata(data2, s2, m2)
    disp_data(data2, ["Basic", "KnowledgeBased"], "Mine Density", "Score",
              "Mine Density vs Score for size 50", 0)
    disp_data(data2, ["Basic", "KnowledgeBased"], "Mine Density", "Time(ms)",
              "Mine Density vs time for size 50", 1)

    data3 = comparison4(s3, m1, iter)
    data3 = reducedata(data3, s1, m1)
    disp_data(data3, ["Basic", "KnowledgeBased", "Probabilistic", "Improved Probabilistic"], "Mine Density", "Score",
              "Size vs Score for mine density 0.4", 0)
    disp_data(data3, ["Basic", "KnowledgeBased", "Probabilistic", "Improved Probabilistic"], "Mine Density", "Time(ms)",
              "Size vs time for mine density 0.4", 1)

    data4 = comparison4(s4, m2, iter)
    data4 = reducedata(data4, s4, m2)
    disp_data(data4, ["Basic", "KnowledgeBased", "Probabilistic", "Improved Probabilistic"], "Sizes", "Score",
              "Mine Density vs Score for size 12", 0)
    disp_data(data4, ["Basic", "KnowledgeBased", "Probabilistic", "Improved Probabilistic"], "Sizes", "Time(ms)",
              "Mine Density vs time for size 12", 1)
    plt.show()


plotdata()
