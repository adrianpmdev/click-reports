<div align="center">

# 📊 Click Reports

### Servicio interno que convierte los clics de los productos en estadísticas sencillas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

[![Author](https://img.shields.io/badge/Author-adrianpmdev-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/adrianpmdev)

</div>

---

<br>

## 📖 Descripción

Pequeño **servicio interno para una tienda online**. Registra los **clics en los productos** y los convierte en **estadísticas sencillas**: total por producto, clics por día y un **reporte CSV** descargable.

---

<br>

## 🚀 Funcionalidades

- 🖱️ **Registro de clics** sobre productos existentes.
- 🏆 **Total de clics por producto**, incluidos los que no tienen ninguno.
- 📅 **Clics por día**, de todos los productos o de uno solo.
- 📄 **Reporte CSV** con los clics por día y producto, generado con Pandas.
- 📚 **Documentación de la API** (Swagger) en `/docs`.

| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `/health` | Estado del servicio |
| POST | `/clicks` | Registrar un clic en un producto |
| GET | `/stats/products` | Total de clics por producto |
| GET | `/stats/daily?product_id=` | Clics por día (filtro opcional por producto) |
| GET | `/reports/clicks.csv` | Descargar el reporte CSV |

---

<br>

## ⚙️ Puesta en marcha

Necesitas **Python 3.12 o superior** ([python.org/downloads](https://www.python.org/downloads/)). Desde la carpeta del proyecto:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Abre http://localhost:8000/docs. En el primer arranque se crean productos y clics de ejemplo de los últimos 30 días.

### 🔧 Ajustes

| Variable | Por defecto | Descripción |
| --- | --- | --- |
| `DB_PATH` | `data/click_reports.db` | Fichero SQLite |
| `SEED_SAMPLE_DATA` | `true` | Crear datos de ejemplo si la base de datos está vacía |
| `SAMPLE_CLICKS` | `500` | Clics de ejemplo |
| `SAMPLE_DAYS` | `30` | Días entre los que se reparten los clics de ejemplo |

### 🧪 Tests

```bash
python -m pytest
```

Los tests usan una base de datos temporal con unos pocos datos conocidos.

---

<br>

## 📝 Decisiones y límites

- 🗄️ **Los totales se calculan en SQL** y Pandas solo genera el CSV, así que no se cargan todos los clics en memoria.
- 🌍 **Los días se agrupan en UTC**: un clic a las 00:30 en Madrid cuenta en el día anterior.
- 🔓 **Sin autenticación ni gestión de productos**: el catálogo vive en otro sistema y el servicio es interno.

---

<br>

## 👤 Autor

[@adrianpmdev](https://github.com/adrianpmdev) · Junior Full Stack Developer

---

<br>

<div align="center">

✨ Made in **2026** by [@adrianpmdev](https://github.com/adrianpmdev) ✨

</div>
