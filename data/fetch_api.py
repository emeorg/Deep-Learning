from libs import *
from utils.helpers import debug
import time

def fetch_weather_data_multi(batch_size=5, wait_minutes=2):

    debug("=== DESCARGA POR LOTES ===")

    url = "https://archive-api.open-meteo.com/v1/archive"

    cities = [
        # América
        ("Santiago", -33.45, -70.66),
        ("Buenos Aires", -34.60, -58.38),
        ("Lima", -12.04, -77.03),
        ("Bogotá", 4.71, -74.07),
        ("Mexico City", 19.43, -99.13),
        ("New York", 40.71, -74.00),
        ("Los Angeles", 34.05, -118.24),
        ("Toronto", 43.65, -79.38),
        ("Chicago", 41.88, -87.63),
        ("Miami", 25.76, -80.19),
        ("São Paulo", -23.55, -46.63),
        ("Rio de Janeiro", -22.90, -43.20),
        ("Vancouver", 49.28, -123.12),
        ("Montreal", 45.50, -73.57),
        ("Barcelona", 41.38, 2.17),
        ("Houston", 29.76, -95.36),

        # Europa
        ("Madrid", 40.41, -3.70),
        ("Paris", 48.85, 2.35),
        ("London", 51.50, -0.12),
        ("Berlin", 52.52, 13.40),
        ("Rome", 41.90, 12.49),
        ("Lisbon", 38.72, -9.13),
        ("Amsterdam", 52.37, 4.89),
        ("Vienna", 48.20, 16.37),
        ("Barcelona", 41.38, 2.17),


        # Asia
        ("Tokyo", 35.68, 139.69),
        ("Beijing", 39.90, 116.40),
        ("Mumbai", 19.07, 72.87),
        ("Dubai", 25.20, 55.27),
        ("Seoul", 37.56, 126.97),
        ("Bangkok", 13.75, 100.50),
        ("Singapore", 1.35, 103.82),
        ("Delhi", 28.61, 77.20),
        ("Istanbul", 41.01, 28.97),

        # África
        ("Cairo", 30.04, 31.23),
        ("Nairobi", -1.29, 36.82),
        ("Cape Town", -33.92, 18.42),
        ("Johannesburg", -26.20, 28.04),

        # Oceanía
        ("Sydney", -33.86, 151.21),
        ("Melbourne", -37.81, 144.96),
        ("Auckland", -36.85, 174.76),
    ]


    output_path = "outputs/datasets/raw_weather_multi.csv"

    if os.path.exists(output_path):
        final_df = pd.read_csv(output_path)
        downloaded = set(final_df["city"].unique())
        print("📂 Continuando descarga...")
    else:
        final_df = pd.DataFrame()
        downloaded = set()

    all_data = []

    for i, (name, lat, lon) in enumerate(cities):

        if name in downloaded:
            print(f"⏩ Saltando {name} (ya descargada)")
            continue

        print(f"\n🌍 {name}")

        try:
            response = requests.get(url, params={
                "latitude": lat,
                "longitude": lon,
                "start_date": "2018-01-01",
                "end_date": "2024-12-31",
                "hourly": [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "dew_point_2m",
                    "apparent_temperature",
                    "precipitation",
                    "rain",
                    "snowfall",
                    "cloudcover",
                    "cloudcover_low",
                    "cloudcover_mid",
                    "cloudcover_high",
                    "surface_pressure",
                    "windspeed_10m",
                    "winddirection_10m",
                    "shortwave_radiation",
                    "et0_fao_evapotranspiration"
                ]
            })

            if response.status_code == 200:

                data = response.json()
                df = pd.DataFrame(data["hourly"])

                df["city"] = name
                df["lat"] = lat
                df["lon"] = lon

                print(f"✅ OK {df.shape}")

                output_path = "outputs/datasets/raw_weather_multi.csv"

                # guardar inmediatamente
                if os.path.exists(output_path):
                    df.to_csv(output_path, mode='a', header=False, index=False)
                else:
                    df.to_csv(output_path, index=False)

                print("💾 Guardado incremental")

            else:
                error_text = response.text.lower()

                print("⛔ RATE LIMIT DETECTADO")
                print(response.text)

                if "hourly" in error_text:
                    wait = 60  # 1 hora
                elif "minutely" in error_text:
                    wait = 2   # 2 minutos
                else:
                    wait = 5   # fallback

                print(f"⏳ Esperando {wait} minutos...")
                time.sleep(wait * 60)

                continue

        except Exception as e:
            print(f"❌ Error: {e}")

        # 🔥 control por lote
        if (i + 1) % batch_size == 0:
            print(f"\n⏳ Pausa {wait_minutes} min por rate limit...")
            time.sleep(wait_minutes * 60)

    # guardar incremental
    if len(all_data) > 0:
        new_df = pd.concat(all_data, ignore_index=True)
        final_df = pd.concat([final_df, new_df], ignore_index=True)

        final_df.to_csv(output_path, index=False)

    print("\n🔥 TOTAL ACTUAL:", final_df.shape)