def get_team_week_info(league='390.l.XXXXXX', team_num='1', week='10'):
    url = 'https://fantasysports.yahooapis.com/fantasy/v2/team/{0}.t.{1}/roster;week={2}'.format(league,team_num,week)
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
        player_points = get_player_points(player_season_id=player_key, week='10')
        team_name = teams['1']['team_name']
        team_player_info = (team_name, week, player_info[0][2]['name']['full'], player_position, player_team_abbr, player_info[1]['selected_position'][1]['position'], player_points)

        team_week_info.append(team_player_info)

    team_week_info_df = pd.DataFrame(team_week_info, index=None)
    header = ['team_name', 'week', 'player_name', 'player_position', 'player_team', 'lineup_position', 'fantasy_points']
    team_week_info_df.columns = header
    return team_week_info_df
