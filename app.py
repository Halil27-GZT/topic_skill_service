import os   # Modul os importieren, um mit Dateipfaden zu arbeiten  
from flask import Flask, jsonify, request
import uuid # Vom Flask und jsonify importieren, um eine Webanwendung zu erstellen
from data_manager import JsonDataManager  # Importiert die JsonDataManager-Klasse aus der Datei data_manager.py

app = Flask(__name__)   # Erstellt eine Flask-Anwendung
data_manager = JsonDataManager()  # Erstellt eine Instanz der JsonDataManager-Klasse

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
# Erstellt einen Pfad zum "data"-Ordner im gleichen Verzeichnis wie diese Datei
TOPICS_FILE = os.path.join(DATA_DIR, 'topics.json')
# Erstellt den vollständigen Pfad zur Datei "topics.json" im data-Ordner
SKILLS_FILE = os.path.join(DATA_DIR, 'skills.json')
# Erstellt den vollständigen Pfad zur Datei "skills.json" im data-Ordner


# Diese Route wird aufgerufen, wenn jemand die Startseite ("/") der Website besucht
@app.route('/')
def hello_world():
     # Gibt eine einfache Textantwort zurück
    return "Hello from Topic and Skill Service!"


@app.route('/topics', methods=['GET'])
# Diese Route wird aufgerufen, wenn ein GET-Request an /topics gesendet wird
def get_topics():
    # Liest die Inhalte der Datei topics.json (z. B. eine Liste von Themen)
    topics = data_manager.read_data(TOPICS_FILE)
    # Gibt die Inhalte als JSON-Antwort zurück
    return jsonify(topics)


@app.route('/skills', methods=['GET'])
# Diese Route wird aufgerufen, wenn ein GET-Request an /skills gesendet wird
def get_skills():
    # Liest die Inhalte der Datei skills.json (z. B. eine Liste von Fähigkeiten)
    skills = data_manager.read_data(SKILLS_FILE)
    # Gibt die Inhalte als JSON-Antwort zurück
    return jsonify(skills)


@app.route('/topics/<id>', methods=['GET'])
# Diese Route wird aufgerufen, wenn ein GET-Request an /topics/<id> gesendet wird
def get_topic_by_id(id):
    # Liest die Inhalte der Datei topics.json
    topics = data_manager.read_data(TOPICS_FILE)
    # Sucht nach dem Thema mit der angegebenen ID
    topic = next((topic for topic in topics if topic.get('id').lower() == id.lower()), None)
    # Gibt das gefundene Thema als JSON-Antwort zurück oder 404, wenn nicht gefunden
    return jsonify(topic) if topic else ('', 404)


@app.route('/skills/<id>', methods=['GET'])
# Diese Route wird aufgerufen, wenn ein GET-Request an /skills/<id> gesendet wird
def get_skill_by_id(id):
    # Liest die Inhalte der Datei skills.json
    skills = data_manager.read_data(SKILLS_FILE)
    # Sucht nach der Fähigkeit mit der angegebenen ID
    skill = next((skill for skill in skills if skill.get('id').lower() == id.lower()), None)
    # Gibt die gefundene Fähigkeit als JSON-Antwort zurück oder 404, wenn nicht gefunden
    return jsonify(skill) if skill else ('', 404)


@app.route('/topics', methods=['POST'])
# Diese Route wird aufgerufen, wenn ein POST-Request an /topics gesendet wird
def create_topic():
    # Liest die Daten aus der Anfrage
    new_topic_data = request.json
    
    if not new_topic_data or 'name' not in new_topic_data or 'description' not in new_topic_data:
        return jsonify({'error': "'name' and 'description' for the topic are required in the request body."}), 400
    
    new_topic_id = str(uuid.uuid4())
    
    topic = {
        'id': new_topic_id,
        'name': new_topic_data.get('name'),
        'description': new_topic_data.get('description', '')
    }
    
    topics = data_manager.read_data(TOPICS_FILE)
    topics.append(topic)
    
    data_manager.write_data(TOPICS_FILE, topics)
    
    return jsonify(topic), 201


@app.route('/skills', methods=['POST'])
# Diese Route wird aufgerufen, wenn ein POST-Request an /skills gesendet wird
def create_skill():
    # Liest die Daten aus der Anfrage
    new_skill_data = request.json
    # Überprüft, ob die erforderlichen Felder 'name' und 'description' im Request-Body vorhanden sind
    
    # Wenn die erforderlichen Felder fehlen, gibt es eine Fehlermeldung zurück
    # Die Felder 'name' und 'description' sind erforderlich
    if not new_skill_data or 'name' not in new_skill_data or 'topicId' not in new_skill_data:
        return jsonify({'error': "Name und Topic ID für den Skill sind erforderlich"}), 400
    
    new_skill_id = str(uuid.uuid4())
    # Generiert eine neue, eindeutige ID für die Fähigkeit
    # Erstellt ein neues Fähigkeitsobjekt mit der generierten ID und den übergebenen Daten
    # Die ID wird als String generiert, um sie in der JSON-Datei zu speichern
    
    skill = {
        'id': new_skill_id,
        'name': new_skill_data.get('name'),
        'topicId': new_skill_data.get('topicId'),
        'difficulty': new_skill_data.get('difficulty', 'unknown'), # Standardwert 'unknown' für Schwierigkeit
    }
    
    skills = data_manager.read_data(SKILLS_FILE)
    skills.append(skill)
    data_manager.write_data(SKILLS_FILE, skills)
    
    return jsonify(skill), 201

# Dieser Block wird nur ausgeführt, wenn das Skript direkt gestartet wird
if __name__ == '__main__':
    # Startet die Flask-Anwendung im Debug-Modus auf Port 5000
    app.run(debug=True, port=5000)
    