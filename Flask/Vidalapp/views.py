from flask import Flask, request, render_template
from . import config
from . import database

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object(config)

@app.route('/')
def home():
    mongo = database.MongoDB()
    collection_medicaments = mongo.db['medicament_items']
    medicaments = collection_medicaments.find()
    return (
        str(medicaments[0]), '/n'
    )

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        return "Vous avez envoyé un message..."
    return '<form action="" method="post"><input type="text" name="msg" /><input type="submit" value="Envoyer" /></form>'

if __name__ == "__main__":
    app.run()
