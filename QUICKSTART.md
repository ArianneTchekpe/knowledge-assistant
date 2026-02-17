# 🚀 Démarrage Rapide (5 minutes)

## Étape 1 : Installation (2 min)

```bash
# Créer l'environnement virtuel
python -m venv .venv

# Activer (Windows)
.\.venv\Scripts\Activate.ps1

# Activer (Mac/Linux)
source .venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

## Étape 2 : Configuration (1 min)

```bash
# Copier le template
copy .env.example .env    # Windows
cp .env.example .env      # Mac/Linux

# Éditer avec votre clé API
notepad .env              # Windows
nano .env                 # Mac/Linux
```

Dans le fichier `.env`, ajoutez :

```env
OPENAI_API_KEY=sk-proj-votre-cle-ici
OBSIDIAN_VAULT_PATH=C:\chemin\vers\votre\vault
```

## Étape 3 : Tester avec les notes d'exemple (1 min)

Pour tester rapidement, utilisez les notes d'exemple :

```env
OBSIDIAN_VAULT_PATH=./examples/sample_vault
```

## Étape 4 : Lancer (1 min)

```bash
python -m streamlit run app.py
```

✅ L'application s'ouvre à http://localhost:8501

## ✨ Première utilisation

1. **Attendez** que l'indexation se termine (barre latérale : "Système initialisé")
2. **Posez une question** dans l'onglet Chat
3. **Explorez** les sources dans la réponse

## 🎯 Questions d'exemple

Avec les notes de démonstration :

- "Qu'est-ce qu'un décorateur Python ?"
- "Explique les types d'apprentissage machine"
- "Comment évaluer un modèle ML ?"

## 🔄 Utilisation quotidienne

```bash
# Activer l'environnement
.\.venv\Scripts\Activate.ps1    # Windows
source .venv/bin/activate        # Mac/Linux

# Lancer l'app
python -m streamlit run app.py
```

## ⚡ Raccourcis utiles

### Windows - Créer lancer.bat

```batch
@echo off
cd /d "%~dp0"
call .venv\Scripts\activate.bat
python -m streamlit run app.py
pause
```

### Mac/Linux - Créer lancer.sh

```bash
#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
python -m streamlit run app.py
```

## 🆘 Problèmes ?

**Module introuvable** :
```bash
pip install -r requirements.txt
```

**Streamlit non reconnu** :
```bash
python -m streamlit run app.py
```

**Erreur .env** :
- Vérifiez que le fichier `.env` existe
- Vérifiez que la clé API est correcte

## 📚 Documentation complète

- `README.md` - Documentation principale
- `INSTALLATION_WINDOWS.md` - Guide Windows détaillé

Bon démarrage ! 🎉
