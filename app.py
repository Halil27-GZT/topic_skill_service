import json     # Modul Json importieren
import os   # Modul os importieren, um mit Dateipfaden zu arbeiten  
from flask import Flask, jsonify    # Vom Flask und jsonify importieren, um eine Webanwendung zu erstellen


app = Flask(__name__)   # Erstellt eine Flask-Anwendung

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
# Erstellt einen Pfad zum "data"-Ordner im gleichen Verzeichnis wie diese Datei
TOPICS_FILE = os.path.join(DATA_DIR, 'topics.json')
# Erstellt den vollständigen Pfad zur Datei "topics.json" im data-Ordner


# Diese Route wird aufgerufen, wenn jemand die Startseite ("/") der Website besucht
@app.route('/')
def hello_world():
     # Gibt eine einfache Textantwort zurück
    return "Hello from Topic and Skill Service!"


def read_json_file(filepath):
    # Wenn die Datei nicht existiert, gib eine leere Liste zurück
    if not os.path.exists(filepath):
        return []
    try:
        # Öffnet die Datei im Lese-Modus mit UTF-8-Kodierung
        with open(filepath, 'r', encoding='utf-8') as file:
            # Versucht, den Inhalt der Datei als JSON zu laden und zurückzugeben
            return json.load(file)
    # Wenn die JSON-Datei fehlerhaft ist (z. B. falsche Syntax)
    except json.JSONDecodeError:
        print(f"Fehler beim Dekodieren der JSON-Datei: {filepath}. Bitte JSON-Syntax überprüfen!")
        return []
     # Allgemeiner Fehlerfall – z. B. Zugriffsfehler oder unerwartete Probleme
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten beim Lesen von {filepath}: {e}")
        return []

@app.route('/topics', methods=['GET'])
# Diese Route wird aufgerufen, wenn ein GET-Request an /topics gesendet wird
def get_topics():
    # Liest die Inhalte der Datei topics.json (z. B. eine Liste von Themen)
    topics = read_json_file(TOPICS_FILE)
    # Gibt die Inhalte als JSON-Antwort zurück
    return jsonify(topics)

# Dieser Block wird nur ausgeführt, wenn das Skript direkt gestartet wird
if __name__ == '__main__':
    # Startet die Flask-Anwendung im Debug-Modus auf Port 5000
    app.run(debug=True, port=5000)
    