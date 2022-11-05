import os
from flask import Flask, render_template, request, url_for, flash, redirect
#from flask import jsonify
import json
import requests
import operator


def call_hh_webapi(text,region):
    api_url = 'https://go-web-hh-vac.cfapps.us10.hana.ondemand.com/hh4?text=' + text + '&' + 'area=' + region
    #api_url = 'http://localhost:8080/hh4?text=' + text + '&' + 'area=' + region
    
    res = requests.get(api_url)

    # Convert data to list of dicts
    data = json.loads(res.text)

    responce_json = data
    return responce_json


def analisys(dict_of_key_skills, responce):
    for line in responce:
        strArrKeySkills = line["strArrKeySkills"]
        if strArrKeySkills == None:
            continue
        for key_skill in strArrKeySkills:
            if dict_of_key_skills.setdefault(key_skill['name']) == None:
                dict_of_key_skills[key_skill['name']] = 1
            else:
                dict_of_key_skills[key_skill['name']] += 1   


def call_back_serv(text,region):
    api_url = 'https://govacbackserv.cfapps.us10.hana.ondemand.com/?text=' + text + '&' + 'area=' + region
    res = requests.get(api_url)
    data = json.loads(res.text)
    responce_json = data
    return responce_json

#from contextlib import redirect_stdout

app = Flask(__name__)
port = int(os.environ.get('PORT', 3000))


@app.route('/')
def hello():
    return "Hello from Python!"


#@app.route('/hh1/', methods=('GET', 'POST'))
#def hh1():
#    str_text = ""
#    str_area = ""
#    if request.method == 'POST':
#        str_text = request.form['strText']
#        str_area = request.form['strArea']
#    return render_template('index.html', strText =  str_text, strArea = str_area )    


@app.route('/hh2/', methods=('GET', 'POST'))
def hh2():
    str_text = ""
    str_area = ""
    sorted_d = {}
    items_num = ""
    if request.method == 'POST':
        str_text = request.form['strText']
        str_area = request.form['strArea']
    
        text = str_text
        region = str_area
        dict_of_key_skills = {} 
        responce = call_hh_webapi(text,region)
        analisys(dict_of_key_skills, responce)
        sorted_d = dict( sorted(dict_of_key_skills.items(), key=operator.itemgetter(1),reverse=True))
        items_num = str(len(sorted_d)) + " skills are found"
    return render_template('index_2.html', strText =  str_text, strArea = str_area, skill_list = sorted_d, strItemsNum = items_num )    


@app.route('/hh4/')
def hh4():
    hh_regions = [ "Воронеж",
                    #"Нижний Новгород",
                    #"Пермь",
                    # "Москва", "Санкт-Петербург",
                ]

    list_of_skills = [
                  #"ABAP developer",
                  #"1С программист",
                  #"Python developer",
                  "Go developer",
                 ]

#with open('C:\TempPy\Results_1f_go.txt', 'w') as f:
#    with redirect_stdout(f): 

    for skill in list_of_skills:
        text = skill
        dict_of_key_skills = {} 
        for region_text in hh_regions:
            print(region_text, ",")
            region = region_text
            responce = call_hh_webapi(text,region)
            analisys(dict_of_key_skills, responce)
        sorted_d = dict( sorted(dict_of_key_skills.items(), key=operator.itemgetter(1),reverse=True))
   
        #return jsonify(sorted_d)
        return sorted_d


# The endpoint is deprecated
@app.route('/hh5/', methods=('GET', 'POST'))
def hh5():
    str_text = ""
    str_area = ""
    sorted_d = {}
    items_num = ""
    if request.method == 'POST':
        str_text = request.form['strText']
        str_area = request.form['strArea']

        text = str_text
        region = str_area
        dict_of_key_skills = {} 
        responce = call_hh_webapi(text,region)
        # analisys(dict_of_key_skills, responce)
        # sorted_d = dict( sorted(dict_of_key_skills.items(), key=operator.itemgetter(1),reverse=True))
        # items_num = str(len(sorted_d)) + " skills are found"
    return render_template('index_2.html', strText =  str_text, strArea = str_area, skill_list = sorted_d, strItemsNum = items_num )


# The endpoint for the central backend service 'go_vac_back_serv'
@app.route('/hh6/', methods=('GET', 'POST'))
def hh6():
    str_text = ""
    str_area = ""
    sorted_d = {}
    items_num = ""

    if request.method == 'POST':
        str_text = request.form['strText']
        str_area = request.form['strArea']
        text = str_text
        region = str_area
        dict_of_key_skills = {}
        
        responce = call_back_serv(text,region)
        point1_data = responce['Point1']
        if point1_data['strErr'] == "":
            items_num = str(point1_data['arrData'][0]['sSummary'][0]['intCount']) + " skills are found"
            point1_skills = point1_data['arrData'][0]['sSummary'][1]['arrTerm']
            for skill in point1_skills:
                key = skill['strTerm'] 
                value = round(skill['dblQuota'], 3)
                sorted_d[key] = value
        else:
            items_num = point1_data['strErr']

    return render_template('index_6.html', strText =  str_text, strArea = str_area, skill_list = sorted_d, strItemsNum = items_num )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
    # app.run(host='localhost', port=port)
