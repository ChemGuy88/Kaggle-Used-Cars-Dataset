"""
This is a template Python script.
"""

import logging
from pathlib import Path
# Third-party packages
from IPython import get_ipython
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as st
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

    summaryStats, (n, bins), figresults, fignums = eda("price", data0)
    logging.info(f"Summary statistics for {'price'}, unmodified:\n{summaryStats.__str__()}")

    # NOTE Insert observation note from previous commits TODO
    # Drop top 11 TODO
    data = data0.sort_values(by="price", ascending=False)[11:]
    summaryStats, (n, bins), figresults, fignums = eda("price", data)
    logging.info(f"Summary statistics for {'price'}, dropping 11 highest values:\n{summaryStats.__str__()}")

    # NOTE Insert observation note from previous commits TODO
    # NOTE Observe the inflection point is somewhere between the 99th percentile and the max. So we scan from the top of the decreasing values using a line search beginning with the top 1% of values. The data has 426,880 rows, so the top 1% of values are the top 4,269 when sorted in descending order. For simplicity we index between the 4,000th and 4,050th rows.

    data['price'].sort_values(ascending=False)[4000:4050]

    # NOTE We don't see an inflection point yet, so we choose the midpoint between the max and the 99th percentile, and repeat until we find an inflection point.
    data['price'].sort_values(ascending=False)[2000:2050]
    data['price'].sort_values(ascending=False)[1000:1050]
    data['price'].sort_values(ascending=False)[500:550]
    data['price'].sort_values(ascending=False)[100:150]
    data['price'].sort_values(ascending=False)[50:100]

    # NOTE Now we see where the values begin to lose their organic appearance, and we begin to question the integrity of the data. So this is an inflection point not in the numeric values, but in the trustworthiness of the data. We choose to drop the top 100 values

    data1 = data0.sort_values(by="price", ascending=False)[50:]
    summaryStats, (n, bins), figresults, fignums = eda("price", data1)
    logging.info(f"Summary statistics for {'price'}, dropping 100 highest values:\n{summaryStats.__str__()}")

    # NOTE However, are data is still very skewed. Depending on the analysis we do, we may or may not need normality. Here's a preview to what `"price"` looks like with a log transform. This also reminds us that we have many 0-valued cases. 34,846, in fact.

    # Log transform
    data2 = data0.copy()
    data2["price"] = data2["price"].apply(lambda el: 0 if el == 0 else np.log(el))
    summaryStats, (n, bins), figresults, fignums = eda("price", data2)
    logging.info(f"Summary statistics for {'price'}, log-transform:\n{summaryStats.__str__()}")

    # Log transform without 0-valued cases.
    data3 = data0.copy()
    mask = data3["price"] == 0
    data3 = data3.drop(mask[mask].index)
    data3["price"] = data3["price"].apply(lambda el: 0 if el == 0 else np.log(el))
    summaryStats, (n, bins), figresults, fignums = eda("price", data3)
    logging.info(f"Summary statistics for {'price'}, log-transform without 0s:\n{summaryStats.__str__()}")

    # Compare normality of original, abridged, transformed, and non-zer0-valued transformed versions of `"price"`. The test checks if the distribution is different from the normal distribution. So a positive result (p<0.05) implies non-normality.
    normalityResult1 = st.normaltest(data0["price"])
    normalityResult2 = st.normaltest(data1["price"])
    normalityResult3 = st.normaltest(data2["price"])
    normalityResult4 = st.normaltest(data3["price"])

    # In [2]: normalityResult1
    # Out[2]: NormaltestResult(statistic=2233711.5020345896, pvalue=0.0)
    # In [3]: normalityResult2
    # Out[3]: NormaltestResult(statistic=655983.617009111, pvalue=0.0)
    # In [4]: normalityResult3
    # Out[4]: NormaltestResult(statistic=200245.54625463966, pvalue=0.0)
    # In [5]: normalityResult4
    # Out[5]: NormaltestResult(statistic=256776.586390601, pvalue=0.0)
    logging.info(f"""{normalityResult1}.""")
    logging.info(f"""{normalityResult2}.""")
    logging.info(f"""{normalityResult3}.""")
    logging.info(f"""{normalityResult4}.""")

    # NOTE Although all four transformations are significantly difference, the third option has the smallest statistic (200245).

    # This concludes our exploratory data anlysis for this variable.

    # End script
    logging.info(f"""Finished running "{thisFilePath.relative_to(projectDir)}".""")
