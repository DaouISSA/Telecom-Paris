# Suivi du projet

**TODO1**

- Réussir à faire tourner les moteurs CHECK
- Assembler des composants pour un premier prototype
- Comprendre comment utiliser les moteurs pour se déplacer (exemple : comment tourner de 30°)
- Réussir à faire communiquer la raspberry à un serveur
- (plus tard) Réussir à détecter un qrcode avec la caméra CHECK

**Répartition des tâches**

- Candide: S'occupe de l'assemblage robot et de la partie web
- Thomas: S'occupe de la gestion des moteurs et de l'assemblage du robot
- Allan: S'occupe de la caméra
- Issa: S'occupe de la partie web

**23/09**

On a installé un OS sur la raspberry permettant de s'y connecter.
On a réussi à connecter le terminal d'un ordinateur à la raspberry par wifi.
-> tous ensemble

**27/09**

On s'est renseigné sur les robots de l'an dernier.
On a branché les moteurs au driver hat.
-> Thomas et Candide sont allés au fablab
On a réfléchi à une forme pour notre premier prototype.
-> tous ensemble
On a eu des difficultés à se reconnecter à la raspberry.
On a réfléchi à l'organisation de notre travail en équipe, à comment dépasser les difficultés de communication etc.
-> tous ensemble
Allan a réussi à brancher la caméra à son ordi et à avoir une image /!\ l'image est anormalement floue /!\ (problème matériel ?)
Issa a réussi à se connecter au git avec le terminal de son pc sous Windows

=> prochaine séance régler le pb de la caméra et tester un proto

**07/10**

Allan a réussi à implémenter un algo qui reconnait les balises : il marche sur sa webcam et pour des balises qui seraient à 5cm de la caméra ~
On a découpé notre plaque pour avoir un premier modèle à tester.
On a testé nos moteurs.
-> Thomas a réussi à les faire fonctionner
On a essayé de voir comment le faire tourner et changer de trajectoire.

**21/10**

Allan a fini le code permettant d'obtenir la position de la caméra par rapport aux balises en tenant compte de la taille des ces dernières: marche sur la caméra et sur la webcam. Problème de flou réglé.
On s'est rendu compte que l'impression précédente n'était pas convaincante, alors on a fait un nouveau plan en .svg avec des nouvelles dimensions (Thomas et Candide).
Issa a commencé une interface web qui nous permettra de controler le robot.
Issa et Candide ont regardé les vidéos de gestion de projet en ligne sur le forum.
Thomas a mis en place son propre pid pour mieux controller la position.

**08/11**

**14/11**

Candide : Calculs de maths sur feuilles pour des fonctions qui seront implémentées à la prochaine séance, qui permet de localiser le robot par triangulation, de localiser les rectangles,
de contourner les balises en faisant un octogone régulier centré sur la balise qui nous ramène à la position initiale et définition des stratégies qui dirigeront le robot (plan : on fait quoi et dans quel ordre)
Allan : Echange avec le serveur de suivi. Fonction test pour la caméra pour répondre au tests_projet.sh
Thomas : J'ai mis en place le serveur sur la raspberry avec flask pour un contrôle manuel. J'ai essayé tout le week-end de régler un problème de saccade des moteurs, qui s'avérais être un problème du micro-controller.
Issa: J'ai continué à travailler sur l'interface web en implémentant une fonction java script qui envoie des requettes au serveur afin d'excecuté des actions avancer, reculer, stopper, aller à droite, aller à gauche.  
**19/11**

Journée très très chargée. Gros travail de discussion pour spécifier les types et les attendus de chacun des domaines.
Candide : Création d'un fichier head.py dans lequel tourne les fonctions de stratégies et de localisation etc, qui fait appel aux programmes associés à la caméra et aux moteurs et fait le lien entre eux pour passer les épreuves.
Allan : Tests avec le serveur de suivi, définition d'une fonction pouvant être appelée pour renvoyer les informations obtenues par la caméra en accord avec ce dont a besoin Candide.
Issa: Modification du code de la page web en augmentant la taille des buttons et la couleur de fond. Essayer de comprendre certains codes de Thomas. Test du robot et discussion de ce qu'on pouvais ameliorer .
Thomas : Changement du micro-controller. Ecriture d'une classe avec subprocess pour controller les moteurs facilement depuis un main programmes.

**20/11**
Thomas, Allan et Issa ont travaillé le matin sur le fichier test_projet.sh afin de valider tous les tests, pendant ce temps Candide travaillait sur la stratégie du robot à mettre en oeuvre pour la capture de drapeau.
L'après-midi on a tous travaillé en commun sur la stratégie et Thomas a fait des réglages sur la précision lors des rotations du robot.

**10/12**
Ensemble le groupe 8, on a discuté sur la stragie collective qu'on va mettre en place pour l'épreuve finale. Thomas a travaillé sur le web et Issa a sur le serveur de suivi de deplacement  


