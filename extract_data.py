import pandas as pd
import cartola_api as cartola

df = cartola.get_all_data()

df.to_csv('data/results.csv', index = False, sep = ",", encoding = 'utf-8')