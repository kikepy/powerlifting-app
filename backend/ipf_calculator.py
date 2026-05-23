# Coeficientes IPF actualizados (varía según categoría de peso y sexo)
# Estos son valores aproximados - ajusta según necesites

# Para cálculos simplificados, usamos la fórmula del IPF points
# IPF Points = (Total Lifted / Coeff) * 100

# Coeficientes por categoría de peso (hombres)
COEFFICIENTS_MEN = {
    "59": 0.72,
    "66": 0.84,
    "74": 0.94,
    "83": 1.02,
    "93": 1.10,
    "105": 1.14,
    "120": 1.18,
    "+120": 1.20
}

# Coeficientes por categoría de peso (mujeres)
COEFFICIENTS_WOMEN = {
    "47": 0.89,
    "52": 0.98,
    "57": 1.04,
    "63": 1.10,
    "69": 1.15,
    "76": 1.20,
    "84": 1.25,
    "+84": 1.30
}

def calculate_ipf_points(total_lifted, categoria_peso, sexo):
    """
    Calcula los puntos IPF según el total levantado y la categoría de peso.
    
    Args:
        total_lifted: Total en kg (sentadilla + press_banca + peso_muerto)
        categoria_peso: Categoría de peso (ej: "59", "66", etc)
        sexo: "M" para hombre, "F" para mujer
    
    Returns:
        float: Puntos IPF
    """
    try:
        if sexo.upper() == "M":
            coeff = COEFFICIENTS_MEN.get(categoria_peso, 1.0)
        else:  # Mujer or "F"
            coeff = COEFFICIENTS_WOMEN.get(categoria_peso, 1.0)
        
        ipf_points = (total_lifted / coeff) * 100
        return round(ipf_points, 2)
    except Exception:
        return 0.0

def get_ranking_by_category(levantamientos_list, sexo, categoria_peso):
    """
    Crea un ranking de concursantes por categoría.
    """
    ranking = sorted(
        levantamientos_list,
        key=lambda x: x['ipf_score'],
        reverse=True
    )
    return ranking
