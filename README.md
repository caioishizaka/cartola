# cartola
Script para extrair dados do cartola

Instruções:

- Para melhor desempenho, logar na usa conta do cartola e pegar o X-GLB-Token
- Colocar o X-GLB-Token em um arquivo config.json como o exemplo abaixo:
{
	"X-GLB-Token":"123123312ab13b123aba1aebbe1a1befbe21abf2eab1abf2e1fca1cecf12cdf3dc1cecf"
}
- Rodar o extract_data.py
- Pegar os resultados em data/results.csv

Release history

- v2.0
	
	- Usa a API do cartola para extrair os dados

- v1.0

	- Extrai nome do jogador, pontuação na última rodada, média e preço (em C$)

Próximos desenvolvimentos

- Função de logar para pegar o glbid