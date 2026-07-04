.PHONY: all setup pull-models run clean help

VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

all: run

setup: $(VENV_DIR)/bin/activate

$(VENV_DIR)/bin/activate: requirements.txt
	@echo "Creando entorno virtual e instalando dependencias..."
	python3 -m venv $(VENV_DIR)
	$(PIP) install -r requirements.txt
	touch $(VENV_DIR)/bin/activate

pull-models:
	@echo "Descargando modelos de Ollama (esto puede tomar tiempo si no existen)..."
	ollama pull llama3.2:3b
	ollama pull phi3:mini
	ollama pull mistral:7b

run: setup pull-models
	@echo "Iniciando pipeline de generacion de datos..."
	$(PYTHON) scripts/generar_datos.py

metricas: setup
	@echo "Generando métricas y gráficos de los modelos..."
	$(PYTHON) scripts/generar_metricas.py

clean:
	@echo "Limpiando entorno virtual y archivos generados..."
	rm -rf $(VENV_DIR)
	rm -f datasets/*.jsonl

# Mostrar la ayuda
help:
	@echo "Comandos disponibles:"
	@echo "  make          - Ejecuta todo el flujo: prepara entorno, descarga modelos y genera datos (equivale a 'make run')"
	@echo "  make setup    - Crea el entorno virtual e instala las dependencias"
	@echo "  make pull-models - Descarga los modelos de Ollama necesarios para el proyecto"
	@echo "  make run      - Ejecuta el script de Python (creará el entorno y descargará modelos si no existen)"
	@echo "  make metricas - Genera las métricas y gráficos de los modelos en HTML"
	@echo "  make clean    - Elimina el entorno virtual y borra los datasets generados"
	@echo "  make help     - Muestra este mensaje de ayuda"
