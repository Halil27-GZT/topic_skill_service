import os   # Modul os importieren, um mit Dateipfaden zu arbeiten  
from flask import Flask, jsonify    # Vom Flask und jsonify importieren, um eine Webanwendung zu erstellen
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

# Dieser Block wird nur ausgeführt, wenn das Skript direkt gestartet wird
if __name__ == '__main__':
    # Startet die Flask-Anwendung im Debug-Modus auf Port 5000
    app.run(debug=True, port=5000)
    