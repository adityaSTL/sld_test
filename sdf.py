import matplotlib.pyplot as plt
from reading_spans import *
import pandas as pd
spanid="ADL-NAR-4670-M-01-GR01-11"
path='data.db'
all_df=get_df(path)
all_df_trimmed=trimmed_df(all_df)
df_spanid=filter_span(all_df_trimmed,spanid)
df=spanificator(df_spanid)
# df.set_index(df.index,inplace=True)
# df.rename(columns = {df.index:'Chainage'}, inplace = True)
#df.to_csv("df.csv")
fig,ax = plt.subplots()
sc = plt.scatter(df,x=df.index, y=["tnd_ot","tnd_hdd","drt"],height=500,markers=True)
#fig1=px.line(df,x=df.index, y=["tnd_ot","tnd_hdd","drt"],height=500,markers=True)
#fig = px.line(df, x=df.index, y=["tnd_ot","tnd_hdd","drt"], title='Life expectancy in Canada'markers=True)
plt.show()