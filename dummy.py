from reading_spans import *
import pandas as pd

spanid="ADL-NAR-4670-M-01-GR01-11"
path='data.db'
#sql extracting dataframes
all_df=get_df(path)

#Extracting only useful columns
all_df_trimmed=trimmed_df(all_df)

#Filter out particular span-id
df_spanid=filter_span(all_df_trimmed,spanid)
# df_drt=df_spanid[2]
# df_drt.to_csv("df_drt.csv")

#Getting all attributes of span-id in one dataframe
df=spanificator(df_spanid)
df.to_csv('spanificator.csv')


#df=ad_logics(df)

#fig=px.line(df,x=df.index,y=[0,1,2,3,4],hover_data=["unique_user"],height=500,markers=True,labels={0: "HDD", 1: "OT", 2: "DRT", 3: "DIT", 4: "Blowing"})    
