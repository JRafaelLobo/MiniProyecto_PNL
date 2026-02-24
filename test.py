import ollama

try:
    response = ollama.embed(
        model='mxbai-embed-large',
        input='Hola mundo, probando embeddings'
    )
    # Ollama devuelve una lista de listas en 'embeddings'
    vector = response['embeddings'][0]
    print(f"✅ ¡Éxito! Tamaño del vector: {len(vector)}")
    print(f"Primeros 5 números: {vector[:5]}")
except Exception as e:
    print(f"❌ Error: {e}")