#!/bin/bash

# Détection de la plateforme
PLATFORM="$(uname -s)"

# Fonction pour créer un raccourci sur le bureau (Linux)
create_desktop_shortcut_linux() {
  echo "Création du raccourci sur le bureau (Linux)..."
  # Assurez-vous que le chemin d'accès au script de démarrage est correct
  START_SCRIPT="./start.sh"
  DESKTOP_DIR="$HOME/Desktop"
  echo "[Desktop Entry]
Name=Synergi
Exec=$START_SCRIPT
Type=Application
Icon=./GUI/preview.png
" > "$DESKTOP_DIR/Synergi.desktop"
  chmod +x "$DESKTOP_DIR/Synergi.desktop"
  echo "Raccourci créé sur le bureau."
}

# Fonction pour créer un raccourci sur le bureau (macOS)
create_desktop_shortcut_macos() {
  echo "Création du raccourci sur le bureau (macOS)..."
  # Assurez-vous que le chemin d'accès au script de démarrage est correct
  START_SCRIPT="./start.sh"
  DESKTOP_DIR="$HOME/Desktop"
  echo "#!/bin/bash
$START_SCRIPT" > "$DESKTOP_DIR/Synergi.command"
  chmod +x "$DESKTOP_DIR/Synergi.command"
  echo "Raccourci créé sur le bureau."
}

# Fonction pour créer un raccourci sur le bureau (Windows)
create_desktop_shortcut_windows() {
  echo "Création du raccourci sur le bureau (Windows)..."
  # Assurez-vous que le chemin d'accès au script de démarrage est correct
  START_SCRIPT="./start.sh"
  DESKTOP_DIR="$HOME/Desktop"
  ln -s "$START_SCRIPT" "$DESKTOP_DIR/Synergi.lnk"
  echo "Raccourci créé sur le bureau."
}

# Fonction pour créer un raccourci dans la barre d'accès rapide (Windows)
create_quick_launch_shortcut_windows() {
  echo "Création du raccourci dans la barre d'accès rapide (Windows)..."
  # Assurez-vous que le chemin d'accès au script de démarrage est correct
  START_SCRIPT="./start.sh"
  QUICK_LAUNCH_DIR="$APPDATA/Microsoft/Internet Explorer/Quick Launch"
  ln -s "$START_SCRIPT" "$QUICK_LAUNCH_DIR/Synergi.lnk"
  echo "Raccourci créé dans la barre d'accès rapide."
}

# Vérification de la présence de Python
if command -v python3 >/dev/null 2>&1; then
  echo "Python est déjà installé."
else
  if [ "$PLATFORM" == "Linux" ] || [ "$PLATFORM" == "Darwin" ]; then
    echo "Installation de Python..."
    # Code pour installer Python sur Linux et macOS
    if [ "$PLATFORM" == "Linux" ]; then
      sudo apt-get update
      sudo apt-get install python3
    elif [ "$PLATFORM" == "Darwin" ]; then
      brew install python@3
    fi
  elif [ "$PLATFORM" == "Windows" ]; then
    echo "Python n'est pas installé sur votre système Windows."
    echo "Veuillez télécharger et installer Python à partir du site officiel :"
    echo "https://www.python.org/downloads/windows/"
    echo "Une fois Python installé, relancez ce script."
    exit 1
  else
    echo "La plateforme $PLATFORM n'est pas prise en charge."
    exit 1
  fi
fi

# Vérification de la présence de Node.js
if command -v node >/dev/null 2>&1; then
  echo "Node.js est déjà installé."
else
  if [ "$PLATFORM" == "Linux" ] || [ "$PLATFORM" == "Darwin" ]; then
    echo "Installation de Node.js..."
    # Code pour installer Node.js sur Linux et macOS
    if [ "$PLATFORM" == "Linux" ]; then
      curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash -
      sudo apt-get install -y nodejs
    elif [ "$PLATFORM" == "Darwin" ]; then
      brew install node@14
    fi
  elif [ "$PLATFORM" == "Windows" ]; then
    echo "Node.js n'est pas installé sur votre système Windows."
    echo "Veuillez télécharger et installer Node.js à partir du site officiel :"
    echo "https://nodejs.org/"
    echo "Une fois Node.js installé, relancez ce script."
    exit 1
  else
    echo "La plateforme $PLATFORM n'est pas prise en charge."
    exit 1
  fi
fi

# Installation des dépendances Python pour le serveur Flask
echo "Installation des dépendances Python pour le serveur Flask..."
pip install -r ./core/requirements.txt

# Installation des dépendances Node.js pour l'application Electron
echo "Installation des dépendances Node.js pour l'application Electron..."
cd ./GUI
npm install

# Création du raccourci en fonction de la plateforme
if [ "$PLATFORM" == "Linux" ]; then
  create_desktop_shortcut_linux
elif [ "$PLATFORM" == "Darwin" ]; then
  create_desktop_shortcut_macos
elif [ "$PLATFORM" == "Windows" ]; then
  create_desktop_shortcut_windows
  create_quick_launch_shortcut_windows
fi

echo "L'installation est terminée. Vous pouvez maintenant exécuter votre application en cliquant sur le raccourci \"Synergi\"."
