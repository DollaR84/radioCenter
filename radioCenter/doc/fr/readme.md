# radioCenter

* Auteur: Ruslan Dolovaniuk (Ukraine)
* PayPal: ruslan.dolovaniuk84@gmail.com

cette extension vous permet d'écouter des stations de radio en ligne et d'enregistrer le flux audio dans un fichier.
L'enregistrement d'une station de radio n'interfère pas avec l'écoute d'une autre station de radio.

Dans les collections, en plus des annuaires Internet, il est également possible d'ajouter un répertoire local avec des fichiers m3u.
Pour obtenir une collection locale, vous devez spécifier le chemin de base du répertoire dans les paramètres.
Tous les fichiers m3u de ce répertoire et tous ses sous-répertoires seront automatiquement analysés.

Avertissements!
Vérifier les stations de radio à partir des collections est un processus assez long et gourmand en ressources.
Il est recommandé de l'exécuter par parties, en fermant périodiquement la fenêtre, et de le réexécuter plus tard.
Après avoir rouvert la fenêtre des collections, les tests se poursuivront jusqu'à ce que toutes les stations de radio aient été vérifiées.
De plus, l'état de santé des liens change souvent, il est donc recommandé de vérifier l'état du lien sur le moment avant de l'ajouter à la liste générale.


## Liste des raccourcis clavier:
* NVDA+ALT+P: lire/mettre en pause la radio ;
* NVDA+ALT+P double clic: désactiver la radio ;
* NVDA+ALT+M: activer/désactiver le mode sourdine ;
* NVDA+ALT+Flèche Haut: augmenter le volume ;
* NVDA+ALT+Flèche Bas: réduire le volume ;
* NVDA+ALT+Flèche Droit: station suivante ;
* NVDA+ALT+Flèche Gauche: station précédente ;
* NVDA+ALT+O: obtenir des informations sur la station ;
* NVDA+ALT+R: ouvrir la fenêtre Contrôle Radio Center ;
* ÉCHAP: fermer les fenêtres Contrôle Radio Center et Collections de Radio ;
* CTRL+C: copier le lien de la station de radio dans le presse-papiers ;

Lors d'un tri manuel dans la liste des stations:
* ALT+Flèche Haut: déplacer la station vers une position plus haute ;
* ALT+Flèche Bas: déplacer la station vers une position plus basse ;

Dans les listes de collections:
* ALT+Flèche Haut ou ALT+Flèche Droit: basculer vers le suivant lien (si la radio dispose de plusieurs liens vers le flux audio) ;
* ALT+Flèche Bas ou ALT+Flèche Gauche: basculer vers le précédent lien (si la radio dispose de plusieurs liens vers le flux audio) ;
* CTRL+C: copier le lien de la station dans le presse-papiers ;

## Tri des stations:
* sans trier ;
* par nom croissant (de A à Z) ;
* par nom décroissant (de Z à A) ;
* par priorité et par nom croissant (de A à Z) ;
* par priorité et nom décroissant (de Z à A) ;
* manuellement ;

## Liste des changements:
###Version 4.2.0
* ajout de l'extraction du nom de la station, le cas échéant, lors du traitement du fichier m3u ;
* Ajout d'une option aux paramètres permettant d'afficher ou non un lien vers la station ;
* une option a été ajoutée aux paramètres pour le nombre de stations par portion à vérifier ;
* correction de quelques erreurs lors de la vérification automatique des stations ;

### Version 4.0.0
* pour NVDA 2023, les collections sont compatibles, à l'exception d'un navigateur radio ;
* créé une collection de vérification des fichiers m3u sur le stockage local ;
* ajout d'un menu de contrôle au menu NVDA ;
* filtres déplacés vers une boîte de dialogue séparée ;
* ajout de la lecture sonore lors de la vérification manuelle d'une station dans les collections ;
* correction d'une erreur de vérification de la station flottante après l'application de filtres ;

### Version 3.6.0
* apporté des modifications pour la compatibilité avec nvda 2023 (les collections sont désactivées pour la version 2023) ;
* ajout de la prise en charge des liens m3u ;
* ajout d'ignorer la casse lors du filtrage par nom et/ou information ;
* ajout de la suppression des espaces au début et à la fin des noms des stations de radio lors de l'analyse dans les collections ;
* ajout de la prononciation de l'état de la station lors de la vérification manuelle à l'aide du bouton de test dans les collections ;
* correction d'une erreur flottante lors de la mise à jour des collections ;

### Version 3.2.0
* ajout de la prise en charge des liens .pls ;
* ajout d'un nom à partir des informations du flux audio lors de la sauvegarde du fichier enregistré ;
* ajout de la gestion des erreurs lorsque l'enregistrement ne peut pas être démarré ;

### Version 3.0.0
* créé un mécanisme de collection pour sélectionner les stations de radio à partir des catalogues ;
* ajouté 3 collections avec des stations de radio ;
* créé un mécanisme pour vérifier automatiquement la fonctionnalité de chaque station de radio dans les collections ;
* ajout d'une vérification manuelle de la fonctionnalité de la station de radio ;
* ajout de la lecture de la radio directement dans la liste des collections ;
* ajout de la sauvegarde des stations de radio à partir de la collection vers la liste générale ;
* ajout d'un filtrage dans les collections par statut ;
* ajout du filtrage dans les collections par texte dans le titre ;
* ajout du filtrage dans les collections par texte dans les informations supplémentaires ;
* ajout de la fermeture des dialogues en appuyant sur ÉCHAP ;
* ajout de la copie du lien de la station de radio dans le presse-papiers dans la liste principale et dans les listes de collection ;
* basculement  des stations améliorées à l'aide de touches de raccourci, car auparavant, elles ne basculent pas toujours ;

### Version 2.1.0
* ajout d'une vérification et d'une correction si des erreurs sont trouvées dans l'indexation des stations ;
* ajout de la localisation espagnole (Rémy Ruiz) ;
* ajout de la localisation française (Rémy Ruiz) ;

### Version 2.0.0
* ajout de la possibilité d'enregistrer un flux audio dans un fichier ;

### Version 1.5.3
* ajout de la localisation tchèque (Jiri Holz) ;

### Version 1.5.1
* ajout d'une vérification de la fonctionnalité du lien avant d'ajouter une nouvelle station de radio ;
* ajout d'une vérification de la fonctionnalité du lien avant de modifier le lien de la station de radio ;
* correction d'un certain nombre d'erreurs mineures de fonctionnement ;

### Version 1.4.2
* ajout du tri manuel des stations ;
* ajout d'une combinaison de touches pour le mode muet ;

### Version 1.2.5
* paramètres ajoutés au panneau de paramètres NVDA ;
* ajout de la possibilité de modifier une station de radio existante ;
* ajout de plusieurs options pour trier les stations de radio ;
* changé la fonction de sourdine ;
* correction du problème d'ouverture de plusieurs fenêtres de contrôle; 

### Version 1.1.1
* ajout de la localisation turque (Umut Korkmaz) ;

### Version 1.1.0
* ajout du GUI au Control Radio Center ;

### Version 1.0.0
* création d'une radio en ligne sur le lecteur VLC de base ;
