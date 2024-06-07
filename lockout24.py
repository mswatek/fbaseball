from yahoofantasy import Context, League
import streamlit as st
import pandas as pd
import numpy as np
import requests,base64
import plotly.express as px
from datetime import datetime
import seaborn as sns
#from time import strftime, localtime

###### to-do list! #####
###### to-do list! #####
###### to-do list! #####
#transactions counter - clean up the table; format date and do a time series chart by day of season
#initial table - games back, difference in wins expected, counts of lucky and unlucky weeks (threshold of 1.5 runs?),IP,PA,Pickups
#luck charts/tables - downgrade them a bit - maybe take off 33%?

#explore individual player data - are players tied to manager team somehow?
#can I incorporate elo rating somehow?
#clusters of teams? might just be similar to the current scatterplot/spider plots

#should I include league info or history info on here? (keeper history, historical standings, league rules, champion photos)
#other cool stuff to add would be the all-time trade history and a map of where everyone lives
#eventually add a tab for the playoff bracket...still need to figure out how to get closer to accurate OBPs without manual

#other individual manager stuff?
#add text/comments
#figure out how to do info button or hover over so that the text doesn't overwhelm on mobile view...st.info ?
#make charts nicer (clean up axis labels)
#format numbers so they look nicer in the tables
#just in general, is there a way to make the interactive charts update faster?

###note for each new season to check if there's an updated version of yahoofantasy to install...otherwise might run into issues

st.set_page_config(layout="wide",page_title="No Lockout!")
st.title(":blue[No More Lockouts in MLB!]")

tab1, tab2, tab3, tab4, tab5= st.tabs(["League Trends","Best Weeks", "Expected Stats", "Individual Team Stats","Transactions"])

now = datetime.now()
now = now.strftime('%Y-%m-%d')

dow = datetime.today().weekday()

if  now > '2024-08-11': currentweek=19
elif now > '2024-08-04': currentweek=18
elif now > '2024-07-28': currentweek=17
elif now > '2024-07-21': currentweek=16
elif now > '2024-07-07': currentweek=15
elif now > '2024-06-30': currentweek=14
elif now > '2024-06-23': currentweek=13
elif now > '2024-06-16': currentweek=12
elif now > '2024-06-09': currentweek=11
elif now > '2024-06-02': currentweek=10
elif now > '2024-05-26': currentweek=9
elif now > '2024-05-19': currentweek=8
elif now > '2024-05-12': currentweek=7
elif now > '2024-05-05': currentweek=6
elif now > '2024-04-28': currentweek=5
elif now > '2024-04-21': currentweek=4
elif now > '2024-04-14': currentweek=3
elif now > '2024-04-07': currentweek=2
else: currentweek=1

if dow>2: theweek = currentweek
else: theweek=currentweek-1


##### ESTABLISH THE CONNECTION #####
##### ESTABLISH THE CONNECTION #####
##### ESTABLISH THE CONNECTION #####


def refreshAuthorizationToken(refreshToken:str) -> dict:
    """Uses existing refresh token to get the new access token"""

    headers: dict = {
        'Authorization': f"Basic {AUTH_HEADER}",
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    }

    data: dict = {
        "redirect_uri": 'oob',
        "grant_type": 'refresh_token',
        "refresh_token": refreshToken
    }

    req = requests.post("https://api.login.yahoo.com/oauth2/get_token",headers=headers,data=data,timeout=100)

    if req.status_code == 200: 

        dobj: dict = req.json()

        return dobj
    
    print("Something went wrong when getting refresh token...try getting the initial access token again!")

    return None


# Plug in your ID & SECRET here from yahoo when you create your app. Make sure you have the correct scope set for fantasy API ex: "read" or "read/write"
CLIENT_ID = "dj0yJmk9VEtpWVNNQzd1TVRtJmQ9WVdrOVRUQkpObXRuTjJrbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTcy"
CLIENT_SECRET = "23f4d294641cc580d381c647f8932711f19a50e8"

# Special auth header for yahoo.
AUTH_HEADER = base64.b64encode(bytes(f"{CLIENT_ID}:{CLIENT_SECRET}".encode("utf-8"))).decode("utf-8")

auth = {
    "access_token": "8gfVehyeulCD48_aK7qLhygosdbMyEFW1fsuuBq32QN8MoZKi4GbTUYkQBnKKCseyQ8u8T65VS74GEVxR_bzbLyZ8O1HCtZz8IVuqwXDLBsJsQFjF.72heACadoNck5sjDKrNGpY.VwqFAoKJFHWoRdhF8Nz_B4Wrr.LWV3WFQunULvnS6A39UF_eHq60H4s7DoZUypxkUp7lqfy7osuZalM1kQASkKWNFlsNogWmJlO6aDU6Ujoo9ZhggvEsY90heL3GsLWSAqjONHcSA6W_6vT4BzTPeFA0M3Se5u0PV6O5LQz8DUxxFeGmBoJ7k8LAxFk0KfVc901fBftS4_ZmMwZtwJUyAsCEnqmjWDsapbAy5eIaiz9LAKAUi_m8S6P2xAhHwqcG2NfDHmGY8pdD7j3KkWerQStNVB6iWDPzjXSpQI18XgVL35oB34GV4n6pWY0di_WMF8v1rFhCJOrMu8afTYnuO6zmD7_G_hJllZDbIT.tXCYOx1p2_A8.HHb.cyOw6Q3qpVOl1Xy33mQmfwVfTxGfDwtuQ5z.85Ka1GUur4kok0laQ6y4kF2qsc4PUMFdhn.p531QtGQToqDsX_1ILeBfCk1FiCe1zNoqfQqn6vBlkVEiJdSjQHR4Ba0spbMzVWIZiKA7mc9vddxf0su6Ho4HwzKQU8.BO0fk2jr3CYLx3Tu4baYReKUTTXBV9oqps6Wn1QBbVUXGjaIe.uFZMsw3DllMnka5I9O74tob3XUA2u8S.kNcIoV4UYn.6jkwKkSw577dOTce.QfWXkWc.rnRvKPX3Q1JRglK7SFfuiVFOuy8Xvu6kFrdjT3SSAwClgmXUcacbocp3zQP8vHSyV9oojCMr_bdXzZC9KRQKZwAUbsbzzf._1RdDYepaP_83dyczYnSPqEHeiY",
    "refresh_token": "AMooCWXYBYMcjT_AzcfJWIeedRC4~000~nJZ43mNIt2q7pdxBi3U-",
    "expires_in": 3600,
    "token_type": "bearer",
}


# Anytime the context is used, I would wrap it in a try except block in case it needs to get a new token.
try:

    ctx = Context(persist_key="oauth2",client_id=CLIENT_ID,client_secret=CLIENT_SECRET,refresh_token=auth["refresh_token"])
    league: list = ctx.get_leagues("mlb", 2024)[0]

except Exception:

    # Get refresh token
    auth = refreshAuthorizationToken(auth["refresh_token"])
    ctx = Context(persist_key="oauth2",client_id=CLIENT_ID,client_secret=CLIENT_SECRET,refresh_token=auth["refresh_token"])
    league: list = ctx.get_leagues("mlb", 2024)[0]


##### TRANSACTIONS DATA #####
##### TRANSACTIONS DATA #####
##### TRANSACTIONS DATA #####

all_transactions=pd.DataFrame()
for transaction in league.transactions():
    df = pd.DataFrame()
    if transaction.type == "add/drop": 
        test = transaction.players.player[0]
        df = pd.DataFrame({"Player":test.name.first+" "+test.name.last,"Team":test.editorial_team_abbr,"Position":test.display_position,"Time":transaction.timestamp,"Type":test.transaction_data.source_type,"Manager":test.transaction_data.destination_team_name}, index=[0])
    elif transaction.type == "add":
        test = transaction.players.player
        df = pd.DataFrame({"Player":test.name.first+" "+test.name.last,"Team":test.editorial_team_abbr,"Position":test.display_position,"Time":transaction.timestamp,"Type":test.transaction_data.source_type,"Manager":test.transaction_data.destination_team_name}, index=[0])
    else: 
        df = pd.DataFrame({"Player":1,"Team":1,"Position":1,"Time":1,"Type":1,"Manager":1}, index=[0])
    
    frames= [all_transactions,df]
    all_transactions = pd.concat(frames)

all_transactions = all_transactions[all_transactions["Player"] != 1]

all_transactions['Time'] = pd.to_datetime(all_transactions['Time'], unit='s', utc=True).map(lambda x: x.tz_convert('US/Pacific'))
all_transactions['Day'] = all_transactions['Time'].dt.date
all_transactions['DOW'] = all_transactions['Time'].dt.day_name()
all_transactions['Position2'] = np.where(all_transactions['Position'].isin(['SP','RP']), "Pitcher", "Hitter")

all_transactions = all_transactions[(all_transactions['Time'] > "2024-03-29")] ##take out first waiver day of the year, 3/28; skews numbers too much

# creating transaction tables
daily_df = all_transactions.groupby(['Day'])['Manager'].agg('count').reset_index(name='Count')
daily_df = (daily_df.set_index('Day')
      .reindex(pd.date_range('2024-03-29', now)) #take out the first day of the season - it skews the numbers!
      .rename_axis(['Day'])
      .fillna(0)
      .reset_index())
daily_df['Rolling'] = daily_df['Count'].rolling(7).mean()

day_order = ['Monday', 'Tuesday', 'Wednesday','Thursday','Friday','Saturday','Sunday']

dow_df = all_transactions.groupby(['DOW',"Position2"])['Manager'].agg('count').reset_index(name='Count')
dow_df = dow_df.set_index('DOW').loc[day_order].reset_index()


player_df = all_transactions.groupby(['Player','Position','Team'])['Manager'].agg('count').reset_index(name='Count')
team_df = all_transactions.groupby(['Team'])['Manager'].agg('count').reset_index(name='Count')
manager_df = all_transactions.groupby(['Manager'])['Player'].agg('count').reset_index(name='Count')
position_df = all_transactions.groupby(['Position'])['Manager'].agg('count').reset_index(name='Count') ##strip out players that have multiple positions to make extra rows

# Split out multi-position players
position_df.Position = position_df.Position.str.split(',')
position_df = position_df.explode('Position')

position_df = position_df.groupby(['Position'])['Count'].agg('sum').reset_index(name='Count')

# create transaction charts
position_tree = px.treemap(position_df, path=['Position'], values='Count',
                  color='Position', hover_data=['Position'],title="Tree Map of Pickups by Position")

team_tree = px.treemap(team_df, path=['Team'], values='Count',
                  color='Team', hover_data=['Team'],title="Tree Map of Pickups by Team")

team_player_tree = px.treemap(player_df, path=['Team','Player'], values='Count',
                  color='Team', hover_data=['Team','Player'],title="Tree Map of Pickups by Team")


trans_line = px.bar(daily_df, x="Day", y="Count",title="Transactions by Day").add_traces(px.line(daily_df, x="Day", y="Rolling",markers=True).update_traces(line_color='#0000ff',showlegend=True, name="Rolling").data)

dow_bar = px.bar(dow_df, x="DOW", y="Count",color="Position2",title="Transactions by Day of Week") 


##### BRING IN ALL WEEKS #####
##### BRING IN ALL WEEKS #####
##### BRING IN ALL WEEKS #####

@st.cache_data
def load_data():
    all_weeks=pd.DataFrame()
    for i in range(0,theweek):
        week = league.weeks()[i]
        df = pd.DataFrame({'Team':[],'Opponent':[], 'cat':[], 'stat':[]})
        df2 = pd.DataFrame({'Team':[], 'Opponent':[],'cat':[], 'stat':[]})
        for matchup in week.matchups:
            for team1_stat, team2_stat in zip(matchup.team1_stats, matchup.team2_stats):
                df.loc[len(df)] = [matchup.team1.name,matchup.team2.name, team1_stat.display, team1_stat.value]
                df2.loc[len(df2)] = [matchup.team2.name,matchup.team1.name, team2_stat.display, team2_stat.value]

        df_combined = pd.concat([df,df2])
        df_wide = pd.pivot(df_combined, index=['Team','Opponent'], columns='cat', values='stat')
        df_wide['Week'] = i+1
        frames= [all_weeks,df_wide]
        all_weeks = pd.concat(frames)

    return all_weeks

all_weeks = load_data()

all_weeks=all_weeks.reset_index()


##### Create Matchup Variable #####
##### Create Matchup Variable #####
##### Create Matchup Variable #####

team_list = all_weeks['Team'].tolist()
team_list = list(set(team_list))
id_list = [1,2,4,8,16,32,64,128,256,512,1024,2048] ##creating unique IDs that are unique no matter the combination of adding two together

teams_df = pd.DataFrame(list(zip(team_list, id_list)), columns = ['Name', 'roster_id'])

all_weeks = pd.merge(all_weeks, teams_df, left_on='Team', right_on='Name',how='left')
all_weeks = pd.merge(all_weeks, teams_df, left_on='Opponent', right_on='Name',how='left')
all_weeks['Matchup1'] = (all_weeks['roster_id_x']+all_weeks['roster_id_y'])
all_weeks['Matchup'] = all_weeks['Matchup1'].astype(str)+'_'+all_weeks['Week'].astype(str)
all_weeks.drop(['roster_id_x', 'roster_id_y', 
                'Matchup1','Name_x','Name_y'], axis=1, inplace=True)

##### GET AT-BATS #####
##### GET AT-BATS #####
##### GET AT-BATS #####

all_weeks[['H', 'AB']] = all_weeks['H/AB'].str.split('/', expand=True)


##### FIX PITCHING CATEGORIES #####
##### FIX PITCHING CATEGORIES #####
##### FIX PITCHING CATEGORIES #####

all_weeks['IP_DECIMAL'] = (all_weeks['IP'] - np.fix(all_weeks['IP']))*10/3
all_weeks['IP_FULL'] = np.fix(all_weeks['IP'])
all_weeks['IP_New'] = all_weeks['IP_DECIMAL'] + all_weeks['IP_FULL']
all_weeks['Earned_Runs'] = all_weeks['ERA']*all_weeks['IP_New']/9
all_weeks['Walk_Hits'] = all_weeks['WHIP']*all_weeks['IP_New']


##### CHANGE VARIABLE FORMATS #####
##### CHANGE VARIABLE FORMATS #####
##### CHANGE VARIABLE FORMATS #####

cat_cols = [col for col in all_weeks.columns if col not in ['H/AB', 'Team','Opponent','ERA','WHIP']]
cat_cols2 = [col for col in all_weeks.columns if col in ['H/AB', 'Team','Opponent']]

for col in cat_cols:
    all_weeks[col] = all_weeks[col].astype('float')

for col in cat_cols2:
    all_weeks[col] = all_weeks[col].astype('string')

##### CREATE OBP VARIABLES #####
##### CREATE OBP VARIABLES #####
##### CREATE OBP VARIABLES #####

all_weeks['OnBase'] = (all_weeks['OBP']*all_weeks['AB']-all_weeks['H'])/(1-all_weeks['OBP'])+all_weeks['H']
all_weeks['PA'] = (all_weeks['OBP']*all_weeks['AB']-all_weeks['H'])/(1-all_weeks['OBP'])+all_weeks['AB']

all_weeks['OnBase'] = all_weeks['OnBase'].astype(int)
all_weeks['PA'] = all_weeks['PA'].astype(int)

for index, row in all_weeks.iterrows():
    while all_weeks.at[index,'OnBase']/all_weeks.at[index,'PA'] - all_weeks.at[index,'OBP'] <-0.0005 :
        all_weeks.at[index,'OnBase'] = all_weeks.at[index,'OnBase']+1
        all_weeks.at[index,'PA'] = all_weeks.at[index,'PA']+2
        all_weeks.at[index,'OBP_New'] = all_weeks.at[index,'OnBase']/all_weeks.at[index,'PA']

##### Create Actual Wins Variable #####
##### Create Actual Wins Variable #####
##### Create Actual Wins Variable #####

def scores(df):
    max_val = df[['R','HR','RBI','SB','OBP','K','QS','SV+H']].max(axis=0)
    count_max = df.eq(max_val, axis=1).sum(axis=1).reset_index(name ='Wins')

    min_val = df[['ERA','WHIP']].min(axis=0)
    count_min = df.eq(min_val, axis=1).sum(axis=1).reset_index(name ='Wins')

    total_1 = pd.concat([count_max,count_min])
    total_1 = total_1.groupby(['index'])[["Wins"]].apply(lambda x : x.astype(int).sum())

    df = df.merge(total_1, left_index=True, right_on='index')

    cols = ['Week','Team','Opponent','Matchup','H','OnBase','PA','AB','R','HR','RBI','SB','OBP','K','QS','SV+H','ERA','WHIP','IP','IP_New','Earned_Runs','Walk_Hits','Wins']
    df = df[cols]

    return df

matchup_list = all_weeks['Matchup'].tolist()
all_matchups =pd.DataFrame()


for i in matchup_list:
    dfsub = all_weeks[all_weeks['Matchup'] == i]
    dfsub = scores(dfsub)
    Total = dfsub['Wins'].sum()
    if Total>10: dfsub['Wins'] = dfsub['Wins']-((Total-10)/2)
    else: dfsub['Wins'] = dfsub['Wins']
    frames= [all_matchups,dfsub]
    all_matchups = pd.concat(frames)

all_matchups.reset_index(inplace=True)
all_weeks = all_matchups #converting the score dataset back to all_weeks
all_weeks = all_weeks.drop_duplicates()
all_weeks = all_weeks.sort_values(['Week', 'Team'], ascending=[True, True])


##### CUMULATIVE SUM AND AVG/MOVING AVG VARIABLES #####
##### CUMULATIVE SUM AND AVG/MOVING AVG VARIABLES #####
##### CUMULATIVE SUM AND AVG/MOVING AVG VARIABLES #####

nonweek1 = all_weeks[all_weeks["Week"] > 1]

cat_cols = [col for col in all_weeks.columns if col not in ['H/AB', 'Team','Opponent','ERA','WHIP','OBP']]
cat_cols2 = [col for col in all_weeks.columns if col in ['H/AB', 'Team','Opponent']]
    
for col in cat_cols:
   all_weeks[f'{col}_Cumulative'] = all_weeks.groupby('Team')[col].cumsum()
   all_weeks[f'{col}_avg'] = all_weeks.groupby('Team')[col].transform(lambda x: x.rolling(20, 1).mean())
   all_weeks[f'{col}_avg3'] = all_weeks.groupby('Team')[col].transform(lambda x: x.rolling(3, 1).mean())
   all_weeks[f'{col}_avg_reg'] = nonweek1.groupby('Team')[col].transform(lambda x: x.rolling(20, 1).mean())

all_weeks['ERA_Cumulative'] = all_weeks['Earned_Runs_Cumulative']/all_weeks['IP_New_Cumulative']*9
all_weeks['ERA_avg'] = all_weeks['Earned_Runs_avg']/all_weeks['IP_New_avg']*9
all_weeks['ERA_avg3'] = all_weeks['Earned_Runs_avg3']/all_weeks['IP_New_avg3']*9
all_weeks['ERA_avg_reg'] = all_weeks['Earned_Runs_avg_reg']/all_weeks['IP_New_avg_reg']*9

all_weeks['WHIP_Cumulative'] = all_weeks['Walk_Hits_Cumulative']/all_weeks['IP_New_Cumulative']
all_weeks['WHIP_avg'] = all_weeks['Walk_Hits_avg']/all_weeks['IP_New_avg']
all_weeks['WHIP_avg3'] = all_weeks['Walk_Hits_avg3']/all_weeks['IP_New_avg3']
all_weeks['WHIP_avg_reg'] = all_weeks['Walk_Hits_avg_reg']/all_weeks['IP_New_avg_reg']

all_weeks['OBP_Cumulative'] = all_weeks['OnBase_Cumulative']/all_weeks['PA_Cumulative']
all_weeks['OBP_avg'] = all_weeks['OnBase_avg']/all_weeks['PA_avg']
all_weeks['OBP_avg3'] = all_weeks['OnBase_avg3']/all_weeks['PA_avg3']
all_weeks['OBP_avg_reg'] = all_weeks['OnBase_avg_reg']/all_weeks['PA_avg_reg']

##### WEEKLY RANKS #####
##### WEEKLY RANKS #####
##### WEEKLY RANKS #####

###ignore week for total wins
###trans_summary = transactions_df.query("type == 'waiver' & week != '1'").groupby(['week','Manager']).agg(WinningBids=('waiver_bid', 'count'),MoneySpent=('waiver_bid', 'sum'),MaxPlayer=('waiver_bid', 'max'),MedianPlayer=('waiver_bid', 'median')).reset_index()
   
cat_cols = [col for col in all_weeks.columns if col in ['R', 'HR','RBI','SB','OBP','K','QS','SV+H']]
cat_cols2 = [col for col in all_weeks.columns if col in ['ERA', 'WHIP']]

for col in cat_cols:
    all_weeks[f'{col}_weekrank'] = all_weeks.groupby('Week')[col].rank(method="average", ascending=True)
    all_weeks[f'{col}_totalrank'] = nonweek1[col].rank(method="average", ascending=True)

for col in cat_cols2:
    all_weeks[f'{col}_weekrank'] = all_weeks.groupby('Week')[col].rank(method="average", ascending=False)
    all_weeks[f'{col}_totalrank'] = nonweek1[col].rank(method="average", ascending=False)

weekrank_list = ['R_weekrank','HR_weekrank','RBI_weekrank','SB_weekrank','OBP_weekrank','ERA_weekrank','WHIP_weekrank','K_weekrank','QS_weekrank','SV+H_weekrank']
all_weeks['Week_Total'] =all_weeks.loc[:,weekrank_list].sum(axis=1)
all_weeks['Week_Expected'] = (all_weeks['Week_Total']-10)/110*10

totalrank_list = ['R_totalrank','HR_totalrank','RBI_totalrank','SB_totalrank','OBP_totalrank','ERA_totalrank','WHIP_totalrank','K_totalrank','QS_totalrank','SV+H_totalrank']
all_weeks['Overall_Total']=all_weeks.loc[:,totalrank_list].sum(axis=1)
maxweek = all_weeks['Week'].max()
all_weeks['Overall_Wins'] = (all_weeks['Overall_Total']-10)/((maxweek-1)*120-10)*10

all_weeks['Wins_Diff'] = all_weeks['Wins'] - all_weeks['Week_Expected'] # do I multiply by 2/3 to reflect managers doing things differently in different matchups?
all_weeks['Wins_Diff_Cumulative'] = all_weeks.groupby('Team')['Wins_Diff'].cumsum()


##### CUMULATIVE RANKS #####
##### CUMULATIVE RANKS #####
##### CUMULATIVE RANKS #####

cat_cols = [col for col in all_weeks.columns if col in ['R_avg', 'HR_avg','RBI_avg','SB_avg','OBP_avg','K_avg','QS_avg','SV+H_avg']]
cat_cols2 = [col for col in all_weeks.columns if col in ['ERA_avg', 'WHIP_avg']]

for col in cat_cols:
   all_weeks[f'{col}_cumrank'] = all_weeks.groupby('Week')[col].rank(method="average", ascending=True)

for col in cat_cols2:
   all_weeks[f'{col}_cumrank'] = all_weeks.groupby('Week')[col].rank(method="average", ascending=False)

cumtotal_list = ['R_avg_cumrank','HR_avg_cumrank','RBI_avg_cumrank','SB_avg_cumrank','OBP_avg_cumrank','ERA_avg_cumrank','WHIP_avg_cumrank','K_avg_cumrank','QS_avg_cumrank','SV+H_avg_cumrank']
all_weeks['Cumulative_Total']=all_weeks.loc[:,cumtotal_list].sum(axis=1)

cat_cols = [col for col in all_weeks.columns if col in ['R_avg3', 'HR_avg3','RBI_avg3','SB_avg3','OBP_avg3','K_avg3','QS_avg3','SV+H_avg3']]
cat_cols2 = [col for col in all_weeks.columns if col in ['ERA_avg3', 'WHIP_avg3']]

for col in cat_cols:
   all_weeks[f'{col}_cumrank'] = all_weeks.groupby('Week')[col].rank(method="average", ascending=True)

for col in cat_cols2:
   all_weeks[f'{col}_cumrank'] = all_weeks.groupby('Week')[col].rank(method="average", ascending=False)

cumtotal3_list = ['R_avg3_cumrank','HR_avg3_cumrank','RBI_avg3_cumrank','SB_avg3_cumrank','OBP_avg3_cumrank','ERA_avg3_cumrank','WHIP_avg3_cumrank','K_avg3_cumrank','QS_avg3_cumrank','SV+H_avg3_cumrank']
all_weeks['Cumulative_Total3']=all_weeks.loc[:,cumtotal3_list].sum(axis=1)

##### Create Strength of Schedule #####
##### Create Strength of Schedule #####
##### Create Strength of Schedule #####

cols = ['Week','Team', 'Opponent','Week_Expected']
strength_df = all_weeks[cols]
strength_df['Avg_Wins'] = strength_df.groupby('Team')['Week_Expected'].transform('mean')
strength_df['Difference'] = strength_df['Week_Expected'] - strength_df['Avg_Wins']
strength_df['% Difference'] = (strength_df['Week_Expected'] - strength_df['Avg_Wins'])/strength_df['Avg_Wins']
strength_df = strength_df[['Opponent', 'Team','Week','Week_Expected','Avg_Wins','Difference','% Difference']] #re-arrange the order
strength_df.rename(columns={'Opponent': 'Team','Team':'Opponent','Week_Expected':'Opponent_Expected','Avg_Wins':'Opponent_Avg'},inplace=True)

strength_cats = strength_df
conditions = [strength_cats['% Difference'] >.3,strength_cats['% Difference'] >.15,strength_cats['% Difference'] <-.3,strength_cats['% Difference']<-.15,strength_cats['% Difference']>0,strength_cats['% Difference']<0]
choices = ['Way Overperformed (30% better)', 'Slightly Overperformed', 'Really Sucked (30% worse)', 'Was A Bit Worse','Was Average (within 15%)','Was Average (within 15%)']
strength_cats['Opponent...'] = np.select(conditions, choices, default='black')
strength_cats= strength_cats.groupby(['Team','Opponent...'])['Opponent...'].agg('count').reset_index(name='Count')
cat_order = ['Really Sucked (30% worse)', 'Was A Bit Worse', 'Was Average (within 15%)', 'Slightly Overperformed','Way Overperformed (30% better)']
strength_cats = strength_cats.set_index('Opponent...').loc[cat_order].reset_index()

strength_overall = strength_df.groupby('Team').agg(DiffSum=('Difference', 'sum'),PercentDiff=('% Difference', 'mean')).reset_index()
strength_overall = strength_overall.sort_values(by='PercentDiff',ascending=False)

##### CREATE SUBSETS FOR TABLES #####
##### CREATE SUBSETS FOR TABLES #####
##### CREATE SUBSETS FOR TABLES #####

cols = ['Week','Team','Opponent','R','HR','RBI','SB','OBP','IP','ERA','WHIP','K','QS','SV+H','Week_Expected','Overall_Wins']
best_weeks = all_weeks[cols]
best_weeks = best_weeks.sort_values('Overall_Wins',ascending = False).head(10)

cols = ['Week','Team','Opponent','Week_Expected','Wins','Wins_Diff']
difference = all_weeks[cols]
lucky_weeks = difference.sort_values('Wins_Diff',ascending = False).head(10)
unlucky_weeks = difference.sort_values('Wins_Diff',ascending = True).head(10)

cols = ['Week','Team','Opponent','R','HR','RBI','SB','OBP','IP','ERA','WHIP','K','QS','SV+H','Week_Expected','Wins','Overall_Wins']
reduced_weeks = all_weeks[cols]

cols = ['Week','Team','R_avg_reg','HR_avg_reg','RBI_avg_reg','SB_avg_reg','OBP_avg_reg','IP_New_avg_reg','ERA_avg_reg','WHIP_avg_reg','K_avg_reg','QS_avg_reg','SV+H_avg_reg']
cumulative_cats_df = all_weeks[cols]
cumulative_cats_df.rename(columns={'R_avg_reg': 'R','HR_avg_reg':'HR','RBI_avg_reg':'RBI','SB_avg_reg':'SB','OBP_avg_reg':'OBP','ERA_avg_reg':'ERA','WHIP_avg_reg':'WHIP','K_avg_reg':'K','QS_avg_reg':'QS','SV+H_avg_reg':'SV+H'},inplace=True)
cumulative_cats_df = cumulative_cats_df[cumulative_cats_df["Week"] > 1]

cols = ['Week','Team','Opponent','R','HR','RBI','SB','OBP','IP','ERA','WHIP','K','QS','SV+H']
top_cats_df = all_weeks[cols]
top_cats_df = top_cats_df[top_cats_df["Week"] > 1] ##get rid of week 1

cols = ['Week','Team','R_avg','HR_avg','RBI_avg','SB_avg','OBP_avg','IP_New_Cumulative','ERA_avg','WHIP_avg','K_avg','QS_avg','SV+H_avg' \
        ,'R_avg3','HR_avg3','RBI_avg3','SB_avg3','OBP_avg3','ERA_avg3','WHIP_avg3','K_avg3','QS_avg3','SV+H_avg3']
avg_df = all_weeks[cols]

cols = ['Week','Team','R_weekrank','HR_weekrank','RBI_weekrank','SB_weekrank','OBP_weekrank','ERA_weekrank','WHIP_weekrank','K_weekrank','QS_weekrank','SV+H_weekrank', 'Week_Total', 'Week_Expected' \
        ,'R_totalrank','HR_totalrank','RBI_totalrank','SB_totalrank','OBP_totalrank','ERA_totalrank','WHIP_totalrank','K_totalrank','QS_totalrank','SV+H_totalrank', 'Overall_Total','Overall_Wins']
rank_df = all_weeks[cols]

cols = ['Week','Team','R_avg_cumrank','HR_avg_cumrank','RBI_avg_cumrank','SB_avg_cumrank','OBP_avg_cumrank','ERA_avg_cumrank','WHIP_avg_cumrank','K_avg_cumrank','QS_avg_cumrank','SV+H_avg_cumrank']
cumrank_df = all_weeks[cols]
cumrank_df.rename(columns={'R_avg_cumrank':'R','HR_avg_cumrank':'HR','RBI_avg_cumrank':'RBI','SB_avg_cumrank':'SB','OBP_avg_cumrank':'OBP','ERA_avg_cumrank':'ERA','WHIP_avg_cumrank':'WHIP','K_avg_cumrank':'K','QS_avg_cumrank':'QS','SV+H_avg_cumrank':'SV+H'},inplace=True)

### standings combined

maxweek = all_weeks['Week'].max()
standings_current = all_weeks.loc[all_weeks['Week'] == maxweek]

cols = ['Team','Wins_Cumulative','Cumulative_Total','Cumulative_Total3']
standings_current = standings_current[cols]

#cols2 = ['Wins_Cumulative','Cumulative_Total','Cumulative_Total3']
#for col in cols2:
#    standings_current[col] = standings_current[col].astype('float')

standings_current = standings_current.sort_values("Wins_Cumulative",ascending = False)

# dont think I need rank columns
standings_current['Place'] = standings_current['Wins_Cumulative'].rank(method="average", ascending=False)
#standings_current['Roto_Rank'] = standings_current['Cumulative_Total'].rank(method="average", ascending=False)
#standings_current['Roto3_Rank'] = standings_current['Cumulative_Total3'].rank(method="average", ascending=False)

cols = ['Team','Place','Wins_Cumulative','Cumulative_Total','Cumulative_Total3']
standings_current = standings_current[cols]

cm_power = sns.light_palette("green", as_cmap=True)

### scatterplot

scatter_current = all_weeks.loc[all_weeks['Week'] == maxweek]



cols = ['Team','Wins_Cumulative','PA_Cumulative','IP_New_Cumulative']
scatter_current = scatter_current[cols]

scatter_current = pd.merge(scatter_current, manager_df, left_on='Team', right_on='Manager', how='left')

med_pa = scatter_current["PA_Cumulative"].median()
med_ip = scatter_current["IP_New_Cumulative"].median()

scatter_plot = px.scatter(scatter_current, x="PA_Cumulative", y="IP_New_Cumulative", color="Wins_Cumulative",
                 size='Count',text='Team').add_hline(y=med_ip,line_color="green").add_vline(x=med_pa,line_color="green").update_layout(title="League Landscape")


############################################################################################################
############################################################################################################
############################################################################################################

with tab1:
   st.header("Overall League Trends")
   st.dataframe(standings_current.style.format({'Wins_Cumulative': "{:.1f}",'Cumulative_Total': "{:.1f}",'Cumulative_Total3': "{:.1f}"}).\
                background_gradient(cmap=cm_power, subset=['Wins_Cumulative','Cumulative_Total','Cumulative_Total3']),hide_index=True,use_container_width=True)
   st.plotly_chart(scatter_plot, theme=None,use_container_width=True)

   st.write("These charts show the standings for if we were in a roto league, where each team is ranked by how well they did in each stat category (10 points for 1st place, 1 for last)."\
              ," The 3-Week Moving Average chart makes it easier to see which teams have been playing well lately. Brett B might be peaking at the right time, according to this chart."\
                 ," The below charts are interactive, so you can hover over the points on each team’s line to see how they progressed in the standings.")
   line = st.selectbox("Choose Metric:", ['Cumulative_Total','Cumulative_Total3'])
   cumulative_roto = px.line(all_weeks, x="Week", y=line, markers=True, color='Team', symbol='Team',color_discrete_sequence=px.colors.qualitative.Light24,title="Cumulative Roto Standings").update_xaxes(type='category')
   st.plotly_chart(cumulative_roto, theme=None,use_container_width=True)
   

with tab2:
   st.header("Best Weeks")
   st.write("Click on each stat category to see how your team has progressed in each category over the season. Below the chart is a list of the 10 best weeks for each category."
            ," Note: I took out Weeks 1 and 15 for all counting stats since it was longer than the typical week.")
   line2 = st.selectbox("Choose Metric:", ['R','HR','RBI','SB','OBP','ERA','WHIP','K','QS','SV+H'])
   cumulative_cats = px.line(cumulative_cats_df, x="Week", y=line2, markers=True, color='Team', symbol='Team',color_discrete_sequence=px.colors.qualitative.Light24,title="Avg Cats by Week").update_xaxes(type='category')
   st.plotly_chart(cumulative_cats, theme=None,use_container_width=True)
   if line2 in ['ERA','WHIP']: top_cats_df2 = top_cats_df.sort_values(line2,ascending = True).head(10)
   else: top_cats_df2 = top_cats_df.sort_values(line2,ascending = False).head(10)
   st.dataframe(top_cats_df2,hide_index=True,use_container_width=True)
   st.write("Here are the best individual weeks of the season.")
   st.dataframe(best_weeks,hide_index=True,use_container_width=True)

with tab3:
   st.header("As Luck Would Have It")
   st.dataframe(lucky_weeks,hide_index=True,use_container_width=True)
   st.dataframe(unlucky_weeks,hide_index=True,use_container_width=True)
   cumulative_expected = px.line(all_weeks, x="Week", y="Wins_Diff_Cumulative", markers=True, color='Team', symbol='Team',color_discrete_sequence=px.colors.qualitative.Light24,title="Difference In Wins (Actual-Expected)").update_xaxes(type='category')
   st.plotly_chart(cumulative_expected, theme=None,use_container_width=True)

with tab4:
   st.header("Individual Teams")
   st.write("Use the dropdown menu to view stats for each team.")
   line3 = st.selectbox("Choose Team:", team_list)
   maxweek = cumrank_df['Week'].max()
   cumrank_current = cumrank_df[cumrank_df['Week']== maxweek]
   cumrank_radar = pd.melt(cumrank_current, id_vars='Team', value_vars=['R','HR','RBI','SB','OBP','ERA','WHIP','K','QS','SV+H'])
   cumrank_radar = cumrank_radar[cumrank_radar['Team']==line3]
   fig = px.line_polar(cumrank_radar, r='value', theta='variable', line_close=True).update_traces(fill='toself')
   team_individual = reduced_weeks[(reduced_weeks['Team']== line3) & (reduced_weeks['Week']>1)]
   indi_best = team_individual .sort_values('Overall_Wins',ascending = False).head(2)
   indi_worst = team_individual .sort_values('Overall_Wins',ascending = True).head(2)
   strength_indi = strength_df[strength_df['Team']==line3]
   st.write("Radar charts are back by popular demand! Figure out where your team struggles and try to make some moves!")
   st.write(fig)
   st.write("These are the best weeks for {team} as defined by Overall_Wins.").format(team=line3)
   st.dataframe(indi_best,hide_index=True,use_container_width=True)
   st.write("These are the worst weeks for {team} as defined by Overall_Wins.").format(team=line3)
   st.dataframe(indi_worst,hide_index=True,use_container_width=True)
   st.write("This table shows how the opponents of {team} did each week (Opponent_Expected) compared to their weekly average (Opponent_Avg). You can compare across weeks with % Difference.").format(team=line3)
   st.dataframe(strength_indi,hide_index=True,use_container_width=True)
   #strength_bar = px.bar(strength_overall, x="Team", y="PercentDiff",color="PercentDiff",color_continuous_scale="RdYlGn_r").update_layout(title="Opponent Performance Relative to Average",yaxis_title="Opponent Performance (% Different Than Average)").update_coloraxes(showscale=False) 
   #st.plotly_chart(strength_bar, theme=None,use_container_width=True)
   #strength_box = px.violin(strength_df, x="Team", y="% Difference",color="Team", hover_data="Opponent").update_layout(title="Opponent Performance Relative to Average",yaxis_title="Opponent Performance (% Different Than Average)",showlegend=False)
   #st.plotly_chart(strength_box, theme=None,use_container_width=True)
   strength_bar = px.bar(strength_cats, x="Team", y="Count",color="Opponent...",color_discrete_sequence=["red", "orange", "yellow", "blue", "green"],title="Opponent Performance By Week")
   st.write("See how opponent variation plays out for each team in the bar chart below. Teams with a lot of green and blue have had some tough schedule luck.")
   st.plotly_chart(strength_bar, theme=None,use_container_width=True)

with tab5:
   st.header("Transactions")
   st.write("This chart shows the number of league-wide transactions per day along with a 7-day rolling average.")
   st.plotly_chart(trans_line)
   st.write("Unsurprisingly, the first and last days of the week have the most adds.")
   st.plotly_chart(dow_bar)
   st.write("A lot of managers stream pitchers, and that shows up in this tree map of adds by position.")
   st.plotly_chart(position_tree)
   st.write("The team/player tree map is kinda fun, identifying players that have been picked up multiple times and teams that have more streamable/volatile players.")
   st.plotly_chart(team_player_tree,use_scontainer_width=True)
   

   
