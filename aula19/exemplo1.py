# import re
# import unicodedata
#from utils import limpar_nome_municipio
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


try:
    print("Obtendo dados...")
    ENDERECO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"


    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')

    # for i in range(2):
    #     df_ocorrencias['munic'] = df_ocorrencias['munic'].apply(limpar_nome_municipio)

    # Demilitando somente as variáveis do Exemplo01: munic e roubo_veiculo
    df_ocorrencias = df_ocorrencias[['munic', 'roubo_veiculo']]

    # Totalizar roubo de veiculo por municipio (agrupar e somar)
    # reset_index(), traz de volta os índeces que numera as colunas, pois eles se perdem
    # nesta operação
    df_roubo_veiculo = df_ocorrencias.groupby('munic').sum(['roubo_veiculo']).reset_index()

    # Printando as linhas iniciais com o método head() apenas para ver se os dados
    # foram obtidos corretamente
    print(df_roubo_veiculo.head())

except Exception as e:
    print(f"Erro ao obter dados: {e}")
    exit()


# Inicando a obtenção das medidas fundamentadas em estatística descritiva
try:
    print('Obtendo informações sobre padrão de roubo de veículos...')

    # Numpy
    # Uso do ARRAY
    # Array faz parte da biblioteca numpy
    # Array é uma estrutura de dados que armazena uma coleção de dados
    # https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html
    # pip install numpy
    # import numpy as np
    # NumPy significa numerical python e tem como objetivo adicionar suporte
    # para arrays e matrizes multidimensionais, juntamente com uma grande
    # coleção de funções matemáticas de alto nível.
    # Uso do array significa ganho computacional
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])

    # Obtendo média de roubo_veiculo
    media_roubo_veiculo = np.mean(array_roubo_veiculo)

    # Obtendo mediana de roubo_veiculo
    # Mediana é o valor que divide a distribuição em duas partes iguais
    # (50% dos dados estão abaixo e 50% acima)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)

    # Distânicia entre média e mediana
    # A distância entre a média e a medida de assimetria
    # A distância é obtida dividindo a diferença entre a média e a mediana
    # pela mediana
    # Se a distância for pequena, a distribuição é simétrica
    # Se a distância for grande, a distribuição é assimétrica
    # A distância é dada em porcentagem
    # Exemplo: 0.1 significa 10%
    # Se a distância for menor que 0.1, a distribuição tende a ser simétrica
    # Se a distância for maior que 0.1 e menor que 0.25, a distribuição tende
    # a ser assimétrica moderada. Pode ser que a média esteja sofrendo 
    # influência de valores extremos. Se a distância for maior que 0.25, a
    # distribuição tende a ser assimétrica forte. A tendência é, que nestes 
    # caso, a média esteja sofrendo influência de valores extremos.
    distancia = abs((media_roubo_veiculo-mediana_roubo_veiculo) / mediana_roubo_veiculo)

    # Medidas de tendência central
    # Se a média for muito diferente da mediana, distribuição é assimétrica. 
    # Não tende a haver um padrão e pode ser, que existam outliers (valores discrepantes)
    # Se a média for próxima (25%) a mediana, distribuição é simétrica. Neste 
    # caso, tende a haver um padrão
    print('\nMedidas de tendência central: ')
    print(30*'-')
    print(f'Média de roubo de veículos: {media_roubo_veiculo}')
    print(f'Mediana de roubo de veículos: {mediana_roubo_veiculo}')
    print(f'Distância entre média e mediana: {distancia:.3f}')


    # Quartis
    # Os quartis são os valores que dividem a distribuição em 4 partes iguais.
    # O primeiro quartil (Q1) é o valor que divide a distribuição em 25% e 75%.
    # O segundo quartil (Q2) é o valor que divide a distribuição em 50% e 50%.
    # O terceiro quartil (Q3) é o valor que divide a distribuição em 75% e 25%.
    # O quartil é uma medida de posição que indica a posição de um valor em relação
    # a uma distribuição.
    
    # OBS: O método weibull é o método padrão, mas NÃO é necessário passá-lo
    # como parâmetro ao calcular os quartis.
    # Podemos emos usar o método 'linear' ou 'hazen' também.
    # A sintaxe pode ser assim, sem os métodos:
    # q1 = np.quantile(array_roubo_veiculo, 0.25)
    # q2 = np.quantile(array_roubo_veiculo, 0.50)
    # q3 = np.quantile(array_roubo_veiculo, 0.75)
    q1 = np.quantile(array_roubo_veiculo, 0.25, method='weibull') # Q1 é 25% 
    q2 = np.quantile(array_roubo_veiculo, 0.50, method='weibull') # Q2 é 50% (mediana)
    q3 = np.quantile(array_roubo_veiculo, 0.75, method='weibull') # Q3 é 75%

    print('\nMedidas de posição: ')
    print(30*'-')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')

    print('Medidas de Dispersão')

    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude_total = maximo - minimo

    # OBTENDO OS MUNÍCIPIOS COM MAIORES E MONORES NÚMEROS DE ROUBOS DE VEÍCULOS
    # Filtramos os registros do DataFrame df_roubo_veiculo para achar os municípios
    # com menores e maiores números de roubos de veículos.
    df_roubo_veiculo_menores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < q1]
    df_roubo_veiculo_maiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > q3]

    print('\nMunicípios com Menores números de Roubos: ')
    print(70*'-')
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))
    print('\nMunicípios com Maiores números de Roubos:')
    print(45*'-')
    print(df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False))

    # ##### DESCOBRIR OUTLIERS #########
    # IQR (Intervalo interquartil)
    # q3 - q1
    # É a amplitude do intervalo dos 50% dos dados centrais
    # Ela ignora os valores extremos.
    # Não sofre a interferência dos valores extremos.
    # Quanto mais próximo de zero, mais homogêneo são os dados.
    # Quanto mais próximo do q3, mais heterogêneo são os dados.
    iqr = q3 - q1

    # Limite superior
    # Vai identificar os outliers acima de q3
    limite_superior = q3 + (1.5 * iqr)

    # Limite inferior
    # Vai identificar os outliers abaixo de q1
    limite_inferior = q1 - (1.5 * iqr)

    print('\nLimites - Medidas de Posição')
    print(45*'-')
    print(f'Limite inferior: {limite_inferior}')
    print(f'Limite superior: {limite_superior}')

    print('\nMedidas')
    print(f'Limite inferior: {limite_inferior}')
    print(f'Menor valor:{minimo}')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')
    print(F'IQR: {iqr}')
    print(f'Limite superior: {limite_superior}')
    print(f'Maior valor:{maximo}')
    print(f'Média: {media_roubo_veiculo}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distância: {distancia}')
    # #### OUTLIERS
    # Obtendo os ouliers inferiores
    # Filtrar o dataframe df_roubo_veiculo para o munics com roubo de veículo
    # abaixo limite inferior (OUTLIERS INFERIORES)
    df_roubo_veiculo_outliers_inferiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]
    
    # Obtendo os ouliers superiores
    # Filtrar o dataframe df_roubo_veiculo para o munics com roubo de veículo
    # acima de limite superior (OUTLIERS SUPERIORES)
    df_roubo_veiculo_outliers_superiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]

    print('\nMunicípios com outliers inferiores: ')
    print(45*'-')
    if len(df_roubo_veiculo_outliers_inferiores) == 0:
        print('Não existem outliers inferiores!')
    else:
        print(df_roubo_veiculo_outliers_inferiores.sort_values(by='roubo_veiculo', ascending=True))

    print('\nMunicípios com outliers superiores: ')
    print(45*'-')
    if len(df_roubo_veiculo_outliers_superiores) == 0:
        print('Não existe outliers superiores!')
    else:
        print(df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=False))

except Exception as e:
    print(f'Erro ao obter informações sobre padrão de roubo de veículos: {e}')
    exit()

try:
    fig, ax = plt.subplots(2,2, figsize=(10, 6))

    plt.subplot(2, 2, 1)
    plt.suptitle('Análise')

    plt.subplot(2,2,1)
    plt.boxplot(array_roubo_veiculo, vert=False, showmeans=True)
    plt.title('Boxplot da distribuição')

    plt.subplot(2, 2, 4)


    plt.tight_layout()

    plt.show()

except Exception as e:
    print(f'Erro ao plotar {e}')
