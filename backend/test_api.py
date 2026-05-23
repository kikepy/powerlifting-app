#!/usr/bin/env python
"""
Script de prueba para la API de Powerlifting
Crea datos de ejemplo para pruebas
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api"

def print_response(response, title=""):
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def create_sample_data():
    """Crea datos de ejemplo para pruebas"""
    
    print("\n🏋️ INICIALIZANDO DATOS DE PRUEBA...")
    
    # 1. Crear concursantes
    print("\n1️⃣ Creando concursantes...")
    concursantes = [
        {
            "nombre": "Carlos López",
            "edad": 26,
            "peso_corporal": 74.5,
            "sexo": "M",
            "categoria_peso": "74",
            "club": "Powerlifting Fuerte",
            "ciudad": "La Habana",
            "ano_inicio": 2019
        },
        {
            "nombre": "María García",
            "edad": 23,
            "peso_corporal": 57.0,
            "sexo": "F",
            "categoria_peso": "57",
            "club": "Atletas de Cuba",
            "ciudad": "Santiago",
            "ano_inicio": 2021
        },
        {
            "nombre": "Juan Martínez",
            "edad": 29,
            "peso_corporal": 93.0,
            "sexo": "M",
            "categoria_peso": "93",
            "club": "Elite Power",
            "ciudad": "Matanzas",
            "ano_inicio": 2018
        },
        {
            "nombre": "Ana Rodríguez",
            "edad": 27,
            "peso_corporal": 69.0,
            "sexo": "F",
            "categoria_peso": "69",
            "club": "Strong Women",
            "ciudad": "Camagüey",
            "ano_inicio": 2020
        }
    ]
    
    concursante_ids = []
    for concursante in concursantes:
        try:
            response = requests.post(f"{BASE_URL}/concursantes", json=concursante)
            if response.status_code == 200:
                data = response.json()
                concursante_ids.append(data['id'])
                print(f"  ✅ {concursante['nombre']} (ID: {data['id']})")
            else:
                print(f"  ❌ Error al crear {concursante['nombre']}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    # 2. Crear competiciones
    print("\n2️⃣ Creando competiciones...")
    competiciones = [
        {
            "nombre": "Campeonato Nacional 2024",
            "fecha": (datetime.now() + timedelta(days=30)).isoformat(),
            "ubicacion": "La Habana",
            "descripcion": "Campeonato anual de powerlifting"
        },
        {
            "nombre": "Open Regional",
            "fecha": (datetime.now() + timedelta(days=60)).isoformat(),
            "ubicacion": "Santiago de Cuba",
            "descripcion": "Competencia regional abierta"
        }
    ]
    
    competicion_ids = []
    for competicion in competiciones:
        try:
            response = requests.post(f"{BASE_URL}/competiciones", json=competicion)
            if response.status_code == 200:
                data = response.json()
                competicion_ids.append(data['id'])
                print(f"  ✅ {competicion['nombre']} (ID: {data['id']})")
            else:
                print(f"  ❌ Error al crear {competicion['nombre']}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    # 3. Crear levantamientos
    print("\n3️⃣ Creando levantamientos...")
    levantamientos_data = [
        {"concursante_id": 1, "sentadilla": 180, "press_banca": 110, "peso_muerto": 210},
        {"concursante_id": 1, "sentadilla": 185, "press_banca": 115, "peso_muerto": 215},
        {"concursante_id": 2, "sentadilla": 120, "press_banca": 60, "peso_muerto": 150},
        {"concursante_id": 3, "sentadilla": 220, "press_banca": 150, "peso_muerto": 260},
        {"concursante_id": 4, "sentadilla": 140, "press_banca": 70, "peso_muerto": 170},
    ]
    
    for lev in levantamientos_data:
        try:
            response = requests.post(f"{BASE_URL}/levantamientos", json=lev)
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ Levantamiento registrado (IPF: {data['ipf_score']})")
            else:
                print(f"  ❌ Error: {response.json()}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n✅ DATOS DE PRUEBA CREADOS EXITOSAMENTE")
    print("\nPrueba estos endpoints:")
    print(f"  - GET {BASE_URL}/concursantes")
    print(f"  - GET {BASE_URL}/ranking")
    print(f"  - GET {BASE_URL}/ranking/74")
    print(f"  - GET {BASE_URL}/estadisticas")

def test_endpoints():
    """Prueba los endpoints principales"""
    
    print("\n🔍 PROBANDO ENDPOINTS...")
    
    # Test: Obtener todos los concursantes
    try:
        response = requests.get(f"{BASE_URL}/concursantes")
        print_response(response, "GET /concursantes")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test: Obtener ranking
    try:
        response = requests.get(f"{BASE_URL}/ranking")
        print_response(response, "GET /ranking")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test: Obtener estadísticas
    try:
        response = requests.get(f"{BASE_URL}/estadisticas")
        print_response(response, "GET /estadisticas")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("🏋️ POWERLIFTING API - SCRIPT DE PRUEBA")
    print("="*60)
    
    try:
        # Verificar conexión
        response = requests.get("http://localhost:8000")
        print("✅ Servidor conectado en http://localhost:8000")
        
        # Crear datos de prueba
        create_sample_data()
        
        # Probar endpoints
        test_endpoints()
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor en http://localhost:8000")
        print("   Asegúrate de que el servidor FastAPI está corriendo:")
        print("   cd backend && python main.py")
    except Exception as e:
        print(f"❌ Error: {e}")
