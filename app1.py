from flask import Flask, render_template, request, Response
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import mpld3

app = Flask(__name__)

df=pd.read_csv("https://raw.githubusercontent.com/wtitze/3E/main/2010.csv", delimiter=';')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/nome')
def nome():
    return render_template('filmInserito.html')

@app.route('/genre')
def genre():
    return render_template('genereNome.html')

@app.route('/tendina')
def tendina():
    generi = df['Genres'].unique()
    #generi = df.drop_duplicates(subset=['Genres'])
    return render_template('genereTendina.html', list= list(generi))

@app.route('/radio')
def radio():
    generi = df['Genres'].unique()
    #generi = df.drop_duplicates(subset=['Genres'])
    return render_template('Radio.html', list= list(generi))

@app.route('/check')
def check():
    generi = df['Genres'].unique()
    #generi = df.drop_duplicates(subset=['Genres'])
    return render_template('Check.html', list= list(generi))

@app.route('/nan')
def nan():
    df1=df[df["Budget"].isnull()]
    df2=df1.to_html()
    #generi = df.drop_duplicates(subset=['Genres'])
    return render_template('NAN.html', list= df2)

@app.route('/graf')
def graf():
    fig, ax= plt.subplots(figsize = (12,8))
    df.groupby("Genres")["Title"].count().sort_values(ascending=False).reset_index ().plot(kind="bar", ax=ax)
    graph = mpld3.fig_to_html(fig)#modo diverso dal solito
    return render_template('grafico.html',graf=graph)

@app.route("/immagine")
def immagine():
    fig, ax= plt.subplots(figsize = (12,8))
    df.groupby("Genres")["Title"].count().sort_values(ascending=False).reset_index ().plot(kind="bar", ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)#metodo tradizionale usato in classe
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/search_nome', methods = ['GET'])
def search():
    film=request.args["nome"]
    mostro=df[df["Title"].str.strip().str.capitalize()==film.strip().capitalize()]
    if mostro.empty:
        return render_template('errore.html') 
    else:
        dfhtm=mostro.to_html()
        return render_template('risultato.html', tabella = dfhtm)

@app.route('/search_genere', methods = ['GET'])
def search_genere():
    film=request.args["genere"]
    genere=df[df["Genres"].str.lower().str.contains(film.strip().lower())]
    dfhtm=genere.to_html()
    return render_template('risultato.html', tabella = dfhtm)

@app.route('/search_tendina', methods = ['GET'])
def search_tendina():
    film=request.args["genere"]
    genere=df[df["Genres"].str.lower().str.contains(film.strip().lower())]
    dfhtm=genere.to_html()
    return render_template('risultato.html', tabella = dfhtm)

@app.route('/search_Radio', methods = ['GET'])
def search_radio():
    film=request.args["genere"]
    genere=df[df["Genres"].str.lower().str.contains(film.strip().lower())]
    dfhtm=genere.to_html()
    return render_template('risultato.html', tabella = dfhtm)

@app.route('/search_check', methods = ['GET'])
def search_check():
    film=request.args.getlist("genere")
    genre=pd.DataFrame()
    for i in film:
        risultato=df[df.Genres.str.contains(i)]
        genre=pd.concat([genre, risultato])
    
    dfhtm=genre.to_html()
    return render_template('risultato.html', tabella = dfhtm)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)