import polars as pl
import re
import os
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
try:
    from langdetect import detect
except ImportError:
    print("[Aviso] langdetect no instalado. Ejecuta: pip install langdetect")
    detect = None
try:
    from sentence_transformers import SentenceTransformer, util
    print("Cargando modelo NLP para Coherencia Semántica (puede tomar unos segundos)...")
    sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    print(f"[Aviso] No se pudo cargar sentence-transformers: {e}. Se usará métrica de coherencia básica por palabra clave.")
    sbert_model = None

# --- Configuración Constantes ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATASETS_DIR = BASE_DIR / "datasets"

FILES = {
    "LLaMA 3.2 3B": DATASETS_DIR / "llama3.2_3b_dataset.jsonl",
    "Phi-3 Mini": DATASETS_DIR / "phi3_mini_dataset.jsonl",
    "Mistral 7B": DATASETS_DIR / "mistral_7b_dataset.jsonl"
}
METRICS_DIR = BASE_DIR / "metricas"

# Reglas Heurísticas
FORMULAS_CORTESIA = ["por favor", "me gustaría saber", "podría proporcionarme", "agradezco", "estimado", "quisiera saber", "necesito ayuda"]
PALABRAS_SOPORTE = ["problema", "error", "ayuda", "configurar", "desplegar", "funciona", "dificultades", "fallo", "garantizar", "asistencia", "issue", "trouble", "help", "soporte", "duda"]

def configurar_entorno():
    METRICS_DIR.mkdir(exist_ok=True)

def calcular_palabras(texto: str) -> list:
    return re.findall(r'\b\w+\b', str(texto).lower())

def detectar_idioma_fuga(texto: str) -> bool:
    if detect is None or not texto.strip():
        return False
    try:
        # Detecta el idioma primario del texto
        return detect(texto) == 'en'
    except Exception:
        # Si no puede detectar idioma (ej. solo símbolos) no marcamos fuga
        return False

def tiene_cortesia_robotica(texto: str) -> bool:
    texto_lower = str(texto).lower()
    for formula in FORMULAS_CORTESIA:
        if formula in texto_lower:
            return True
    return False

def evaluar_adherencia_formato(texto: str) -> bool:
    """Verifica si el texto suena como una solicitud de soporte técnico (tiene verbos o sustantivos de problema)."""
    texto_lower = str(texto).lower()
    for palabra in PALABRAS_SOPORTE:
        if palabra in texto_lower:
            return True
    return False

def evaluar_coherencia(texto: str, tema: str) -> float:
    """Evalúa qué tan relacionado está el texto generado con la etiqueta de tema esperada."""
    if sbert_model is not None:
        emb_texto = sbert_model.encode(texto, convert_to_tensor=True)
        emb_tema = sbert_model.encode(tema, convert_to_tensor=True)
        sim = util.cos_sim(emb_texto, emb_tema).item()
        # Escalar similitud coseno (-1 a 1) a porcentaje aproximado (focalizado en los valores positivos típicos)
        puntaje = max(0.0, sim) * 100
        # Aumentar un poco el puntaje base porque "Docker" vs una oración completa siempre da < 1.0 incluso si es coherente
        return min(100.0, puntaje * 2.5) 
    else:
        # Fallback: simple text inclusion
        if tema.lower() in texto.lower():
            return 100.0
        return 0.0

def cargar_datos(ruta: str) -> pl.DataFrame:
    if not os.path.exists(ruta):
        return None
        
    registros = []
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                try:
                    data = json.loads(line)
                    if "texto_consulta" in data and "etiqueta_tema" in data:
                        registros.append({"texto_consulta": str(data["texto_consulta"]), "etiqueta_tema": str(data["etiqueta_tema"])})
                    else:
                        for k, v in data.items():
                            if isinstance(v, list):
                                for item in v:
                                    if isinstance(item, dict) and "texto_consulta" in item and "etiqueta_tema" in item:
                                        registros.append({"texto_consulta": str(item["texto_consulta"]), "etiqueta_tema": str(item["etiqueta_tema"])})
                except json.JSONDecodeError:
                    pass
    except Exception as e:
        print(f"Error al leer {ruta}: {e}")
        return None
        
    if not registros:
        return pl.DataFrame(schema={"texto_consulta": pl.String, "etiqueta_tema": pl.String})
        
    return pl.DataFrame(registros)

def calcular_metricas(df: pl.DataFrame) -> dict:
    metricas = {}
    metricas['total_registros'] = df.height
    if df.height == 0:
        return metricas
    
    es_robotico = [tiene_cortesia_robotica(t) for t in df["texto_consulta"]]
    metricas['cortesia_robotica'] = (sum(es_robotico) / len(es_robotico)) * 100
    
    es_pregunta = [1 if '?' in t or '¿' in t else 0 for t in df["texto_consulta"]]
    metricas['proporcion_interrogacion'] = (sum(es_pregunta) / len(es_pregunta)) * 100
    
    conteos_palabras = [len(calcular_palabras(t)) for t in df["texto_consulta"]]
    df_temp = pl.DataFrame({"conteos": conteos_palabras})
    std = df_temp["conteos"].std()
    metricas['variabilidad_longitud'] = std if std is not None else 0.0
    
    def complejidad(t):
        palabras = calcular_palabras(t)
        if not palabras: return 0.0
        return sum(len(p) for p in palabras) / len(palabras)
        
    complejidades = [complejidad(t) for t in df["texto_consulta"]]
    metricas['complejidad_lexica'] = sum(complejidades) / len(complejidades)
    
    fugas = [detectar_idioma_fuga(t) for t in df["texto_consulta"]]
    metricas['fugas_idioma'] = (sum(fugas) / len(fugas)) * 100
    
    # NUEVO: Coherencia y Formato
    coherencias = [evaluar_coherencia(t, e) for t, e in zip(df["texto_consulta"], df["etiqueta_tema"])]
    metricas['coherencia_semantica'] = sum(coherencias) / len(coherencias) if coherencias else 0
    
    adherencias = [evaluar_adherencia_formato(t) for t in df["texto_consulta"]]
    metricas['adherencia_formato'] = (sum(adherencias) / len(adherencias)) * 100 if adherencias else 0
    
    return metricas

def generar_reporte_consola(modelo: str, metricas: dict):
    print(f"\n--- Métricas para {modelo} ---")
    print(f"Total de consultas: {metricas['total_registros']}")
    print(f"Cortesía Robótica: {metricas.get('cortesia_robotica', 0):.1f}%")
    print(f"Preguntas Directas: {metricas.get('proporcion_interrogacion', 0):.1f}%")
    print(f"Fugas de Idioma: {metricas.get('fugas_idioma', 0):.1f}%")
    print(f"Variabilidad de Longitud (Std): {metricas.get('variabilidad_longitud', 0):.2f}")
    print(f"Complejidad Léxica (Letras/Palabra): {metricas.get('complejidad_lexica', 0):.2f}")
    print(f"Coherencia Semántica: {metricas.get('coherencia_semantica', 0):.1f}%")
    print(f"Adherencia a Formato Soporte: {metricas.get('adherencia_formato', 0):.1f}%")

def guardar_grafico_radar(todas_las_metricas: dict):
    """Genera un gráfico de radar en una cuadrícula 2x2."""
    categorias = ['Cortesía Robótica (%)', 'Preguntas Directas (%)', 'Fugas de Idioma (%)', 'Variabilidad (Escalada)', 'Complejidad (Escalada)', 'Coherencia Semántica (%)', 'Adherencia Formato (%)']
    
    modelos = list(todas_las_metricas.keys())
    titulos = modelos + ["Todos Combinados"]
    
    fig = make_subplots(
        rows=2, cols=2, 
        specs=[[{'type': 'polar'}, {'type': 'polar'}],
               [{'type': 'polar'}, {'type': 'polar'}]],
        subplot_titles=titulos,
        horizontal_spacing=0.08,
        vertical_spacing=0.12
    )
    
    posiciones = [(1,1), (1,2), (2,1)]
    
    for i, (modelo, metricas) in enumerate(todas_las_metricas.items()):
        if 'cortesia_robotica' not in metricas: continue
        
        # Escalamos variabilidad y complejidad para que sean visibles en el rango 0-100 del radar
        valores = [
            metricas['cortesia_robotica'],
            metricas['proporcion_interrogacion'],
            metricas['fugas_idioma'],
            min(100, metricas['variabilidad_longitud'] * 5),
            min(100, metricas['complejidad_lexica'] * 15),
            metricas.get('coherencia_semantica', 0),
            metricas.get('adherencia_formato', 0)
        ]
        
        # Cerrar el radar añadiendo el primer valor al final
        valores.append(valores[0])
        cats = categorias + [categorias[0]]
        
        if i < len(posiciones):
            row, col = posiciones[i]
            # Gráfico individual
            fig.add_trace(go.Scatterpolar(
                r=valores,
                theta=cats,
                fill='toself',
                name=modelo,
                showlegend=False
            ), row=row, col=col)
        
        # Añadir al 4to gráfico (Todos Combinados) en (2,2)
        fig.add_trace(go.Scatterpolar(
            r=valores,
            theta=cats,
            fill='toself',
            name=modelo,
            showlegend=True
        ), row=2, col=2)

    # Configurar el rango (0-100) para cada uno de los 4 ejes polares
    fig.update_layout(
        height=800,
        title_text="Dashboard de Calidad Generativa: Evaluación Multidimensional",
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        polar2=dict(radialaxis=dict(visible=True, range=[0, 100])),
        polar3=dict(radialaxis=dict(visible=True, range=[0, 100])),
        polar4=dict(radialaxis=dict(visible=True, range=[0, 100]))
    )
    
    filename = METRICS_DIR / "comparativa_modelos_radar.html"
    fig.write_html(str(filename))
    print(f"\nGráfico Radar 2x2 (HTML) guardado en: {filename}")

def main():
    configurar_entorno()
    print("Iniciando análisis avanzado de modelos y generación de métricas...")
    
    todas_las_metricas = {}
    
    for modelo, ruta in FILES.items():
        df = cargar_datos(ruta)
        if df is None or df.height == 0:
            print(f"\n[Warning] No se encontraron datos para {modelo} en {ruta}. Saltando...")
            continue
            
        metricas = calcular_metricas(df)
        generar_reporte_consola(modelo, metricas)
        todas_las_metricas[modelo] = metricas
        
    if todas_las_metricas:
        guardar_grafico_radar(todas_las_metricas)

if __name__ == "__main__":
    main()