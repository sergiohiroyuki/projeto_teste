import numpy as np
import pandas as pd
import plotly.express as px
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class Grafico_1():
    def __init__(self, nome_cidade):
        self.nome_cidade = nome_cidade

    def grafico_plot(self):
        # Carregar o conjunto de dados
        df_producao_clima = pd.read_csv('C:\\Users\\hiroy\\myproject\\.venv\\dataset\\producao_clima.csv')
        df_producao_clima = df_producao_clima.drop(['data'], axis=1)

        # Separar os recursos (X) e os rótulos (y)
        X = df_producao_clima.drop(['codigo_ibge', 'anual_prodution', 'date'], axis=1)
        y = df_producao_clima['anual_prodution']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        # Treinar o modelo
        regressor = lgb.LGBMRegressor(learning_rate=0.11, min_samples_leaf=14)
        regressor.fit(X_train, y_train)

        # Filtrar o DataFrame para incluir apenas a cidade desejada
        dicionario = {
            'Abatiá': 4100103, 'Altamira do Paraná': 4100459, 'Alto Paraná': 4100608, 'Alto Piquiri': 4100707, 'Altônia': 4100509, 
        'Alvorada do Sul': 4100806, 'Ampére': 4101002, 'Anahy': 4101051, 'Andirá': 4101101, 'Ângulo': 4101150, 'Antônio Olinto': 4101309, 
        'Apucarana': 4101408, 'Arapoti': 4101606, 'Arapuã': 4101655, 'Araruna': 4101705, 'Araucária': 4101804, 'Ariranha do Ivaí': 4101853, 
        'Assaí': 4101903, 'Assis Chateaubriand': 4102000, 'Astorga': 4102109, 'Atalaia': 4102208, 'Balsa Nova': 4102307, 'Bandeirantes': 4102406, 
        'Barbosa Ferraz': 4102505, 'Barra do Jacaré': 4102703, 'Barracão': 4102604, 'Bela Vista da Caroba': 4102752, 'Bela Vista do Paraíso': 4102802, 
        'Bituruna': 4102901, 'Boa Esperança': 4103008, 'Boa Esperança do Iguaçu': 4103024, 'Boa Ventura de São Roque': 4103040, 
        'Boa Vista da Aparecida': 4103057, 'Bom Jesus do Sul': 4103156, 'Bom Sucesso': 4103206, 'Bom Sucesso do Sul': 4103222, 
        'Borrazópolis': 4103305, 'Braganey': 4103354, 'Brasilândia do Sul': 4103370, 'Cafeara': 4103404, 'Cafelândia': 4103453, 
        'Cafezal do Sul': 4103479, 'Califórnia': 4103503, 'Cambará': 4103602, 'Cambé': 4103701, 'Cambira': 4103800, 'Campina da Lagoa': 4103909, 
        'Campina do Simão': 4103958, 'Campo Bonito': 4104055, 'Campo do Tenente': 4104105, 'Campo Largo': 4104204, 'Campo Magro': 4104253, 
        'Campo Mourão': 4104303, 'Cândido de Abreu': 4104402, 'Candói': 4104428, 'Cantagalo': 4104451, 'Capanema': 4104501, 
        'Capitão Leônidas Marques': 4104600, 'Carambeí': 4104659, 'Carlópolis': 4104709, 'Cascavel': 4104808, 'Castro': 4104907, 'Catanduvas': 4105003, 
        'Centenário do Sul': 4105102, 'Céu Azul': 4105300, 'Chopinzinho': 4105409, 'Cianorte': 4105508, 'Cidade Gaúcha': 4105607, 'Clevelândia': 4105706, 
        'Colorado': 4105904, 'Congonhinhas': 4106001, 'Conselheiro Mairinck': 4106100, 'Contenda': 4106209, 'Corbélia': 4106308, 
        'Cornélio Procópio': 4106407, 'Coronel Domingos Soares': 4106456, 'Coronel Vivida': 4106506, 'Corumbataí do Sul': 4106555, 
        'Cruz Machado': 4106803, 'Cruzeiro do Iguaçu': 4106571, 'Cruzeiro do Oeste': 4106605, 'Cruzeiro do Sul': 4106704, 'Cruzmaltina': 4106852, 
        'Curiúva': 4107009, 'Diamante do Sul': 4107124, "Diamante D'Oeste": 4107157, 'Dois Vizinhos': 4107207, 'Douradina': 4107256, 
        'Doutor Camargo': 4107306, 'Enéas Marques': 4107405, 'Engenheiro Beltrão': 4107504, 'Entre Rios do Oeste': 4107538, 
        'Espigão Alto do Iguaçu': 4107546, 'Farol': 4107553, 'Faxinal': 4107603, 'Fazenda Rio Grande': 4107652, 'Fênix': 4107702, 
        'Fernandes Pinheiro': 4107736, 'Figueira': 4107751, 'Flor da Serra do Sul': 4107850, 'Floraí': 4107801, 'Floresta': 4107900, 
        'Florestópolis': 4108007, 'Flórida': 4108106, 'Formosa do Oeste': 4108205, 'Foz do Iguaçu': 4108304, 'Foz do Jordão': 4108452, 
        'Francisco Alves': 4108320, 'Francisco Beltrão': 4108403, 'General Carneiro': 4108502, 'Godoy Moreira': 4108551, 'Goioerê': 4108601, 
        'Goioxim': 4108650, 'Grandes Rios': 4108700, 'Guaíra': 4108809, 'Guamiranga': 4108957, 'Guapirama': 4109005, 'Guaporema': 4109104, 
        'Guaraci': 4109203, 'Guaraniaçu': 4109302, 'Guarapuava': 4109401, 'Honório Serpa': 4109658, 'Ibaiti': 4109708, 'Ibema': 4109757, 
        'Ibiporã': 4109807, 'Icaraíma': 4109906, 'Iguaraçu': 4110003, 'Iguatu': 4110052, 'Imbaú': 4110078, 'Imbituva': 4110102, 'Indianópolis': 4110409, 
        'Ipiranga': 4110508, 'Iporã': 4110607, 'Iracema do Oeste': 4110656, 'Irati': 4110706, 'Iretama': 4110805, 'Itaguajé': 4110904, 
        'Itaipulândia': 4110953, 'Itambaracá': 4111001, 'Itambé': 4111100, "Itapejara d'Oeste": 4111209, 'Ivaí': 4111407, 'Ivaiporã': 4111506, 
        'Ivatuba': 4111605, 'Jaboti': 4111704, 'Jaguapitã': 4111902, 'Jaguariaíva': 4112009, 'Jandaia do Sul': 4112108, 'Janiópolis': 4112207, 
        'Japira': 4112306, 'Japurá': 4112405, 'Jardim Alegre': 4112504, 'Jardim Olinda': 4112603, 'Jataizinho': 4112702, 'Jesuítas': 4112751, 
        'Joaquim Távora': 4112801, 'Jundiaí do Sul': 4112900, 'Juranda': 4112959, 'Jussara': 4113007, 'Kaloré': 4113106, 'Lapa': 4113205, 
        'Laranjal': 4113254, 'Laranjeiras do Sul': 4113304, 'Leópolis': 4113403, 'Lidianópolis': 4113429, 'Lindoeste': 4113452, 'Lobato': 4113601, 
        'Londrina': 4113700, 'Luiziana': 4113734, 'Lunardelli': 4113759, 'Lupionópolis': 4113809, 'Mallet': 4113908, 'Mamborê': 4114005, 
        'Mandaguaçu': 4114104, 'Mandaguari': 4114203, 'Mandirituba': 4114302, 'Manfrinópolis': 4114351, 'Mangueirinha': 4114401, 
        'Manoel Ribas': 4114500, 'Marechal Cândido Rondon': 4114609, 'Maria Helena': 4114708, 'Marialva': 4114807, 'Marilândia do Sul': 4114906, 
        'Mariluz': 4115101, 'Maringá': 4115200, 'Mariópolis': 4115309, 'Maripá': 4115358, 'Marmeleiro': 4115408, 'Marquinho': 4115457, 
        'Marumbi': 4115507, 'Matelândia': 4115606, 'Mauá da Serra': 4115754, 'Medianeira': 4115804, 'Mercedes': 4115853, 'Mirador': 4115903, 
        'Miraselva': 4116000, 'Missal': 4116059, 'Moreira Sales': 4116109, 'Munhoz de Melo': 4116307, 'Nossa Senhora das Graças': 4116406, 
        'Nova Aliança do Ivaí': 4116505, 'Nova América da Colina': 4116604, 'Nova Aurora': 4116703, 'Nova Cantu': 4116802, 'Nova Esperança': 4116901, 
        'Nova Esperança do Sudoeste': 4116950, 'Nova Fátima': 4117008, 'Nova Laranjeiras': 4117057, 'Nova Prata do Iguaçu': 4117255, 
        'Nova Santa Bárbara': 4117214, 'Nova Santa Rosa': 4117222, 'Nova Tebas': 4117271, 'Novo Itacolomi': 4117297, 'Ortigueira': 4117305, 
        'Ourizona': 4117404, 'Ouro Verde do Oeste': 4117453, 'Paiçandu': 4117503, 'Palmas': 4117602, 'Palmeira': 4117701, 'Palmital': 4117800, 
        'Palotina': 4117909, 'Paraíso do Norte': 4118006, 'Paranacity': 4118105, 'Paranapoema': 4118303, 'Paranavaí': 4118402, 'Pato Bragado': 4118451, 
        'Pato Branco': 4118501, 'Paula Freitas': 4118600, 'Paulo Frontin': 4118709, 'Peabiru': 4118808, 'Perobal': 4118857, "Pérola d'Oeste": 4119004, 
        'Pinhal de São Bento': 4119251, 'Pinhalão': 4119202, 'Pinhão': 4119301, 'Piraí do Sul': 4119400, 'Piraquara': 4119509, 'Pitanga': 4119608, 
        'Pitangueiras': 4119657, 'Planalto': 4119806, 'Ponta Grossa': 4119905, 'Porecatu': 4120002, 'Porto Amazonas': 4120101, 
        'Porto Barreiro': 4120150, 'Porto Vitória': 4120309, 'Prado Ferreira': 4120333, 'Pranchita': 4120358, 'Presidente Castelo Branco': 4120408, 
        'Primeiro de Maio': 4120507, 'Prudentópolis': 4120606, 'Quarto Centenário': 4120655, 'Quatro Pontes': 4120853, 'Quedas do Iguaçu': 4120903, 
        'Querência do Norte': 4121000, 'Quinta do Sol': 4121109, 'Quitandinha': 4121208, 'Ramilândia': 4121257, 'Rancho Alegre': 4121307, 
        "Rancho Alegre D'Oeste": 4121356, 'Realeza': 4121406, 'Rebouças': 4121505, 'Renascença': 4121604, 'Reserva': 4121703, 
        'Reserva do Iguaçu': 4121752, 'Ribeirão Claro': 4121802, 'Ribeirão do Pinhal': 4121901, 'Rio Azul': 4122008, 'Rio Bom': 4122107, 
        'Rio Bonito do Iguaçu': 4122156, 'Rio Branco do Ivaí': 4122172, 'Rio Negro': 4122305, 'Rolândia': 4122404, 'Roncador': 4122503, 
        'Rondon': 4122602, 'Rosário do Ivaí': 4122651, 'Salgado Filho': 4122800, 'Salto do Itararé': 4122909, 'Salto do Lontra': 4123006, 
        'Santa Amélia': 4123105, 'Santa Cecília do Pavão': 4123204, 'Santa Cruz de Monte Castelo': 4123303, 'Santa Fé': 4123402, 
        'Santa Helena': 4123501, 'Santa Inês': 4123600, 'Santa Isabel do Ivaí': 4123709, 'Santa Izabel do Oeste': 4123808, 'Santa Lúcia': 4123824, 
        'Santa Maria do Oeste': 4123857, 'Santa Mariana': 4123907, 'Santa Mônica': 4123956, 'Santa Tereza do Oeste': 4124020, 
        'Santa Terezinha de Itaipu': 4124053, 'Santana do Itararé': 4124004, 'Santo Antônio da Platina': 4124103, 'Santo Antônio do Paraíso': 4124301, 
        'Santo Antônio do Sudoeste': 4124400, 'Santo Inácio': 4124509, 'São Carlos do Ivaí': 4124608, 'São Jerônimo da Serra': 4124707, 
        'São João': 4124806, 'São João do Ivaí': 4125001, 'São João do Triunfo': 4125100, 'São Jorge do Ivaí': 4125308, 
        'São Jorge do Patrocínio': 4125357, "São Jorge d'Oeste": 4125209, 'São José da Boa Vista': 4125407, 'São José das Palmeiras': 4125456, 
        'São José dos Pinhais': 4125506, 'São Manoel do Paraná': 4125555, 'São Mateus do Sul': 4125605, 'São Miguel do Iguaçu': 4125704, 
        'São Pedro do Iguaçu': 4125753, 'São Pedro do Ivaí': 4125803, 'São Sebastião da Amoreira': 4126009, 'São Tomé': 4126108, 'Sapopema': 4126207, 
        'Sarandi': 4126256, 'Saudade do Iguaçu': 4126272, 'Sengés': 4126306, 'Serranópolis do Iguaçu': 4126355, 'Sertaneja': 4126405, 
        'Sertanópolis': 4126504, 'Siqueira Campos': 4126603, 'Sulina': 4126652, 'Tamarana': 4126678, 'Tamboara': 4126702, 'Teixeira Soares': 4127007, 
        'Telêmaco Borba': 4127106, 'Terra Boa': 4127205, 'Terra Roxa': 4127403, 'Tibagi': 4127502, 'Tijucas do Sul': 4127601, 'Toledo': 4127700, 
        'Tomazina': 4127809, 'Três Barras do Paraná': 4127858, 'Tuneiras do Oeste': 4127908, 'Tupãssi': 4127957, 'Turvo': 4127965, 'Ubiratã': 4128005, 
        'Umuarama': 4128104, 'União da Vitória': 4128203, 'Uniflor': 4128302, 'Uraí': 4128401, 'Ventania': 4128534, 'Vera Cruz do Oeste': 4128559, 
        'Verê': 4128609, 'Virmond': 4128658, 'Vitorino': 4128708, 'Wenceslau Braz': 4128500
        }

        nome_cidade = self.nome_cidade
        codigo_ibge_desejado = dicionario[nome_cidade] 
        dados_cidade_desejada = df_producao_clima[df_producao_clima['codigo_ibge'] == codigo_ibge_desejado]

        # Resetar o índice do DataFrame filtrado
        dados_cidade_desejada.reset_index(drop=True, inplace=True)

        # Separar os dados em recursos (X) e rótulos (y)
        X_cidade = dados_cidade_desejada.drop(['codigo_ibge', 'anual_prodution', 'date'], axis=1)

        # Fazer previsões para a cidade
        predicao_cidade = regressor.predict(X_cidade)

        # Carregar os dados futuros diretamente de um arquivo CSV (substitua 'dados_futuros.csv' pelo seu arquivo CSV real)
        dados_futuros = pd.read_csv('C:\\Users\\hiroy\\myproject\\.venv\\dataset\\predicao_futura.csv')

        # Filtrar o DataFrame para incluir apenas a cidade desejada
        dados_cidade_desejada_predicao = dados_futuros[dados_futuros['codigo_ibge'] == codigo_ibge_desejado]

        # Fazer previsões para os anos futuros
        X_futuro = dados_cidade_desejada_predicao.drop(['date', 'data', 'codigo_ibge'], axis=1) 
        predicao_futuro = regressor.predict(X_futuro)

        # Concatenar as previsões passadas e futuras
        predicoes_totais = np.concatenate((predicao_cidade, predicao_futuro))

        # Criar uma lista de anos que inclui tanto os anos passados quanto os futuros
        anos_passados = dados_cidade_desejada['date']
        anos_futuros = dados_cidade_desejada_predicao['date']

        # Criar um DataFrame para facilitar a criação do gráfico
        df_grafico = pd.DataFrame({
            'Ano': anos_passados.tolist() + anos_futuros.tolist(),
            'Valores Previstos (Passado)': predicao_cidade.tolist() + [None] * len(anos_futuros),
            'Valores Reais': dados_cidade_desejada['anual_prodution'].tolist() + [None] * len(anos_futuros),
            'Valores Previstos (Futuros)': [None] * len(anos_passados) + predicao_futuro.tolist()
        })

        # Criar um gráfico interativo do Plotly Express
        fig = px.line(df_grafico, x='Ano', y=['Valores Previstos (Passado)', 'Valores Reais', 'Valores Previstos (Futuros)'],
                      labels={'Ano': 'Ano', 'value': 'Produção de Soja'}, title=f'Produção de Soja - Nome da Cidade - {nome_cidade}')


        # Exibir o gráfico
        #fig.show()

        return df_grafico

        

# Exemplo de uso:
# grafico = Grafico('SuaCidade')
# grafico.grafico_plot()
