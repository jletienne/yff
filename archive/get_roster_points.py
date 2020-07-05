
def get_roster_points():

    url = 'https://fantasysports.yahooapis.com/fantasy/v2/team/390.l.XXXXXX.t.1/roster;week=10'
    response = oauth.session.get(url, params={'format': 'json'})
    r = response.json()


    team_info = r['fantasy_content']['team'][1]['roster']['0']['players']
    num_players = team_info['count']
    for i in range(num_players):
        player_info = team_info[str(i)]['player']
        print(player_info[0][2]['name']['full'], player_info[1]['selected_position'][1]['position'])
