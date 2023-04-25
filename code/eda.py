"""
This is a template Python script.
"""

import logging
from pathlib import Path
# Third-party packages
from IPython import get_ipython
import matplotlib.pyplot as plt
import pandas as pd
# Local packages
from hermanCode.hermanCode import getTimestamp, make_dir_path

# Arguments
LOG_LEVEL = "INFO"

DATA_PATH = Path("data/input/vehicles.csv")

# Settings: Interactive Pyplot
# get_ipython().run_line_magic('matplotlib', "")

# Variables: Path construction: General
runTimestamp = getTimestamp()
thisFilePath = Path(__file__)
thisFileStem = thisFilePath.stem
projectDir = thisFilePath.absolute().parent.parent
dataDir = projectDir.joinpath("data")
if dataDir:
    inputDataDir = dataDir.joinpath("input")
    intermediateDataDir = dataDir.joinpath("intermediate")
    outputDataDir = dataDir.joinpath("output")
    if intermediateDataDir:
        runIntermediateDataDir = intermediateDataDir.joinpath(thisFileStem, runTimestamp)
    if outputDataDir:
        runOutputDataDir = outputDataDir.joinpath(thisFileStem, runTimestamp)
logsDir = projectDir.joinpath("logs")
if logsDir:
    runLogsDir = logsDir.joinpath(thisFileStem)
sqlDir = projectDir.joinpath("sql")


# Variables: Path construction: Project-specific
pass

# Directory creation: General
make_dir_path(runIntermediateDataDir)
make_dir_path(runOutputDataDir)
make_dir_path(runLogsDir)


if __name__ == "__main__":
    # Logging block
    logpath = runLogsDir.joinpath(f"log {runTimestamp}.log")
    fileHandler = logging.FileHandler(logpath)
    fileHandler.setLevel(LOG_LEVEL)
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(LOG_LEVEL)

    logging.basicConfig(format="[%(asctime)s][%(levelname)s](%(funcName)s): %(message)s",
                        handlers=[fileHandler, streamHandler],
                        level=LOG_LEVEL)

    logging.info(f"""Begin running "{thisFilePath}".""")
    logging.info(f"""All other paths will be reported in debugging relative to `projectDir`: "{projectDir}".""")

    # Script
    logging.info("Reading data")
    data = pd.read_csv(DATA_PATH)
    logging.info("Finished reading data")

    # Analysis for `price`
    VARIABLE_NAME = 'price'
    x = data[VARIABLE_NAME]
    logging.info(f"Analyzing {VARIABLE_NAME}")

    # Manually determine bin widths for `VARIABLE_NAME`
    logging.info("  Getting five-number summary.")
    x1 = x.min()
    x2 = x.quantile(.25)
    x3 = x.quantile(.50)
    x4 = x.mean()
    x5 = x.quantile(.75)
    x6 = x.quantile(.90)
    x7 = x.quantile(.95)
    x8 = x.quantile(.99)
    x9 = x.max()
    sumStatsValues = [x1, x2, x3, x4, x5, x6, x7, x8, x9]
    sumStatsNames = ['min',
                     '25th ptile',
                     'median',
                     'mean',
                     '75th ptile',
                     '90th ptile',
                     '95th ptile',
                     '99th ptile',
                     'max']
    summaryStats = pd.DataFrame([sumStatsValues], columns=sumStatsNames).T
    logging.info(f"Summary statistics for {VARIABLE_NAME}:\n{summaryStats.__str__()}")

    fig1 = plt.figure()
    fignum = fig1.number
    fig = plt.boxplot(data[VARIABLE_NAME])

    # Scatterplots
    logging.info("Plotting scatterplots")
    fig1 = plt.figure()
    fignum = fig1.number
    fig = plt.scatter(data[VARIABLE_NAME], [1] * len(data))
    plt.xlabel(VARIABLE_NAME)
    plt.title('One-Dimensional Scatter Plot')  # (boxplot without box, haha)
    plt.legend(loc="lower right")

    if True:
        # Histogram
        logging.info("Plotting histograms")
        # bins = None  # TODO Can get bin widths using `summaryStats` as starting point
        fig2 = plt.figure()
        fignum = fig2.number
        # NOTE for `bins` I already tried `10`, `1000`, and `20000`. The lines are so thin I can't see them.
        # bins = [x1, x2, x3, x5, x6, x7, x8, x9]  # All same height
        # n, bins, array = plt.hist(data[VARIABLE_NAME], bins='fd')  # NOTE WARNING Freezes computer
        # n, bins, array = plt.hist(data[VARIABLE_NAME], log=True)  # Best result so far
        n, bins, array = plt.hist(data[VARIABLE_NAME])
        # array([4.26869e+05, 0.00000e+00, 4.00000e+00, 2.00000e+00, 0.00000e+00,
    #    0.00000e+00, 0.00000e+00, 0.00000e+00, 3.00000e+00, 2.00000e+00])  # NOTE That there are 4+2+3+2=11 values that are outside the first bin. I sohuld create one bin from the nine right-most bins, and then split up the first bin. The first bin has the following edges: array([0.00000000e+00, 3.73692871e+08]) TODO
        plt.show()

    # End script
    logging.info(f"""Finished running "{thisFilePath.relative_to(projectDir)}".""")
