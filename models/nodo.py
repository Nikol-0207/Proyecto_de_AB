class Nodo:
    def __init__(self, valor):
        
        self.valor = valor
        self.izq = None
        self.der = None
        self._altura = 1

    # --- GETTERS Y SETTERS ---

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, nuevo_valor):
        self._valor = nuevo_valor

    @property
    def izq(self):
        return self._izq

    @izq.setter
    def izq(self, nodo):
        if nodo is not None and not isinstance(nodo, Nodo):
            raise TypeError("El hijo izquierdo debe ser una instancia de Nodo o None")
        self._izq = nodo

    @property
    def der(self):
        return self._der

    @der.setter
    def der(self, nodo):
        if nodo is not None and not isinstance(nodo, Nodo):
            raise TypeError("El hijo derecho debe ser una instancia de Nodo o None")
        self._der = nodo

    @property
    def altura(self):
        return self._altura

    @altura.setter
    def altura(self, nueva_altura):
        self._altura = nueva_altura
    # ------------------------------

    def es_hoja(self):
        """Verifica si tiene hijos para ser considerada hoja"""
        return self._izq is None and self._der is None
    def to_dict(self):
        """Serializa recursivamente el nodo para la API JSON."""
        return {
            "valor": self._valor,
            "izq": self._izq.to_dict() if self._izq else None,
            "der": self._der.to_dict() if self._der else None
        }
    