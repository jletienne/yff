weekly_team_stats = []

opponent = {'0': '1', '1': '0'}
url = 'https://fantasysports.yahooapis.com/fantasy/v2/team/390.l.XXXXXX.t.1/roster;week=10'
response = oauth.session.get(url, params={'format': 'json'})
r = response.json()
r


team_info = r['fantasy_content']['team'][1]['roster']['0']['players']
num_players = team_info['count']
for i in range(num_players):
    player_info = team_info[str(i)]['player']
    print(player_info[0][2]['name']['full'], player_info[1]['selected_position'][1]['position'])




weekly_team_stats = []

opponent = {'0': '1', '1': '0'}
url = 'https://fantasysports.yahooapis.com/fantasy/v2/player/390.p.28389/stats;week=10'
response = oauth.session.get(url, params={'format': 'json'})
r = response.json()
r

player_stats = {}
for i in stats:
    player_stats[i['stat']['stat_id']] = i['stat']['value']
player_stats


def get_league_settings(league_id='390.l.XXXXXX'):


    url = 'https://fantasysports.yahooapis.com/fantasy/v2/league//settings'.format(league_id)
    response = oauth.session.get(url, params={'format': 'json'})
    r = response.json()


    league_stats = r['fantasy_content']['league'][1]['settings'][0]['stat_modifiers']['stats']

    league_stats_dict = {}
    for stat in league_stats:
        try:
            league_stats_dict[str(stat['stat']['stat_id'])] = stat['stat']['value']
        except:
            pass


    league_stats_dict['10'] = '0.04'
    league_stats_dict['11'] = '5'
    league_stats_dict['12'] = '-1'
    league_stats_dict['16'] = '0.1'
    league_stats_dict

    league_stats_df = pd.DataFrame(list(league_stats_dict.items()), index=None)

    header = ['stat_id', 'stat_multiplier']
    league_stats_df.columns = header
    return league_stats_df
