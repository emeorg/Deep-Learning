# Deep Learning - Tarea 1

Este repositorio contiene la implementación de una Red Neuronal Profunda (DNN) para datos tabulares de gran escala, utilizando datos climáticos de Open-Meteo.

## Estructura del Proyecto

*   `main.ipynb`: Cuaderno principal que orquestal el flujo de trabajo.
*   `data/`: Módulos para extracción y construcción de datasets.
*   `models/`: Definiciones de modelos y AutoML.
*   `utils/`: Herramientas auxiliares y logging.
*   `outputs/`: Directorio para logs, plots y datasets generados.

## Configuración del Entorno

Para ejecutar este proyecto, se recomienda el uso de un entorno virtual (.venv).

### Pasos para la instalación:

1.  **Crear el entorno virtual**:
    ```bash
    python -m venv .venv
    ```

2.  **Activar el entorno**:
    *   Linux/macOS: `source .venv/bin/activate`
    *   Windows: `.venv\Scripts\activate`

3.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

Abre el cuaderno `main.ipynb` en tu entorno Jupyter y ejecuta las celdas secuencialmente. Nota que se ha eliminado el script `install.py` en favor del uso de `requirements.txt`.
