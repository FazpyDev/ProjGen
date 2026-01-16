#!/bin/bash

# =====================================
# ProjGen Installer (Linux / macOS)
# =====================================

set -e  # Exit immediately if a command fails

echo "====================================="
echo "ProjGen Installer"
echo "====================================="
echo

# ---- Resolve paths ----
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$ROOT_DIR/app"
BUILD_APP="$ROOT_DIR/run.py"
INSTALL_DIR="$HOME/projgen"

# ---- Sanity check ----
if [ ! -f "$BUILD_APP" ]; then
    echo "ERROR: run.py not found in project root."
    exit 1
fi

# ---- Check Python ----
if ! command -v python3 >/dev/null 2>&1; then
    echo "Python3 is not installed or not in PATH."
    echo "Install it from https://www.python.org/"
    exit 1
fi

# ---- Check PyInstaller ----
if ! python3 -m PyInstaller --version >/dev/null 2>&1; then
    echo "PyInstaller not found. Installing..."
    python3 -m pip install --upgrade pyinstaller
fi

# ---- Build EXE ----
echo
echo "Building projgen executable..."
echo

python3 -m PyInstaller \
    --onefile \
    --name projgen \
    --paths "$APP_DIR" \
    --hidden-import app.TemplateFunctions \
    --hidden-import app.utils \
    --add-data "$APP_DIR/TemplateOptions.json:app" \
    --add-data "$APP_DIR/templates:app/templates" \
    "$BUILD_APP"

# ---- Install directory ----
mkdir -p "$INSTALL_DIR"

# ---- Copy EXE ----
cp "$ROOT_DIR/dist/projgen" "$INSTALL_DIR/"

cp -r "$APP_DIR/templates" "$INSTALL_DIR/"
cp "$APP_DIR/TemplateOptions.json" "$INSTALL_DIR/"

# ---- Add to PATH (if not already in PATH) ----
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    SHELL_RC="$HOME/.bashrc"
    if [ -n "$ZSH_VERSION" ]; then
        SHELL_RC="$HOME/.zshrc"
    fi

    echo "export PATH=\"\$PATH:$INSTALL_DIR\"" >> "$SHELL_RC"
    echo "Added $INSTALL_DIR to PATH. Please run 'source $SHELL_RC' or restart your terminal."
fi

# ---- Cleanup ----
rm -rf "$ROOT_DIR/build" "$ROOT_DIR/dist" "$ROOT_DIR/projgen.spec"

echo
echo "====================================="
echo "Installation Completed Successfully"
echo "Run 'projgen' in a new terminal to start."
echo "====================================="
