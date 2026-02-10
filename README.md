# Maptraining 🚴

Outil open source de génération de parcours cyclistes optimisés et d'analyse d'entraînement.

## 🎯 Fonctionnalités

### Génération de Parcours GPX
- Création de parcours cyclistes personnalisés basés sur vos besoins
- Spécification du point de départ (ville, adresse ou coordonnées GPS)
- Choix de la distance et du niveau de difficulté
- Génération de fichiers GPX compatibles avec tous les GPS et applications
- Optimisation des routes en fonction des itinéraires populaires

### Analyse d'Entraînement
- Upload de fichiers GPX de vos entraînements
- Calcul automatique des métriques clés :
  - Distance et durée
  - Vitesse et allure moyennes
  - Dénivelé positif et négatif
  - Intensité de l'effort
  - Charge d'entraînement (TSS-like)
- Recommandations personnalisées
- Visualisation interactive du parcours sur carte
- Retour immédiat sur les performances

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
pip install -r requirements.txt
```

## 💻 Utilisation

### Démarrer l'application web

```bash
python app.py
```

L'application sera accessible à l'adresse : http://localhost:5000

### Interface Web

1. **Page d'accueil** : Vue d'ensemble des fonctionnalités
2. **Générer un parcours** : Créez un nouveau parcours GPX
   - Entrez votre nom
   - Spécifiez le point de départ
   - Choisissez la distance et la difficulté
   - Téléchargez le fichier GPX généré

3. **Analyser un entraînement** : Uploadez un fichier GPX
   - Sélectionnez votre fichier GPX
   - Obtenez une analyse détaillée
   - Consultez les recommandations

### API REST

L'application fournit également une API REST pour l'intégration avec d'autres outils.

#### Générer un parcours
```bash
POST /api/generate-route
Content-Type: application/json

{
  "start_location": "Paris, France",
  "distance": 50,
  "difficulty": "medium",
  "athlete_name": "Jean Dupont"
}
```

#### Analyser un entraînement
```bash
POST /api/analyze
Content-Type: multipart/form-data

gpx_file: [votre fichier GPX]
```

## 📁 Structure du Projet

```
Maptraining/
├── app.py                    # Application Flask principale
├── route_generator.py        # Module de génération de parcours
├── training_analyzer.py      # Module d'analyse d'entraînement
├── requirements.txt          # Dépendances Python
├── templates/                # Templates HTML
│   ├── base.html
│   ├── index.html
│   ├── generate_route.html
│   ├── route_result.html
│   ├── analyze.html
│   └── analysis_result.html
├── uploads/                  # Fichiers GPX générés (créé automatiquement)
└── README.md
```

## 🛠️ Technologies Utilisées

- **Flask** : Framework web Python
- **gpxpy** : Manipulation de fichiers GPX
- **geopy** : Géocodage et calculs géographiques
- **folium** : Visualisation de cartes interactives
- **numpy** : Calculs numériques

## 📊 Métriques d'Analyse

### Charge d'Entraînement
La charge d'entraînement est calculée en fonction de :
- Durée de l'effort
- Distance parcourue
- Dénivelé accumulé
- Intensité estimée

### Intensité
L'intensité est classifiée en 4 niveaux :
- **Facile** : Récupération, endurance de base
- **Modéré** : Entraînement standard
- **Difficile** : Effort intense, développement spécifique
- **Intense** : Effort maximal

## 🎯 Cas d'Usage

1. **Préparation d'Entraînement**
   - Générez des parcours variés pour vos sorties
   - Adaptez la difficulté à votre plan d'entraînement
   - Exportez vers votre GPS favori

2. **Analyse Post-Entraînement**
   - Uploadez vos fichiers GPX après chaque sortie
   - Obtenez un retour immédiat sur vos performances
   - Suivez votre progression

3. **Planification**
   - Créez des parcours pour des événements spécifiques
   - Testez différentes distances et profils
   - Optimisez vos itinéraires

## 🔧 Configuration Avancée

### Personnalisation des Paramètres

Vous pouvez modifier les paramètres dans les modules :
- `route_generator.py` : Algorithmes de génération de parcours
- `training_analyzer.py` : Seuils et critères d'analyse

### Variables d'Environnement

- `FLASK_ENV` : Environnement (development/production)
- `FLASK_SECRET_KEY` : Clé secrète pour les sessions

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des nouvelles fonctionnalités
- Soumettre des pull requests

## 📝 Licence

Ce projet est un outil open source destiné à la communauté des cyclistes.

## 🌟 Fonctionnalités Futures

- [ ] Intégration avec Strava API
- [ ] Base de données de segments populaires
- [ ] Comparaison de multiples entraînements
- [ ] Export de statistiques en PDF
- [ ] Application mobile
- [ ] Prédiction de performances
- [ ] Planification d'entraînement sur plusieurs semaines

## 📞 Support

Pour toute question ou assistance, n'hésitez pas à ouvrir une issue sur GitHub.

---

Fait avec ❤️ pour la communauté cycliste