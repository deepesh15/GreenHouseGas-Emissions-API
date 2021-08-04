import sqlite3
import json

conn = sqlite3.connect('data.db',check_same_thread=False)
conn.row_factory = sqlite3.Row
cur = conn.cursor()
category_dic = {"CO2":"6737efdb","GHG(indirect)":"066f4b5c","GHG":"52322f3e","HFC":"93b1175f","CH4":"1db1e409","NF3":"fbafb8ae","N20":"b0ae316d","PFC":"c428f144","SF6":"f9871080","HFC(unspecified)":"66a892e3"}
country_id_lst = ['691c052d', '1510c1b7', '275a4f89', 'ad35b9f2', '0aaa9325', '15a88656', '78e4745e', '6c1088d4', '1ff64114', '22a538f7', '31bc89ee', '3fe5c5c4', 'fda284e0', '7c39069f', '593d6e36', '19fbb276', '0d99ac61', 'debe5302', '1c2a8324', '897f0527', 'fff865f8', '4ebefb6b', '019aaf9a', '42227c7d', '7a1b0dc4', 'c0fdf29b', 'c5611df5', '7a075572', '56644481', 'b8fe3183', 'b1603ef9', '28fac1f3', '86f03a2d', 'ea07fd80', '3e54c14d', 'bba1b18d', 'b509301f', '3460da95', '7fc020e1', 'dcf9661f', 'fdc5f179', '74667528', '741d42b8']
category_id_lst = ['066f4b5c', '66a892e3', '93b1175f', 'f9871080', '1db1e409', 'fbafb8ae', 'c428f144', '6737efdb', '52322f3e', 'b0ae316d']

def getAll():
    cur.execute('SELECT * FROM data')
    rows = cur.fetchall()
    return json.dumps([dict(x) for x in rows])
    
def getAllCountries():
    cur.execute('SELECT DISTINCT country_id,country FROM data' )
    rows = cur.fetchall()
    return json.dumps([dict(x) for x in rows])

def getAllCategories():
    cur.execute('SELECT DISTINCT category_id,category FROM data' )
    rows = cur.fetchall()
    return json.dumps([dict(x) for x in rows])

def getCountryData(id,start,end,params):
    cur.execute('SELECT * FROM data WHERE country_id = "{}" AND (year BETWEEN {} and {}) AND category_id IN {} ORDER by year ASC'.format(id,start,end,params))
    rows = cur.fetchall()
    return json.dumps([dict(x) for x in rows])

def getDataBetweenYears(start,end):
    cur.execute('SELECT * FROM data WHERE year  BETWEEN {} and {} ORDER BY year'.format(start,end))
    return cur.fetchall()

def temp():
    cur.execute("SELECT * FROM(SELECT * FROM data WHERE category_id = '6737efdb' or category_id='93b1175f')WHERE country_id = '7fc020e1'")
    rows = cur.fetchall()
    return json.dumps([dict(x) for x in rows])


