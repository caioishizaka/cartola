from requests import post,get
import pandas as pd

def get_summary():
	"""
	Bate na rota atletas/mercado da api, e retorna o resumo de todos os jogadores
	"""
	url = "https://api.cartolafc.globo.com/atletas/mercado"
	try:
		resp = get(url)
	except Exception:
		return null
	if resp.status_code != 200:
		return null
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