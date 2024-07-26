import pandas as pd
import plotnine

df = pd.read_csv('/Users/maciewheeler/Downloads/housing.csv')

maxLoc = df['Price'].idxmax()
ndf = df.iloc[(maxLoc + 1):len(df), ]

p = plotnine.ggplot(data=ndf, mapping=plotnine.aes(x='Location', y='Price')) +\
    plotnine.geom_boxplot(size=2, fill='crimson')

print(p)
