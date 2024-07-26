import pandas as pd
import plotnine

df = pd.read_csv('/Users/maciewheeler/Downloads/global_temp.csv')

p = plotnine.ggplot(data=df, mapping=plotnine.aes(x='Year', y='Mean', color='Source')) +\
    plotnine.xlab("Year") +\
    plotnine.ylab("Temperature (°C)") +\
    plotnine.ggtitle('Average Global Temperature in °C per Year') +\
    plotnine.geom_line(size=1.5)

print(p)
