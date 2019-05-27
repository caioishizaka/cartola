from requests import post,get
import pandas as pd
import os
import json

# def login():
# 	"""
# 	Loga no cartola
# 	"""

# 	url = "https://login.globo.com/api/authentication"
# 	username = ''
# 	password = ''
# 	body = {"payload":{"email":username,"password":password,"serviceId":438},"captcha":""}
# 	print body
# 	header = {'Content-Type':'application/json'}

# 	return post(url, data = body, headers = header)

def get_summary():
	"""
	Bate na rota atletas/mercado da api, e retorna o resumo de todos os jogadores
	"""
	url = "https://api.cartolafc.globo.com/atletas/mercado"
	try:
		resp = get(url)
	except Exception as e:
		print e
		return None
	if resp.status_code != 200:
		print resp.status_code
		return None
	resp_json = resp.json()

	data_jogadores = resp_json['atletas']
	clubes_dict = resp_json['clubes']
	posicoes_dict = resp_json['posicoes']
	status_dict = resp_json['status']

	df = pd.DataFrame(data_jogadores)	
	df['clube'] = df.apply(lambda x: clubes_dict[str(x['clube_id'])]['nome'],axis = 1)
	df['posicao'] = df.apply(lambda x: posicoes_dict[str(x['posicao_id'])]['nome'],axis = 1)
	df['status'] = df.apply(lambda x: status_dict[str(x['status_id'])]['nome'],axis = 1)

	return df

def get_player_stats(atleta_id):
	"""
	Bate na rota mercado/atleta da api, e retorna os stats do jogador
	"""
	url = "https://api.cartolafc.globo.com/auth/mercado/atleta/" + str(atleta_id) + "/pontuacao"

	if os.path.isfile('config.json'):
		with open('config.json') as file:
			filedata = json.load(file)
		header = {'X-GLB-Token':filedata['X-GLB-Token']}
	else:
		header = {}
	try:
		resp = get(url, headers = header)
	except Exception as e:
		# print e
		return None
	if resp.status_code != 200:
		# print resp.status_code
		return resp.status_code
	resp_json = resp.json()

	df = pd.DataFrame(resp_json)

	return df[df['pontos'].notnull()]

def get_players_stats_from_list(players_list, verbose = False):
	players_df = None

	for player in players_list:
		player_data = get_player_stats(player)
		# print(player_data)
		if isinstance(player_data,pd.DataFrame):
			if not isinstance(players_df,pd.DataFrame):
				players_df = player_data
			elif isinstance(player_data,pd.DataFrame):
				players_df = players_df.append(player_data, ignore_index = True)
			if verbose:
				print 'Player ' + str(player) + ' success'
		else:
			print 'Player ' + str(player) + ' fail with error: ' + str(player_data) 
	return players_df

def get_all_data(max_attempts = 100, verbose = False):
	"""
	Pega o sumario dos jogadores e os stats de cada um e faz uma tabelona
	"""
	main_df = get_summary()
	players_list = list(set(list(main_df['atleta_id'])))
	number_players = len(players_list)
	if verbose:
		print "Trying " + str(number_players) + " players"
	players_df = get_players_stats_from_list(players_list, verbose = verbose)
	attempts = 0
	if verbose:
		print str(len(set(players_df['atleta_id']))) + '/' + str(number_players) + ' players retrieved'
	while len(set(players_df['atleta_id'])) < number_players and attempts < max_attempts:
		attempts += 1
		if verbose:
			print 'Tentativa: ' + str(attempts + 1)
		players_list = list(set(players_list) - set(list(players_df['atleta_id'])))
		new_players_df = get_players_stats_from_list(players_list, verbose = verbose)

		if not isinstance(players_df,pd.DataFrame):
			players_df = new_players_df
		elif isinstance(new_players_df,pd.DataFrame):
			players_df = players_df.append(new_players_df, ignore_index = True)
		if verbose:
			print str(len(players_df.index)) + '/' + str(len(players_list)) + ' players retrieved'

	for rounds in range(1,39):
		rodada_df = players_df[['atleta_id','media','pontos','preco','variacao']][players_df['rodada_id'] == rounds]
		main_df = main_df.merge(rodada_df,how = 'left', left_on = 'atleta_id', right_on = 'atleta_id', suffixes = ('','_'+str(rounds)))

	return main_df

	


	