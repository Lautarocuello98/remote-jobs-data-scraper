# Remote Jobs Data Scraper

Scraper en Python para obtener vacantes remotas desde la API de RemoteOK, limpiarlas y exportarlas en CSV, Excel y JSON.

## Requisitos

- Python 3.10+
- Dependencias en `requirements.txt`

## Instalacion

```bash
pip install -r requirements.txt
```

Opcional: copia `.env.example` a `.env` y ajusta valores.

## Configuracion (`.env`)

- `USER_AGENT`: encabezado User-Agent para requests.
- `REQUEST_TIMEOUT`: timeout en segundos para la llamada HTTP.

## Ejecucion

```bash
python main.py
```

## Salidas

- `data/raw/jobs_raw.csv`
- `data/processed/remote_jobs_clean.csv`
- `output/remote_jobs.xlsx`
- `output/remote_jobs.json`

## Tests

```bash
pytest -q
```
