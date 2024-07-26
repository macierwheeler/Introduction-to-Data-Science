import pandas as pd
import plotnine

df = pd.read_csv('/Users/maciewheeler/Downloads/housing.csv')

p = plotnine.ggplot(data=df, mapping=plotnine.aes(x='Price')) +\
    plotnine.geom_histogram(bins=4) +\
    plotnine.ggtitle("Histogram of Price with Outlier")

print(p)
print('The minimum number of bins for the outlier to first be visible is 4')
