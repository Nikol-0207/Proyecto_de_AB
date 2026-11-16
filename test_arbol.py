from models.arbol_binario import ArbolBinarioBusqueda
def imprimir_arbol(nodo, prefijo="", es_izq=True):
    """Imprime el árbol de forma visual en la terminal."""
    if nodo is not None:
        print(prefijo + ("|-- " if es_izq else "\\-- ") + f"[{nodo.valor}] (h={nodo.altura})")
        imprimir_arbol(nodo.izq, prefijo + ("|   " if es_izq else "    "), True)
        imprimir_arbol(nodo.der, prefijo + ("|   " if es_izq else "    "), False)

def probar_abb():
    print("=" * 40)
    print(" PRUEBA: ÁRBOL BINARIO DE BÚSQUEDA (ABB)")
    print("=" * 40)
    
    abb = ArbolBinarioBusqueda()
    valores = [10, 20, 30, 40, 50, 60, 70]
    
    print(f"Insertando valores: {valores}")
    for v in valores:
        abb.insertar(v)
        
    print("\n--- Verificación de Hojas y Ramas ---")
    for v in [50, 30, 20, 40, 70, 80, 99]:
        es_h = abb.hoja(v)
        print(f"¿El valor {v} es hoja?: {es_h}")
    print("Estructura del árbol balanceado:")
    imprimir_arbol(abb.raiz)
    print(f"\nRaíz resultante: {abb.raiz.valor}")

   
if __name__ == "__main__":
    probar_abb()