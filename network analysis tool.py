import socket
import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime
from queue import Queue
import threading

# --- Die Scan-Logik (leicht angepasst für die GUI) ---

class PortScannerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Netzwerk-Analyse-Tool")
        master.geometry("500x400")

        self.print_lock = threading.Lock()
        self.found_ports_count = 0

        # --- GUI Elemente erstellen ---
        self.label = tk.Label(master, text="Ziel-IP-Adresse oder Hostname:")
        self.label.pack(pady=5)

        self.ip_entry = tk.Entry(master, width=50)
        self.ip_entry.pack(pady=5)
        self.ip_entry.insert(0, "127.0.0.1") # Standardwert

        self.scan_button = tk.Button(master, text="Scan starten", command=self.start_scan_thread)
        self.scan_button.pack(pady=10)

        self.results_text = scrolledtext.ScrolledText(master, width=60, height=15)
        self.results_text.pack(pady=10)

        self.status_label = tk.Label(master, text="Bereit.")
        self.status_label.pack(pady=5)

    def log(self, message):
        """Schreibt eine Nachricht in das Ergebnis-Textfeld."""
        self.results_text.insert(tk.END, message + "\n")
        self.results_text.see(tk.END) # Auto-scroll

    def set_status(self, message):
        """Aktualisiert die Statusleiste."""
        self.status_label.config(text=message)

    def start_scan_thread(self):
        """Startet den Scan in einem separaten Thread, um die GUI nicht zu blockieren."""
        self.scan_button.config(state=tk.DISABLED)
        self.results_text.delete(1.0, tk.END) # Alte Ergebnisse löschen
        self.found_ports_count = 0
        
        scan_thread = threading.Thread(target=self.run_scan)
        scan_thread.daemon = True
        scan_thread.start()

    def run_scan(self):
        """Die Haupt-Scan-Funktion, die im Thread läuft."""
        try:
            target_ip_input = self.ip_entry.get()
            target_ip = socket.gethostbyname(target_ip_input)
        except (socket.gaierror, socket.error):
            messagebox.showerror("Fehler", "Ungültiger Hostname oder IP-Adresse.")
            self.set_status("Fehler.")
            self.scan_button.config(state=tk.NORMAL)
            return

        self.set_status(f"Scanne Host: {target_ip}...")
        self.log("-" * 50)
        self.log(f"Scan gestartet für: {target_ip}")
        self.log(f"Zeit: {datetime.now()}")
        self.log("-" * 50)

        q = Queue()
        for port in range(1, 1025):
            q.put(port)

        # Threads erstellen und starten
        for _ in range(100):
            thread = threading.Thread(target=self.thread_worker, args=(q, target_ip))
            thread.daemon = True
            thread.start()
        
        q.join() # Warten, bis alle Ports gescannt sind

        # Scan beendet
        self.log("-" * 50)
        if self.found_ports_count == 0:
            self.log("Scan beendet. Keine offenen Ports gefunden.")
        else:
            self.log(f"Scan beendet. {self.found_ports_count} offene(r) Port(s) gefunden.")
        
        self.set_status("Fertig.")
        self.scan_button.config(state=tk.NORMAL)

    def thread_worker(self, q, target_ip):
        """Nimmt einen Port aus der Queue und scannt ihn."""
        while not q.empty():
            port = q.get()
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                if sock.connect_ex((target_ip, port)) == 0:
                    with self.print_lock:
                        self.log(f"Port {port}: Offen")
                        self.found_ports_count += 1
                sock.close()
            except socket.error:
                pass
            finally:
                q.task_done()

# --- Hauptprogramm ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PortScannerGUI(root)
    root.mainloop()
