from yahoofantasy import Context, League
import streamlit as st
import pandas as pd
import numpy as np
import requests,base64
import plotly.express as px
from datetime import datetime

###### to-do list! #####
###### to-do list! #####
###### to-do list! #####
#have best weeks for each category come up on the same trigger as the average cumulative category trend charts
#get rid of index columns on all tables
#change team and opponent to capital first letters
#scatterplot of moves, games played and innings pitched (refer to previous league reports)
#transactions counter - by position, player names, repeats per team
#should I include league info or history info on here? (keeper history, historical standings, league rules, champion photos)
#other cool stuff to add would be the all-time trade history and a map of where everyone lives
#eventually add a tab for the playoff bracket...still need to figure out how to get closer to accurate OBPs without manual
#other individual manager stuff? lucky and unlucky based on how their opponents did compared to average weeks (e.g., I should be expected to do better but a team could get lucky if I have a down week)
#do I take out week 1 for calculating rolling average?
#redo the teams_df table so that it's not hard-coded...will be easier to update next season
#change variable names (e.g.,  cum_total etc)
#add text
#reformat charts
#format numbers so they look nicer in the tables

###note for each new season to check if there's an updated version of yahoofantasy to install...otherwise might run into issues

st.set_page_config(layout="wide",page_title="No Lockout!")
st.title(":blue[No More Lockouts in MLB!]")

tab1, tab2, tab3= st.tabs(["League Trends", "Expected Stats", "Individual Team Stats"])

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

if dow>1: theweek = currentweek
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


##### BRING IN ALL WEEKS #####
##### BRING IN ALL WEEKS #####
##### BRING IN ALL WEEKS #####
    
all_weeks=pd.DataFrame()
for i in range(0,theweek): #need to automate which week it is. don't pull new week until friday maybe?
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

all_weeks=all_weeks.reset_index()

##### Create Matchup Variable #####
##### Create Matchup Variable #####
##### Create Matchup Variable #####

# initialize list of lists
data = [['Lumberjacks', 1], ['Acuña Moncada', 2], ['Aluminum Power', 4],['Bryzzo', 8],['El Squeezo Bunto Dos', 16],['Frozen Ropes',32],['Humdingers', 64], ['I Shota The Sheriff', 128], \
['The Chandler Mandrills', 256],['Baseball GPT', 512],['Santos L. Halper', 1024],['Sheangels',2048]]

# Create the pandas DataFrame
teams_df = pd.DataFrame(data, columns=['Name', 'roster_id'])

all_weeks = pd.merge(all_weeks, teams_df, left_on='Team', right_on='Name',how='left')
all_weeks = pd.merge(all_weeks, teams_df, left_on='Opponent', right_on='Name',how='left')
all_weeks['Matchup1'] = (all_weeks['roster_id_x']+all_weeks['roster_id_y'])
all_weeks['Matchup'] = all_weeks['Matchup1'].astype(str)+'_'+all_weeks['Week'].astype(str)
all_weeks.drop(['roster_id_x', 'roster_id_y', 
                'Matchup1','Name_x','Name_y'], axis=1, inplace=True)


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

    cols = ['Week','Team','Opponent','Matchup','R','HR','RBI','SB','OBP','K','QS','SV+H','ERA','WHIP','IP','IP_New','Earned_Runs','Walk_Hits','Wins']
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

cat_cols = [col for col in all_weeks.columns if col not in ['H/AB', 'Team','Opponent','ERA','WHIP']]
cat_cols2 = [col for col in all_weeks.columns if col in ['H/AB', 'Team','Opponent']]
    
for col in cat_cols:
   all_weeks[f'{col}_cum'] = all_weeks.groupby('Team')[col].cumsum()
   all_weeks[f'{col}_avg'] = all_weeks.groupby('Team')[col].transform(lambda x: x.rolling(20, 1).mean())
   all_weeks[f'{col}_avg3'] = all_weeks.groupby('Team')[col].transform(lambda x: x.rolling(3, 1).mean())

all_weeks['ERA_cum'] = all_weeks['Earned_Runs_cum']/all_weeks['IP_New_cum']*9
all_weeks['ERA_avg'] = all_weeks['Earned_Runs_avg']/all_weeks['IP_New_avg']*9
all_weeks['ERA_avg3'] = all_weeks['Earned_Runs_avg3']/all_weeks['IP_New_avg3']*9

all_weeks['WHIP_cum'] = all_weeks['Walk_Hits_cum']/all_weeks['IP_New_cum']
all_weeks['WHIP_avg'] = all_weeks['Walk_Hits_avg']/all_weeks['IP_New_avg']
all_weeks['WHIP_avg3'] = all_weeks['Walk_Hits_avg3']/all_weeks['IP_New_avg3']

##### WEEKLY RANKS #####
##### WEEKLY RANKS #####
##### WEEKLY RANKS #####

###ignore week for total wins
###trans_summary = transactions_df.query("type == 'waiver' & week != '1'").groupby(['week','Manager']).agg(WinningBids=('waiver_bid', 'count'),MoneySpent=('waiver_bid', 'sum'),MaxPlayer=('waiver_bid', 'max'),MedianPlayer=('waiver_bid', 'median')).reset_index()

nonweek1 = all_weeks[all_weeks["Week"] > 1]
   
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

all_weeks['Wins_Diff'] = all_weeks['Wins'] - all_weeks['Week_Expected']
all_weeks['Wins_Diff_cum'] = all_weeks.groupby('Team')['Wins_Diff'].cumsum()


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


cols = ['Week','Team','R_avg','HR_avg','RBI_avg','SB_avg','OBP_avg','IP_New_cum','ERA_avg','WHIP_avg','K_avg','QS_avg','SV+H_avg' \
        ,'R_avg3','HR_avg3','RBI_avg3','SB_avg3','OBP_avg3','ERA_avg3','WHIP_avg3','K_avg3','QS_avg3','SV+H_avg3']
avg_df = all_weeks[cols]

cols = ['Week','Team','R_weekrank','HR_weekrank','RBI_weekrank','SB_weekrank','OBP_weekrank','ERA_weekrank','WHIP_weekrank','K_weekrank','QS_weekrank','SV+H_weekrank', 'Week_Total', 'Week_Expected' \
        ,'R_totalrank','HR_totalrank','RBI_totalrank','SB_totalrank','OBP_totalrank','ERA_totalrank','WHIP_totalrank','K_totalrank','QS_totalrank','SV+H_totalrank', 'Overall_Total','Overall_Wins']
rank_df = all_weeks[cols]

cols = ['Week','Team','R_avg_cumrank','HR_avg_cumrank','RBI_avg_cumrank','SB_avg_cumrank','OBP_avg_cumrank','ERA_avg_cumrank','WHIP_avg_cumrank','K_avg_cumrank','QS_avg_cumrank','SV+H_avg_cumrank']
cumrank_df = all_weeks[cols]


############################################################################################################
############################################################################################################
############################################################################################################

with tab1:
   st.header("Roto Score by Week")
   st.write("These charts show the standings for if we were in a roto league, where each team is ranked by how well they did in each stat category (10 points for 1st place, 1 for last)."\
              ," The 3-Week Moving Average chart makes it easier to see which teams have been playing well lately. Brett B might be peaking at the right time, according to this chart."\
                 ," The below charts are interactive, so you can hover over the points on each team’s line to see how they progressed in the standings.")
   line = st.selectbox("Choose Metric:", ['Cumulative_Total','Cumulative_Total3'])
   cumulative_roto = px.line(all_weeks, x="Week", y=line, markers=True, color='Team',title="Roto Score by Week").update_xaxes(type='category')
   st.plotly_chart(cumulative_roto, theme=None,use_container_width=True)
   st.write("Click on each stat category to see how your team has progressed in each category over the season. Below the chart is a list of the 10 best weeks for each category."
            ," Note: I took out Weeks 1 and 15 for all counting stats since it was longer than the typical week.")
   line2 = st.selectbox("Choose Metric:", ['R_avg','HR_avg','RBI_avg','SB_avg','OBP_avg','ERA_avg','WHIP_avg','K_avg','QS_avg','SV+H_avg'])
   cumulative_cats = px.line(all_weeks, x="Week", y=line2, markers=True, color='Team',title="Avg Cats by Week").update_xaxes(type='category')
   st.plotly_chart(cumulative_cats, theme=None,use_container_width=True)
   st.write("Here are the best individual weeks of the season.")
   st.write(best_weeks)

with tab2:
   st.header("As Luck Would Have It")
   st.write(lucky_weeks)
   st.write(unlucky_weeks)
   cumulative_expected = px.line(all_weeks, x="Week", y="Wins_Diff_cum", markers=True, color='Team',title="Diff in Expected Wins").update_xaxes(type='category')
   st.plotly_chart(cumulative_expected, theme=None,use_container_width=True)

with tab3:
   st.header("Individual Teams")
   line3 = st.selectbox("Choose Team:", ['Acuña Moncada','Aluminum Power','Bryzzo','El Squeezo Bunto Dos','Frozen Ropes'\
                                     ,'Humdingers', 'I Shota The Sheriff','Lumberjacks','The Chandler Mandrills','Baseball GPT','Santos L. Halper','Sheangels'])
   maxweek = all_weeks['Week'].max()
   cumrank_current = cumrank_df[cumrank_df['Week']== maxweek]
   cumrank_radar = pd.melt(cumrank_current, id_vars='Team', value_vars=['R_avg_cumrank','HR_avg_cumrank','RBI_avg_cumrank','SB_avg_cumrank','OBP_avg_cumrank','ERA_avg_cumrank','WHIP_avg_cumrank','K_avg_cumrank','QS_avg_cumrank','SV+H_avg_cumrank'])

   cumrank_radar = cumrank_radar[cumrank_radar['Team']==line3]
   fig = px.line_polar(cumrank_radar, r='value', theta='variable', line_close=True).update_traces(fill='toself')
   team_individual = reduced_weeks[(reduced_weeks['Team']== line3) & (reduced_weeks['Week']>1)]
   indi_best = team_individual .sort_values('Overall_Wins',ascending = False).head(1)
   indi_worst = team_individual .sort_values('Overall_Wins',ascending = True).head(1)
   st.write(fig)
   st.write(indi_best)
   st.write(indi_worst)

   
