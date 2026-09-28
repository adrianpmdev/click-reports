<div align="center">

# Click Reports

### Servicio interno que convierte los clics de los productos en estadísticas sencillas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
[![Author](https://img.shields.io/badge/Author-adrianpmdev-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/adrianpmdev)

</div>

---

## Descripción

Pequeño servicio interno para una tienda online. Registra los clics en los productos y los convierte en estadísticas sencillas: total de clics por producto, clics por día y un reporte CSV descargable.

## Funcionalidades

- Endpoint para registrar un clic en un producto.
- Total de clics por producto, ordenados de más a menos.
- Clics por día, de todos los productos o de uno solo.
- Exportación a CSV con los clics por día y producto.
- Datos de ejemplo generados en el primer arranque (productos y clics de los últimos 30 días).
- Documentación interactiva de la API (Swagger) en `/docs`.

## Tecnologías

| Tecnología | Uso |
| --- | --- |
| Python 3.11+ | Lenguaje |
| FastAPI | API REST |
| Pandas | Agregaciones y exportación a CSV |
| SQLite | Almacenamiento |

## Estructura del proyecto

```
click-reports/
├── app/
│   ├── main.py          # Punto de entrada, ciclo de vida y routers
│   ├── config.py        # Configuración (variables de entorno)
│   ├── database.py      # Conexión SQLite, esquema y datos de ejemplo
│   ├── schemas.py       # Modelos Pydantic
│   ├── repository.py    # Consultas SQL
│   ├── reports.py       # Estadísticas con Pandas
│   └── routers/
│       ├── clicks.py    # Endpoints /clicks
│       └── stats.py     # Endpoints /stats y /reports
├── data/                # Base de datos SQLite (se crea al arrancar)
└── requirements.txt
```

## Puesta en marcha

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Abre http://localhost:8000/docs.

### Configuración

| Variable | Por defecto | Descripción |
| --- | --- | --- |
| `DB_PATH` | `data/click_reports.db` | Fichero SQLite |
| `SAMPLE_CLICKS` | `500` | Clics de ejemplo creados en el primer arranque |
| `SAMPLE_DAYS` | `30` | Días entre los que se reparten los clics de ejemplo |

## Endpoints

| Método | Ruta | Descripción |
| --- | --- | --- |
| POST | `/clicks` | Registrar un clic en un producto |
| GET | `/stats/products` | Total de clics por producto |
| GET | `/stats/daily?product_id=` | Clics por día (filtro opcional por producto) |
| GET | `/reports/clicks.csv` | Descargar el reporte CSV |

---

<div align="center">

Made in 2026 by [@adrianpmdev](https://github.com/adrianpmdev)

</div>
