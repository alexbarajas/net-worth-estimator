import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
import scipy.stats as stats
import datetime as dt
import matplotlib.dates as mdates
import json
from matplotlib import style

filename = "portfolio_data.json"


class Plot:
    def __init__(self, filename):
        self.filename = filename
        # let's style the plot up
        style.use("dark_background")

        # set up arrays for the data
        dates = []
        values = []

        with open(self.filename) as jsonFile:
            # make 2 lists because dictionaries in Python are unordered
            data = json.load(jsonFile)
            # add the dates and their values to separate lists
            for i in range(len(data)):
                dates.append(list(data[i].keys())[0])
                values.append(sum(list(data[i][dates[i]].values())))
            jsonFile.close()

        # sets up the arrays for the plot
        self.xs = [dt.datetime.strptime(d, "%Y-%m-%d").date() for d in dates]
        self.xs_dates = [(self.xs[i] - self.xs[0]).days for i in range(len(self.xs))]
        self.ys = values

        # allows the arrays to be used in vector multiplication
        self.xs_np = np.array(self.xs)
        self.xs_dates_np = np.array(self.xs_dates)
        self.ys_np = np.array(self.ys)

    # provides the best fit slope and y-intercept
    def best_fit_slope_and_intercept(self, xs_dates_np, ys):
        m = (((mean(xs_dates_np) * mean(ys)) - mean(xs_dates_np * ys)) /
             ((mean(xs_dates_np) ** 2) - (mean(x ** 2 for x in xs_dates_np))))
        b = mean(ys) - m * mean(xs_dates_np)
        return m, b

    def setup_plot(self):
        # gets m and b for y = mx + b
        m, b = self.best_fit_slope_and_intercept(self.xs_dates_np, self.ys)

        # sets up the plot data
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.xticks(self.xs)  # sets the ticks on the x-axis according to the dates with data
        plt.plot(self.xs, self.ys)
        plt.gcf().autofmt_xdate()

        # sets up the plot title and labels
        plt.title("Net Worth Estimate")
        plt.xlabel("Date")
        plt.ylabel("Net Worth")

        # gets the regression line
        regression_line = [(m * x) + b for x in self.xs_dates_np]

        # adds the regression line to the plot
        plt.plot(self.xs, regression_line)

        # shows the plot
        plt.show()


# Plot(filename).setup_plot()
