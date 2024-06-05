from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3

                                                                                                                                       
app = Flask(__name__)
# ======================= Créer une route pour les contacts ===================================
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
  
# ======================= Créer une route pour le Graphique ===================================
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
  
# ======================= Créer une route pour l'histogramme ===================================
@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")
  
# ======================= Créer une route pour les Commits =====================================
@app.route('/metriques/')
def ali_commit():
    response = urlopen('https://api.github.com/repos/Alilou-75/5MCSI_Metriques/commits')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for commit in commits:
        commit_time = commit['commit']['author']['date']
        commit_minute = datetime.strptime(commit_time, '%Y-%m-%dT%H:%M:%SZ').strftime('%H:%M')
        if commit_minute in commits_per_minute:
            commits_per_minute[commit_minute] += 1
        else:
            commits_per_minute[commit_minute] = 1

    sorted_commits = sorted(commits_per_minute.items())

    return [{'time': time, 'count': count} for time, count in sorted_commits]






# Remplacez par votre token GitHub si nécessaire
GITHUB_TOKEN = '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'
GITHUB_API_URL = 'https://api.github.com'

@app.route("/mes_commits/")
def get_commits_data():
    headers = {
        'Authorization': f'token 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 '
    }
    commits_url = f'https://api.github.com/repos/Alilou-75/5MCSI_Metriques/commits'
    now = datetime.utcnow()
    timedelta = 1
    since = now - timedelta(hours=1)  # Récupère les commits de la dernière heure

    params = {
        'since': since.isoformat() + 'Z',
        'per_page': 100
    }

    response = requests.get(commits_url, headers=headers, params=params)
    response.raise_for_status()
    commits = response.json()

    commits_per_minute = {}

    for commit in commits:
        commit_time = commit['commit']['author']['date']
        commit_minute = datetime.strptime(commit_time, '%Y-%m-%dT%H:%M:%SZ').strftime('%H:%M')
        if commit_minute in commits_per_minute:
            commits_per_minute[commit_minute] += 1
        else:
            commits_per_minute[commit_minute] = 1

    sorted_commits = sorted(commits_per_minute.items())

    return [{'time': time, 'count': count} for time, count in sorted_commits]

@app.route("/commits/")
def mescommits():
    return render_template("commits.html")

@app.route('/data')
def data():
    owner = 'Alilou-75'  # Remplacez par le propriétaire du repo
    repo = '5MCSI_Metriques'   # Remplacez par le nom du repo
    commits = get_commits_data(owner, repo)
    return jsonify(commits)

if __name__ == '__main__':
    app.run(debug=True)




@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})

  
if __name__ == "__main__":
  app.run(debug=True)
