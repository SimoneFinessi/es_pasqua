from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

df=pd.read_csv("https://raw.githubusercontent.com/wtitze/3E/main/2010.csv", delimiter=';')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/nome')
def nome():
    return render_template('filmInserito.html')

@app.route('/search_nome', methods = ['GET'])
def search():
    film=request.args["nome"]
    mostro=df[df["Title"].str.lower()==film.lower()]
    dfhtm=mostro.to_html()
    return render_template('risultato.html', tabella = dfhtm)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)