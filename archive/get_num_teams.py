def get_num_teams(league_id='390.l.XXXXXX'):
    url = 'https://fantasysports.yahooapis.com/fantasy/v2/leagues;league_keys={}'.format('390.l.227235')
    response = oauth.session.get(url, params={'format': 'json'})
    r = response.json()

    return r['fantasy_content']['leagues']['0']['league'][0]['num_teams']
