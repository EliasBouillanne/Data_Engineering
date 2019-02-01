from flask import Flask, request, render_template
from . import config
from . import database

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object(config)

@app.route('/')
def accueil():
    substance = [{'_id': '5c52f95c9ca7eede97332113',
 'fiche': "Pharmacologiquement, le citrate de clomifène présente les caractéristiques d'un composé antiestrogénique. Le citrate de clomifène se fixe sur les récepteurs estrogéniques hypothalamiques, supprimant ainsi l'effet freinateur des estrogènes et aboutissant à une stimulation des sécrétions hypophysaires de FSH\xa0et de\xa0LH.",
 'indication': 'Le clomifène est utilisé dans la prise en charge de\xa0:      inductions de l’ovulation,     hypofertilités,     tests au clomifène.',
 'lien_substance': 'https://www.vidal.fr/substances/6745/clomifene/',
 'liste_medicament': [{'Lien_Medicament': 'https://www.vidal.fr/Medicament/clomid_50_mg_cp-4095.htm',
   'Nom_Medicament': 'CLOMID 50 mg cp'},
  {'Lien_Medicament': 'https://www.vidal.fr/Medicament/pergotime_50_mg_cp_sec-12986.htm',
   'Nom_Medicament': 'PERGOTIME 50 mg cp séc'}],
 'nom_substance': 'clomifène'}]
    data = [{'_id': '5c541d059ca7eede97343e1a',
 'descriptif': {'agréé_aux_collectivités': 'oui',
  'cip': '34009300532253400930053263',
  'commercialisé': 'oui',
  'liste': 'liste 1',
  'modalités_de_conservation': "avant ouverture : durant 30 mois (conserver à l'abri de la lumière, conserver dans son emballage).",
  'modèle_hospitalier': 'non',
  'remboursement': '65%'},
 'excipient': ['povidone K 30',
  'crospovidone',
  'cellulose poudre',
  'copovidone',
  'silice colloïdale anhydre',
  'magnésium stéarate',
  'titane dioxyde',
  'alcool polyvinylique',
  'macrogol',
  'talc',
  'lactose monohydrate'],
 'lien_medicament': 'https://www.vidal.fr/Medicament/rosuvastatine_eg_10_mg_cp_pellic-173632.htm',
 'nom_medicament': 'ROSUVASTATINE EG 10 mg cp pellic',
 'substance': ['Rosuvastatine calcique']}]
    return render_template('real-app.html', substance = substance, data = data)


@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        return "Vous avez envoyé un message..."
    return '<form action="" method="post"><input type="text" name="msg" /><input type="submit" value="Envoyer" /></form>'

if __name__ == "__main__":
    app.run()
