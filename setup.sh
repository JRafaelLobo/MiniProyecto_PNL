#!/bin/bash
set -e
echo "=== Creando entorno virtual ==="
python3 -m venv venv
source venv/bin/activate
echo "=== Instalando dependencias de Python ==="
pip install -r requirements.txt
echo "=== Instalando Ollama ==="
curl -fsSL https://ollama.com/install.sh | sh
echo "=== Iniciando servicio de Ollama (si no está corriendo) ==="
systemctl start ollama 2>/dev/null || ollama serve &
echo "=== Descargando modelos ==="
ollama pull nomic-embed-text
ollama pull llama3.1
echo "=== Todo listo ==="