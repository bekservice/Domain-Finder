# Domain Finder

Ein Docker-basiertes Tool zur Suche nach verfügbaren .de Domains.

## Funktionen

- Live-Prüfung von 2- und 3-Zeichen-Domains (.de) mit Anzeige des Fortschritts
- Unterstützung von Buchstaben (a-z) und Zahlen (0-9) für 2-Zeichen-Domains
- Optional: Prefix (Vorsilbe) und/oder Suffix (Nachsilbe) für Domains wählbar
- Nur verfügbare Domains werden angezeigt
- Moderne Benutzeroberfläche mit Live-Updates (Server-Sent Events)

## Voraussetzungen

- Docker
- Docker Compose

## Installation und Start

1. Klonen Sie das Repository:
```bash
git clone [repository-url]
cd Domain-Finder
```

2. Starten Sie die Anwendung mit Docker Compose:
```bash
docker-compose up --build
```

3. Öffnen Sie die Anwendung im Browser:
```
http://localhost:5001
```

## Verwendung

1. Optional: Geben Sie einen Prefix (Vorsilbe) und/oder Suffix (Nachsilbe) ein
2. Klicken Sie auf "Alle 2-Zeichen-Domains prüfen" oder "Alle 3-Buchstaben-Domains prüfen"
3. Sie sehen live den Fortschritt und nur verfügbare Domains
4. Mit dem Button "Domain registrieren" können Sie die Domain direkt bei BEK Service prüfen und registrieren

## Technologien

- Python/Flask
- Docker
- Tailwind CSS
- WHOIS-Protokoll
- JavaScript/Fetch API
- Server-Sent Events (SSE)

## Autor

BEK Service GmbH  
https://bekservice.de 