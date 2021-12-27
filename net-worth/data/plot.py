import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
import scipy.stats as stats
import datetime as dt
import matplotlib.dates as mdates
import json
from matplotlib import style

# let's style the plot up
style.use("dark_background")

# set up arrays for the data
dates = []
values = []

with open("portfolio_data.json") as jsonFile:
    # make 2 lists because dictionaries in Python are unordered
    data = json.load(jsonFile)
    # add the dates and their values to separate lists
    for i in range(len(data)):
        dates.append(list(data[i].keys())[0])
        values.append(sum(list(data[i][dates[i]].values())))
    jsonFile.close()

# sets up the arrays for the plot
xs = [dt.datetime.strptime(d, "%Y-%m-%d").date() for d in dates]
xs_dates = [(xs[i] - xs[0]).days for i in range(len(xs))]
ys = values

# allows the arrays to be used in vector multiplication
xs_np = np.array(xs)
xs_dates_np = np.array(xs_dates)
ys_np = np.array(ys)


# provides the best fit slope and y-intercept
def best_fit_slope_and_intercept(xs_dates_np, ys):
    m = (((mean(xs_dates_np) * mean(ys)) - mean(xs_dates_np * ys)) /
         ((mean(xs_dates_np) ** 2) - (mean(x ** 2 for x in xs_dates_np))))
    b = mean(ys) - m * mean(xs_dates_np)
    return m, b


# gets m and b for y = mx + b
m, b = best_fit_slope_and_intercept(xs_dates_np, ys)

# sets up the plot data
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
plt.xticks(xs)  # sets the ticks on the x-axis according to the dates with data
plt.plot(xs, ys)
plt.gcf().autofmt_xdate()

# sets up the plot title and labels
plt.title("Net Worth Estimate")
plt.xlabel("Date")
plt.ylabel("Net Worth")

# gets the regression line
regression_line = [(m * x) + b for x in xs_dates_np]

# adds the regression line to the plot
plt.plot(xs, regression_line)

# shows the plot
plt.show()
