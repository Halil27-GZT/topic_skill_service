import json
import os

class JsonDataManager:
    
    
    def __init__(self):
        pass
    
    
    def read_data(self, filepath):
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
    
    
    def write_data(self, filepath, data):
        with open(filepath, 'w', encoding='utf-8') as file:
            
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            # Erstellt das Verzeichnis, falls es nicht existiert
            try:
                # Versucht, die Daten als JSON in die Datei zu schreiben
                json.dump(data, file, indent=4)
                return True
            except Exception as e:
                print(f"Ein Fehler ist aufgetreten beim Schreiben in {filepath}: {e}")
                return False
                

        
        