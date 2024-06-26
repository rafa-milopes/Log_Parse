import re
from collections import defaultdict




# Esta função pega um caminho de arquivo como entrada e analisa o arquivo de log para extrair dados de partida, dados de mortes, pontuações de jogadores e total de mortes.
# Percorre cada linha do arquivo de log, identifica o início e o fim das partidas,
# Analisa eventos de eliminação e rastreia conexões de jogadores e mudanças de nome.
def parse_log_file(file_path):
    match_data = defaultdict(list)
    deaths_data = defaultdict(lambda: defaultdict(int))
    player_scores = defaultdict(int)
    total_kills = 0

    with open(file_path, 'r') as file:
        current_match = None
        for line in file:
            if "InitGame" in line:
                current_match = defaultdict(list)
            elif "ShutdownGame" in line:
                if current_match:
                    match_data[len(match_data) + 1] = current_match
            elif "Kill:" in line:
                total_kills += 1
                match = re.search(r'Kill: (\d+) (\d+) \d+: (\S+) killed (\S+)', line)
                if match:
                    killer, victim = match.group(3), match.group(4)
                    if killer == "<world>":
                        player_scores[victim] -= 1
                        deaths_data[len(match_data)][victim] += 1
                    else:
                        player_scores[killer] += 1
                        deaths_data[len(match_data)][victim] += 1
            elif "ClientConnect" in line:
                match = re.search(r'ClientConnect: (\d+)', line)
                if match:
                    player_id = match.group(1)
                    current_match[player_id].append({'name': '', 'kills': 0})
            elif "ClientUserinfoChanged" in line:
                match = re.search(r'ClientUserinfoChanged: (\d+) n\\(.+?)\\', line)
                if match:
                    player_id, player_name = match.group(1), match.group(2)
                    if player_id in current_match:
                        current_match[player_id][-1]['name'] = player_name

    return match_data, deaths_data, player_scores, total_kills


#Esta função pega os dados da partida analisados, dados de mortes e pontuações dos jogadores como entrada e imprime um relatório para cada partida. 
#Exibe informações sobre os jogadores, suas mortes e suas mortes.
def print_match_report(match_data, deaths_data, player_scores):
    for match_number, players_data in match_data.items():
        print(f"Match {match_number}:")
        print("Players:")
        for player_id, player_info in players_data.items():
            print(f"Player {player_id}: {player_info[0]['name']}, Kills: {player_scores[player_id]}")
        print("Deaths:")
        for player, deaths in deaths_data[match_number].items():
            print(f"{player}: {deaths} deaths")

if __name__ == "__main__":
    log_file_path = "quake3_log"  
    match_data, deaths_data, player_scores, total_kills = parse_log_file(log_file_path)
    print("Match Report:")
    print_match_report(match_data, deaths_data, player_scores)
    print("\nTotal Kills:", total_kills)
