# Contributing to Maptraining

Merci de votre intérêt pour contribuer à Maptraining ! 🚴

## Comment Contribuer

### Signaler des Bugs

Si vous trouvez un bug, veuillez :
1. Vérifier que le bug n'a pas déjà été signalé dans les issues
2. Créer une nouvelle issue avec :
   - Une description claire du problème
   - Les étapes pour reproduire le bug
   - Le comportement attendu vs le comportement observé
   - Votre environnement (OS, version Python, etc.)

### Proposer des Fonctionnalités

Pour proposer une nouvelle fonctionnalité :
1. Ouvrez une issue pour discuter de l'idée
2. Expliquez le cas d'usage et les bénéfices
3. Attendez les retours avant de commencer l'implémentation

### Soumettre des Pull Requests

1. **Fork le dépôt** et créez une branche depuis `main`
2. **Installez les dépendances** : `pip install -r requirements.txt`
3. **Faites vos modifications** en suivant les bonnes pratiques
4. **Testez vos changements** : Assurez-vous que tout fonctionne
5. **Commitez avec des messages clairs**
6. **Soumettez votre PR** avec une description détaillée

## Standards de Code

### Style Python
- Suivez PEP 8
- Utilisez des noms de variables descriptifs
- Commentez le code complexe
- Ajoutez des docstrings aux fonctions

### Bonnes Pratiques
- Pas de credentials hardcodés
- Utilisez des variables d'environnement pour la configuration
- Gérez les erreurs de manière appropriée
- Ajoutez des tests pour les nouvelles fonctionnalités

### Structure des Commits
```
<type>: <description courte>

<description détaillée si nécessaire>
```

Types de commits :
- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation
- `style`: Formatage, style
- `refactor`: Refactorisation du code
- `test`: Ajout/modification de tests
- `chore`: Tâches de maintenance

## Domaines de Contribution

### Développement
- Nouvelles fonctionnalités
- Corrections de bugs
- Optimisations de performance
- Tests automatisés

### Documentation
- Amélioration du README
- Tutoriels et guides
- Traductions
- Commentaires de code

### Design
- Interface utilisateur
- Expérience utilisateur
- Icônes et graphismes
- Responsive design

### Idées de Fonctionnalités

Quelques idées pour contribuer :
- [ ] Intégration avec Strava API
- [ ] Base de données de segments populaires
- [ ] Comparaison de multiples entraînements
- [ ] Export PDF des statistiques
- [ ] Application mobile
- [ ] Prédiction de performances
- [ ] Planification d'entraînement sur plusieurs semaines
- [ ] Support multilingue complet
- [ ] Intégration avec d'autres plateformes (Garmin, Wahoo, etc.)
- [ ] Analyse de puissance (watts)
- [ ] Zones de fréquence cardiaque

## Tests

Avant de soumettre une PR :
```bash
# Testez votre code
python demo.py

# Vérifiez qu'il n'y a pas d'erreurs
python -m py_compile app.py route_generator.py training_analyzer.py
```

## Questions ?

Si vous avez des questions :
- Ouvrez une issue avec le label `question`
- Consultez la documentation existante
- Regardez les issues existantes

## Code of Conduct

- Soyez respectueux et inclusif
- Acceptez les critiques constructives
- Concentrez-vous sur ce qui est meilleur pour la communauté
- Faites preuve d'empathie envers les autres membres

Merci de contribuer à Maptraining ! 🎉
