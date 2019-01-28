from flask import Flask, request
app = Flask(__name__)

@app.route('/coucou')
def dire_coucou():
    return 'Coucou !'

@app.route('/discussion')
@app.route('/discussion/page/<int:num_page>')
def mon_chat(num_page = 1):
    premier_msg = 1 + 50 * (num_page - 1)
    dernier_msg = premier_msg + 50
    return 'affichage des messages {} à {}'.format(premier_msg, dernier_msg)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        # afficher le formulaire
        return 's'
    else:
        return 'd'
        # traiter les données reçues
        # afficher : "Merci de m'avoir laissé un message !"

from PIL import Image
from io import BytesIO
from flask import make_response

@app.route('/image')
def genere_image():
    mon_image = BytesIO()
    Image.new("RGB", (300,300), "#92C41D").save(mon_image, 'BMP')
    reponse = make_response(mon_image.getvalue())
    reponse.mimetype = "image/bmp"  # à la place de "text/html"
    return reponse

from flask import redirect, url_for

@app.route('/profil/<utilisateur>')
def profil(utilisateur):
    if utilisateur:
        return redirect(url_for('afficher_profil', pseudo="Luc1664"))
    return "Vous êtes bien identifié, voici la page demandée : ..."

@app.route('/login/<pseudo>')
def page_de_login(pseudo):
    return 'jj'

if __name__ == '__main__':
    app.run(debug=True)
