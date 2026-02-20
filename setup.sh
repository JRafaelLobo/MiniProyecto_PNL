#!/bin/bash
set -evenv

python3 -m venv .venv
source ./bin/activate

if ! command -v ollama >/dev/null 2>&1; then
  echo "[INFO] Ollama no está instalado. Instalando..."
  curl -fsSL https://ollama.com/install.sh | sh
else
  echo "[INFO] Ollama ya está instalado. Saltando instalación."
fi

ollama pull nomic-embed-text

pip install --upgrade pip
pip install -r requirements.txt