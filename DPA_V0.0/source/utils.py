#coding: UTF-8 
#########################################################################################
# Developer: Deiner Zapata Silva.
# Date: 29/11/2018
# Last update: 06/05/2019
# Description: Codigo util, para uso general
# sys.setdefaultencoding('utf-8') #reload(sys)
# hash- > hashlib https://recursospython.com/guias-y-manuales/hashlib-md5-sha/
# crypto -> DES https://www.laurentluce.com/posts/python-and-cryptography-with-pycrypto/
# pip install pycryptodome
#########################################################################################
import sys, requests, json, csv
#from flask import Flask, request, abort
import jwt # pip install pyjwt
import time, os, socket
from subprocess import Popen, PIPE
from collections import OrderedDict
import functools, yaml #pip install pyyaml
import base64 as b64
#######################################################################################
def print_list(lista, num=0, sort=True):
    if(sort): lista.sort()
    for item in lista:
        print("   {0:03d}. {1} ".format( num, item) )
        num+=1
    return
########################################################################################
def print_json(json_obj,codification='utf-8'):
    try:
        print(json.dumps(json_obj, indent=2, sort_keys=True))
    except:
        print("[ERROR] print_json -> error type={0}".format(type(json_obj)))
    
    return
#######################################################################################
def fileTXT_save(text, nameFile = "fileTXT_save.txt", coding='utf-8'):
    fnew  = open(nameFile,"wb")
    fnew.write(text.encode(coding)) # str(aux=[line])+'\n'
    fnew.close() 
    return
#######################################################################################
def count_elapsed_time(f,*args,**kwargs):
    """
    Decorator.
    Calculate the elapsed time of a function.
    """
    def wrapper(*args):
        #from time import time
        start_time = time.time()
        ret = f(*args,**kwargs)
        elapsed_time = time.time() - start_time
        print("[count_elapsed_time] "+f.__name__+"Elapsed time: %0.10f seconds." % elapsed_time)
        return ret
    return wrapper
#######################################################################################
def string2hex(s,char_sep=":"): #convert string to hex
    lst = []
    for ch in s:
        num_ascci = ord(ch)
        hv = hex(num_ascci).replace('0x', '')
        if len(hv) == 1:
            hv = '0'+hv
        lst.append(hv)
    if(len(lst)>0):
        return functools.reduce(lambda x,y:x+char_sep+y, lst)
    else:
        #print("[ERROR] string2hex [{0}]".format(s))
        return ""
#######################################################################################
"""
    #Ejemplo de uso
    data_json1 = {
        "A1": 1,
        "A2": {
            "A2_1": 2,
            "A2_2": {
                "A2_2_1": 4,
                "A2_3_4": 5
            },
            "A3": [
                {
                    "A3_1": 31,
                    "A3_2": {
                        "A3_2_1": 321,
                        "A3_2_2": 322,
                        "A3_2_3": [
                            {
                            "A3_2_3_1": 3231.1,
                            "B1": {
                                    "B1_1": 1.1
                                }
                            }
                            ,
                            {
                            "A3_2_3_1": 3231.2
                            }
                        ]
                    }
                },
                {
                    "A3_1": 32,
                    "A3_2": {
                        "A3_2_3": [
                            {
                            "A3_2_3_1": 3231.3,
                            "B1": {
                                    "B1_1": 1.1
                                }
                            },
                            {
                            "A3_2_3_1": 3231.4
                            }
                        ]
                    }
                },
                {
                    "A3_1": 33
                }
            ]
        }
    }
    path_element1 = "A2.[A3].A3_2.[A3_2_3].B1.B1_1"
    rpt_json = getelementfromjson(data_json1,path_element1)
    print_list(rpt_json)
"""
def getelementfromjson(data_json,path_to_element):
    # Accede a un elemento anidado en un json, con un camino especificado de la forma
    # path_to_element = "payload.aggregations.[clientes].[sedes][ip_s]"
    list_keys = []
    list_path_element = path_to_element.split(".")
    walker = data_json
    #print("PATH       :        "+ path_to_element)
    for element in list_path_element:
        current_path = path_to_element[ path_to_element.find(element)+len(element)+ 1: ]
        #print("<{0}>".format(element))
        if element.find("[")==0 and element.find("]")>0 :#si tiene corchetes, significa q es un array
            #print("->    <{0}> {1}".format(element,current_path))
            list_temp = []
            only_element = element[1:len(element)-1]
            if (only_element in walker):
                array_walker = walker[only_element]
                if len(current_path)==0: #Caso: agregar todo el array
                    list_keys.append(array_walker)
                    break
                # Caso: recorrer el array
                #print("[INI] {0} | {1} | values from array".format(element,current_path))
                for element_in_array in array_walker:
                    rpt_json = getelementfromjson(element_in_array,current_path)
                    #print_json(rpt_json)
                    if (type(rpt_json)==list):
                        for val_in_list in rpt_json:
                            list_keys.append(val_in_list)
                    elif len(rpt_json)>0:
                        list_keys.append(rpt_json)
                #print("[END] {0} | {1} | values from array".format(element,current_path))
                return list_keys
            else:
                #print("[ERROR] getelementfromjson|{1}| key:{0} don't found in json.".format(only_element,path_to_element))
                pass
        else:#sino, entonces es un elemento simple ha acceder en el json
            #print("->    <{0}> {1}".format(element,current_path))
            if (element in walker):
                #Si es el fin del path, entonces solo queda agregar el elemento
                if(len(current_path)==0):
                    walker = walker[element]
                    list_keys.append(walker)
                    #print("[INI] {0} | {1} | Adding value".format(element,path_to_element))
                    #print_json(walker)
                    #print("[END] {0} | {1} | Adding value".format(element,path_to_element))
                    break
                else:
                    walker = walker[element]
            else:
                #print("[ERROR] getelementfromjson|{1}|key:{0} don't found in json.".format(element,path_to_element))
                pass
    #list_keys.append(walker)
    #print_json(walker)
    return list_keys
#######################################################################################
def list2json(list_field, list_value,remove_char=None,type_data=None,return_err=False):
    data_json = {}
    len_field = len(list_field)
    len_value = len(list_value)
    flag_err = 0

    if (type_data!=None and len_field!=len(type_data)):
        print("[ERROR] list2json type_data disabled.")
        type_data=None

    if ( len_field > len_value):
        print("[ERROR] list2json len_field:{0} > len_value:{1}".format(len_field,len_value))
        for i in range(0,len_value):
            print(" ->  {0:02d} |[{1}:{2}]".format(i, str(list_field[i]), str(list_value[i])))
        for i in range(len_value,len_field):
            print(" ->  {0:02d} |[{1}:NULL]".format(i, str(list_field[i])))
        flag_err=-1
    elif( len_field < len_value ):
        print("[WARN] list2json len_field:{0} < len_value:{1}  ".format(len_field,len_value))
        for i in range(0,len_field):
            print(" ->  {0:02d} |[{1}:{2}]".format(i, str(list_field[i]), str(list_value[i]) ))
        for i in range(len_field,len_value):
            print(" ->  {0:02d} |[{1}]".format(i, str(list_value[i]) ))
        flag_err=1
    
    for i in range(0,len_field):
        if (len(list_field[i])>0):
            if(remove_char!=None):
                list_value[i]=list_value[i].replace(remove_char,"")
            
            if(type_data==None):
                data_json.update({list_field[i] : list_value[i]})
            else:
                if(type_data[i]=='int'):
                    data_json.update({list_field[i] : int(list_value[i])})
                elif(type_data[i]=='float'):
                    data_json.update({list_field[i] : float(list_value[i])})
                else:
                    data_json.update({list_field[i] : list_value[i]})
            
            if not(len(list_value[i])>0):
                print("[WARN] field lost [{0}:{1}]".format(list_field[i],list_value[i]))
                flag_err=2
    
    if(return_err):
        return data_json, flag_err
    else:
        return data_json
#######################################################################################
def loadCSVtoJSON(path,encoding="utf-8"):
    csvfile = open(path,encoding=encoding)
    data = csv.DictReader(csvfile)#,delimiter =";",quotechar=";")
    list_data = []
    row = dict()
    for row in data:
        #print("loadCVStoJSON -> "+str(type(row)))
        #print(row)
        #list_data.append( dict( OrderedDict(row) ) ) 
        list_data.append( row )
    
    print("["+str(path)+"] -> Datos cargados:" + str(len(list_data)))
    return list_data
###############################################################################
def loadYMLtoJSON(path):
    data_loaded = None
    with open(path,'r') as stream:
        try:
            data_loaded = yaml.load(stream)
        except:
            print("[ERROR] loadYMLtoJSON")
    return data_loaded
#######################################################################################
def isAliveIP(host, count=1, timeout=1000):
    if sys.platform == 'win32':
        count_arg = '-n'
        timeout_arg = '-w'
    else:
        count_arg = '-c'
        timeout_arg = '-W'

    args = map(str, [ 'ping', count_arg, count, timeout_arg, timeout, host ])

    p = Popen(args, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()

    # success
    val = p.returncode
    if p.returncode == 0:
        #try:
            #m = re.search("time=(\d+(?:\.\d+){0,1})\s*ms", output)
            #time = float(m.group(1))
            #time = 1
        #except Exception, e:
        #	time = -1
        return True
    else:
        #time = None
        return False    
    #return (time, p.returncode)
###############################################################################
def renameValues(old_dict,old_value,value_to_set,cont=0):
    new_dict = {}
    if(cont==5): #para evitar que caiga en un bucle, solo busca en 5 niveles top-down
        return
    for key,value in zip(old_dict.keys(),old_dict.values()):
        #print("renameValues->{2} {0}:{1}".format(key,value,type(value)))
        if type(value)==dict:
            cont=cont+1
            new_value =renameValues(value,old_value,value_to_set, cont) #Recurcividad
        elif(value==old_value):
            new_value = value_to_set
        else:
            new_value = value
        # Si value_to_set==None -> la key actual es eliminada y se borra dicho valor.
        if new_value!=None:
            new_dict.update( {key : new_value} )
        
    return new_dict
###############################################################################
def renameKeys(old_dict,dict_oldkey_newkey,cont=0):
    new_dict = {}
    if(cont==5):
        return
    for key,value in zip(old_dict.keys(), old_dict.values()):
        #Analizando "value"
        if type(value)==dict:
            cont = cont + 1
            new_value = renameKeys(value,dict_oldkey_newkey,cont)
        else:
            new_value = value
        #Analizando "key"
        if key in dict_oldkey_newkey:
            new_key = dict_oldkey_newkey[key]
        else:
            new_key = key
        new_dict[new_key] = new_value
    return new_dict
###############################################################################
def build_table_json(list_name_keys, list_data_json):
    #La unica condicion es que los datos tengas la misma cantidad de llaves
    # list_name_keys = ['key1','key2',...]
    # list_data_json = [{'aux1': 'val1', 'aux2':'VAL1',...},{'aux1':'val2','aux2':'VAL2',...},]
    # return [{'key1':'val1','key2':'VAL1',...},{'key1': 'val2','key2': 'VAL2',...}, ...]
    list_keys = list(list_data_json[0])
    table_json = []
    for key in list_keys:
        rpt_json = {}
        cont = 0
        for data_json in list_data_json:
            rpt_json.update( {list_name_keys[cont] : data_json[key]} )
            table_json.append(rpt_json)
            cont += 1
    return table_json
###############################################################################
def convert_data(data_to_convert,strc_dict):
    data_converted = {}
    try:
        # path_of_multi_dict: Especifica la ruta con los multiples diccionarios a cargar
        if 'path_of_multi_dict' in strc_dict:
            path_of_multi_dict = strc_dict['path_of_multi_dict']
            dict_to_load = strc_dict['dict_to_load']
            #print("dict "+dict_to_load)
            dict_yml = loadYMLtoJSON(path_of_multi_dict)
            dictionary = dict_yml[dict_to_load]
            data_converted=renameKeys(data_to_convert, dictionary)
        # strc_dict   : Es un diccionario que contiene multiples diccionarios
        # dict_to_load: Especifica que diccionario se va a utilzar para convertir la data
        elif 'dict_to_load' in strc_dict:
            dict_to_load = strc_dict['dict_to_load']
            dictionary = strc_dict['multi_dict'][dict_to_load]
            data_converted=renameKeys(data_to_convert, dictionary)
        else:
            print("[ERROR] convert_data {0}".format(str(strc_dict)))
            data_converted = data_to_convert
        #print_json(data_converted)
    except:
        print("[ERROR] returned data without convert.")
        data_converted = data_to_convert
    return data_converted
    
###############################################################################
def send_json(msg, IP="0.0.0.0", PORT = 2233, dictionary={}, emulate=False):
    """
        #Configuracion en /etc/logstash/conf.d/logstash-syslog.conf
        input{
            tcp{
                port => [PORT_NUMBER]
                codec => json
            }
        }

        Si se desea convertir algunos campos antes de ser enviados
        se pasa la variable dictionary
    """
    if(type(PORT)==str):
        PORT = int(PORT)
    try:
        if(len(dictionary)>0):
            msg = convert_data(msg,dictionary)
        #Printing message
        #print( "Sending message... emulate = {0}".format(emulate) )
        if not (emulate): #If emulate=True don't send data to logstash
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect( (IP,PORT) )    
            datajs = json.dumps(msg)
            sock.sendall( datajs.encode() )
            #print_json(msg)
    except:
        print("Error inesperado: "+sys.exc_info()[0])
        #sys.exit(1)
        return
    finally:
        try:
            sock.close()
        except:
            pass
        return
#######################################################################################
def save_yml(data_json, nameFile="data.yml", type_open="w"):
    with open(nameFile, type_open) as yaml_file:
        yaml.dump(data_json, yaml_file, default_flow_style=False)
    return
#######################################################################################
def save_json(data_json, nameFile="data.json"):
    with open(nameFile, 'w') as json_file:
        for release in data_json.values():
            json_file.write(release)
            json_file.write("\n")
    return
#######################################################################################
# doc_jwt http://ras-software-blog.com/?p=107
def hmac_json_encode(data_json, password="", algorithm="HS256"):
    #data_json_encrypted = header.payload.signature(openssl sha256 -hmac <password>)
    data_json_to_encrypt = data_json
    data_json_encrypted = jwt.encode(data_json_to_encrypt, password, algorithm=algorithm)

    return data_json_encrypted
#######################################################################################
def hmac_json_decode(data_json, password="", algorithm="HS256"):
    #data_json = header.payload.signature(openssl sha256 -hmac <password>)
    data_json_to_decode = data_json
    data_json_decoded = jwt.decode(data_json_to_decode, password, algorithm=algorithm)
    return data_json_decoded
#######################################################################################
def test_hmac_json():
    #function to test hmac algorithm
    data_json = {
        "FirstName":"Rob",
        "LastName":"Stanfield",
        "Occupation":"Software Developer"
    }
    data_signated = hmac_json_encode(data_json, password="ABC")
    print("-----------------------------------------------------------\ndata signed:\n")
    print("{0}".format(data_signated))
    data_json = hmac_json_decode(data_signated, password="ABC")
    print("-----------------------------------------------------------\ndata json :\n")
    print_json(data_json)
    return
#######################################################################################
def encode(str_to_encode, base_coding="base64", encoding='utf-8'):
    data_encoded = ""
    flag_str=False
    try:
        if type(str_to_encode)==str:
            flag_str = True
            data_bytes = str_to_encode.encode(encoding)
        else:
            data_bytes = str_to_encode
        data_encoded = b64.b64encode(data_bytes)
        #print("[INFO ] encoded [{0}]".format(data_encoded))
    except:
        print("[ERROR] encoded {1} [{0}]".format(str_to_encode, type(str_to_encode) ))
    finally:
        if flag_str:
            return data_encoded.decode(encoding)
        else:
            return data_encoded
#######################################################################################
def decode(data_encoded, base_coding="base64", encoding='utf-8'):
    data_decoded = ""
    flag_str=False
    try:
        if type(data_encoded)==str: 
            flag_str = True
            data_bytes = data_encoded.encode(encoding)
        else:
            data_bytes = data_encoded
        data_decoded = b64.b64decode(data_encoded)
        #print("[INFO ] decode [{0}]".format(data_decoded))
    except:
        print("[ERROR] decode [{0}]".format(data_encoded))
    finally:
        if flag_str:
            return data_decoded.decode(encoding)
        else:
            return data_decoded
#######################################################################################
if __name__ == "__main__":
    #Testing function
    print("[INFO] {0}".format(__file__ ))
    test_hmac_json()