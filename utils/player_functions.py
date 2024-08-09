import requests
from dotenv import load_dotenv
import os
import json

load_dotenv() 
hypixel_api_key = os.getenv("HYPIXEL_API_KEY")

""" ==========================================
* Player Functions SECTION
*
* This module contains utility functions for
* getting player data values such as ranks, levels,
* and plus colors, etc.
*
* NOTE: Running the /restart does not work on utils.
* Utils requires a full client restart.
========================================== """



""" ==========================================
* Player rank/tags functions below
========================================== """

def fetch_player_data(api_key, uuid):
    url = f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}"
    response = requests.get(url)
    data = response.json()
    #print(data)
    return data



def get_player_rank(player_data):
    if not player_data['success']:
        return f"Error: {player_data['cause']}"
    
    player = player_data['player']
    if player is None:
        return "Player not found"
    
    rank = ''
    if 'prefix' in player:
        rank = player['prefix'].replace('§', '').replace('[', '').replace(']', '')
    elif 'rank' in player and player['rank'] != 'NORMAL':
        rank = player['rank']
    elif 'monthlyPackageRank' in player and player['monthlyPackageRank'] != 'NONE':
        rank = 'MVP++'
    elif 'newPackageRank' in player:
        rank = player['newPackageRank'].replace('_PLUS', '+')
    else:
        rank = 'Non-Rank'
    
    return rank


ranks = {
    "ADMIN": [['c', "[ADMIN]"]],
    "MODERATOR": [['2', "[MOD]"]],
    "HELPER": [['9', "[HELPER]"]],
    "JR_HELPER": [['9', "[JR HELPER]"]],
    "YOUTUBER": [['c', "[YOUTUBE]", 'f', "]"]],
    "SUPERSTAR": [['%r', "[MVP"], ['%p', "++"], ['%r', "]"]],
    "MVP_PLUS": [['b', "[MVP"], ['%p', "+"], ['b', "]"]],
    "MVP": [['b', "[MVP]"]],
    "VIP_PLUS": [['a', "[VIP"], ['6', "+"], ['a', "]"]],
    "VIP": [['a', "[VIP]"]],
    "DEFAULT": [['7', ""]]
}

colors = {
    "BLACK": '0', "DARK_BLUE": '1', "DARK_GREEN": '2', "DARK_AQUA": '3',
    "DARK_RED": '4', "DARK_PURPLE": '5', "GOLD": '6', "GRAY": '7',
    "DARK_GRAY": '8', "BLUE": '9', "GREEN": 'a', "AQUA": 'b',
    "RED": 'c', "LIGHT_PURPLE": 'd', "YELLOW": 'e', "WHITE": 'f'
}

default_plus_color = 'c'  # %p
default_rank_color = '6'  # %r

def replace_custom_colors(rank, p, r):
    if not isinstance(rank, list):
        return rank

    new_rank = json.loads(json.dumps(rank))  # Deep copy

    if not p or len(p) > 1:
        p = default_plus_color
    if not r or len(r) > 1:
        r = default_rank_color

    for component in new_rank:
        if isinstance(component, list) and len(component) >= 2:
            if component[0] == "%p":
                component[0] = p
            if component[0] == "%r":
                component[0] = r

    return new_rank

def parse_minecraft_tag(tag):
    if tag and isinstance(tag, str):
        new_rank = []
        split_tag = tag.split('§')
        split_tag.pop(0)  # Remove the first empty string
        split_tag.insert(0, 'f')  # Beginning is always white

        for i in range(0, len(split_tag), 2):
            j = i // 2  # First index
            k = i % 2  # Second index

            if len(new_rank) <= j:
                new_rank.append(['', ''])
            new_rank[j][k] = split_tag[i]

        return new_rank
    else:
        return [['f', '']]

def calc_tag(player):
    if player and isinstance(player, dict):
        package_rank = player.get('packageRank')
        new_package_rank = player.get('newPackageRank')
        monthly_package_rank = player.get('monthlyPackageRank')
        rank_plus_color = player.get('rankPlusColor')
        monthly_rank_color = player.get('monthlyRankColor')
        rank = player.get('rank')
        prefix = player.get('prefix')

        if rank == "NORMAL":
            rank = None
        if monthly_package_rank == "NONE":
            monthly_package_rank = None
        if package_rank == "NONE":
            package_rank = None
        if new_package_rank == "NONE":
            new_package_rank = None

        if prefix and isinstance(prefix, str):
            return parse_minecraft_tag(prefix)
        if rank or monthly_package_rank or new_package_rank or package_rank:
            rank_key = rank or monthly_package_rank or new_package_rank or package_rank
            return replace_custom_colors(ranks.get(rank_key, ranks['DEFAULT']), colors.get(rank_plus_color), colors.get(monthly_rank_color))

    return replace_custom_colors(ranks['DEFAULT'], None, None)

def get_player_tag(data):

    if not data['success']:
        return f"Error: {data['cause']}"
    
    player = data['player']
    if player is None:
        return "Player not found"
    
    tag = calc_tag(player)
    return tag





""" ==========================================
* Player network level section below
========================================== """

def get_level(exp):
    BASE = 10000
    GROWTH = 2500
    HALF_GROWTH = 0.5 * GROWTH
    REVERSE_PQ_PREFIX = -(BASE - 0.5 * GROWTH) / GROWTH
    REVERSE_CONST = REVERSE_PQ_PREFIX * REVERSE_PQ_PREFIX
    GROWTH_DIVIDES_2 = 2 / GROWTH

    if exp < 0:
        return 1
    level = 1 + REVERSE_PQ_PREFIX + (REVERSE_CONST + GROWTH_DIVIDES_2 * exp) ** 0.5
    return level

def get_exact_level(exp):
    return get_level(exp) + get_percentage_to_next_level(exp)

def get_percentage_to_next_level(exp):
    level = get_level(exp)
    x0 = get_total_exp_to_level(level)
    return (exp - x0) / (get_total_exp_to_level(level + 1) - x0)

def get_total_exp_to_level(level):
    BASE = 10000
    GROWTH = 2500
    HALF_GROWTH = 0.5 * GROWTH

    if level < 1:
        return BASE
    return (HALF_GROWTH * (level - 2) + BASE) * (level - 1)

def get_network_level(player_data):
    if not player_data['success']:
        return f"Error: {player_data['cause']}"
    
    player = player_data['player']
    if player is None:
        return "Player not found"
    
    experience = player.get('networkExp', 0)
    level = round(get_exact_level(experience), 2)
    
    return level


# Fetch player data
def fetch_player_data(api_key, uuid):
    url = f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}"
    response = requests.get(url)
    return response.json()



def get_bedwars_level_tag(level):
    # NOTE that after level 999, tags carry different
    # colors etc. This will be implemented later. 
    # as for now, they will all be color 4.
    
    if level >= 1000:
        color_code = '4'
    elif level >= 900:
        color_code = '5'
    elif level >= 800:
        color_code = '9'
    elif level >= 700:
        color_code = 'd'
    elif level >= 600:
        color_code = 'c'
    elif level >= 500:
        color_code = '3'
    elif level >= 400:
        color_code = '2'
    elif level >= 300:
        color_code = 'b'
    elif level >= 200:
        color_code = '6'
    elif level >= 100:
        color_code = 'f'
    else:
        color_code = '7'

    # Generate the tag
    tag = [[color_code, f"[{level}✫]"]]
    
    return tag

