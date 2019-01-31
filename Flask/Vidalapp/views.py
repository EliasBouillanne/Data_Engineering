from flask import Flask, request, render_template
from . import config

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object(config)

@app.route('/')
def accueil():
    mots = ["bonjour", "à", "toi,", "visiteur."]
    return render_template('accueil.html', titre="Bienvenue !", mots=mots)

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        return "Vous avez envoyé un message..."
    return '<form action="" method="post"><input type="text" name="msg" /><input type="submit" value="Envoyer" /></form>'

if __name__ == "__main__":
    app.run()
