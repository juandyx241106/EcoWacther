def generar_recomendaciones(inputs, score):
    """Generar recomendaciones basadas en el ecoscore y variables individuales."""
    recomendaciones = []

    # ===== CATEGORÍA GENERAL =====
    if score < 200:
        recomendaciones.append(
            {
                "texto": "El ecosistema está en estado CRÍTICO. Se requiere intervención urgente.",
                "clase": "critico",
            }
        )
    elif score < 350:
        recomendaciones.append(
            {
                "texto": "Estado MODERADO: hay problemas, pero pueden mejorarse con acciones continuas.",
                "clase": "moderado",
            }
        )
    elif score < 450:
        recomendaciones.append(
            {
                "texto": "Estado BUENO: sigue fortaleciendo los aspectos ambientales.",
                "clase": "bueno",
            }
        )
    else:
        recomendaciones.append(
            {
                "texto": "¡Excelente estado ambiental! Mantén las prácticas actuales.",
                "clase": "excelente",
            }
        )

    # ===== VARIABLES INDIVIDUALES =====
    if inputs["ha_verdes_km2"] < 5:
        recomendaciones.append(
            {
                "texto": "Muy pocas hectáreas verdes. Se recomienda ampliar zonas verdes.",
                "clase": "critico",
            }
        )
    elif inputs["ha_verdes_km2"] < 10:
        recomendaciones.append(
            {
                "texto": "Las zonas verdes son bajas. Plantar árboles ayudaría.",
                "clase": "moderado",
            }
        )

    if inputs["cobertura_arbolado_pct"] < 10:
        recomendaciones.append(
            {
                "texto": "Cobertura arbórea muy baja. Urgente reforestación.",
                "clase": "critico",
            }
        )
    elif inputs["cobertura_arbolado_pct"] < 20:
        recomendaciones.append(
            {
                "texto": "Aumentar árboles mejoraría la calidad ambiental.",
                "clase": "moderado",
            }
        )

    if inputs["pm25"] > 40:
        recomendaciones.append(
            {
                "texto": "PM2.5 extremadamente alto. Revisar fuentes de contaminación.",
                "clase": "critico",
            }
        )
    elif inputs["pm25"] > 25:
        recomendaciones.append(
            {"texto": "PM2.5 elevado. Reducir emisiones ayudaría.", "clase": "moderado"}
        )

    if inputs["pm10"] > 60:
        recomendaciones.append(
            {
                "texto": "PM10 elevado. Revisar fuentes de partículas.",
                "clase": "moderado",
            }
        )

    if inputs["residuos_no_gestionados"] > 0.7:
        recomendaciones.append(
            {
                "texto": "Muchos residuos sin gestionar. Mejorar manejo de basuras.",
                "clase": "critico",
            }
        )
    elif inputs["residuos_no_gestionados"] > 0.3:
        recomendaciones.append(
            {"texto": "Manejo de residuos mejorable.", "clase": "moderado"}
        )

    if inputs["porcentaje_reciclaje"] < 10:
        recomendaciones.append(
            {
                "texto": "Reciclaje muy bajo. Incrementarlo ayudaría mucho.",
                "clase": "critico",
            }
        )
    elif inputs["porcentaje_reciclaje"] < 25:
        recomendaciones.append(
            {"texto": "Se puede mejorar el reciclaje.", "clase": "moderado"}
        )

    if inputs["porcentaje_transporte_limpio"] < 10:
        recomendaciones.append(
            {
                "texto": "Muy poco transporte limpio. Fomentar medios sostenibles.",
                "clase": "critico",
            }
        )
    elif inputs["porcentaje_transporte_limpio"] < 25:
        recomendaciones.append(
            {
                "texto": "Incrementar transporte limpio sería beneficioso.",
                "clase": "moderado",
            }
        )

    return recomendaciones
