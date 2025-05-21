from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import subprocess

app = Flask(__name__)
app.secret_key = 'segredo123'  # Requerido para mensagens flash

CSV_FILE = 'ofertas.csv'

def read_csv():
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def write_csv(data):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['produto', 'preco', 'descricao', 'grupo', 'canal'])
        writer.writeheader()
        writer.writerows(data)

@app.route('/')
def index():
    ofertas = read_csv()
    return render_template('index.html', ofertas=ofertas)

@app.route('/add', methods=['POST'])
def add():
    nova = {
        'produto': request.form['produto'],
        'preco': request.form['preco'],
        'descricao': request.form['descricao'],
        'grupo': request.form['grupo'],
        'canal': request.form['canal']
    }
    data = read_csv()
    data.append(nova)
    write_csv(data)
    return redirect(url_for('index'))

@app.route('/delete/<int:index>')
def delete(index):
    data = read_csv()
    data.pop(index)
    write_csv(data)
    return redirect(url_for('index'))

@app.route('/update/<int:index>', methods=['POST'])
def update(index):
    data = read_csv()
    data[index] = {
        'produto': request.form['produto'],
        'preco': request.form['preco'],
        'descricao': request.form['descricao'],
        'grupo': request.form['grupo'],
        'canal': request.form['canal']
    }
    write_csv(data)
    return redirect(url_for('index'))

@app.route('/disparar/<canal>')
def disparar(canal):
    if canal in ['telegram', 'whatsapp', 'ambos']:
        subprocess.Popen(['python', 'main.py', canal])
        flash(f'Disparo iniciado com sucesso para: {canal.capitalize()}', 'success')
    else:
        flash('Canal inválido.', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
