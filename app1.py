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
#es1
@app.route('/nome')
def nome():
    return render_template('filmInserito.html')
#es2
@app.route('/genre')
def genre():
    return render_template('genereNome.html')
#es3
@app.route('/tendina')
def tendina():
    generi =list(set(df[~df['Genres'].str.contains('\|')]['Genres']))
    #generi = df.drop_duplicates(subset=['Genres'])
    return render_template('genereTendina.html', list= list(generi))
#es4
@app.route('/radio')
def radio():
    generi =list(set(df[~df['Genres'].str.contains('\|')]['Genres']))
    #generi = df.drop_duplicates(subset=['Genres'])
    return render_template('Radio.html', list= list(generi))
#es5
@app.route('/check')
def check():
    generi =list(set(df[~df['Genres'].str.contains('\|')]['Genres']))
    #generi = df.drop_duplicates(subset=['Genres'])
    return render_template('Check.html', list= list(generi))
#es6
@app.route('/nan')
def nan():
    df1=df[df["Budget"].isnull()]
    df2=df1.to_html()
    #generi = df.drop_duplicates(subset=['Genres'])
    return render_template('NAN.html', list= df2)
#es7 variante 1
@app.route('/graf')
def graf():
    dfgraf=df.groupby("Language").count()[["Title"]].sort_values(by="Title",ascending=False).reset_index()
    fig, ax= plt.subplots(figsize = (12,8))
    ax.bar(dfgraf["Language"],dfgraf["Title"])
    graph = mpld3.fig_to_html(fig)#modo diverso dal solito
    return render_template('grafico.html',graf=graph)

#es7 variante 2
@app.route("/immagine")
def immagine():
    dfgraf=df.groupby("Language").count()[["Title"]].sort_values(by="Title",ascending=False).reset_index()
    fig, ax= plt.subplots(figsize = (20,8))
    ax.bar(dfgraf["Language"],dfgraf["Title"])
    plt.xticks(rotation=90)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)#metodo tradizionale usato in classe
    return Response(output.getvalue(), mimetype='image/png')
#es1
@app.route('/search_nome', methods = ['GET'])
def search():
    film=request.args["nome"]
    mostro=df[df["Title"].str.strip().str.capitalize()==film.strip().capitalize()]
    if mostro.empty:
        return render_template('errore.html') 
    else:
        dfhtm=mostro.to_html()
        return render_template('risultato.html', tabella = dfhtm)
#es2
@app.route('/search_genere', methods = ['GET'])
def search_genere():
    film=request.args["genere"]
    genere=df[df["Genres"].str.lower().str.contains(film.strip().lower())]
    dfhtm=genere.to_html()
    return render_template('risultato.html', tabella = dfhtm)
#es3
@app.route('/search_tendina', methods = ['GET'])
def search_tendina():
    film=request.args["genere"]
    genere=df[df["Genres"].str.lower().str.contains(film.strip().lower())]
    dfhtm=genere.to_html()
    return render_template('risultato.html', tabella = dfhtm)
#es4
@app.route('/search_Radio', methods = ['GET'])
def search_radio():
    film=request.args["genere"]
    genere=df[df["Genres"].str.lower().str.contains(film.strip().lower())]
    dfhtm=genere.to_html()
    return render_template('risultato.html', tabella = dfhtm)
#es5
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