from flask import Flask, render_template, request
import csv
from datetime import datetime
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <h2>Snookie Cookie Bestellung</h2>
    <form method="POST" action="/bestellen">
        Name: <input type="text" name="name"><br>
        Adresse: <input type="text" name="adresse"><br>
        Cookie-Sorte:
        <select name="cookie">
            <option>Chocolate Chip</option>
            <option>Snookie Original</option>
            <option>Matcha Mint</option>
        </select><br>
        Menge: <input type="number" name="menge"><br>
        <input type="submit" value="Bestellen">
    </form>
    '''

@app.route('/bestellen', methods=['POST'])
def bestellen():
    name = request.form['name']
    adresse = request.form['adresse']
    cookie = request.form['cookie']
    menge = request.form['menge']
      # 📅 Datum und Uhrzeit holen
    jetzt = datetime.now()
    datum = jetzt.strftime("%Y-%m-%d")
    uhrzeit = jetzt.strftime("%H:%M:%S")

    # 📄 In CSV-Datei schreiben
    with open('bestellungen.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([datum, uhrzeit, name, adresse, cookie, menge])

         # 📧 E-Mail vorbereiten
    msg = EmailMessage()
    msg['Subject'] = f'Neue Snookie-Bestellung von {name}'
    msg['From'] = 'snookie241224@gmail.com'         # <-- Hier deine E-Mail
    msg['To'] = 'snookie241224@gmail.com'           # <-- Empfänger (du selbst oder jemand anderes)

    msg.set_content(f'''
Neue Bestellung bei Snookie 🍪

Name: {name}
Adresse: {adresse}
Cookie: {cookie}
Menge: {menge}
Datum: {datum}
Uhrzeit: {uhrzeit}
''')

    # 📬 E-Mail senden
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('snookie241224@gmail.com', 'qchxcnewffcrrfvz')  # <-- Hier dein App-Passwort
            smtp.send_message(msg)
    except Exception as e:
        print("Fehler beim Senden der E-Mail:", e)

    return f'''
    <h2>Vielen Dank für deine Bestellung, {name}!</h2>
    <p>Adresse: {adresse}</p>
    <p>Produkt: {cookie}</p>
    <p>Menge: {menge}</p>
    '''

if __name__ == '__main__':
    app.run(debug=True)

