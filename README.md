# network-analysis-tool
# Projekt: Netzwerk-Analyse-Tool mit GUI

Dieses in Python entwickelte Werkzeug dient der Analyse von lokalen Netzwerken durch das Scannen von Ports. Es wurde als Übung konzipiert, um defensive Sicherheitskonzepte zu verstehen und die eigene Netzwerk-Konfiguration zu überprüfen.

**Ziel des Projekts:** Ein performantes und benutzerfreundliches Tool zu schaffen, das Administratoren oder technisch interessierten Nutzern hilft, offene Ports in ihrem eigenen Netzwerk schnell zu identifizieren.

### Kernfunktionen

*   **Multithreaded Scanning:** Nutzt über 100 Threads, um Ports parallel zu scannen, was die Scan-Geschwindigkeit im Vergleich zu einem sequenziellen Ansatz drastisch reduziert (von mehreren Minuten auf wenige Sekunden).
*   **Grafische Benutzeroberfläche (GUI):** Eine mit Tkinter erstellte, intuitive Oberfläche zur Eingabe der Ziel-IP und zur übersichtlichen Anzeige der Ergebnisse.
*   **Hostname-Auflösung:** Kann sowohl mit IP-Adressen (z.B. `192.168.1.1`) als auch mit Hostnamen (z.B. `localhost`) umgehen.

### Ethischer Hinweis

Dieses Tool ist ausschließlich für Bildungszwecke und den Einsatz in eigenen Netzwerken oder mit ausdrücklicher Genehmigung des Netzwerkbetreibers vorgesehen. Das unbefugte Scannen fremder Netzwerke ist illegal.

### Verwendete Technologien
*   Python 3
*   **Bibliotheken:** `socket`, `threading`, `queue`, `tkinter`
