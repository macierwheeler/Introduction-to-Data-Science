import pandas as pd
import plotnine

df = pd.read_csv('/Users/maciewheeler/Downloads/cars_information.csv')

p = plotnine.ggplot(data=df, mapping=plotnine.aes(x='hp', y='mpg', color='factor(am)')) +\
    plotnine.geom_point() +\
    plotnine.geom_smooth(method='lm')

print(p)
