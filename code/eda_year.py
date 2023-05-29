"""
This is a template Python script.
"""

import logging
from pathlib import Path
# Third-party packages
from IPython import get_ipython
import pprint as pp
import matplotlib.pyplot as plt
import pandas as pd
# Local packages
from drapi.drapi import getTimestamp, make_dir_path

# Arguments
LOG_LEVEL = "INFO"

DATA_PATH = Path("data/input/vehicles.csv")


# Arguments: Functions


def eda(columnName, data):
    """
    """
    series = data[columnName]

    # Manually determine bin widths for `columnName`
    x1 = series.min()
    x2 = series.quantile(.25)
    x3 = series.quantile(.50)
    y3 = series.mean()
    x4 = series.quantile(.75)
    x5 = series.quantile(.90)
    x6 = series.quantile(.95)
    x7 = series.quantile(.99)
    x8 = series.max()
    sumStatsValues1 = [x1, x2, x3, x4, x5, x6, x7, x8]
    sumStatsValues2 = ["", "", y3, "", "", "", "", ""]
    sumStatsNames1 = ['min',
                      '25th ptile',
                      'median',
                      '75th ptile',
                      '90th ptile',
                      '95th ptile',
                      '99th ptile',
                      'max']
    sumStatsNames2 = ['',
                      '',
                      'mean',
                      '',
                      '',
                      '',
                      '',
                      '']
    summaryStats = pd.DataFrame([sumStatsNames1, sumStatsValues1, sumStatsValues2, sumStatsNames2]).T
    summaryStats.columns = ["", "Percentiles", "Means", ""]
    summaryStats.index = range(1, len(summaryStats) + 1)
    summaryStats[["Percentiles", "Means"]] = summaryStats[["Percentiles", "Means"]].applymap(lambda el: "" if isinstance(el, str) else f"{int(el):,}")

    # Boxplot
    fig1 = plt.figure()
    fignum1 = fig1.number
    fig1result = plt.boxplot(data[columnName])

    # Histogram
    fig2 = plt.figure()
    fignum2 = fig2.number
    n, bins, fig2result = plt.hist(data[columnName])
    plt.show()
    return summaryStats, (n, bins), [fig1result, fig2result], [fignum1, fignum2]


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
    data0 = pd.read_csv(DATA_PATH)
    logging.info("Finished reading data")

    # EDA
    x = sorted(data0["year"].unique())
    text = pp.pformat(x)
    logging.info(f"""{text}""")

    # View distribution TODO

    # End script
    logging.info(f"""Finished running "{thisFilePath.relative_to(projectDir)}".""")
