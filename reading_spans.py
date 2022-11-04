import sqlite3
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mplcursors import cursor  # separate package must be installed
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter
import datetime


#class get_span:
def get_df(path):
    cnx = sqlite3.connect(path)
    df_tnd = pd.read_sql_query("SELECT * FROM 'tnd'", cnx)
    df_hdd = pd.read_sql_query("SELECT * FROM 'hdd'", cnx)
    # cnx.execute("ALTER TABLE drt RENAME COLUMN ch_to TO Chainage_To")    
    # cnx.execute("ALTER TABLE drt RENAME COLUMN ch_from TO Chainage_From")
    df_drt = pd.read_sql_query("SELECT * FROM 'drt'", cnx)
    df_dit = pd.read_sql_query("SELECT * FROM 'dit'", cnx)
    df_blow = pd.read_sql_query("SELECT * FROM 'blowing'", cnx)
    # df_tnd.to_csv('tnd.csv')
    # df_hdd.to_csv('hdd.csv')
    # df_drt.to_csv('drt.csv')
    # df_dit.to_csv('dit.csv')
    # df_blow.to_csv('blow.csv')
    all_df=[df_tnd,df_hdd,df_drt,df_dit,df_blow]
    return all_df

def trimmed_date(all_df):
    [df_tnd,df_hdd,df_drt,df_dit,df_blow]=all_df
    for i in range(len(all_df)):
        all_df[i]=all_df[i][all_df[i].end > pd.to_datetime(datetime.datetime.now() - pd.to_timedelta("7day"))]

    return all_df

def trimmed_col(all_df):
    [df_tnd,df_hdd,df_drt,df_dit,df_blow]=all_df
    # df_hdd["Method"]="HDD"
    # df_tnd["Method"]="OT"
    # df_drt["Method"]="DRT"
    # df_dit["Method"]="DIT"
    # df_blow["Method"]="Blowing"


    df_hdd=df_hdd[["User","end","Span_ID","Chainage_From","Chainage_To"]]
    df_tnd=df_tnd[["User","end","Span_ID","Chainage_From","Chainage_To"]]
    df_drt=df_drt[["User","end","Span_ID","Chainage_From","Chainage_To","Duct_dam_punct_loc_ch_from","Duct_dam_punct_loc_ch_to","Duct_miss_ch_from","Duct_miss_ch_to"]]
    df_dit=df_dit[["User","end","Span_ID","Chainage_From","Chainage_To"]]
    df_blow=df_blow[["User","end","Span_ID","Chainage_From","Chainage_To"]]
    df_hdd=df_hdd.mask(df_hdd == '')
    df_tnd=df_tnd.mask(df_tnd == '')
    df_drt=df_drt.mask(df_drt == '')
    df_dit=df_dit.mask(df_dit == '')
    df_blow=df_blow.mask(df_blow == '')
    all_df=[df_tnd,df_hdd,df_drt,df_dit,df_blow]
    return all_df


def spanificator(all_df):
    start=0
    end=7210
    df=pd.DataFrame()
    #tnd (ot) i=0
    i=0
    array = [0 for x in range(start,end)]
    for j in range(len(all_df[i])):
        for k in range(int(all_df[i].loc[j,"Chainage_From"]),int(all_df[i].loc[j,"Chainage_To"])):
            if array[k]<=1: 
                array[k]+=1
    df["tnd_ot"]=array
    
    i=1
    array = [0 for x in range(start,end)]
    for j in range(len(all_df[i])):
        for k in range(int(all_df[i].loc[j,"Chainage_From"]),int(all_df[i].loc[j,"Chainage_To"])):
            if array[k]<=1: 
                array[k]+=1
    df["tnd_hdd"]=array

    i=2
    array = [0 for x in range(start,end)]
    for j in range(len(all_df[i])):
        for k in range(int(all_df[i].loc[j,"Chainage_From"]),int(all_df[i].loc[j,"Chainage_To"])):
            if pd.isnull(all_df[i].loc[j,"Duct_dam_punct_loc_ch_from"]) and pd.isnull(all_df[i].loc[j,"Duct_dam_punct_loc_ch_to"]) and pd.isnull(all_df[i].loc[j,"Duct_miss_ch_from"]) and pd.isnull(all_df[i].loc[j,"Duct_miss_ch_to"]):
                    if array[k]<=1: 
                        array[k]+=1
            elif pd.isnull(all_df[i].loc[j,"Duct_miss_ch_from"]) and pd.isnull(all_df[i].loc[j,"Duct_miss_ch_to"]):
                    if array[k]<=10: 
                        array[k]+=10
            elif pd.isnull(all_df[i].loc[j,"Duct_dam_punct_loc_ch_from"]) and pd.isnull(all_df[i].loc[j,"Duct_dam_punct_loc_ch_to"]):
                   if array[k]<=100: 
                        array[k]+=100
    df["drt"]=array
    
    i=4
    array = [0 for x in range(start,end)]
    array3 = [3 for x in range(start,end)]
    for j in range(len(all_df[i])):
        for k in range(int(all_df[i].loc[j,"Chainage_From"]),int(all_df[i].loc[j,"Chainage_To"])):
            if array[k]<=1: 
                array[k]+=1
    df["blow"]=array

    i=4
    array = [0 for x in range(start,end)]
    for j in range(len(all_df[i])):
            array[int(all_df[i].loc[j,"Chainage_From"])]+=1
            array[int(all_df[i].loc[j,"Chainage_To"])]+=1
    df["blow_marker"]=array 

    return df

def spanfill(all_df):
    start=-200
    end=20000
    df=pd.DataFrame()
    for i in range(len(all_df)):
        array=[]
        arb=[]
        arc=[]
        array = [0 for i in range(start,end)]
        arb = [0 for i in range(start,end)]
        arc = [0 for i in range(start,end)]
        for j in range(len(all_df[i])):
            for k in range(int(all_df[i].loc[j,"Chainage_From"]),int(all_df[i].loc[j,"Chainage_To"])):
                array[k]+=1
                arb[k]=all_df[i].loc[j,"User"]
                arc[k]=all_df[i].loc[j,"end"]
        df[i]=array
        a=str(i)+" User"
        b=str(i)+" Date"
        df[a]=arb
        df[b]=arc
        #print(df.head())
    return df
                      
def filter_span(all_df,span_id):
    for i in range(len(all_df)):
        all_df[i]=all_df[i][all_df[i].Span_ID==span_id]
        all_df[i] = all_df[i].reset_index(drop=True)
    return all_df    
        
        
def ad_logics(df):
    ##trim the df
    #df_user=df[["0 User","1 User","2 User","3 User","4 User"]]
    df["unique_user"]=np.nan
    for i in range(len(df)):
        a=df.loc[i,"0 User"]
        b=df.loc[i,"1 User"]
        c=df.loc[i,"2 User"]
        d=df.loc[i,"3 User"]
        e=df.loc[i,"4 User"]
        df.loc[i,'unique_user'] = a if a!=0 else b if b!=0 else c if c!=0 else d if d!=0 else e if e!=0 else np.nan
            
    #df_user['uniques_user'] =  df_user.replace(0, np.NaN).unique(axis=1)
    #df["users"]=df_user['uniques_user']
    return df

###########################################################################################################################
##Need to check span id if not available throw warning?/ explicitly write on terminal
def check_span(spanid,all_df):
    df=0
    for j in range(len(all_df)):
        count=0
        for i in range(len(all_df[j])):
            if (all_df[j]['Span_ID'][i]==spanid):
                count+=1
        if count==0:
            print("No span id matching in "+str(df))
        df+=1       
###########################################################################################################################             
def df_formatdata(all_df):
    for i in range(len(all_df)):
        all_df[i]['end'] = pd.to_datetime(all_df[i]['end'], format='%Y-%m-%d %H:%M:%S.%f').dt.date
    return all_df
###########################################################################################################################             
def df_info(all_df):
    for i in range(len(all_df)):
        print(all_df[i].info())
###########################################################################################################################
def plot_span(y,df,spanid,method,color):
    #xmin=df['Chainage_From'][0]
    #print("1")
    for i in range(len(df)):
        if (df['Span_ID'][i]==spanid):
            plt.hlines(y,df['Chainage_From'][i],df['Chainage_To'][i],color=color,linewidth=7)
            #xmin=min(xmin,df['Chainage_From'][i])
    #plt.text(xmin,y,method, ha='left', va='baseline',weight='bold')       
###########################################################################################################################
def plot_fig(df,spanid):
    fig,ax=plt.subplots(figsize=(40, 5))
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

    plt.fill_between(df.index+shift*df["one"],(df["blow"]+shift*df["one"]),shift,where=((df["blow"])==1),color="orange",label="Blowing")
    plt.fill_between(df.index+shift*df["one"],(df["blow"]+(shift-1)*df["one"]),shift,where=((df["blow"])==2),color="darkorange",label="Blowing Overlap")

    plt.fill_between(df.index+shift*df["one"],(df["blow_marker"]+(shift)*df["one"]),shift,where=((df["blow_marker"])==1),color="blue",label="Open Loop")
    plt.fill_between(df.index+shift*df["one"],(df["blow_marker"]+(shift-1)*df["one"]),shift,where=((df["blow_marker"])==2),color="lime",label="Joint Loop")
    plt.fill_between(df.index+shift*df["one"],(df["blow_marker"]+(shift-2)*df["one"]),shift,where=((df["blow_marker"])==3),color="black",label="Other joints")


    ax.plot(df.index,(df["drt"]>0),linewidth=1,color="brown",linestyle="--")

    #cursor(hover=True)
    ax.set_xlabel('Chainage')
    ax.set_ylabel('Method of Execution')
    ax.set_title(spanid)
    ax.legend()
    x=df.index
    plt.xticks(np.arange(min(x), max(x)+1, 50))
    mpl.pyplot.yticks(color='w')
    plt.xticks(rotation = 90)
    plt.show()
    image=spanid+"-visualize"+".svg"
    fig.savefig(image, format='svg', dpi=1200)
    