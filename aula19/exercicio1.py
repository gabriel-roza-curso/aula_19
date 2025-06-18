import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    ENDEREÇO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"

    df_ocorrencias = pd.read_csv(ENDEREÇO_DADOS, sep=';', encoding='iso-8859-1')

    df_ocorrencias = df_ocorrencias[['munic', 'estelionato']]

    df_estelionato = df_ocorrencias.groupby('munic').sum(['estelionato']).reset_index()

    print(df_estelionato.head())

except Exception as e:
    print(f'Erro ao obter dados: {e}')
    exit()

try:
    print('Obtendo informações sobre padrão de estelionatos por município')

    array_estelionato = np.array(df_estelionato['estelionato'])

    media_estelionato = np.mean(array_estelionato)

    mediana_estelionato =np.median(array_estelionato)

    distancia = abs((media_estelionato - mediana_estelionato) / mediana_estelionato)

    print('\nMedidas de tendência central: ')
    print(30*'-')
    print(f'Média de estelionatos: {media_estelionato:.2f}')
    print(f'Mediana de estelionatos: {mediana_estelionato}')
    print(f'Distância entre média e mediana: {distancia:.2f}')

    q1, q2, q3 = np.quantile(array_estelionato, [0.25, 0.5, 0.75])
    print(f'\nQuartis: \nQ1: {q1}, Q2: {q2}, Q3: {q3}')

    df_estelionato_menores = df_estelionato[df_estelionato['estelionato'] < q1]
    df_estelionato_maiores = df_estelionato[df_estelionato['estelionato'] > q3]

    print('\nMunicípios com Menores números de Roubos: ')
    print(70*'-')
    print(df_estelionato_menores.sort_values(by='estelionato', ascending=True))
    print('\nMunicípios com Maiores números de Roubos:')
    print(45*'-')
    print(df_estelionato_maiores.sort_values(by='estelionato', ascending=False))

    iqr = q3 - q1

    limite_superior = q3 + (1.5 * iqr)
    limite_inferior = q1 - (1.5 * iqr)

    print('\nLimites - Medidas de Posição')
    print(45*'-')
    print(f'Limite inferior: {limite_inferior}')
    print(f'Limite superior: {limite_superior}')

    df_estelionato_outlier_inf = df_estelionato[df_estelionato['estelionato'] < limite_inferior]

    df_estelionato_outlier_sup = df_estelionato[df_estelionato['estelionato'] > limite_superior]

    print('\nMunicípios com outliers inferiores: ')
    print(45*'-')
    if len(df_estelionato_outlier_inf) == 0:
        print('Não existem outliers inferiores!')
    else:
        print(df_estelionato_outlier_inf.sort_values(by='roubo_veiculo', ascending=True))

    print('\nMunicípios com outliers superiores: ')
    print(45*'-')
    if len(df_estelionato_outlier_sup) == 0:
        print('Não existe outliers superiores!')
    else:
        print(df_estelionato_outlier_sup.sort_values(by='estelionato', ascending=False))

    print('\nMedidas de disperção:')
    print(45*'-')
    
    variancia = np.var(array_estelionato)
    desvio_padrao = np.std(array_estelionato)
    coef_var = desvio_padrao / media_estelionato
    distancia_var_media = variancia / (media_estelionato ** 2)

    print(f'A variância foi de: {variancia}')
    print(f'A distância da média é: {distancia_var_media}')
    print(f'Este é o desvio padrão: {desvio_padrao}')
    print(f'O coeficiente é de: {coef_var}')

    #Boxplot

    plt.figure(figsize=(10, 5))
    plt.boxplot(array_estelionato, vert=False)
    plt.title('Boxplot dos casos de Estelionato por Município')
    plt.xlabel('Quantidade de Estelionatos')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


    print('\nANÁLISE FINAL')
    print(45*'-')
    print('Tendo em vista que o coeficiente e o desvio padrão são muito altos, a média não deve ser considerada, pois os dados estão muito dispersos')
except Exception as e:
    print(f'Erro: {e}')

