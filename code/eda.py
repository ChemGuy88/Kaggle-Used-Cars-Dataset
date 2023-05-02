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
get_ipython().run_line_magic('matplotlib', "")

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

    # Analysis for `price`: Round 1
    x = data['price']
    logging.info(f"Analyzing {'price'}")

    # Manually determine bin widths for `'price'`
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
    logging.info(f"Summary statistics for {'price'}:\n{summaryStats.__str__()}")

    # Boxplot
    fig1 = plt.figure()
    fignum = fig1.number
    fig = plt.boxplot(data['price'])

    # Histogram
    logging.info("Plotting histograms")
    fig2 = plt.figure()
    fignum = fig2.number
    n, bins, array = plt.hist(data['price'])
    # NOTE `n` reveals that there are 4 + 2 + 3 + 2 = 11 values that are outside the first bin. We can create one bin from the nine right-most bins, and then split up the first bin. We are justified in removing these outliers because we are confident they do not represent actual variable values, but erroneous data inputs. The values are most likely phone numbers.
    # array([4.26869e+05, 0.00000e+00, 4.00000e+00, 2.00000e+00, 0.00000e+00,
#    0.00000e+00, 0.00000e+00, 0.00000e+00, 3.00000e+00, 2.00000e+00])
    plt.show()

    # Remove outliers (first try)
    NUM_OUTLIERS = 11
    x_new = x.sort_values()[:len(x) - 1 - NUM_OUTLIERS]
    
    # NOTE When we remove the top 11 values we still notice that there are some unusual variable values, namely sequential or repeating values. The values are more unusual as we go from the top 100 to the top 20 values. We can make notes of these cases and revisit them in the future. Perhaps there is a reason why the input price value is as exceptional as it is. In the meantime we will only drop the values which made the visualization unsuable, i.e., the top 11 values.

    priceOutliers = x.sort_values()[-NUM_OUTLIERS:]

    # Analysis for `price`: Round 2
    logging.info(f"Analyzing {'price'} without outliers")

    # Manually determine bin widths for `'price'`
    logging.info("  Getting five-number summary.")
    x1 = x_new.min()
    x2 = x_new.quantile(.25)
    x3 = x_new.quantile(.50)
    x4 = x_new.mean()
    x5 = x_new.quantile(.75)
    x6 = x_new.quantile(.90)
    x7 = x_new.quantile(.95)
    x8 = x_new.quantile(.99)
    x9 = x_new.max()
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
    logging.info(f"Summary statistics for {'price'}:\n{summaryStats.__str__()}")

    # Boxplot
    fig1 = plt.figure()
    fignum = fig1.number
    fig = plt.boxplot(x_new)

    # Histogram
    logging.info("Plotting histograms")
    fig2 = plt.figure()
    fignum = fig2.number
    n, bins, array = plt.hist(x_new)
    plt.show()

    # NOTE: After the second round of visualization, we see that the data is still very skewed to the right. This time we have 10 values which are outside the first bin. I should create a function for this and repeat until I get a usuable visualization.

    # End script
    logging.info(f"""Finished running "{thisFilePath.relative_to(projectDir)}".""")
