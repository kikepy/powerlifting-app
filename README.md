# 🏋️ Powerlifting Cuba - Web Application

Sistema web completo para la Hermandad Cubana de Powerlifting. Permite registrar concursantes, competiciones y levantamientos con cálculo automático del IPF Score. Soporta fotos tipo carnet por concursante, filtros por categoría, competiciones y records nacionales.

## 📋 Características

- ✅ Directorio de concursantes con datos completos
- ✅ Registro de levantamientos por disciplina (sentadilla, press banca, peso muerto)
- ✅ Cálculo automático del IPF Score
- ✅ Rankings dinámicos por categoría de peso
- ✅ Dashboard con estadísticas en tiempo real
- ✅ API RESTful con FastAPI
- ✅ Frontend moderno con colores azul, negro y rojo
- ✅ Base de datos SQLite

## 🚀 Instalación

### Backend

1. **Navega a la carpeta backend:**
```bash
cd backend
```

2. **Crea un entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instala las dependencias:**
```bash
pip install -r requirements.txt
```

4. **Ejecuta el servidor:**
```bash
python main.py
```

El servidor estará disponible en `http://localhost:8000`
- API: `http://localhost:8000/api`
- Swagger UI: `http://localhost:8000/docs`

### Frontend

1. **Navega a la carpeta frontend:**
```bash
cd ../frontend
```

2. **Abre `index.html` en tu navegador** (o usa un servidor local):
```bash
# Con Python 3
python -m http.server 8001

# Luego abre http://localhost:8001
```

## 📚 Estructura del Proyecto

```
powerlifting-app/
├── backend/
│   ├── main.py              # Aplicación FastAPI principal
│   ├── models.py            # Modelos de base de datos
│   ├── schemas.py           # Esquemas de validación
│   ├── database.py          # Configuración de BD
│   ├── ipf_calculator.py    # Cálculo de puntos IPF
│   ├── requirements.txt     # Dependencias Python
│   └── powerlifting.db      # Base de datos SQLite (se crea automáticamente)
└── frontend/
    ├── index.html           # Página principal
    ├── style.css            # Estilos (colores azul, negro y rojo)
    └── script.js            # Lógica del frontend
```

## 🔌 API Endpoints

### Concursantes
- `GET /api/concursantes` - Obtener todos
- `POST /api/concursantes` - Crear nuevo
- `GET /api/concursantes/{id}` - Obtener por ID
- `PUT /api/concursantes/{id}` - Actualizar
- `DELETE /api/concursantes/{id}` - Eliminar

### Competiciones
- `GET /api/competiciones` - Obtener todas
- `POST /api/competiciones` - Crear nueva
- `GET /api/competiciones/{id}` - Obtener por ID

### Levantamientos
- `GET /api/levantamientos` - Obtener todos
- `POST /api/levantamientos` - Crear nuevo (calcula IPF automáticamente)
- `GET /api/levantamientos/concursante/{id}` - Obtener por concursante

### Rankings
- `GET /api/ranking` - Ranking general por IPF
- `GET /api/ranking/{categoria}` - Ranking por categoría de peso

### Estadísticas
- `GET /api/estadisticas` - Estadísticas generales
- `GET /` - Health check

## 💾 Modelo de Datos

### Concursante
```json
{
  "id": 1,
  "nombre": "Juan Pérez",
  "edad": 28,
  "peso_corporal": 74.5,
  "sexo": "M",
  "categoria_peso": "74",
  "club": "Club Fuerte Cuba",
  "ciudad": "La Habana",
  "ano_inicio": 2019,
  "fecha_registro": "2024-05-23T10:30:00"
}
```

### Levantamiento
```json
{
  "id": 1,
  "concursante_id": 1,
  "competicion_id": 1,
  "sentadilla": 180,
  "press_banca": 120,
  "peso_muerto": 200,
  "ipf_score": 285.45,
  "fecha_levantamiento": "2024-05-23T10:30:00"
}
```

## 📊 Cálculo del IPF

El IPF Score se calcula automáticamente según:
- **Total levantado** = Sentadilla + Press Banca + Peso Muerto
- **Fórmula**: `IPF = (Total / Coeficiente) × 100`

Los coeficientes varían según:
- Categoría de peso
- Sexo del atleta

**Categorías de peso (Hombres):** 59, 66, 74, 83, 93, 105, 120, +120 kg
**Categorías de peso (Mujeres):** 47, 52, 57, 63, 69, 76, 84, +84 kg

## 🎨 Diseño

- **Colores principales:**
  - Azul: #1e90ff (primario)
  - Negro: #1a1a2e (fondo)
  - Rojo: #e74c3c (acentos y resaltes)

- **Responsivo:** Funciona en desktop, tablet y móvil
- **Animaciones suaves:** Transiciones y efectos visuales mejorados

## 📝 Ejemplo de Uso

### 1. Registrar un concursante
```bash
curl -X POST http://localhost:8000/api/concursantes \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Carlos López",
    "edad": 25,
    "peso_corporal": 82.5,
    "sexo": "M",
    "categoria_peso": "83",
    "club": "Powerlifting Heroes",
    "ciudad": "Santa Clara",
    "ano_inicio": 2020
  }'
```

### 2. Registrar un levantamiento
```bash
curl -X POST http://localhost:8000/api/levantamientos \
  -H "Content-Type: application/json" \
  -d '{
    "concursante_id": 1,
    "competicion_id": 1,
    "sentadilla": 180,
    "press_banca": 110,
    "peso_muerto": 210
  }'
```

### 3. Obtener ranking
```bash
curl http://localhost:8000/api/ranking
```

## 🔧 Tecnologías

- **Backend:** FastAPI, SQLAlchemy, SQLite
- **Frontend:** HTML5, CSS3, JavaScript Vanilla
- **Base de datos:** SQLite (portable, sin configuración)

## 📄 Licencia

© 2024 Asociación Cubana de Powerlifting

## 👨‍💻 Desarrollador

Creado con ❤️ para la comunidad de powerlifting cubana.

---

**¿Necesitas ayuda?** Consulta los endpoints en Swagger: `http://localhost:8000/docs`
