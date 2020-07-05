#team_key, team_id, name
def get_team_info(team_info = None, info = 'team_key'):
    for i in team_info:
        if list(i.keys())[0] == info:
            return i[info]
    return None
