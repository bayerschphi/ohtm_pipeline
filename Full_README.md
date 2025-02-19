
# OHTM Pipeline - Version 0.8
(Orahl History Topic Modeling Pipeline)

## Übersicht
Diese Pipeline stellt einen vollständigen Funktionssatz für LDA Mallet-Topic-Modeling bereit. Mit einem einfachen Haupt-Hub können alle Variablen gesteuert und verwendet werden.

Die Pipeline bietet die Möglichkeit, Ergebnisse zu analysieren, Themen nach Gewicht zu durchsuchen, die Themenliste auszugeben oder Ergebnisse mithilfe von Balkendiagrammen oder Heatmaps für den gesamten Korpus oder einzelne Interviews zu visualisieren. Der Korpus und alle Ergebnisse werden in einer speziell strukturierten `ohtm_file` gespeichert.

---

## 1. OHTM-Dateistruktur
Das Hauptteil dieser Pipeline ist die `ohtm_file`. Sie ist ein verschachteltes Wörterbuch mit sechs Hauptebenen:

- `corpus`: Enthält alle Dokumente
- `weight`: Enthält die Wahrscheinlichkeits-Ergebnisse des Topic-Modellings
- `words`: Enthält die Wörterlisten für jedes Thema
- `stopwords`: Liste der entfernten Stopwörter
- `correlation`: Wird später hinzugefügt
- `settings`: Informationen zu allen ausgewählten Optionen

### Korpus-Struktur:
```plaintext
ohtm_file["corpus"]
    - ["archive_1"]
    - ["archive_2"]
    - ["archive_3"]
        - ["interview_1"]
```

### Gewicht-Struktur:
```plaintext
ohtm_file["weight"]
    - ["archive_1"]
        - ["interview_1"]
            - ["0"]
            - ["1"]
```

### Einstellungen-Struktur:
```plaintext
ohtm_file["settings"]
    - ["interviews"]
    - ["preprocessing"]
        - ["preprocessed"]
        - ["chunked"]
```

---

## 2. Funktionen
Mit dieser Pipeline können Sie folgende Optionen und Einstellungen nutzen:

- Dokumente aus `.csv`, `.odt` oder `.txt` importieren
- Vorverarbeitung:
  - Tokenisierung
  - Stopwortentfernung
  - Lemmatization mit Spacy
  - Chunking
- Topic Modeling durchführen
- Ergebnisse speichern und visualisieren (Balkendiagramme, Heatmaps)

---

## 3. Installation
1. Installiere alle benötigten Pakete aus `requirements.txt`.
2. Lade und starte die Pipeline über `main_template.py`.
3. Installiere Mallet (Version 20.0.2 oder höher).

---

## 4. Dateiformate
### `.csv` Struktur
| Tape | Timecode | Speaker | Sentences |

### `.ods` Struktur
| Timecode | Speaker | Sentences |

### `.txt` Struktur
Jeder Sprecher sollte mit `*speaker*` gekennzeichnet werden.

---

## 5. Nutzung
Beispielkonfigurationen:
```python
os.environ["MALLET_HOME"] = r'C:\mallet-2.0.8'
mallet_path = r'C:\mallet-2.0.8in\mallet'
source = ["folder_1", "folder_2"]
```

### Optionen
- `create_ohtm_file = True`: Erstellen eines neuen `ohtm_file`
- `use_preprocessing = True`: Startet die Vorverarbeitung
- `use_topic_modeling = True`: Aktiviert das Topic-Modeling

---

## 6. Visualisierung und Ergebnisanalyse
- `show_bar_graph_corpus = True`: Balkendiagramm für den gesamten Korpus
- `show_heatmap_corpus = True`: Heatmap des gesamten Korpus
- `show_heatmap_interview = True`: Heatmap für ein einzelnes Interview

---

## 7. Inferring neuer Dokumente
- `infer_new_documents = True`: Neue Dokumente mit einem trainierten Modell anreichern
- `save_separate_ohtm_file = True`: Neue Dokumente separat speichern

