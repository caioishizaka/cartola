import pandas as pd

with open('data/dados_jogadores.txt') as datafile:
	line = datafile.readline()
	data = []
	while line:
		player_name = line.strip()
		for i in range(5):
			line = datafile.readline()
		try:
			dt = line.strip().split(" ")
			last_score = float(dt[0])
			avg_score = float(dt[1])
			matches = int(dt[2])
		except:
			last_score = 0
			avg_score = 0
			matches = 0
		for i in range(4):
			line = datafile.readline()
		try:
			current_price = float(line.strip().split(" ")[1])
		except:
			current_price = 0
		data += [{'Nome':player_name,'Ultima_rodada':last_score,'Media':avg_score,'Preco':current_price, 'Jogos':matches}]
		line = datafile.readline()
		line = datafile.readline()

print data

df = pd.DataFrame(data)
df.to_csv('data/results.csv', index = False)