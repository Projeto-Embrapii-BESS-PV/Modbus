#bibliotecas necessárias
import socket
import time
import config
import emails


#Inversor
_register_map =  {

    #Bibliotecas Destacadas
    'Model':      {'addr': '30000', 'registers': 15, 'name': 'Model',                            'scale': 1,    'type': 'str',  'units': ''    , 'use': 'info',  'method': 'hold'},
    'PV_U1':      {'addr': '32016', 'registers': 1,  'name': 'PV1 voltage',                      'scale': 10,   'type': 'I16',  'units': 'V'   , 'use': 'mult',  'method': 'hold'},
    'PV_I1':      {'addr': '32017', 'registers': 1,  'name': 'PV1 current',                      'scale': 100,  'type': 'I16',  'units': 'A'   , 'use': 'mult',  'method': 'hold'},
    'PV_U2':      {'addr': '32018', 'registers': 1,  'name': 'PV2 voltage',                      'scale': 10,   'type': 'I16',  'units': 'V'   , 'use': 'mult',  'method': 'hold'},
    'PV_I2':      {'addr': '32019', 'registers': 1,  'name': 'PV2 current',                      'scale': 100,  'type': 'I16',  'units': 'A'   , 'use': 'mult',  'method': 'hold'},
    'PV_P':       {'addr': '32064', 'registers': 2,  'name': 'Input power',                      'scale': 1000, 'type': 'I32',  'units': 'kW'  , 'use': 'data',  'method': 'hold'},
    'U_A-B':      {'addr': '32066', 'registers': 1,  'name': 'Line Voltage A-B',                 'scale': 10,   'type': 'U16',  'units': 'V'   , 'use': 'data',  'method': 'hold'},
    'I_A':        {'addr': '32072', 'registers': 2,  'name': 'Phase Current A',                  'scale': 1000, 'type': 'I32',  'units': 'A'   , 'use': 'data',  'method': 'hold'},
    'P_active':   {'addr': '32080', 'registers': 2,  'name': 'Active power',                     'scale': 1000, 'type': 'I32',  'units': 'kW'  , 'use': 'data',  'method': 'hold'},
    'P_reactive': {'addr': '32082', 'registers': 2,  'name': 'Reactive power',                   'scale': 1000, 'type': 'I32',  'units': 'kVar', 'use': 'data',  'method': 'hold'},
    'PF':         {'addr': '32084', 'registers': 1,  'name': 'Power Factor',                     'scale': 1000, 'type': 'I16',  'units': ''    , 'use': 'data',  'method': 'hold'},
    'Frequency':  {'addr': '32085', 'registers': 1,  'name': 'Grid frequency',                   'scale': 100,  'type': 'U16',  'units': 'Hz'  , 'use': 'data',  'method': 'hold'},
    'η':          {'addr': '32086', 'registers': 1,  'name': 'Efficiency',                       'scale': 100,  'type': 'U16',  'units': '%'   , 'use': 'data',  'method': 'hold'},
    'Temp':       {'addr': '32087', 'registers': 1,  'name': 'Internal temperature',             'scale': 10,   'type': 'I16',  'units': '°C'  , 'use': 'data',  'method': 'hold'},
    'Start':      {'addr': '32091', 'registers': 2,  'name': 'Startup time',                     'scale': 1,    'type': 'U32',  'units': 's'   , 'use': 'info',  'method': 'hold'},
    'Shutdown':   {'addr': '32093', 'registers': 2,  'name': 'Shutdown time',                    'scale': 1,    'type': 'U32',  'units': 's'   , 'use': 'info',  'method': 'hold'},
    'Time':       {'addr': '40000', 'registers': 2,  'name': 'Current time',                     'scale': 1,    'type': 'U32',  'units': 's'   , 'use': 'info',  'method': 'hold'},
    'Derating_kw':{'addr': '40120', 'registers': 1,  'name': 'Active power derating',            'scale': 10,   'type': 'U16',  'units': 'KW'  , 'use': 'info',  'method': 'hold'},
    'Derating':   {'addr': '40125', 'registers': 1,  'name': 'Active power derating percent',    'scale': 10,   'type': 'U16',  'units': '%'   , 'use': 'info',  'method': 'hold'},
    'Derating_w': {'addr': '40126', 'registers': 2,  'name': 'Active power derating',            'scale': 1,    'type': 'U32',  'units': 'W'   , 'use': 'info',  'method': 'hold'},
    'Power_on':   {'addr': '40200', 'registers': 1,  'name': 'Power on',                         'scale': 1,    'type': 'U16',  'units': ''    , 'use': 'info',  'method': 'hold'},
    'Power_off':  {'addr': '40201', 'registers': 1,  'name': 'Power off',                        'scale': 1,    'type': 'U16',  'units': ''    , 'use': 'info',  'method': 'hold'},
    'Power_cg':   {'addr': '40217', 'registers': 1,  'name': 'Active power change gradient',     'scale': 1000, 'type': 'U32',  'units': '%/s' , 'use': 'info',  'method': 'hold'},


    #Bibliotecas Complementares
    'SN':         {'addr': '30015', 'registers': 10, 'name': 'Serial Number',                    'scale': 1,    'type': 'str',  'units': ''    , 'use': 'info',  'method': 'hold'},
    'strings':    {'addr': '30071', 'registers': 1,  'name': 'Number of strings',                'scale': 1,    'type': 'U16',  'units': ''    , 'use': 'info',  'method': 'hold'},
    'Pn':         {'addr': '30073', 'registers': 2,  'name': 'Rated power',                      'scale': 1000, 'type': 'U32',  'units': 'kW'  , 'use': 'info',  'method': 'hold'},
    'Pmax':       {'addr': '30075', 'registers': 2,  'name': 'Maximum active power',             'scale': 1000, 'type': 'U32',  'units': 'kW'  , 'use': 'info',  'method': 'hold'},
    'Smax':       {'addr': '30077', 'registers': 2,  'name': 'Maximum apparent power',           'scale': 1000, 'type': 'U32',  'units': 'kVA' , 'use': 'info',  'method': 'hold'},
    'Qmax':       {'addr': '30079', 'registers': 2,  'name': 'Maximum reactive power to grid',   'scale': 1000, 'type': 'I32',  'units': 'kVar', 'use': 'info',  'method': 'hold'},
    'Qgrid':      {'addr': '30081', 'registers': 2,  'name': 'Maximum reactive power from grid', 'scale': 1000, 'type': 'I32',  'units': 'kVar', 'use': 'info',  'method': 'hold'},
    'Insulation': {'addr': '32088', 'registers': 1,  'name': 'Insulation resistance',            'scale': 1000, 'type': 'U16',  'units': 'MΩ'  , 'use': 'info',  'method': 'hold'},
    'Time1?':     {'addr': '32110', 'registers': 2,  'name': 'some time 1',                      'scale': 1,    'type': 'U32',  'units': 's'   , 'use': 'ext',   'method': 'hold'},
    'Time2?':     {'addr': '32156', 'registers': 2,  'name': 'some time 2',                      'scale': 1,    'type': 'U32',  'units': 's'   , 'use': 'ext',   'method': 'hold'},
    'Time3?':     {'addr': '32160', 'registers': 2,  'name': 'some time 3',                      'scale': 1,    'type': 'U32',  'units': 's'   , 'use': 'ext',   'method': 'hold'},
    'Time4?':     {'addr': '35113', 'registers': 2,  'name': 'some time 4',                      'scale': 1,    'type': 'U32',  'units': 's'   , 'use': 'ext',   'method': 'hold'},
    'Time5?':     {'addr': '40500', 'registers': 2,  'name': 'some time 5',                      'scale': 1,    'type': 'U32',  'units': 's'   , 'use': 'ext',   'method': 'hold'},
    'State1':     {'addr': '32000', 'registers': 1,  'name': 'Status 1',                         'scale': 1,    'type': 'Bit16','units': ''    , 'use': 'stat',  'method': 'hold'},
    'State2':     {'addr': '32002', 'registers': 1,  'name': 'Status 2',                         'scale': 1,    'type': 'Bit16','units': ''    , 'use': 'stat',  'method': 'hold'},
    'State3':     {'addr': '32003', 'registers': 2,  'name': 'Status 3',                         'scale': 1,    'type': 'Bit32','units': ''    , 'use': 'stat',  'method': 'hold'},
    'Alarm1':     {'addr': '32008', 'registers': 1,  'name': 'Alarm 1',                          'scale': 1,    'type': 'Bit16','units': ''    , 'use': 'stat',  'method': 'hold'},
    'Alarm2':     {'addr': '32009', 'registers': 1,  'name': 'Alarm 2',                          'scale': 1,    'type': 'Bit16','units': ''    , 'use': 'stat',  'method': 'hold'},
    'Alarm3':     {'addr': '32010', 'registers': 1,  'name': 'Alarm 3',                          'scale': 1,    'type': 'Bit16','units': ''    , 'use': 'stat',  'method': 'hold'},
    'Status':     {'addr': '32089', 'registers': 1,  'name': 'Device status',                    'scale': 1,    'type': 'U16',  'units': ''    , 'use': 'stat',  'method': 'hold'},
    'Fault':      {'addr': '32090', 'registers': 1,  'name': 'Fault code',                       'scale': 1,    'type': 'U16',  'units': ''    , 'use': 'stat',  'method': 'hold'},
    'PV_P':       {'addr': '32064', 'registers': 2,  'name': 'Input power',                      'scale': 1000, 'type': 'I32',  'units': 'kW'  , 'use': 'data',  'method': 'hold'},
    'U_B-C':      {'addr': '32067', 'registers': 1,  'name': 'Line Voltage B-C',                 'scale': 10,   'type': 'U16',  'units': 'V'   , 'use': 'ext' ,  'method': 'hold'},
    'U_C-A':      {'addr': '32068', 'registers': 1,  'name': 'Line Voltage C-A',                 'scale': 10,   'type': 'U16',  'units': 'V'   , 'use': 'ext' ,  'method': 'hold'},
    'U_A':        {'addr': '32069', 'registers': 1,  'name': 'Phase Voltage A',                  'scale': 10,   'type': 'U16',  'units': 'V'   , 'use': 'data',  'method': 'hold'},
    'U_B':        {'addr': '32070', 'registers': 1,  'name': 'Phase Voltage B',                  'scale': 10,   'type': 'U16',  'units': 'V'   , 'use': 'data',  'method': 'hold'},
    'U_C':        {'addr': '32071', 'registers': 1,  'name': 'Phase Voltage C',                  'scale': 10,   'type': 'U16',  'units': 'V'   , 'use': 'ext' ,  'method': 'hold'},
    'I_A':        {'addr': '32072', 'registers': 2,  'name': 'Phase Current A',                  'scale': 1000, 'type': 'I32',  'units': 'A'   , 'use': 'data',  'method': 'hold'},
    'I_B':        {'addr': '32074', 'registers': 2,  'name': 'Phase Current B',                  'scale': 1000, 'type': 'I32',  'units': 'A'   , 'use': 'ext' ,  'method': 'hold'},
    'I_C':        {'addr': '32076', 'registers': 2,  'name': 'Phase Current C',                  'scale': 1000, 'type': 'I32',  'units': 'A'   , 'use': 'ext' ,  'method': 'hold'},
    'P_peak':     {'addr': '32078', 'registers': 2,  'name': 'Peak Power',                       'scale': 1000, 'type': 'I32',  'units': 'kW'  , 'use': 'data',  'method': 'hold'},
    'P_accum':    {'addr': '32106', 'registers': 2,  'name': 'Accumulated energy yield',         'scale': 100,  'type': 'U32',  'units': 'kWh' , 'use': 'data',  'method': 'hold'},
    'P_daily':    {'addr': '32114', 'registers': 2,  'name': 'Daily energy yield',               'scale': 100,  'type': 'U32',  'units': 'kWh' , 'use': 'data',  'method': 'hold'},
    'M_status':   {'addr': '37100', 'registers': 1,  'name': 'Meter status',                     'scale': 1,    'type': 'U16',  'units': ''    , 'use': 'stat',  'method': 'hold'},
    'M_check':    {'addr': '37138', 'registers': 1,  'name': 'Meter detection result',           'scale': 1,    'type': 'U16',  'units': ''    , 'use': 'stat',  'method': 'hold'},
    'M_type':     {'addr': '37125', 'registers': 1,  'name': 'Meter type'  ,                     'scale': 1,    'type': 'U16',  'units': ''    , 'use': 'stat',  'method': 'hold'},
    'M_P':        {'addr': '37113', 'registers': 2,  'name': 'Active Grid power',                'scale': 1,    'type': 'I32',  'units': 'W'   , 'use': 'data',  'method': 'hold'},
    'M_Pr':       {'addr': '37115', 'registers': 2,  'name': 'Active Grid reactive power',       'scale': 1,    'type': 'I32',  'units': 'VAR' , 'use': 'data',  'method': 'hold'},
    'M_A-U':      {'addr': '37101', 'registers': 2,  'name': 'Active Grid A Voltage',            'scale': 10,   'type': 'I32',  'units': 'V'   , 'use': 'data',  'method': 'hold'},
    'M_B-U':      {'addr': '37103', 'registers': 2,  'name': 'Active Grid B Voltage',            'scale': 10,   'type': 'I32',  'units': 'V'   , 'use': 'data',  'method': 'hold'},
    'M_C-U':      {'addr': '37105', 'registers': 2,  'name': 'Active Grid C Voltage',            'scale': 10,   'type': 'I32',  'units': 'V'   , 'use': 'data',  'method': 'hold'},
    'M_A-I':      {'addr': '37107', 'registers': 2,  'name': 'Active Grid A Current',            'scale': 100,  'type': 'I32',  'units': 'I'   , 'use': 'data',  'method': 'hold'},
    'M_B-I':      {'addr': '37109', 'registers': 2,  'name': 'Active Grid B Current',            'scale': 100,  'type': 'I32',  'units': 'I'   , 'use': 'data',  'method': 'hold'},
    'M_C-I':      {'addr': '37111', 'registers': 2,  'name': 'Active Grid C Current',            'scale': 100,  'type': 'I32',  'units': 'I'   , 'use': 'data',  'method': 'hold'},
    'M_PF':       {'addr': '37117', 'registers': 1,  'name': 'Active Grid PF',                   'scale': 1000, 'type': 'I16',  'units': ''    , 'use': 'data',  'method': 'hold'},
    'M_Freq':     {'addr': '37118', 'registers': 1,  'name': 'Active Grid Frequency',            'scale': 100,  'type': 'I16',  'units': 'Hz'  , 'use': 'data',  'method': 'hold'},
    'M_PExp':     {'addr': '37119', 'registers': 2,  'name': 'Grid Exported Energy',             'scale': 100,  'type': 'I32',  'units': 'kWh' , 'use': 'data',  'method': 'hold'},
    'M_U_AB':     {'addr': '37126', 'registers': 2,  'name': 'Active Grid A-B Voltage',          'scale': 10,   'type': 'I32',  'units': 'V'   , 'use': 'data',  'method': 'hold'},
    'M_U_BC':     {'addr': '37128', 'registers': 2,  'name': 'Active Grid B-C Voltage',          'scale': 10,   'type': 'I32',  'units': 'V'   , 'use': 'data',  'method': 'hold'},
    'M_U_CA':     {'addr': '37130', 'registers': 2,  'name': 'Active Grid C-A Voltage',          'scale': 10,   'type': 'I32',  'units': 'V'   , 'use': 'data',  'method': 'hold'},
    'M_A-P':      {'addr': '37132', 'registers': 2,  'name': 'Active Grid A power',              'scale': 1,    'type': 'I32',  'units': 'W'   , 'use': 'data',  'method': 'hold'},
    'M_B-P':      {'addr': '37134', 'registers': 2,  'name': 'Active Grid B power',              'scale': 1,    'type': 'I32',  'units': 'W'   , 'use': 'data',  'method': 'hold'},
    'M_C-P':      {'addr': '37136', 'registers': 2,  'name': 'Active Grid C power',              'scale': 1,    'type': 'I32',  'units': 'W'   , 'use': 'data',  'method': 'hold'},
    'M_PTot':     {'addr': '37121', 'registers': 2,  'name': 'Grid Accumulated Energy',          'scale': 100,  'type': 'U32',  'units': 'kWh' , 'use': 'data',  'method': 'hold'},
    'M_RPTot':    {'addr': '37123', 'registers': 2,  'name': 'Grid Accumulated Reactive Energy', 'scale': 100,  'type': 'I32',  'units': 'KVarh','use': 'data',  'method': 'hold'},
    'ModelID':    {'addr': '30070', 'registers': 1,  'name': 'Model ID',                         'scale': 1,    'type': 'U16',  'units': ''    , 'use': 'info',  'method': 'hold'},
    'MPPT_N':     {'addr': '30072', 'registers': 1,  'name': 'MPPT Number',                      'scale': 1,    'type': 'U16',  'units': ''    , 'use': 'info',  'method': 'hold'},
    'PF_comp':    {'addr': '40122', 'registers': 1,  'name': 'Reactive power compensation',      'scale': 1000, 'type': 'I16',  'units': ''    , 'use': 'data',  'method': 'hold'},
    'Q/S':        {'addr': '40123', 'registers': 1,  'name': 'Reactive power compensation(Q/S)', 'scale': 1000, 'type': 'I16',  'units': ''    , 'use': 'data',  'method': 'hold'},
    'Grid':       {'addr': '42000', 'registers': 1,  'name': 'Grid Code',                        'scale': 1,    'type': 'U16',  'units': ''    , 'use': 'info',  'method': 'hold'},
    'TZ':         {'addr': '43006', 'registers': 1,  'name': 'Time Zone',                        'scale': 1,    'type': 'I16',  'units': 'min' , 'use': 'info',  'method': 'hold'}


}



#Bateria
if (config.has_ESU) :
    _register_map.update({
        'ESU_status':             {'addr': '37000', 'registers': 1,  'name': 'ESU status',                       'scale': 1,    'type': 'U16',  'units': '' ,       'use': 'status','method':'hold' },
        'ESU_power':              {'addr': '37001', 'registers': 2,  'name': 'ESU power',                        'scale': 1,    'type': 'I32',  'units': 'W',       'use': 'data',  'method': 'hold'},
        'ESU_voltage':            {'addr': '37003', 'registers': 1,  'name': 'ESU voltage',                      'scale': 10,   'type': 'I16',  'units': 'V',       'use': 'data',  'method': 'hold'},
        'ESU_soc':                {'addr': '37004', 'registers': 1,  'name': 'ESU SOC',                          'scale': 10,   'type': 'U16',  'units': '%',       'use': 'data',  'method': 'hold'},
        'ESU_mode':               {'addr': '37006', 'registers': 1,  'name': 'ESU working mode b',               'scale': 1,    'type': 'U16',  'units': '%',       'use': 'data',  'method': 'hold'},
        'ESU_rated_power':        {'addr': '37007', 'registers': 2,  'name': 'ESU rated power',                  'scale': 1,    'type': 'U32',  'units': 'W',       'use': 'info',  'method': 'hold'},
        'ESU_rated_discharge':    {'addr': '37009', 'registers': 2,  'name': 'ESU rated discharge',              'scale': 1,    'type': 'U32',  'units': 'W',       'use': 'info',  'method': 'hold'},
        'ESU_charge':             {'addr': '37015', 'registers': 2,  'name': 'ESU Current Charge',               'scale': 100,  'type': 'U32',  'units': 'kWh',     'use': 'data',  'method': 'hold'},
        'ESU_discharge':          {'addr': '37017', 'registers': 2,  'name': 'ESU Current Discharge',            'scale': 100,  'type': 'U32',  'units': 'kWh',     'use': 'data',  'method': 'hold'},
        'ESU_current':            {'addr': '37021', 'registers': 1,  'name': 'ESU Current',                      'scale': 10,   'type': 'I16',  'units': 'A',       'use': 'data',  'method': 'hold'},
        'ESU_temp':               {'addr': '37022', 'registers': 1,  'name': 'ESU temperature',                  'scale': 10,   'type': 'I16',  'units': '°C',      'use': 'data',  'method': 'hold'},
        'ESU_time':               {'addr': '37025', 'registers': 1,  'name': 'ESU remaining time',               'scale': 1,    'type': 'U16',  'units': 'min',     'use': 'data',  'method': 'hold'},
        'ESU_dcdc_v':             {'addr': '37026', 'registers': 10, 'name': 'ESU DC-DC version',                'scale': 1,    'type': 'str',  'units': '' ,       'use': 'info',  'method': 'hold'},
        'ESU_bms_v':              {'addr': '37036', 'registers': 10, 'name': 'ESU BMS version',                  'scale': 1,    'type': 'str',  'units': '' ,       'use': 'info',  'method': 'hold'},
        'ESU_max_charge':         {'addr': '37046', 'registers': 2,  'name': 'ESU max charge power',             'scale': 1,    'type': 'U32',  'units': 'W',       'use': 'info',  'method': 'hold'},
        'ESU_max_discharge':      {'addr': '37048', 'registers': 2,  'name': 'ESU max discharge power',          'scale': 1,    'type': 'U32',  'units': 'W',       'use': 'info',  'method': 'hold'},
        'ESU_serialN':            {'addr': '37052', 'registers': 10, 'name': 'ESU serial number',                'scale': 1,    'type': 'str',  'units': '' ,       'use': 'info',  'method': 'hold'},
        'ESU_tot_charge':         {'addr': '37066', 'registers': 2,  'name': 'ESU total charge',                 'scale': 100,  'type': 'U32',  'units': 'kWh',     'use': 'info',  'method': 'hold'},
        'ESU_tot_discharge':      {'addr': '37068', 'registers': 2,  'name': 'ESU total discharge',              'scale': 100,  'type': 'U32',  'units': 'kWh',     'use': 'info',  'method': 'hold'},

        #Geral
        'ES_soc':                 {'addr': '37760', 'registers': 2,  'name': 'ES SOC',                           'scale': 10,   'type': 'U16',  'units': '%',       'use': 'data',  'method': 'hold'},
        'ES_voltage':             {'addr': '37763', 'registers': 1,  'name': 'ES voltage',                       'scale': 10,   'type': 'U16',  'units': 'V',       'use': 'data',  'method': 'hold'},
        'ES_current':             {'addr': '37764', 'registers': 1,  'name': 'ES current',                       'scale': 10,   'type': 'U16',  'units': 'A',       'use': 'data',  'method': 'hold'},
        'ES_power':               {'addr': '37765', 'registers': 2,  'name': 'ES charge/discharge power',        'scale': 1,    'type': 'U32',  'units': 'W',       'use': 'info',  'method': 'hold'},
        'ES_tot_charge':          {'addr': '37780', 'registers': 2,  'name': 'ES total charge',                  'scale': 100,  'type': 'U32',  'units': 'kWh',     'use': 'info',  'method': 'hold'},
        'ES_tot_discharge':       {'addr': '37782', 'registers': 2,  'name': 'ES total discharge',               'scale': 100,  'type': 'U32',  'units': 'kWh',     'use': 'info',  'method': 'hold'},
       


        'ESU_pack1_soc':          {'addr': '38229', 'registers': 1,  'name': 'ESU pack1 SOC',                    'scale': 10,   'type': 'U16',  'units': '%',       'use': 'info',  'method': 'hold'},
        'ESU_pack1_power':        {'addr': '38233', 'registers': 1,  'name': 'ESU pack1 charge/discharge power', 'scale': 100,  'type': 'I32',  'units': 'kW',      'use': 'info',  'method': 'hold'},
        'ESU_pack1_voltage':      {'addr': '38235', 'registers': 1,  'name': 'ESU pack1 voltage',                'scale': 10,   'type': 'U16',  'units': 'V',       'use': 'info',  'method': 'hold'},
        'ESU_pack1_current':      {'addr': '38236', 'registers': 1,  'name': 'ESU pack1 current',                'scale': 10,   'type': 'I16',  'units': 'A',       'use': 'data',  'method': 'hold'},
        'ESU_pack1_tot_charge':   {'addr': '38238', 'registers': 2,  'name': 'ESU pack1 total charge',           'scale': 100,  'type': 'U32',  'units': 'kWh',     'use': 'info',  'method': 'hold'},
        'ESU_pack1_tot_discharge':{'addr': '38240', 'registers': 2,  'name': 'ESU pack1 total discharge',        'scale': 100,  'type': 'U32',  'units': 'kWh',     'use': 'info',  'method': 'hold'},
        'ESU_pack2_soc':          {'addr': '38271', 'registers': 1,  'name': 'ESU pack2 SOC',                    'scale': 10,   'type': 'U16',  'units': '%',       'use': 'info',  'method': 'hold'},
        'ESU_pack2_power':        {'addr': '38275', 'registers': 2,  'name': 'ESU pack2 charge/discharge power', 'scale': 1000, 'type': 'U16',  'units': '%',       'use': 'info',  'method': 'hold'},
        'ESU_pack2_voltage':      {'addr': '38277', 'registers': 1,  'name': 'ESU pack2 voltage',                'scale': 10,   'type': 'U16',  'units': 'V',       'use': 'info',  'method': 'hold'},
        'ESU_pack2_current':      {'addr': '38278', 'registers': 1,  'name': 'ESU pack2 current',                'scale': 10,   'type': 'I16',  'units': 'A',       'use': 'info',  'method': 'hold'},
        'ESU_pack2_tot_charge':   {'addr': '38280', 'registers': 2,  'name': 'ESU pack2 total charge',           'scale': 100,   'type': 'U32',  'units': 'kWh',    'use': 'info',  'method': 'hold'},
        'ESU_pack2_tot_discharge':{'addr': '38282', 'registers': 2,  'name': 'ESU pack2 total discharge',        'scale': 100,   'type': 'U32',  'units': 'kWh',    'use': 'info',  'method': 'hold'},



        
        'ESU_model':              {'addr': '47000', 'registers': 1,  'name': 'ESU battery type',                 'scale': 1,    'type': 'U16',  'units': '' ,       'use': 'info',  'method': 'hold'},
        'ESU_charging':           {'addr': '47075', 'registers': 2,  'name': 'ESU max charging power',           'scale': 1,    'type': 'U32',  'units': 'W',       'use': 'info',  'method': 'hold'},
        'ESU_discharging':        {'addr': '47077', 'registers': 2,  'name': 'ESU max discharging power',        'scale': 1,    'type': 'U32',  'units': 'W',       'use': 'info',  'method': 'hold'},
        'ESU_charging_cutoff':    {'addr': '47081', 'registers': 1,  'name': 'ESU charging cutoff',              'scale': 10,   'type': 'U16',  'units': '%',       'use': 'info',  'method': 'hold'},
        'ESU_discharging_cutoff': {'addr': '47082', 'registers': 1,  'name': 'ESU discharging cutoff',           'scale': 10,   'type': 'U16',  'units': '%',       'use': 'info',  'method': 'hold'},
        'ESU_forced':             {'addr': '47083', 'registers': 1,  'name': 'ESU forced cutoff',                'scale': 1,    'type': 'U16',  'units': 'min',     'use': 'info',  'method': 'hold'},
        'ESU_mode2':              {'addr': '47086', 'registers': 1,  'name': 'ESU mode 2',                       'scale': 1,    'type': 'U16',  'units': '' ,       'use': 'info',  'method': 'hold'},
        'ESU_grid':               {'addr': '47087', 'registers': 1,  'name': 'ESU grid charging',                'scale': 1,    'type': 'U16',  'units': '' ,       'use': 'info',  'method': 'hold'},
        'ESU_forcible_power':     {'addr': '47100', 'registers': 1,  'name': 'ESU forcible charge/discharge',    'scale': 1,    'type': 'U16',  'units': '' ,       'use': 'info',  'method': 'hold'},
        'ESU_forcible_charge':    {'addr': '47247', 'registers': 2,  'name': 'ESU forcible charge power',        'scale': 1,    'type': 'U32',  'units': 'KW' ,     'use': 'info',  'method': 'hold'},
        'ESU_forcible_discharge': {'addr': '47249', 'registers': 2,  'name': 'ESU forcible discharge power',     'scale': 1000, 'type': 'U32',  'units': 'kW' ,     'use': 'info',  'method': 'hold'},

        })



