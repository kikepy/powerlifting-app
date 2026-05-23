from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import datetime
import os
import shutil

from database import engine, Base, get_db
from models import Concursante, Competicion, Levantamiento
from schemas import (
    Concursante as ConcursanteSchema,
    ConcursanteCreate,
    Competicion as CompeticionSchema,
    CompeticionCreate,
    Levantamiento as LevantamientoSchema,
    LevantamientoCreate
)
from ipf_calculator import calculate_ipf_points

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Powerlifting API - Cuba", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar carpeta estática para fotos
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
PHOTOS_DIR = os.path.join(STATIC_DIR, "photos")
os.makedirs(PHOTOS_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ==================== RUTAS CONCURSANTES ====================

@app.get("/api/concursantes", response_model=list[ConcursanteSchema])
def get_concursantes(db: Session = Depends(get_db)):
    """Obtener todos los concursantes"""
    return db.query(Concursante).all()

@app.post("/api/concursantes", response_model=ConcursanteSchema)
def create_concursante(concursante: ConcursanteCreate, db: Session = Depends(get_db)):
    """Crear un nuevo concursante"""
    # Verificar que no exista
    db_concursante = db.query(Concursante).filter(
        Concursante.nombre == concursante.nombre
    ).first()
    if db_concursante:
        raise HTTPException(status_code=400, detail="Concursante ya existe")
    
    new_concursante = Concursante(**concursante.dict())
    db.add(new_concursante)
    db.commit()
    db.refresh(new_concursante)
    return new_concursante


@app.post("/api/concursantes/{concursante_id}/photo")
def upload_concursante_photo(concursante_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Subir foto tipo carnet para un concursante"""
    db_concursante = db.query(Concursante).filter(Concursante.id == concursante_id).first()
    if not db_concursante:
        raise HTTPException(status_code=404, detail="Concursante no encontrado")

    filename = f"conc_{concursante_id}_{int(datetime.utcnow().timestamp())}_{file.filename}"
    safe_path = os.path.join(PHOTOS_DIR, filename)
    try:
        with open(safe_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()

    db_concursante.photo_filename = filename
    db.add(db_concursante)
    db.commit()
    db.refresh(db_concursante)
    return {"message": "Foto subida", "photo_url": db_concursante.photo_url}

@app.get("/api/concursantes/{concursante_id}", response_model=ConcursanteSchema)
def get_concursante(concursante_id: int, db: Session = Depends(get_db)):
    """Obtener detalles de un concursante"""
    db_concursante = db.query(Concursante).filter(
        Concursante.id == concursante_id
    ).first()
    if not db_concursante:
        raise HTTPException(status_code=404, detail="Concursante no encontrado")
    return db_concursante

@app.put("/api/concursantes/{concursante_id}", response_model=ConcursanteSchema)
def update_concursante(
    concursante_id: int, 
    concursante: ConcursanteCreate, 
    db: Session = Depends(get_db)
):
    """Actualizar concursante"""
    db_concursante = db.query(Concursante).filter(
        Concursante.id == concursante_id
    ).first()
    if not db_concursante:
        raise HTTPException(status_code=404, detail="Concursante no encontrado")
    
    for key, value in concursante.dict().items():
        setattr(db_concursante, key, value)
    
    db.commit()
    db.refresh(db_concursante)
    return db_concursante

@app.delete("/api/concursantes/{concursante_id}")
def delete_concursante(concursante_id: int, db: Session = Depends(get_db)):
    """Eliminar concursante"""
    db_concursante = db.query(Concursante).filter(
        Concursante.id == concursante_id
    ).first()
    if not db_concursante:
        raise HTTPException(status_code=404, detail="Concursante no encontrado")
    
    db.delete(db_concursante)
    db.commit()
    return {"message": "Concursante eliminado"}

# ==================== RUTAS COMPETICIONES ====================

@app.get("/api/competiciones", response_model=list[CompeticionSchema])
def get_competiciones(db: Session = Depends(get_db)):
    """Obtener todas las competiciones"""
    return db.query(Competicion).all()

@app.post("/api/competiciones", response_model=CompeticionSchema)
def create_competicion(competicion: CompeticionCreate, db: Session = Depends(get_db)):
    """Crear una nueva competición"""
    new_competicion = Competicion(**competicion.dict())
    db.add(new_competicion)
    db.commit()
    db.refresh(new_competicion)
    return new_competicion

@app.get("/api/competiciones/{competicion_id}", response_model=CompeticionSchema)
def get_competicion(competicion_id: int, db: Session = Depends(get_db)):
    """Obtener detalles de una competición"""
    db_competicion = db.query(Competicion).filter(
        Competicion.id == competicion_id
    ).first()
    if not db_competicion:
        raise HTTPException(status_code=404, detail="Competición no encontrada")
    # Construir respuesta con levantamientos y datos del concursante embebidos
    levantamientos = []
    for l in db_competicion.levantamientos:
        levantamientos.append({
            "id": l.id,
            "concursante_id": l.concursante_id,
            "concursante": {
                "id": l.concursante.id,
                "nombre": l.concursante.nombre,
                "sexo": l.concursante.sexo,
                "categoria_peso": l.concursante.categoria_peso,
                "photo_url": l.concursante.photo_url
            },
            "sentadilla": l.sentadilla,
            "press_banca": l.press_banca,
            "peso_muerto": l.peso_muerto,
            "total": l.sentadilla + l.press_banca + l.peso_muerto,
            "ipf_score": l.ipf_score,
            "fecha_levantamiento": l.fecha_levantamiento.isoformat()
        })

    return {
        "id": db_competicion.id,
        "nombre": db_competicion.nombre,
        "fecha": db_competicion.fecha.isoformat() if db_competicion.fecha else None,
        "ubicacion": db_competicion.ubicacion,
        "descripcion": db_competicion.descripcion,
        "levantamientos": levantamientos
    }

# ==================== RUTAS LEVANTAMIENTOS ====================

@app.get("/api/levantamientos", response_model=list[LevantamientoSchema])
def get_levantamientos(db: Session = Depends(get_db)):
    """Obtener todos los levantamientos"""
    return db.query(Levantamiento).all()

@app.post("/api/levantamientos", response_model=LevantamientoSchema)
def create_levantamiento(levantamiento: LevantamientoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo levantamiento y calcular IPF"""
    # Verificar que exista el concursante
    db_concursante = db.query(Concursante).filter(
        Concursante.id == levantamiento.concursante_id
    ).first()
    if not db_concursante:
        raise HTTPException(status_code=404, detail="Concursante no encontrado")
    
    # Calcular IPF
    total = levantamiento.sentadilla + levantamiento.press_banca + levantamiento.peso_muerto
    ipf_score = calculate_ipf_points(
        total, 
        db_concursante.categoria_peso, 
        db_concursante.sexo
    )
    
    new_levantamiento = Levantamiento(
        **levantamiento.dict(),
        ipf_score=ipf_score
    )
    db.add(new_levantamiento)
    db.commit()
    db.refresh(new_levantamiento)
    return new_levantamiento

@app.get("/api/levantamientos/concursante/{concursante_id}", response_model=list[LevantamientoSchema])
def get_levantamientos_concursante(concursante_id: int, db: Session = Depends(get_db)):
    """Obtener todos los levantamientos de un concursante"""
    return db.query(Levantamiento).filter(
        Levantamiento.concursante_id == concursante_id
    ).all()

# ==================== RUTAS RANKING ====================

@app.get("/api/ranking")
def get_ranking(db: Session = Depends(get_db)):
    """Obtener ranking de concursantes por IPF"""
    levantamientos = db.query(Levantamiento).all()
    ranking = sorted(
        [
            {
                "concursante_id": l.concursante_id,
                "nombre": l.concursante.nombre,
                "sexo": l.concursante.sexo,
                "categoria_peso": l.concursante.categoria_peso,
                "total": l.sentadilla + l.press_banca + l.peso_muerto,
                "ipf_score": l.ipf_score,
                "sentadilla": l.sentadilla,
                "press_banca": l.press_banca,
                "peso_muerto": l.peso_muerto
            }
            for l in levantamientos
        ],
        key=lambda x: x['ipf_score'],
        reverse=True
    )
    return ranking

@app.get("/api/ranking/{categoria}")
def get_ranking_categoria(categoria: str, db: Session = Depends(get_db)):
    """Obtener ranking por categoría de peso"""
    levantamientos = db.query(Levantamiento).all()
    ranking = sorted(
        [
            {
                "concursante_id": l.concursante_id,
                "nombre": l.concursante.nombre,
                "sexo": l.concursante.sexo,
                "total": l.sentadilla + l.press_banca + l.peso_muerto,
                "ipf_score": l.ipf_score,
                "sentadilla": l.sentadilla,
                "press_banca": l.press_banca,
                "peso_muerto": l.peso_muerto
            }
            for l in levantamientos
            if l.concursante.categoria_peso == categoria
        ],
        key=lambda x: x['ipf_score'],
        reverse=True
    )
    return ranking


@app.get("/api/records")
def get_records(db: Session = Depends(get_db)):
    """Obtener records por categoría (mejores levantamientos)"""
    levantamientos = db.query(Levantamiento).all()
    records = {}
    for l in levantamientos:
        cat = l.concursante.categoria_peso
        total = l.sentadilla + l.press_banca + l.peso_muerto
        if cat not in records:
            records[cat] = {
                "categoria": cat,
                "sentadilla": l.sentadilla,
                "press_banca": l.press_banca,
                "peso_muerto": l.peso_muerto,
                "total": total,
                "ipf_score": l.ipf_score,
                "concursante": l.concursante.nombre
            }
        else:
            # comparar y actualizar
            if l.sentadilla > records[cat]["sentadilla"]:
                records[cat]["sentadilla"] = l.sentadilla
            if l.press_banca > records[cat]["press_banca"]:
                records[cat]["press_banca"] = l.press_banca
            if l.peso_muerto > records[cat]["peso_muerto"]:
                records[cat]["peso_muerto"] = l.peso_muerto
            if total > records[cat]["total"]:
                records[cat]["total"] = total
                records[cat]["concursante"] = l.concursante.nombre
            if l.ipf_score > records[cat]["ipf_score"]:
                records[cat]["ipf_score"] = l.ipf_score

    # devolver lista ordenada por categoría
    return list(records.values())

# ==================== RUTAS ESTADÍSTICAS ====================

@app.get("/api/estadisticas")
def get_estadisticas(db: Session = Depends(get_db)):
    """Obtener estadísticas generales"""
    total_concursantes = db.query(Concursante).count()
    total_competiciones = db.query(Competicion).count()
    total_levantamientos = db.query(Levantamiento).count()
    
    levantamientos = db.query(Levantamiento).all()
    mejor_ipf = max([l.ipf_score for l in levantamientos], default=0) if levantamientos else 0
    
    return {
        "total_concursantes": total_concursantes,
        "total_competiciones": total_competiciones,
        "total_levantamientos": total_levantamientos,
        "mejor_ipf": mejor_ipf
    }

# ==================== RUTA SALUD ====================

@app.get("/")
def read_root():
    """Health check"""
    return {"message": "Powerlifting API - Hermandad Cubana", "status": "online"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
