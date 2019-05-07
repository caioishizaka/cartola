import pandas as pd
import cartola_api as cartola

#Puxa o sumario de todos os jogadores
data_jogadores = cartola.get_summary()
print(data_jogadores.head())