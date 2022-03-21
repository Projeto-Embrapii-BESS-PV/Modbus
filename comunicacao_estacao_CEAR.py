## Importação de Pacotes
from pyModbusTCP import client
from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
import pymysql
import pandas as pd
import time



#conexão BD

con = pymysql.connect( host = 'localhost', user= 'root', passwd='', database='Ammonit')
cr = con.cursor()
#cr.execute("CREATE DATABASE IF NOT EXISTS Ammonit")

#criar tabela
def create_table():
    
    cr = con.cursor()
    cr.execute('CREATE TABLE IF NOT EXISTS dados_cear (id INT PRIMARY KEY AUTO_INCREMENT,ano REAL,mes REAL, dia REAL,hora REAL,minuto REAL,segundo REAL, vel_vento REAL, vel_vento_media REAL,vel_vento_max REAL, vel_vento_min REAL, vel_vento_sdtdev REAL, dir_vento REAL, dir_vento_media REAL, umid_rel REAL, umid_rel_media REAL, umid_rel_max REAL, umid_rel_min REAL, umid_rel_stddev REAL, temp_amb REAL, temp_amb_media REAL, temp_amb_max REAL, temp_amb_min REAL, temp_amb_stddev REAL, pressao_atm REAL, pressao_atm_media REAL, pressao_atm_max REAL, pressao_atm_min REAL, pressao_atm_stddev REAL, DHI REAL, DHI_media REAL, DHI_max REAL, DHI_min REAL, DHI_stddev REAL, GHI REAL, GHI_media REAL, GHI_max REAL, GHI_min REAL, GHI_stddev REAL, DNI REAL, DNI_media REAL, DNI_max REAL, DNI_min REAL, DNI_stddev REAL, DNI_estado_sol REAL, precipitacao REAL, GTI REAL, GTI_media REAL, GTI_max REAL, GTI_min REAL, GTI_stddev REAL, theta REAL)')
   
    con.commit()

    print ('Tabela criada na base de dados')
   
    cr.close()


# Manipulação de float 
class FloatModbusClient(ModbusClient):
    def read_float(self, address, number=1):
        reg_l = self.read_holding_registers(address, number * 2)
        if reg_l:
            return [utils.decode_ieee(f) for f in utils.word_list_to_long(reg_l)]
        else:
            return None

    def write_float(self, address, floats_list):
        b32_l = [utils.encode_ieee(f) for f in floats_list]
        b16_l = utils.long_list_to_word(b32_l)
        return self.write_multiple_registers(address, b16_l)


def data_entry():
   
    
    # Ler dados
     m = FloatModbusClient(host='150.165.161.188', port=502, auto_open=True)    
     print(m.is_open())
     dados = [m.read_holding_registers(1,1), #ano
             m.read_holding_registers(2,1), #mês
             m.read_holding_registers(3,1), #dia
             m.read_holding_registers(4,1), #hora
             m.read_holding_registers(5,1), #minuto    
             m.read_holding_registers(6,1), #segundo
             m.read_float(1,1), #velocidade do vento
             m.read_float(8,1), #velocidade do vento média
             m.read_float(5,1), #velocidade do vento máx
             m.read_float(10,1), #velocidade do vento min
             m.read_float(9,1), #velocidade do vento stddev
             m.read_float(11,1),#direção do vento
             m.read_float(13,1),#direção do vento média
             m.read_float(15,1),#umidade relativa
             m.read_float(17,1),#umidade relativa média
             m.read_float(19,1),#umidade relativa máx
             m.read_float(21,1),#umidade relativa min
             m.read_float(23,1),#umidade relativa stddev
             m.read_float(25,1),#temperatura
             m.read_float(27,1),#temperatura média
             m.read_float(29,1),#temperatura máx
             m.read_float(31,1),#temperatura min
             m.read_float(33,1),#temperatura stddev
             m.read_float(35,1),#pressão atmosférica
             m.read_float(37,1),#pressão atmosférica média
             m.read_float(39,1),#presão atmosférica máx
             m.read_float(41,1),#pressão atmosférica min
             m.read_float(43,1),#pressão atmosférica stddev
             m.read_float(45,1),#dhi 
             m.read_float(47,1),#dhi média
             m.read_float(49,1),#dhi máx
             m.read_float(51,1),#dhi min
             m.read_float(53,1),#dhi stddev
             m.read_float(55,1),#ghi
             m.read_float(57,1),#ghi média
             m.read_float(59,1),#ghi máx
             m.read_float(61,1),#ghi min
             m.read_float(63,1),#ghi stddev
             m.read_float(65,1),#dni
             m.read_float(67,1),#dni média
             m.read_float(69,1),#dni máx
             m.read_float(71,1),#dni min
             m.read_float(73,1),#dni stddev
             m.read_float(75,1),#dni estado do sol estimado
             m.read_float(77,1),#precipitação
             m.read_float(79,1),#gti
             m.read_float(81,1),#gti média
             m.read_float(83,1),#gti máx
             m.read_float(85,1), #gti min
             m.read_float(89,1), #gti stddev
             m.read_float(73,1)
                            ]

     

     #fecha conexão Modbus
     m.close()

    
     x = dados
     return x



#Insere dados no banco de dados
def inserir():

    #Atribui á variável n a função com os dados 
    n=data_entry()

    #Converte a lista em um Data Frame
    df = pd.DataFrame(n)
    
    #Converte Nan em 0
    df = df.fillna(0)
  

    y = df.values.tolist()
    print(y)

    #Estabelece conexão
    c = con.cursor()

    #Insere os Dados
    c.execute('INSERT INTO dados_cear (ano,mes,dia,hora,minuto,segundo,vel_vento, vel_vento_media,vel_vento_max, vel_vento_min, vel_vento_sdtdev, dir_vento, dir_vento_media, umid_rel,umid_rel_media,umid_rel_max, umid_rel_min, umid_rel_stddev,temp_amb, temp_amb_media, temp_amb_max, temp_amb_min, temp_amb_stddev,pressao_atm, pressao_atm_media, pressao_atm_max, pressao_atm_min, pressao_atm_stddev,DHI, DHI_media, DHI_max, DHI_min, DHI_stddev, GHI, GHI_media, GHI_max, GHI_min, GHI_stddev, DNI , DNI_media , DNI_max , DNI_min , DNI_stddev,DNI_estado_sol, precipitacao,GTI, GTI_media, GTI_max, GTI_min, GTI_stddev, theta) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(y[0][0],y[1][0],y[2][0],y[3][0],y[4][0],y[5][0],y[6][0],y[7][0],y[8][0],y[9][0],y[10][0],y[11][0],y[12][0],y[13][0],y[14][0],y[15][0],y[16][0],y[17][0],y[18][0],y[19][0],y[20][0],y[21][0],y[22][0],y[23][0],y[24][0],y[25][0],y[26][0],y[27][0],y[28][0],y[29][0],y[30][0],y[31][0],y[32][0],y[33][0],y[34][0],y[35][0],y[36][0],y[37][0],y[38][0],y[39][0],y[40][0],y[41][0],y[42][0],y[43][0],y[44][0],y[45][0],y[46][0],y[47][0],y[48][0],y[49][0], y[50][0]))
    con.commit()
    
    #fecha o acesso
    c.close()

   


create_table()

# Loop infinito de update de base de dados
i=1
while True:
    # Atualiza banco de dados
    inserir()
    print(i)
    # Tempo de amostragem
    time.sleep(600)
    if i == 4320:
        break
    else:
        i+=1



print ('Base de dados ''ammonit'' desconectada')