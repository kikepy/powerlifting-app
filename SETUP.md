# Instrucciones para ejecutar la aplicación

## Opción 1: Ejecución Manual (Recomendado)

### 1. Terminal 1 - Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Esperarás ver:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### 2. Terminal 2 - Frontend
```bash
cd frontend
python -m http.server 8001
```

Luego abre en tu navegador: **http://localhost:8001**

### 3. Terminal 3 - Cargar datos de prueba (opcional)
```bash
cd backend
pip install requests
python test_api.py
```

## Accesos Rápidos

- **Frontend:** http://localhost:8001
- **API Base:** http://localhost:8000/api
- **Swagger UI:** http://localhost:8000/docs (documentación interactiva)
- **ReDoc:** http://localhost:8000/redoc

## Pasos Iniciales

1. Abre el frontend en tu navegador
2. Ve a la pestaña "Agregar" y registra algunos concursantes
3. Importa datos de prueba (ejecuta test_api.py)
4. Ve al Dashboard para ver las estadísticas
5. Explora el Ranking y los Concursantes

## Estructura de la BD

La base de datos SQLite se crea automáticamente en `backend/powerlifting.db`

Contiene 3 tablas principales:
- **concursantes** - Atletas registrados
- **competiciones** - Competencias/eventos
- **levantamientos** - Récords de levantamientos con IPF calculado

## Troubleshooting

**Error: "Ya existe un concursante con ese nombre"**
- Usa nombres únicos al registrar

**Error: CORS**
- El backend ya tiene CORS configurado para aceptar todas las solicitudes

**Error de conexión al API**
- Verifica que el servidor FastAPI esté corriendo en puerto 8000

**Error de puerto ocupado**
- Cambia los puertos en los comandos si necesitas

## Personalizar

### Cambiar colores
Edita [frontend/style.css](frontend/style.css) - líneas 7-12

### Cambiar fórmula IPF
Edita [backend/ipf_calculator.py](backend/ipf_calculator.py)

### Agregar nuevos campos
Modifica [backend/models.py](backend/models.py) y agrega los endpoints en [backend/main.py](backend/main.py)
