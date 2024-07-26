import pandas as pd
import plotnine

df = pd.read_csv('/Users/maciewheeler/Downloads/housing.csv')

p = plotnine.ggplot(data=df, mapping=plotnine.aes(x='Sqft', y='Price')) +\
    plotnine.geom_point(mapping=plotnine.aes(color='Location', size='Baths'), alpha=.6) +\
    plotnine.xlab('Area in square feet') +\
    plotnine.ylab('Price per square foot') +\
    plotnine.ggtitle('Visualization of House prices')

print(p)
