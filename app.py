from flask import render_template, Flask, redirect
import os
import requests
import math
from staff_info import staff_information
import psycopg2


app = Flask(__name__)

baseurl = 'http://127.123.123.123:5000'
domain = baseurl

group_ids = {
    "Admins": [1055102391046918166, 751494512236429415, 513652385424605193, 721800684671991828, 1145793269574410261],
    "CoOwners": [513652385424605193],
    "Contributors": [513652385424605193, 721800684671991828, 1145793269574410261, 1055102391046918166, 751494512236429415, 1058795248400203816],
    "Designers": [721800684671991828, 1058795248400203816],
    "Owner": [721800684671991828],
    "Translator": [1145793269574410261, 721800684671991828, 812592544969654313, 1055102391046918166, 266512529746952192],
    "Partner": [909446748613779486, 392444539060879372, 1059943522591047700]
}
def encode_badges(user_id, badges_dict):
    sorted_badge_names = sorted(badges_dict.keys())
    badges_number = 0
    for badge_name in sorted_badge_names:
        if user_id in badges_dict[badge_name]:
            badge_index = sorted_badge_names.index(badge_name)
            power_of_2 = 2**badge_index
            badges_number |= power_of_2
    return badges_number

def decode_badges(badges_number, badges_dict):
    decoded_badges = []
    current_power_of_2 = 1
    while badges_number:
        if badges_number & 1:
            badge_index = int(math.log2(current_power_of_2))
            badge_name = sorted(badges_dict.keys())[badge_index]  # Use sorted keys
            decoded_badges.append(badge_name)
        badges_number >>= 1
        current_power_of_2 <<= 1
    return decoded_badges


def user_badges(userid, badges):
    badgess = []
    for badge in badges:
        for id in badges[badge]:
            if int(userid) == int(id):
                badgess.append(badge)
    return badgess


staff = {
    "721800684671991828": {"stat":"Developer", "icon":"static/staff/pfps/dangercode.png", "type": "", "link": "/staff/dangercode"},
    "513652385424605193": {"stat":"Developer", "icon":"static/staff/pfps/lediamant.png", "type": "copy", "link": "/staff/lediamant"},
    "692197998939209789": {"stat":"Moderator", "icon":"static/staff/pfps/franklin.png", "type": "freelancer", "link": "/staff/franklin"},
    "832687914198630462": {"stat":"Contributor", "icon":"static/staff/pfps/qi.png", "type": "blog", "link": "/staff/qi"},
}

def get_invite(guildid):
    invites = {
        "1171130263556866158" : "https://discord.gg/WyW4u7FntM",
        "1125196330646638592" : "https://discord.gg/VZfSa9HuXy",
        "1009171205808476260" : "https://discord.gg/mKMmDNMxH4",
        "1113407305464164352" : "https://discord.gg/uDKEWGQKAk",
        "1165489533526220840" : "https://discord.gg/jCvEKtES6d",
        "1118225386824794174" : "https://discord.gg/H7ZUaj9PnC",
         "945617849848836097" : "https://discord.gg/bTB7RRnx84",
    }
    return invites[str(guildid)]

@app.route('/')
def mainpage():
        return redirect("/en")

@app.route('/en')
def home():
    return render_template('/home/index.html', baseurl=baseurl, staff=staff)

@app.route('/invite/bot')
def invitebot():
    return redirect("https://discord.com/api/oauth2/authorize?client_id=996646955885277245&permissions=8&scope=bot%20applications.commands")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)