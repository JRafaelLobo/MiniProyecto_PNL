#!/bin/bash
set -e

python3 -m venv .venv
source .venv/bin/activate

if ! command -v ollama &> /dev/null; then
  echo "[INFO] Ollama no está instalado. Instalando..."
  curl -fsSL https://ollama.com/install.sh | sh
else
  echo "[INFO] Ollama ya está instalado. Saltando instalación."
fi

ollama pull nomic-embed-text
pip install -r requirements.txt