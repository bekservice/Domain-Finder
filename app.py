from flask import Flask, render_template, request, Response, jsonify
import itertools
import socket
import string
import time

app = Flask(__name__)

# Hilfsfunktion: Generiere alle 2- oder 3-Buchstaben-Kombinationen (keine Wiederholung)
def generate_all_domains(length, prefix='', suffix=''):
    if length == 1:
        alphabet = list(string.ascii_lowercase) + list(string.digits)
        if prefix and not suffix:
            # Prefix + 1 Zeichen
            return [f"{prefix}{c}.de" for c in alphabet]
        elif suffix and not prefix:
            # 1 Zeichen + Suffix
            return [f"{c}{suffix}.de" for c in alphabet]
        elif prefix and suffix:
            # Prefix + 1 Zeichen + Suffix
            return [f"{prefix}{c}{suffix}.de" for c in alphabet]
        else:
            # Ohne Prefix/Suffix keine 1-Zeichen-Domains
            return []
    if length == 2:
        alphabet = list(string.ascii_lowercase) + list(string.digits)
        if prefix and not suffix:
            # Prefix + 2 Zeichen
            combinations = itertools.product(alphabet, repeat=2)
            return [f"{prefix}{''.join(combo)}.de" for combo in combinations]
        elif suffix and not prefix:
            # 2 Zeichen + Suffix
            combinations = itertools.product(alphabet, repeat=2)
            return [f"{''.join(combo)}{suffix}.de" for combo in combinations]
        elif prefix and suffix:
            # Prefix + 2 Zeichen + Suffix (insgesamt länger als 2, daher keine Domains)
            return []
        else:
            # Nur 2 Zeichen
            combinations = itertools.product(alphabet, repeat=2)
            return [f"{''.join(combo)}.de" for combo in combinations]
    else:
        alphabet = list(string.ascii_lowercase)
        core_length = length
        if prefix:
            core_length -= len(prefix)
        if suffix:
            core_length -= len(suffix)
        if core_length <= 0:
            # Prefix+Suffix ist zu lang, keine Domains möglich
            return []
        combinations = itertools.product(alphabet, repeat=core_length)
        return [f"{prefix}{''.join(combo)}{suffix}.de" for combo in combinations]

def check_domain_availability(domain):
    try:
        # Erste Prüfung über WHOIS
        whois_server = "whois.denic.de"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((whois_server, 43))
        sock.send((domain + "\r\n").encode())
        response = sock.recv(4096).decode()
        sock.close()
        
        # Wenn "Status: free" in der Antwort steht, ist die Domain verfügbar
        return "Status: free" in response
    except:
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
    length = int(request.args.get('length', 2))
    prefix = request.args.get('prefix', '').lower()
    suffix = request.args.get('suffix', '').lower()
    all_domains = generate_all_domains(length, prefix, suffix)
    def event_stream():
        for domain in all_domains:
            available = check_domain_availability(domain)
            if available:
                yield f"data: {{\"domain\": \"{domain}\", \"available\": true}}\n\n"
            else:
                yield f"data: {{\"domain\": \"{domain}\", \"available\": false}}\n\n"
            time.sleep(0.1)  # kleine Pause, um Server zu schonen
    return Response(event_stream(), mimetype="text/event-stream")

@app.route('/checkdomain')
def checkdomain():
    name = request.args.get('name', '').lower()
    if not name or not all(c in string.ascii_lowercase + string.digits + '-' for c in name):
        return jsonify({'error': 'Ungültiger Domainname'}), 400
    domain = f"{name}.de"
    available = check_domain_availability(domain)
    return jsonify({'domain': domain, 'available': available})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) 