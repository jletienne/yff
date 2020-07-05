
def get_player_points(player_season_id='390.p.28389')
    url = 'https://fantasysports.yahooapis.com/fantasy/v2/player/{}/stats;week=10;type=week'.format(player_season_id)
    response = oauth.session.get(url, params={'format': 'json'})
    r = response.json()


    stats = r['fantasy_content']['player'][1]['player_stats']['stats']

    player_stats = {}

    for i in stats:
        player_stats[i['stat']['stat_id']] = i['stat']['value']
        
    player_stats_df = pd.DataFrame(list(player_stats.items()), index=None)
    header = ['stat_id', 'value']
    player_stats_df.columns = header

    league_multiplier = get_league_settings()

    player_scores = player_stats_df.merge(league_multiplier, on='stat_id', how='left').fillna(0)
    player_scores["stat_multiplier"] = player_scores.stat_multiplier.astype(float)
    player_scores["value"] = player_scores.value.astype(float)
    player_scores["fantasy_points"] = player_scores["stat_multiplier"] * player_scores["value"]

    return sum(player_scores["fantasy_points"])
