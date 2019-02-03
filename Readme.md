#Know what your drugs are made of.

Ce projet a été réalisé dans le cadre de l’unité DSIA-4203C qui s’intègre dans
le cursus de la filière Datascience et Intelligence Artificielle.

Le but est de scraper des données depuis un site choisi puis de les restituer
dans une web application. Le site choisi dans ce projet est :
<https://www.vidal.fr> . Nous avons ainsi récolter des informations sur plus de
14 000 médicaments et plus de 1700 substances différentes.

##How to run the app ?

*Etape 1 : Récupérer les scripts depuis github*

Cloner le projet grâce à :

\$ git clone https://github.com/YayaBou/Data_Engineering.git

*Etape 2 : Récupérer la base de données*

Se rendre à l’endroit où MongoDB est installé. Par exemple :

cd C:\\Program Files\\MongoDB\\Server\\4.0\\bin

Exécuter les commandes suivantes :

mongorestore -d [your_db_name] [your_dump_dir]

Ici, la base de données est “Vidal” et le chemin d’accès est de la forme :
C:\\Users\\Documents\\Data_Engineering\\Vidal

(la base de données se trouve dans le sous-dossier *Vidal* du dossier principal
*Data_Engineering*.

*Etape 3 : Ouvrir elasticsearch*

Se rendre à l’emplacement où Elasticsearch a été installé. Dans le dossier .bin,
ouvrir le fichier *elasticsearch.bat*. Un terminal s’ouvre, le laisser tourner
en arrière plan et ne pas le fermer.

*Etape 4 : Exécution du programme principal*

Exécuter le script *run.py* qui se trouve dans le dossier *Flask* :

python run.py

User Guide

Lorsque l’on se rend à l’adresse indiquée, nous arrivons sur l’unique page de
notre application web. En dessous de l’introduction se trouve deux exemples
types de pages de page que l’on a scrappé depuis le site officiel du Vidal.
*Abacavir* est un exemple de substance, *Bactox* est un exemple de médicaments
contenant la substance *Amoxicilline*.

![](media/cadd4716461aa435369fc4d44c88a5dc.png)

Vous pouvez ensuite faire vous-même vos recherche dans le carré gris en haut à
droite. Entrez par exemple une substance bien connue, le *Paracétamol*. Une
description de la substance s’affichera, ainsi que la liste des médicaments
contenant cette dernière.

Vous pouvez ensuite affiner votre recherche en supprimant par exemple les
médicaments contenant du *sodium benzoate* parmi les excipients.

Reference Guide

L’application *Know what your drugs are made of* a été réalisé grâce à :

-   Scrapy, permet de récupérer les données depuis le site web.

-   MongoDB, permet de stocker les données dans une database grâce au NoSQL.

-   Elasticsearch, outils de recherche rapide dans la database.

-   Flask, framework de développement web en Python.

Pour toute question relative à la réalisation ou à l’exécution du projet, ne pas
hésiter à contacter :

<elias.bouillanne@edu.esiee.fr>

<marine.dussaussois@edu.esiee.fr>
