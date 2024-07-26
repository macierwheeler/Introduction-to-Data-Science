import pandas as pd
import plotnine

df = pd.read_csv('/Users/maciewheeler/Downloads/cars_information.csv')

fdf = pd.melt(df, id_vars=['mpg'], value_vars=['disp', 'hp'])

p = plotnine.ggplot(data=fdf, mapping=plotnine.aes(x='mpg', y='value')) +\
    plotnine.geom_point() +\
    plotnine.geom_smooth(method='lm') +\
    plotnine.facet_wrap('variable')

print(p)
