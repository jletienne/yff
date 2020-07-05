def get_team_names(league_id='390.l.XXXXXX'):
    teams = {}
    num_teams = get_num_teams(league_id)
    for i in range(1, num_teams+1):
        url = 'https://fantasysports.yahooapis.com/fantasy/v2/team/{0}.t.{1}'.format('390.l.227235',str(i))
        response = oauth.session.get(url, params={'format': 'json'})
        r = response.json()

        team = r['fantasy_content']['team'][0]
        team_key = team[0]['team_key']
        team_id = team[1]['team_id']
        team_name = team[2]['name']

        teams[str(team_id)] = {'team_name': team_name, 'team_key': team_key}


    return teams
