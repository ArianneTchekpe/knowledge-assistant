# Example Vault - Notes de démonstration

Ce dossier contient des notes d'exemple pour tester le système.

## Utilisation

Pour tester avec ces notes :

1. Dans le fichier `.env`, définissez :
```env
OBSIDIAN_VAULT_PATH=./examples/sample_vault
```

2. Lancez l'application
3. Le système indexera automatiquement ces notes

## Exemples de questions à poser

Une fois les notes indexées, essayez :

1. "Qu'est-ce qu'un décorateur Python ?"
2. "Explique-moi les réseaux de neurones"
3. "Quelles sont les métriques pour évaluer un modèle de classification ?"
4. "Qu'est-ce que l'apprentissage supervisé ?"

## Ajout de vos propres notes

Vous pouvez ajouter d'autres fichiers `.md` dans ce dossier, puis reconstruire l'index dans l'application.

### Structure recommandée

```markdown
---
title: Titre de votre note
tags: [tag1, tag2]
created: 2024-01-01
---

# Titre

Votre contenu ici...

## Section

Plus de contenu...

#tags #additionnels
```

## Notes incluses

- **Python Programming.md** - Bases de Python et décorateurs
- **Machine Learning.md** - Concepts fondamentaux du ML
