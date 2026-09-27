import itertools
import time

# ============================================
# DATOS DEL PROBLEMA
# ============================================
# Representa el conjunto de objetos disponibles.
# Cada objeto es un diccionario con su id, peso (en kg) y valor (en $)
OBJETOS_DISPONIBLES = [
    {"id": 1, "peso": 2, "valor": 10},
    {"id": 2, "peso": 3, "valor": 15},
    {"id": 3, "peso": 5, "valor": 25},
    {"id": 4, "peso": 7, "valor": 30},
    {"id": 5, "peso": 1, "valor": 5},
    {"id": 6, "peso": 4, "valor": 20},
    {"id": 7, "peso": 6, "valor": 18}
]

# Capacidad máxima que soporta la mochila
CAPACIDAD_MAXIMA = 15

# ============================================
# ALGORITMO DE BÚSQUEDA EXHAUSTIVA (FUERZA BRUTA)
# ============================================
def busqueda_exhaustiva(objetos, capacidad):
    """
    Implementación del algoritmo de Búsqueda Exhaustiva (Fuerza Bruta).

    Explora todo el espacio de estados generando todas las combinaciones
    posibles de objetos (2^n combinaciones). Garantiza encontrar la 
    solución óptima global, pero tiene una complejidad temporal exponencial.

    Parámetros:
    - objetos: lista de diccionarios que representan los objetos disponibles.
    - capacidad: peso máximo que soporta la mochila.

    Retorna:
    - Lista con los objetos seleccionados que maximizan el valor.
    - Peso total de la combinación óptima.
    - Valor total de la combinación óptima.
    - Número de combinaciones evaluadas (similar a nodos expandidos).
    """
    mejor_valor = 0
    mejor_combinacion = []
    mejor_peso = 0
    combinaciones_evaluadas = 0

    # Generar todas las combinaciones posibles (desde 1 objeto hasta todos)
    for r in range(1, len(objetos) + 1):
        for combinacion in itertools.combinations(objetos, r):
            combinaciones_evaluadas += 1
            
            # Calcular el peso y valor acumulado de la combinación actual
            peso_actual = sum(obj["peso"] for obj in combinacion)
            valor_actual = sum(obj["valor"] for obj in combinacion)
            
            # Verificar si es válida (no supera el peso) y si mejora la ganancia conocida
            if peso_actual <= capacidad and valor_actual > mejor_valor:
                mejor_valor = valor_actual
                mejor_combinacion = list(combinacion)
                mejor_peso = peso_actual
                
    return mejor_combinacion, mejor_peso, mejor_valor, combinaciones_evaluadas


# ============================================
# ALGORITMOS DE BÚSQUEDA GREEDY (VORAZ)
# ============================================
def busqueda_greedy(objetos, capacidad, criterio):
    """
    Implementación del algoritmo de Búsqueda Greedy (Voraz).

    Construye la solución paso a paso seleccionando el mejor objeto disponible
    según una heurística o criterio local, sin retroceder (no backtracking).
    Es muy rápido pero no garantiza encontrar la solución óptima global.

    Parámetros:
    - objetos: lista de diccionarios que representan los objetos disponibles.
    - capacidad: peso máximo que soporta la mochila.
    - criterio: string ('valor', 'peso', o 'densidad') que define la heurística.

    Retorna:
    - Lista con los objetos seleccionados.
    - Peso total acumulado.
    - Valor total acumulado.
    - Número de objetos evaluados.
    """
    # Hacemos una copia profunda superficial para no modificar el orden de la lista original
    objetos_ordenados = objetos.copy()
    
    # Ordenar los objetos dependiendo de la variante elegida
    if criterio == 'valor':
        # Prioridad: Mayor valor monetario (de mayor a menor)
        objetos_ordenados.sort(key=lambda x: x["valor"], reverse=True)
    elif criterio == 'peso':
        # Prioridad: Menor peso físico (de menor a mayor)
        objetos_ordenados.sort(key=lambda x: x["peso"])
    elif criterio == 'densidad':
        # Prioridad: Mejor relación Valor/Peso (de mayor a menor)
        objetos_ordenados.sort(key=lambda x: x["valor"] / x["peso"], reverse=True)
        
    mochila = []
    peso_total = 0
    valor_total = 0
    objetos_evaluados = 0
    
    # Recorrer los objetos ordenados e intentar meterlos en la mochila
    for obj in objetos_ordenados:
        objetos_evaluados += 1
        # Si el objeto actual cabe en el espacio restante de la mochila
        if peso_total + obj["peso"] <= capacidad:
            mochila.append(obj)
            peso_total += obj["peso"]
            valor_total += obj["valor"]
            
    return mochila, peso_total, valor_total, objetos_evaluados


# ====================================================================================================================================
# EJECUCIÓN PRINCIPAL (Comparativa de algoritmos)
# ====================================================================================================================================
if __name__ == "__main__":
    
    print("=" * 60)
    print("RESOLVIENDO EL PROBLEMA DE LA MOCHILA")
    print(f"Capacidad máxima: {CAPACIDAD_MAXIMA} kg | Objetos disponibles: {len(OBJETOS_DISPONIBLES)}")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. BÚSQUEDA EXHAUSTIVA
    # ---------------------------------------------------------
    print("\n" + "-" * 50)
    print("BUSCANDO SOLUCIÓN CON EXHAUSTIVA (FUERZA BRUTA)")
    print("-" * 50)
    
    inicio_t = time.perf_counter()
    sol_fb, peso_fb, valor_fb, eval_fb = busqueda_exhaustiva(OBJETOS_DISPONIBLES, CAPACIDAD_MAXIMA)
    tiempo_fb = time.perf_counter() - inicio_t

    if sol_fb:
        ids_fb = [obj["id"] for obj in sol_fb]
        print(f"Objetos seleccionados: {ids_fb}")
        print(f"Peso Total: {peso_fb} kg / {CAPACIDAD_MAXIMA} kg")
        print(f"Valor Total Obtenido: ${valor_fb}")
        print(f"Combinaciones evaluadas: {eval_fb}")
        print(f"Tiempo: {tiempo_fb:.6f} segundos")

    # ---------------------------------------------------------
    # 2. GREEDY VARIANTE A (Por Valor)
    # ---------------------------------------------------------
    print("\n" + "-" * 50)
    print("BUSCANDO SOLUCIÓN CON GREEDY (Por Valor)")
    print("-" * 50)
    
    inicio_t = time.perf_counter()
    sol_gv, peso_gv, valor_gv, eval_gv = busqueda_greedy(OBJETOS_DISPONIBLES, CAPACIDAD_MAXIMA, 'valor')
    tiempo_gv = time.perf_counter() - inicio_t

    if sol_gv:
        ids_gv = [obj["id"] for obj in sol_gv]
        print(f"Objetos seleccionados: {ids_gv}")
        print(f"Peso Total: {peso_gv} kg / {CAPACIDAD_MAXIMA} kg")
        print(f"Valor Total Obtenido: ${valor_gv}")
        print(f"Objetos evaluados: {eval_gv}")
        print(f"Tiempo: {tiempo_gv:.6f} segundos")

    # ---------------------------------------------------------
    # 3. GREEDY VARIANTE B (Por Peso)
    # ---------------------------------------------------------
    print("\n" + "-" * 50)
    print("BUSCANDO SOLUCIÓN CON GREEDY (Por Peso)")
    print("-" * 50)
    
    inicio_t = time.perf_counter()
    sol_gp, peso_gp, valor_gp, eval_gp = busqueda_greedy(OBJETOS_DISPONIBLES, CAPACIDAD_MAXIMA, 'peso')
    tiempo_gp = time.perf_counter() - inicio_t

    if sol_gp:
        ids_gp = [obj["id"] for obj in sol_gp]
        print(f"Objetos seleccionados: {ids_gp}")
        print(f"Peso Total: {peso_gp} kg / {CAPACIDAD_MAXIMA} kg")
        print(f"Valor Total Obtenido: ${valor_gp}")
        print(f"Objetos evaluados: {eval_gp}")
        print(f"Tiempo: {tiempo_gp:.6f} segundos")

    # ---------------------------------------------------------
    # 4. GREEDY VARIANTE C (Por Densidad)
    # ---------------------------------------------------------
    print("\n" + "-" * 50)
    print("BUSCANDO SOLUCIÓN CON GREEDY (Por Densidad)")
    print("-" * 50)
    
    inicio_t = time.perf_counter()
    sol_gd, peso_gd, valor_gd, eval_gd = busqueda_greedy(OBJETOS_DISPONIBLES, CAPACIDAD_MAXIMA, 'densidad')
    tiempo_gd = time.perf_counter() - inicio_t

    if sol_gd:
        ids_gd = [obj["id"] for obj in sol_gd]
        print(f"Objetos seleccionados: {ids_gd}")
        print(f"Peso Total: {peso_gd} kg / {CAPACIDAD_MAXIMA} kg")
        print(f"Valor Total Obtenido: ${valor_gd}")
        print(f"Objetos evaluados: {eval_gd}")
        print(f"Tiempo: {tiempo_gd:.6f} segundos")

    # ---------------------------------------------------------
    # RESUMEN FINAL
    # ---------------------------------------------------------
    print("\n" + "=" * 60)
    print("RESUMEN FINAL DE ESTRATEGIAS")
    print("=" * 60)
    print(f"{'Algoritmo':<20} | {'Valor ($)':<10} | {'Peso (kg)':<10} | {'Evaluaciones':<13} | {'Tiempo (s)':<12}")
    print("-" * 75)
    print(f"{'Fuerza Bruta':<20} | {valor_fb:<10} | {peso_fb:<10} | {eval_fb:<13} | {tiempo_fb:.6f}")
    print(f"{'Greedy (Valor)':<20} | {valor_gv:<10} | {peso_gv:<10} | {eval_gv:<13} | {tiempo_gv:.6f}")
    print(f"{'Greedy (Peso)':<20} | {valor_gp:<10} | {peso_gp:<10} | {eval_gp:<13} | {tiempo_gp:.6f}")
    print(f"{'Greedy (Densidad)':<20} | {valor_gd:<10} | {peso_gd:<10} | {eval_gd:<13} | {tiempo_gd:.6f}")
    
    print("\nPrograma finalizado correctamente")