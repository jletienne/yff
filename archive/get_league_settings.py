
def get_league_settings(league_id='390.l.XXXXXX'):


    #url = 'https://fantasysports.yahooapis.com/fantasy/v2/leagues;league_keys=390.l.XXXXXX'.format(16)
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


    league_stats_dict['10'] = '0.04'
    league_stats_dict['11'] = '5'
    league_stats_dict['12'] = '-1'
    league_stats_dict['16'] = '0.1'
    league_stats_dict

    league_stats_df = pd.DataFrame(list(league_stats_dict.items()), index=None)

    header = ['stat_id', 'stat_multiplier']
    league_stats_df.columns = header
    return league_stats_df
