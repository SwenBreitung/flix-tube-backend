## Entwicklungsumgebung starten

Um den RQ-Worker für die Verarbeitung von Hintergrundaufgaben zu starten, führen Sie folgenden Befehl aus:

```bash
python manage.py rqworker --worker-class flix_tube_backend.simpleworker.SimpleWorker default