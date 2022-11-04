import plotly
import plotly.express as px
from reading_spans import *
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mplcursors import cursor  # separate package must be installed
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter


spanid="ADL-NAR-4670-M-01-GR01-10"
path='data.db'
all_df=get_df(path)
all_df_trimmed=trimmed_df(all_df)
df_spanid=filter_span(all_df_trimmed,spanid)
df=spanificator(df_spanid)
df1=pd.DataFrame()
df1["ot_bool"]=(df["tnd_ot"]>0)
df1["hdd_bool"]=(df["tnd_hdd"]>0)
df1["drt_bool"]=(df["drt"]>0)

df.to_csv("df_spani.csv")

fig,ax=plt.subplots(figsize=(30, 5))
 
#print((df1["ot_bool"]))
#ax.plot(df.index,df["tnd_ot"])
#ax.plot(df.index,df1["ot_bool"],linewidth=2,color="green")
#ax.plot(df.index,(df["tnd_ot"]==1),color="grey")
df["one"]=1
shift=2
        
plt.fill_between(df.index, ((df["tnd_ot"]==1) & (df["tnd_hdd"]==0) & ((df["drt"]==0) ) ),color="palegreen",label="OT Normal case")
plt.fill_between(df.index, ((df["tnd_ot"]==2) & (df["tnd_hdd"]==0) & ((df["drt"]==0) ) ),color="lightgreen",label="OT Overlap case")
plt.fill_between(df.index, ((df["tnd_ot"]==0) & (df["tnd_hdd"]==1) & ((df["drt"]==0) ) ),color="powderblue",label="HDD Normal case")
plt.fill_between(df.index, ((df["tnd_ot"]==0) & (df["tnd_hdd"]==2) & ((df["drt"]==0) ) ),color="lightblue",label="HDD Overlap case")
plt.fill_between(df.index, ((df["tnd_ot"]==0) & (df["tnd_hdd"]==0) & ((df["drt"]==1) ) ),color="sandybrown",label="DRT Normal case")
plt.fill_between(df.index, ((df["tnd_ot"]==0) & (df["tnd_hdd"]==0) & ((df["drt"]==2) ) ),color="peru",label="DRT Overlap case")
plt.fill_between(df.index, ((df["drt"]>2)     & (df["tnd_hdd"]>0)  & (df["tnd_ot"]==0 ) ),color="skyblue",label="DRT where HDD")
plt.fill_between(df.index, ((df["drt"]>2)     & (df["tnd_hdd"]==0)  & (df["tnd_ot"]>0 ) ),color="limegreen",label="DRT where OT")
plt.fill_between(df.index, ((df["tnd_ot"]>0) & (df["tnd_hdd"]>0)),color="indianred",label="OT & HDD overlap")

plt.fill_between(df.index+shift*df["one"],(df["blow"]+shift*df["one"]),shift,where=((df["blow"])==1),color="gold",label="Blowing")
plt.fill_between(df.index+shift*df["one"],(df["blow"]+(shift-1)*df["one"]),shift,where=((df["blow"])==2),color="goldenrod",label="Blowing Overlap")

plt.fill_between(df.index+shift*df["one"],(df["blow_marker"]+(shift)*df["one"]),shift,where=((df["blow_marker"])==1),color="blue",label="Open Loop")
plt.fill_between(df.index+shift*df["one"],(df["blow_marker"]+(shift-1)*df["one"]),shift,where=((df["blow_marker"])==2),color="lime",label="Joint Loop")
plt.fill_between(df.index+shift*df["one"],(df["blow_marker"]+(shift-2)*df["one"]),shift,where=((df["blow_marker"])==3),color="black",label="Other joints")


ax.plot(df.index,(df["drt"]>0),linewidth=1,color="brown",linestyle="--")

cursor(hover=True)
ax.set_xlabel('Chainage')
ax.set_ylabel('Method of Execution')
ax.set_title(spanid)
ax.legend()
x=df.index
plt.xticks(np.arange(min(x), max(x)+1, 100))
mpl.pyplot.yticks(color='w')
plt.xticks(rotation=90)
plt.show()


fig.savefig('myimage.svg', format='svg', dpi=1200)
