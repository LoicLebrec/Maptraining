# Quick Start Guide - Maptraining

Bienvenue sur Maptraining ! Ce guide vous aidera à démarrer rapidement avec la plateforme.

## Installation Rapide

### Prérequis
- Python 3.8 ou supérieur
- pip (installé automatiquement avec Python)

### Étapes d'installation

1. **Cloner le dépôt** (ou télécharger les fichiers)
   ```bash
   git clone https://github.com/LoicLebrec/Maptraining.git
   cd Maptraining
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer l'application**
   ```bash
   python app.py
   ```

4. **Accéder à l'interface web**
   
   Ouvrez votre navigateur et allez sur : http://localhost:5000

## Utilisation Rapide

### 1. Générer un Parcours

1. Cliquez sur "Générer un parcours" dans le menu
2. Entrez votre nom
3. Spécifiez votre point de départ :
   - Nom de ville : "Paris, France"
   - Adresse : "Tour Eiffel, Paris"
   - Coordonnées GPS : "48.8566, 2.3522"
4. Choisissez la distance (entre 1 et 200 km)
5. Sélectionnez le niveau de difficulté :
   - **Facile** : Terrain plat, idéal pour la récupération
   - **Moyen** : Quelques dénivelés, entraînement standard
   - **Difficile** : Terrain vallonné, entraînement intense
6. Cliquez sur "Générer le Parcours"
7. Téléchargez le fichier GPX généré

### 2. Analyser un Entraînement

1. Cliquez sur "Analyser un entraînement" dans le menu
2. Cliquez sur "Choose File" et sélectionnez votre fichier GPX
3. Cliquez sur "Analyser l'Entraînement"
4. Consultez vos statistiques et recommandations

## Démo Script

Vous pouvez également tester les fonctionnalités via le script de démonstration :

```bash
python scripts/demo.py
```

Ce script créera (dans le dossier samples/) :
- Un parcours de 25 km depuis Paris
- Plusieurs exemples de parcours (récupération, sortie longue, entraînement en côte)
- Une analyse complète d'un entraînement

## Exemples de Parcours

### Sortie de Récupération (15 km, facile)
```python
from route_generator import RouteGenerator

generator = RouteGenerator()
athlete_profile = {
    'name': 'Jean',
    'difficulty': 'easy',
    'terrain': 'rolling'
}

route_points, metadata = generator.optimize_route_for_athlete(
    "48.8566, 2.3522",  # Paris
    15,  # 15 km
    athlete_profile
)

generator.create_gpx_file(
   route_points,
   "samples/recovery_ride.gpx",
   "Jean",
   "Sortie Récupération"
)
```

### Sortie Longue Weekend (80 km, moyen)
```python
route_points, metadata = generator.optimize_route_for_athlete(
    "Lyon, France",
    80,
    {'name': 'Marie', 'difficulty': 'medium', 'terrain': 'rolling'}
)

generator.create_gpx_file(
   route_points,
   "samples/long_ride.gpx",
   "Marie",
   "Sortie Longue Weekend"
)
```

## Utilisation de l'API

### Générer un Parcours via API

```bash
curl -X POST http://localhost:5000/api/generate-route \
  -H "Content-Type: application/json" \
  -d '{
    "start_location": "Paris, France",
    "distance": 50,
    "difficulty": "medium",
    "athlete_name": "Jean Dupont"
  }'
```

### Analyser un Entraînement via API

```bash
curl -X POST http://localhost:5000/api/analyze \
  -F "gpx_file=@my_training.gpx"
```

## Compatibilité des Fichiers GPX

Les fichiers GPX générés sont compatibles avec :
- **GPS** : Garmin, Wahoo, Polar, Bryton, etc.
- **Applications** : Strava, Komoot, TrainingPeaks, RideWithGPS, etc.
- **Logiciels** : Google Earth, BaseCamp, etc.

## Sources de Fichiers GPX pour l'Analyse

Vous pouvez obtenir des fichiers GPX depuis :
- Votre compteur GPS (Garmin Connect, Wahoo, etc.)
- Strava (Export GPX)
- Komoot (Export GPX)
- TrainingPeaks
- Parcours générés sur Maptraining

## Configuration pour Production

Pour un environnement de production :

```bash
# Définir une clé secrète sécurisée
export FLASK_SECRET_KEY="votre-cle-secrete-complexe-ici"

# Désactiver le mode debug (défaut)
export FLASK_DEBUG="false"

# Lancer l'application
python app.py
```

**Important** : N'utilisez jamais `debug=True` en production !

## Dépannage

### Problème de géocodage

Si vous avez des erreurs de géocodage (pas d'accès internet) :
- Utilisez directement des coordonnées GPS : "48.8566, 2.3522"
- Le format est : "latitude, longitude"

### Port déjà utilisé

Si le port 5000 est déjà utilisé :
```python
# Modifiez dans app.py
app.run(debug=debug_mode, host='0.0.0.0', port=8080)
```

### Problèmes d'installation

Si `pip install` échoue :
```bash
# Mettez à jour pip
pip install --upgrade pip

# Réessayez l'installation
pip install -r requirements.txt
```

## Support et Contribution

- 📖 Documentation complète : voir README.md
- 🐛 Signaler un bug : Ouvrez une issue sur GitHub
- 💡 Proposer une fonctionnalité : Créez une pull request
- 💬 Questions : Ouvrez une discussion sur GitHub

## Prochaines Étapes

Une fois l'application lancée :

1. **Explorez l'interface** : Familiarisez-vous avec les différentes pages
2. **Générez votre premier parcours** : Créez un parcours depuis votre domicile
3. **Analysez un entraînement** : Uploadez un fichier GPX existant
4. **Personnalisez** : Modifiez les paramètres pour vos besoins spécifiques

Bon entraînement ! 🚴
