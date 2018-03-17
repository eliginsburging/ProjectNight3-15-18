from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from pprint import pprint as pp
import pdb
from itertools import groupby

app = Flask(__name__)
app.debug = True
import meetup.api
app.config['SECRET_KEY'] = 'foobar'

toolbar = DebugToolbarExtension(app)

def get_names():
    client = meetup.api.Client("your meetup API key here (keep quotes)")

    rsvps=client.GetRsvps(event_id='your meetup event ID here', urlname='_ChiPy_')
    member_id = ','.join([str(i['member']['member_id']) for i in rsvps.results])
    members = client.GetMembers(member_id=member_id)

    foo={}
    for member in members.results:
        try:
            foo[member['name']] = member['photo']['thumb_link']
        except:
            pass # ignore those who do not have a complete profile
    return foo

member_rsvps=get_names()

@app.route('/rsvps')
def rsvps():
    return render_template('rsvps.html', rsvps=member_rsvps)


@app.route('/teams', methods=['GET', 'POST'])
def teams():
    all_people = request.form.to_dict()
    all_teams = []
    count = 0
    team = {}
    total_lines = 0
    for person, num_lines in all_people.items():
        pdb.set_trace()
        count += 1
        team[person] = num_lines
        total_lines += int(num_lines)
        if count == 4:
            all_teams.append((team, total_lines))
            count = 0
            total_lines = 0
            team = {}
    if team:
        all_teams.append((team, total_lines))
    # pdb.set_trace()
    pp(all_teams)
    return render_template('teams.html', teams=all_teams)

if __name__ == '__main__':
    app.run(debug=True)
