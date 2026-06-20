# Deep Learning - Tarea 3

## Generación de Datos Sintéticos con LLMs Locales

Este repositorio contiene el desarrollo de la **Tarea 3 del curso Deep Learning**, cuyo objetivo es evaluar y comparar modelos de lenguaje ejecutados localmente para la generación de datos sintéticos.

Se utilizarán tres modelos de lenguaje:

* LLaMA
* Phi
* Mistral

El trabajo considera instalación local de modelos, diseño de prompts, generación de datasets sintéticos y análisis comparativo de resultados.

# Integrantes

* Nombre Integrante 1
* Nombre Integrante 2
* Nombre Integrante 3

# Objetivos

* Ejecutar modelos de lenguaje localmente.
* Generar datasets sintéticos utilizando el mismo conjunto de prompts.
* Comparar desempeño entre modelos.
* Analizar resultados obtenidos.

# Estructura del Proyecto

```text
.
├── README.md
├── prompts/
│   └── prompts.md
│
├── datasets/
│   ├── llama_dataset.csv
│   ├── phi_dataset.csv
│   └── mistral_dataset.csv
│
├── scripts/
│   └── generar_datos.py
│
├── capturas/
│   ├── neofetch.png
│   ├── ollama_list.png
│   └── ejecucion_modelos.png
│
├── resultados/
│   └── comparacion.md
│
└── presentacion/
    └── presentacion.pdf
```

# Entorno de Ejecución

```bash
            .-/+oossssoo+/-.               michelle@michelle 
        `:+ssssssssssssssssss+:`           ----------------- 
      -+ssssssssssssssssssyyssss+-         OS: Ubuntu 24.04.4 LTS x86_64 
    .ossssssssssssssssssdMMMNysssso.       Host: VivoBook_ASUSLaptop X515JAB_X515JA 1.0 
   /ssssssssssshdmmNNmmyNMMMMhssssss/      Kernel: 6.8.0-124-generic 
  +ssssssssshmydMMMMMMMNddddyssssssss+     Uptime: 1 day, 16 hours, 54 mins 
 /sssssssshNMMMyhhyyyyhmNMMMNhssssssss/    Packages: 3065 (dpkg), 13 (flatpak), 23 (snap) 
.ssssssssdMMMNhsssssssssshNMMMdssssssss.   Shell: bash 5.2.21 
+sssshhhyNMMNyssssssssssssyNMMMysssssss+   Resolution: 1920x1080 
ossyNMMMNyMMhsssssssssssssshmmmhssssssso   DE: GNOME 46.0 
ossyNMMMNyMMhsssssssssssssshmmmhssssssso   WM: Mutter 
+sssshhhyNMMNyssssssssssssyNMMMysssssss+   WM Theme: Adwaita 
.ssssssssdMMMNhsssssssssshNMMMdssssssss.   Theme: Yaru-sage-dark [GTK2/3] 
 /sssssssshNMMMyhhyyyyhdNMMMNhssssssss/    Icons: Yaru-sage [GTK2/3] 
  +sssssssssdmydMMMMMMMMddddyssssssss+     Terminal: WarpTerminal 
   /ssssssssssshdmNNNNmyNMMMMhssssss/      CPU: Intel i3-1005G1 (4) @ 3.400GHz 
    .ossssssssssssssssssdMMMNysssso.       GPU: Intel Iris Plus Graphics G1 
      -+sssssssssssssssssyyyssss+-         Memory: 5179MiB / 7682MiB 
        `:+ssssssssssssssssss+:`
            .-/+oossssoo+/-.
```

# Herramienta de Ejecución

* Ollama

## Modelos Utilizados

* llama3.2:3b
* phi3:mini
* mistral:7b

# Instalación

## Instalar Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

```bash
ollama -v
ollama version is 0.24.0
```

## Descargar modelos

```bash
ollama pull llama3.2:3b
ollama pull phi3:mini
ollama pull mistral:7b
```

```bash
ollama list
NAME           ID              SIZE      MODIFIED
mistral:7b     6577803aa9a0    4.4 GB    8 seconds ago
phi3:mini      4f2222927938    2.2 GB    3 minutes ago
llama3.2:3b    a80c4f17acd5    2.0 GB    5 minutes ago
```


# Tópico
Generación de un dataset de preguntas frecuentes (FAQ) y consultas de soporte técnico orientadas a usuarios de una plataforma de hosting e infraestructura cloud. Los textos simularán dudas de clientes sobre el despliegue de contenedores Docker, configuración de bases de datos PostgreSQL utilizando estructuras dinámicas (JSONB), y las garantías de disponibilidad de un modelo de hosting estándar de 4 niveles con resiliencia máxima Tier IV.

## Justificación
Se seleccionó este tópico debido al alto volumen de consultas que reciben los servicios de infraestructura web (IaaS/PaaS).

# Prompts

Los prompts utilizados serán almacenados en:

```text
prompts/prompts.md
```

Todos los modelos serán evaluados utilizando exactamente los mismos prompts.

# Datasets Generados

Los datasets generados serán almacenados en:

```text
datasets/
```

Formato `.jsonl`.

## Estructura del archivo

```json
[
    {
        "id_consulta": 1,
        "texto_consulta": "Necesito ayuda urgente. El contenedor Docker de producción ha fallado durante el despliegue y mi aplicación está caída.",
        "etiqueta_tema": "Docker"
    }
]
```

# Ejecución

```bash
python3 scripts/generar_datos.py
Iniciando el pipeline de generacion de datos sinteticos.

--- Iniciando recoleccion de datos con el modelo: llama3.2:3b ---
  Procesando iteracion 1...
  Exito: Datos de la iteracion 1 guardados correctamente.
  Procesando iteracion 2...
  Exito: Datos de la iteracion 2 guardados correctamente.
  Procesando iteracion 3...
  Exito: Datos de la iteracion 3 guardados correctamente.
  Procesando iteracion 4...
  Exito: Datos de la iteracion 4 guardados correctamente.
  Procesando iteracion 5...
  Exito: Datos de la iteracion 5 guardados correctamente.

--- Iniciando recoleccion de datos con el modelo: phi3:mini ---
  Procesando iteracion 1...
  Exito: Datos de la iteracion 1 guardados correctamente.
  Procesando iteracion 2...
  Exito: Datos de la iteracion 2 guardados correctamente.
  Procesando iteracion 3...
  Exito: Datos de la iteracion 3 guardados correctamente.
  Procesando iteracion 4...
  Exito: Datos de la iteracion 4 guardados correctamente.
  Procesando iteracion 5...
  Exito: Datos de la iteracion 5 guardados correctamente.

--- Iniciando recoleccion de datos con el modelo: mistral:7b ---
  Procesando iteracion 1...
  Exito: Datos de la iteracion 1 guardados correctamente.
  Procesando iteracion 2...
  Exito: Datos de la iteracion 2 guardados correctamente.
  Procesando iteracion 3...
  Exito: Datos de la iteracion 3 guardados correctamente.
  Procesando iteracion 4...
  Exito: Datos de la iteracion 4 guardados correctamente.
  Procesando iteracion 5...
  Exito: Datos de la iteracion 5 guardados correctamente.

Proceso finalizado. Los datasets generados se encuentran en el directorio de salida.
```

# Resultados

La comparación incluirá:

* Coherencia del texto generado
* Relevancia respecto al tópico
* Diversidad
* Cumplimiento del formato solicitado

Los resultados serán almacenados en:

```text
resultados/comparacion.md
```