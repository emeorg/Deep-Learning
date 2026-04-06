import os

packages = [
    "numpy",
    "pandas",
    "requests",
    "scikit-learn",
    "matplotlib",
    "jupyter",
    "keras-tuner"
]

for pkg in packages:
    print(f"Instalando {pkg}...")
    os.system(f"pip install {pkg}")

print("Instalación completa")