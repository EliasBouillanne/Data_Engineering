<span class="c20 c22">Know what your drugs are made of.</span>

* * *

<span class="c8"></span>

<span class="c1"></span>

<span class="c1">Ce projet a été réalisé dans le cadre de l’unité DSIA-4203C qui s’intègre dans le cursus de la filière Datascience et Intelligence Artificielle.</span>

<span class="c5">Le but est de scraper des données depuis un site choisi puis de les restituer dans une web application. Le site choisi dans ce projet est :</span> <span class="c3">[https://www.vidal.fr](https://www.google.com/url?q=https://www.vidal.fr&sa=D&ust=1549232120554000)</span>

<span class="c1"></span>

<span class="c22 c20"></span>

<span class="c20">How to run the app ?</span>

* * *

<span class="c1"></span>

<span class="c5 c10 c25"></span>

<span class="c11 c5 c10">Etape 1</span> <span class="c4">: Récupérer les scripts depuis github</span>

<span class="c4"></span>

<span class="c5">Cloner le projet grâce à :</span>

<span class="c1"></span>

<span class="c23">$ git clone https://github.com/YayaBou/Data_Engineering.git</span>

<span class="c1"></span>

<span class="c5 c10 c11">Etape 2</span> <span class="c4">: Récupérer la base de données</span>

<span class="c4"></span>

<span class="c1">Se rendre à l’endroit où MongoDB est installé. Par exemple :</span>

<span class="c0"></span>

<span class="c17">cd C:\Program Files\MongoDB\Server\4.0\bin</span>

<span class="c4"></span>

<span class="c1">Exécuter les commandes suivantes :</span>

<span class="c0"></span>

<span class="c26">mongorestore -d [your_db_name] [your_dump_dir]</span>

<span class="c1">Ici, la base de données est “Vidal” et le chemin d’accès est de la forme : C:\Users\Documents\Data_Engineering\Vidal</span>

<span class="c5">(la base de données se trouve dans le sous-dossier</span> <span class="c5 c10">Vidal</span><span class="c5">du dossier principal</span> <span class="c5 c10">Data_Engineering</span><span class="c1">.</span>

<span class="c0"></span>

<span class="c11 c5 c10">Etape 3</span> <span class="c4">: Ouvrir elasticsearch</span>

<span class="c0"></span>

<span class="c5">Se rendre à l’emplacement où Elasticsearch a été installé. Dans le dossier .bin, ouvrir le fichier</span> <span class="c5 c10">elasticsearch.bat</span><span class="c1">. Un terminal s’ouvre, le laisser tourner en arrière plan et ne pas le fermer.</span>

<span class="c0"></span>

<span class="c11 c5 c10">Etape 4</span> <span class="c4">: Exécution du programme principal</span>

<span class="c4"></span>

<span class="c5">Exécuter le script</span> <span class="c5 c10">run.py</span><span class="c5"> qui se trouve dans le dossier</span><span class="c5 c10">Flask</span> <span class="c1">:</span>

<span class="c1"></span>

<span class="c17">python run.py</span>

<span class="c7">User Guide</span>

* * *

<span class="c7"></span>

<span class="c1"></span>

<span class="c5">Lorsque l’on se rend à l’adresse indiquée, nous arrivons sur l’unique page de notre application web. En dessous de l’introduction se trouve deux exemples types de pages de page que l’on a scrappé depuis le site officiel du Vidal.</span> <span class="c5 c10">Abacavir</span> <span class="c5">est un exemple de substance,</span> <span class="c5 c10">Bactox</span> <span class="c5">est un exemple de médicaments contenant la substance</span> <span class="c5 c10">Amoxicilline</span><span class="c1">.</span>

<span class="c8"></span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px -0.00px; border: 1.33px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 602.00px; height: 338.67px;">![](images/image1.png)</span>

<span class="c1"></span>

<span class="c5">Vous pouvez ensuite faire vous-même vos recherche dans le carré gris en haut à droite. Entrez par exemple une substance bien connue, le</span> <span class="c5 c10">Paracétamol</span><span class="c1">. Une description de la substance s’affichera, ainsi que la liste des médicaments contenant cette dernière.</span>

<span class="c5">Vous pouvez ensuite affiner votre recherche en supprimant par exemple les médicaments contenant du</span> <span class="c5 c10">sodium benzoate</span><span class="c1"> parmi les excipients.</span>

<span class="c1"></span>

<span class="c1"></span>

<span class="c7">Reference Guide</span>

* * *

<span class="c7"></span>

<span class="c7"></span>

<span class="c5">L’application</span> <span class="c5 c10">Know what your drugs are made of</span> <span class="c1">a été réalisé grâce à :</span>

<span class="c1"></span>

*   <span class="c9">Scrapy,</span> <span class="c1">permet de récupérer les données depuis le site web.</span>
*   <span class="c9">MongoDB,</span> <span class="c1">permet de stocker les données dans une database grâce au NoSQL.</span>
*   <span class="c9">Elasticsearch,</span> <span class="c1">outils de recherche rapide dans la database.</span>
*   <span class="c9">Flask,</span> <span class="c1">framework de développement web en Python.</span>

<span class="c1"></span>

<span class="c1">Pour toute question relative à la réalisation ou à l’exécution du projet, ne pas hésiter à contacter :</span>

<span class="c1"></span>

<span class="c9 c14">[elias.bouillanne@edu.esiee.fr](mailto:elias.bouillanne@edu.esiee.fr)</span>

<span class="c14 c9">[marine.dussaussois@edu.esiee.fr](mailto:marine.dussaussois@edu.esiee.fr)</span>

<span class="c15 c9"></span>

<span class="c8"></span>