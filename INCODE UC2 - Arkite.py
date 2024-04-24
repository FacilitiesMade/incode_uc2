from flask import Flask, request, jsonify
import requests
import urllib3

urllib3.disable_warnings()

app = Flask(__name__)

next_production_cycle = False

# Funzione per fare partire il ciclo produttivo sulla macchina
def start_production_cycle():

    # URL e Payload per fare partire il ciclo produttivo sulla macchina
    start_url = 'https://10.250.2.51:7778/api/v1/units/185410950048177/projects/8039084817662898446/load'
    start_payload = {'apikey': 'kADAkavhx', 'apieìkey': 'EfvA6nkOB'}

    # Invio Post ad Arkite
    response = requests.post(start_url, params=start_payload, verify= False)

    if response.status_code == 200 or response.status_code == 204:
        print("Ciclo produttivo avviato con successo")
    else:
        print("Errore durante l'avvio del ciclo produttivo")

# Funzione per fare partire il ciclo produttivo automatico
def start_automatic_cycle():
    
    # URL e Payload per fare partire il ciclo produttivo sulla macchina
    start_url = ''
    start_payload = {'': '', '': ''}

    # Invio Post ad Arkite
    response = requests.post(start_url, params=start_payload, verify= False)

    if response.status_code == 200 or response.status_code == 204:
        print("Ciclo produttivo automatico avviato con successo")
    else:
        print("Errore durante l'avvio del ciclo produttivo")

# Funzione per resettare il programma base di Arkite
def reset_program():
    "funzione per resettare il programma predifinito NON di Incode"

    payload = {'apikey' : 'kADAkavhx', 'apieìkey' : 'EfvA6nkOB'}
    url = 'https://10.250.2.51:7778/api/v1/units/185410950048177/projects/8338512118773050826/load'

    r = requests.post(url, params = payload, verify = False)

@app.route('/')
def homepage():
    return "<p>Incode project</p>"

# Funzione per gestire i post dalla terza parte
@app.route('/third_party_post', methods=['POST'])
def handle_third_party_post():
    global next_production_cycle
    data = request.get_json()
    print("Post third party:", data)

    # A seconda del valore ricevuto si decide quale ciclo fare partire
    if data['automatic'] == 'False':
        next_production_cycle = False
    elif data['automatic'] == 'True':
        next_production_cycle = True

    return jsonify({"message": "Post ricevuto e elaborato"})

# Funzione per gestire i post dalla macchina produttiva
@app.route('/machine_post', methods = ['POST'])
def handle_machine_post():

    global next_production_cycle

    # Per ora, stamperemo semplicemente i dati ricevuti
    data = request.get_json()
    print("Post dalla macchina produttiva:", data)

    if data['EndCycle'] == 'True':
        print('Assemblaggio finito')
        if next_production_cycle:
            start_automatic_cycle()
        else:
            start_production_cycle()
    return jsonify({"message": "Post ricevuto e elaborato"})




if __name__ == "__main__":

    # Invio comando start assemblaggio ad Arkite
    start_production_cycle()
    
    # Avvio app
    app.run(debug = True)


