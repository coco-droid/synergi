#!/bin/bash

# Chemin d'accès au serveur Flask
FLASK_APP_PATH="./core/server.py"

# Commande pour lancer le serveur Flask
python3 "$FLASK_APP_PATH" &

# Attendre quelques secondes pour que le serveur Flask démarre complètement
sleep 5

# Lancement du serveur Redis (assurez-vous que Redis est installé)
echo "Lancement du serveur Redis..."
redis-server &

# Chemin d'accès au dossier Gui
GUI_DIR="./Gui"

# Vérifier si Electron.js est installé dans le dossier Gui
if [ ! -d "$GUI_DIR/node_modules/electron" ]; then
  echo "Electron.js n'est pas installé. Installation en cours..."
  # Vérifier si Yarn est installé
  if ! command -v yarn >/dev/null 2>&1; then
    echo "Yarn n'est pas installé. Installation en cours..."
    # Installer Yarn
    npm install -g yarn
  fi
  # Installer Electron.js avec Yarn
  cd "$GUI_DIR"
  yarn install electron
fi

# Lancer l'application Electron
echo "Lancement de l'application Electron..."
cd "$GUI_DIR"
npm start
