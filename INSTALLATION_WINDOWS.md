# 🪟 Guide d'installation Windows

Guide complet pour installer Obsidian Knowledge Assistant sur Windows.

## Prérequis

- Windows 10 ou 11
- Python 3.10 ou supérieur
- PowerShell (inclus avec Windows)
- Compte OpenAI avec clé API

## Étape 1 : Vérifier Python

Ouvrez PowerShell et vérifiez la version de Python :

```powershell
python --version
```

Vous devriez voir `Python 3.10` ou supérieur.

**Si Python n'est pas installé** :
1. Téléchargez depuis https://www.python.org/downloads/
2. ✅ Cochez "Add Python to PATH" pendant l'installation
3. Redémarrez PowerShell

## Étape 2 : Extraire le projet

1. Téléchargez le dossier `obsidian-knowledge-assistant`
2. Extrayez-le dans un emplacement facile d'accès
3. Exemple : `C:\Users\VotreNom\Desktop\obsidian-knowledge-assistant`

## Étape 3 : Ouvrir PowerShell

1. Ouvrez le dossier du projet dans l'Explorateur Windows
2. Maintenez `Shift` + Clic droit dans le dossier
3. Sélectionnez "Ouvrir PowerShell ici" ou "Ouvrir dans Terminal"

## Étape 4 : Créer l'environnement virtuel

```powershell
python -m venv .venv
```

## Étape 5 : Activer l'environnement virtuel

```powershell
.\.venv\Scripts\Activate.ps1
```

**Si vous obtenez une erreur de politique d'exécution** :

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Puis réessayez d'activer l'environnement.

Vous devriez voir `(.venv)` au début de votre ligne PowerShell.

## Étape 6 : Mettre à jour pip

```powershell
python -m pip install --upgrade pip
```

## Étape 7 : Installer les dépendances

```powershell
pip install -r requirements.txt
```

**⏱️ Cela peut prendre 5-10 minutes.**

Si vous rencontrez des erreurs, installez les packages un par un :

```powershell
pip install python-dotenv
pip install langchain langchain-community langchain-openai
pip install openai
pip install faiss-cpu
pip install streamlit
pip install sentence-transformers
pip install python-frontmatter
pip install markdown
pip install tiktoken
pip install pandas numpy
```

## Étape 8 : Créer le fichier .env

```powershell
Copy-Item .env.example .env
```

Puis éditez le fichier :

```powershell
notepad .env
```

**Remplissez les valeurs obligatoires** :

```env
OPENAI_API_KEY=sk-proj-votre-cle-ici
OBSIDIAN_VAULT_PATH=C:\Users\VotreNom\Documents\MonVault
```

### Comment trouver votre clé API OpenAI

1. Allez sur https://platform.openai.com/api-keys
2. Connectez-vous
3. Cliquez sur "Create new secret key"
4. Copiez la clé (elle commence par `sk-proj-` ou `sk-`)
5. Collez-la dans le fichier `.env`

### Comment trouver le chemin de votre vault Obsidian

1. Ouvrez Obsidian
2. Allez dans Settings (⚙️) → About
3. Faites défiler pour voir le chemin du vault
4. Copiez ce chemin dans `.env`

Exemple : `C:\Users\VotreNom\Documents\ObsidianVault`

**Sauvegardez et fermez** le fichier `.env`.

## Étape 9 : Lancer l'application

```powershell
python -m streamlit run app.py
```

L'application devrait s'ouvrir automatiquement dans votre navigateur !

Si elle ne s'ouvre pas, allez manuellement sur : http://localhost:8501

## ✅ Vérification

Vous devriez voir :
- ✅ "Système initialisé" dans la barre latérale
- Nombre de notes indexées
- Interface de chat fonctionnelle

## 🔄 Utilisation future

Pour lancer l'application plus tard :

```powershell
# 1. Ouvrez PowerShell dans le dossier du projet
# 2. Activez l'environnement virtuel
.\.venv\Scripts\Activate.ps1

# 3. Lancez l'application
python -m streamlit run app.py
```

## 🎯 Création d'un raccourci (Optionnel)

Créez un fichier `lancer.bat` :

```batch
@echo off
cd /d "%~dp0"
call .venv\Scripts\activate.bat
python -m streamlit run app.py
pause
```

Double-cliquez sur `lancer.bat` pour démarrer l'application !

## ❌ Problèmes courants

### Erreur "streamlit: command not found"

Utilisez toujours :
```powershell
python -m streamlit run app.py
```

### Erreur "ModuleNotFoundError"

Assurez-vous que l'environnement virtuel est activé (vous devez voir `(.venv)`).

Réinstallez les dépendances :
```powershell
pip install -r requirements.txt
```

### Erreur "No module named 'src'"

Assurez-vous d'être dans le bon dossier :
```powershell
cd "C:\chemin\vers\obsidian-knowledge-assistant"
```

### L'application ne démarre pas

1. Vérifiez que le fichier `.env` existe
2. Vérifiez que `OPENAI_API_KEY` est définie
3. Vérifiez que `OBSIDIAN_VAULT_PATH` pointe vers un dossier existant

## 📞 Besoin d'aide ?

Vérifiez dans l'ordre :

1. ✅ Python 3.10+ installé
2. ✅ Environnement virtuel activé (voir `(.venv)`)
3. ✅ Toutes les dépendances installées
4. ✅ Fichier `.env` créé et rempli
5. ✅ Chemin du vault Obsidian correct

## 🎉 Félicitations !

Vous êtes prêt à utiliser votre Knowledge Assistant !

Posez votre première question dans l'onglet Chat. 🚀
