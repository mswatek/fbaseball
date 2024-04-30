from yahoofantasy import Context, League
import streamlit as st
import pandas as pd
import numpy as np
import requests,base64
import plotly.express as px
from datetime import datetime

###note for each new season to check if there's an updated version of yahoofantasy to install...otherwise might run into issues

st.set_page_config(layout="wide",page_title="No Lockout!")
st.title(":blue[No More Lockouts in MLB!]")

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


##### BRING IN ALL WEEKS #####
##### BRING IN ALL WEEKS #####
##### BRING IN ALL WEEKS #####
    
all_weeks=pd.DataFrame()
for i in range(0,theweek): #need to automate which week it is. don't pull new week until friday maybe?
    week = league.weeks()[i]
    df = pd.DataFrame({'team':[],'opponent':[], 'cat':[], 'stat':[]})
    df2 = pd.DataFrame({'team':[], 'opponent':[],'cat':[], 'stat':[]})
    for matchup in week.matchups:
        for team1_stat, team2_stat in zip(matchup.team1_stats, matchup.team2_stats):
            df.loc[len(df)] = [matchup.team1.name,matchup.team2.name, team1_stat.display, team1_stat.value]
            df2.loc[len(df2)] = [matchup.team2.name,matchup.team1.name, team2_stat.display, team2_stat.value]

    df_combined = pd.concat([df,df2])
    df_wide = pd.pivot(df_combined, index=['team','opponent'], columns='cat', values='stat')
    df_wide['Week'] = i+1
    frames= [all_weeks,df_wide]
    all_weeks = pd.concat(frames)

all_weeks.reset_index(inplace=True)

st.write(all_weeks)
