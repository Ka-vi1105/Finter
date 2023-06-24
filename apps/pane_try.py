import pandas as pd
import numpy as np
import panel as pn
import hvplot.pandas

pn.extension('tabulator')

df = pd.read_csv('/home/uwu/Finter/logs_table.csv')
# print(df[df['event'] == 'modified'])
# print(df)
idf = df.interactive()
# df.hvplot(x='event', y='modified', kind='line')
df_plot = df.hvplot(x='event', y='modified')


template = pn.template.FastListTemplate(
    title="IDK",
    main=[pn.Row(pn.Column(df_plot.panel(width=700), margin=(0, 25)))]
)
template.servable()