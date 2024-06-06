from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3

                                                                                                                                       
app = Flask(__name__)

# =========================== Créer une route pour les contacts ===================================
@app.route("/contact/")
def moncontact():
    return render_template("contact.html")
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')
  
  # ======================= Créer une route la meteo de la ville de tawarano  =====================
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
  
# ============================ Créer une route pour le Graphique ===================================
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
  
# =========================== Créer une route pour l'histogramme ===================================
@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")
  
# ============== Créer une route pour extraire l'activité du repository (Commits) ==================
@app.route('/metriques/')
def ali_commit():
    url = 'https://api.github.com/repos/Alilou-75/5MCSI_Metriques/commits'
    response = urlopen(url)
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []

    for commit in json_content:
        commit_time = commit['commit']['author']['date']
        dt_value = datetime.strptime(commit_time, '%Y-%m-%dT%H:%M:%SZ')
        minute = dt_value.strftime('%Y-%m-%d %H:%M')
        results.append(minute)

    # Comptabiliser le nombre de commits par minute
    commit_counts = {}
    for minute in results:
        if minute in commit_counts:
            commit_counts[minute] += 1
        else:
            commit_counts[minute] = 1

    # Convertir les données en une liste de listes pour Google Charts
    chart_data = [['Minute', 'Commits']]
    for minute, count in commit_counts.items():
        chart_data.append([minute, count])

    return jsonify(results=chart_data)
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    try:
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})
    except ValueError:
        return jsonify({'error': 'Invalid date format, expected format: YYYY-MM-DDTHH:MM:SSZ'}), 400

# =================== Créer une route pour un Graphique des Commits par minutes =====================
@app.route("/commits/")
def mescommits():
    return render_template("commits.html")

#@app.route('/extract-minutes/<date_string>')
#def extract_minutes(date_string):
 #       date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
  #      minutes = date_object.minute
   #     return jsonify({'minutes': minutes})

  
if __name__ == "__main__":
  app.run(debug=True)
