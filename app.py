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


@app.route('/topics/<id>', methods=['PUT'])
# Diese Route wird aufgerufen, wenn ein PUT-Request an /topics/<id> gesendet wird
def update_topic(id):
    updated_data = request.json
    # Liest die Daten aus der Anfrage
    
    # Überprüft, ob die erforderlichen Felder 'name' und 'description' im Request-Body vorhanden sind
    # Wenn die erforderlichen Felder fehlen, gibt es eine Fehlermeldung zurück
    # Die Felder 'name' und 'description' sind erforderlich
    if not updated_data or 'name' not in updated_data or 'description' not in updated_data:
        return jsonify({'error': "Name und Beschreibung für das Topic sind erforderlich."}), 400
    
    topics = data_manager.read_data(TOPICS_FILE)
    # Liest die Inhalte der Datei topics.json
    
    found_index = -1
    # Initialisiert den Index des gefundenen Themas auf -1 (nicht gefunden)
    for index, topic in enumerate(topics):
        if topic.get('id').lower() == id.lower():
            found_index = index
            break
        
    if found_index == -1: 
        # Wenn das Thema nicht gefunden wurde, gibt es eine 404-Fehlermeldung zurück
        return jsonify({"error": "Topic not found"}), 404
    # Aktualisiert das gefundene Thema mit den neuen Daten
    topics[found_index]['name'] = updated_data.get('name') # Aktualisiert den Namen des Themas
    topics[found_index]['description'] = updated_data.get('description', '') # Standardwert für Beschreibung ist ein leerer String
    # Schreibt die aktualisierten Themen zurück in die Datei
    data_manager.write_data(TOPICS_FILE, topics) # Gibt das aktualisierte Thema als JSON-Antwort zurück
    return jsonify(topics[found_index]), 200


@app.route('/skills/<id>', methods=['PUT'])
# Diese Route wird aufgerufen, wenn ein PUT-Request an /skills/<id> gesendet wird
def update_skill(id):
    update_data = request.json
    # Liest die Daten aus der Anfrage
    # Überprüft, ob die erforderlichen Felder 'name' und 'topicId' im Request-Body vorhanden sind
    if not update_data or 'name' not in update_data or 'topicId' not in update_data:
        return jsonify({'error': "Name und Topic ID für den Skill sind erforderlich"}), 400
    
    skills = data_manager.read_data(SKILLS_FILE)
    # Liest die Inhalte der Datei skills.json
    found_index = -1
    # Initialisiert den Index des gefundenen Skills auf -1 (nicht gefunden)
    for index, skill in enumerate(skills):
        if skill.get('id').lower() == id.lower():
            found_index = index
            break
    
    if found_index == -1:
        # Wenn der Skill nicht gefunden wurde, gibt es eine 404-Fehlermeldung zurück
        return jsonify({"error": "Skill not found"}), 404
    
    # Aktualisiert den gefundenen Skill mit den neuen Daten
    skills[found_index]['name'] = update_data.get('name')
    skills[found_index]['topicId'] = update_data.get('topicId')
    skills[found_index]['difficulty'] = update_data.get('difficulty', 'unknown')
    # Standardwert für Schwierigkeit ist 'unknown'
    # Schreibt die aktualisierten Skills zurück in die Datei
    data_manager.write_data(SKILLS_FILE, skills)
    # Gibt den aktualisierten Skill als JSON-Antwort zurück
    return jsonify(skills[found_index]), 200


@app.route('/topics/<id>', methods=['DELETE'])
# Diese Route wird aufgerufen, wenn ein DELETE-Request an /topics/<id> gesendet wird
# Löscht ein Thema mit der angegebenen ID
def delte_topic(id):
    topics = data_manager.read_data(TOPICS_FILE)
    # Liest die Inhalte der Datei topics.json

    found_index = -1
    # Initialisiert den Index des gefundenen Themas auf -1 (nicht gefunden)
    for index, topic in enumerate(topics):
        if topic.get('id').lower() == id.lower():
            found_index = index
            break
        
    if found_index == -1:
        # Wenn das Thema nicht gefunden wurde, gibt es eine 404-Fehlermeldung zurück
        return jsonify({"error": "Topic not found"}), 404
    # Entfernt das gefundene Thema aus der Liste
    deleted_topic = topics.pop(found_index)
    # Schreibt die aktualisierten Themen zurück in die Datei
    data_manager.write_data(TOPICS_FILE, topics)
    # Gibt das gelöschte Thema als JSON-Antwort zurück
    return '', 204  # 204 No Content, da das Thema erfolgreich gelöscht wurde


@app.route('/skills/<id>', methods=['DELETE'])
# Diese Route wird aufgerufen, wenn ein DELETE-Request an /skills/<id> gesendet wird
def delete_skill(id):
    skills = data_manager.read_data(SKILLS_FILE)
    # Liest die Inhalte der Datei skills.json

    found_index = -1
    # Initialisiert den Index des gefundenen Skills auf -1 (nicht gefunden)
    for index, skill in enumerate(skills):
        if skill.get('id').lower() == id.lower():
            found_index = index
            break
    
    if found_index == -1:
        # Wenn der Skill nicht gefunden wurde, gibt es eine 404-Fehlermeldung zurück
        return jsonify({"error": "Skill not found"}), 404
    
    # Entfernt den gefundenen Skill aus der Liste
    deleted_skill = skills.pop(found_index)
    # Schreibt die aktualisierten Skills zurück in die Datei
    data_manager.write_data(SKILLS_FILE, skills)
    # Gibt das gelöschte Thema als JSON-Antwort zurück
    return '', 204


# Dieser Block wird nur ausgeführt, wenn das Skript direkt gestartet wird
if __name__ == '__main__':
    # Startet die Flask-Anwendung im Debug-Modus auf Port 5000
    # Dies ermöglicht eine einfachere Fehlersuche und automatisches Neuladen bei Änderungen
    app.run(debug=True, port=5000)
    