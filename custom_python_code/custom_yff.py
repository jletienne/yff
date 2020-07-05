import pandas as pd
from yahoo_oauth import OAuth2
import logging
import json
from json import dumps
import datetime
import time


class Yahoo_Api():
    def __init__(self,
                 consumer_key,
                 consumer_secret,
                 access_token
                ):
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._access_token = access_token
        self._authorization = None
    def _login(self):
        global oauth
        oauth = OAuth2(None, None, from_file='oauth2yahoo.json')
        if not oauth.token_is_valid():
            oauth.refresh_access_token()

def get_league_settings(league_id):


    url = 'https://fantasysports.yahooapis.com/fantasy/v2/league/{}/settings'.format(league_id)
    response = oauth.session.get(url, params={'format': 'json'})
    r = response.json()


    league_stats = r['fantasy_content']['league'][1]['settings'][0]['stat_modifiers']['stats']

    league_stats_dict = {}
    for stat in league_stats:
        try:
            league_stats_dict[str(stat['stat']['stat_id'])] = stat['stat']['value']
        except:
            pass


    league_stats_dict['10'] = '6' #rush tds are worth 6 points
    league_stats_dict['11'] = '1' #receptions are worth 1 points
    league_stats_dict['12'] = '.1' #receiving yards ere worth .1 points
    league_stats_dict['16'] = '2' #two point conversions are worth 2 points
    league_stats_dict

    league_stats_df = pd.DataFrame(list(league_stats_dict.items()), index=None)

    header = ['stat_id', 'stat_multiplier']
    league_stats_df.columns = header
    return league_stats_df

def get_num_teams(league_id):
    url = 'https://fantasysports.yahooapis.com/fantasy/v2/leagues;league_keys={}'.format(league_id)
    response = oauth.session.get(url, params={'format': 'json'})
    r = response.json()

    return r['fantasy_content']['leagues']['0']['league'][0]['num_teams']

def get_team_names(league_id):
    teams = {}
    num_teams = get_num_teams(league_id)
    for i in range(1, num_teams+1):
        url = 'https://fantasysports.yahooapis.com/fantasy/v2/team/{0}.t.{1}'.format(league_id,str(i))
        response = oauth.session.get(url, params={'format': 'json'})
        r = response.json()

        team = r['fantasy_content']['team'][0]
        team_key = get_team_info(team, 'team_key')
        team_id = get_team_info(team, 'team_id')
        team_name = get_team_info(team, 'name')

        teams[str(team_id)] = {'team_name': team_name, 'team_key': team_key}


    return teams

#team_key, team_id, name
def get_team_info(team_info = None, info = None):
    for i in team_info:
        if list(i.keys())[0] == info:
            return i[info]
    return None

def get_player_points(player_season_id=None, week=None, league_id=None):
    url = 'https://fantasysports.yahooapis.com/fantasy/v2/player/{0}/stats;week={1};type=week'.format(player_season_id, week)
    response = oauth.session.get(url, params={'format': 'json'})
    r = response.json()


    stats = r['fantasy_content']['player'][1]['player_stats']['stats']

    player_stats = {}

    for i in stats:
        player_stats[i['stat']['stat_id']] = i['stat']['value']

    player_stats_df = pd.DataFrame(list(player_stats.items()), index=None)
    header = ['stat_id', 'value']
    player_stats_df.columns = header

    player_scores = player_stats_df.merge(league_multiplier, on='stat_id', how='left').fillna(0)
    player_scores["stat_multiplier"] = player_scores.stat_multiplier.astype(float)
    player_scores["value"] = player_scores.value.astype(float)
    player_scores["fantasy_points"] = player_scores["stat_multiplier"] * player_scores["value"]

    return round(sum(player_scores["fantasy_points"]),2)

#editorial_team_abbr or display_position or player_key
def get_player_info(player_info=None, info=None):

    for i in player_info[0]:
        if list(i.keys())[0] == info:
            return i[info]
    return None

def get_team_week_info(league=None, team_num=None, week=None):
    url = 'https://fantasysports.yahooapis.com/fantasy/v2/team/390.l.XXXXXX.t.{1}/roster;week={2}'.format(league,team_num,week)
    response = oauth.session.get(url, params={'format': 'json'})
    r = response.json()

    team_week_info = []
    team_info = r['fantasy_content']['team'][1]['roster']['0']['players']
    num_players = team_info['count']
    for i in range(num_players):
        player_info = team_info[str(i)]['player']
        player_position = get_player_info(player_info, 'display_position')
        player_team_abbr = get_player_info(player_info, 'editorial_team_abbr')
        player_key = get_player_info(player_info, 'player_key')
        player_points = get_player_points(player_season_id=player_key, week=week, league_id=league)
        team_name = teams[team_num]['team_name']
        team_player_info = (team_name, week, player_info[0][2]['name']['full'], player_position, player_team_abbr, player_info[1]['selected_position'][1]['position'], player_points)

        team_week_info.append(team_player_info)

    team_week_info_df = pd.DataFrame(team_week_info, index=None)
    header = ['team_name', 'week', 'player_name', 'player_position', 'player_team', 'lineup_position', 'fantasy_points']
    team_week_info_df.columns = header
    return team_week_info_df

if __name__ == '__main__':
    'hello'
