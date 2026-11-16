
from models.nodo import Nodo


class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    def _obtener_altura(self, nodo):
        return nodo.altura if nodo else 0

    def _factor_balance(self, nodo):
        if nodo is None:
            return 0
        return self._obtener_altura(nodo.izq) - self._obtener_altura(nodo.der)

    def _actualizar_altura(self, nodo):
        nodo.altura = 1 + max(self._obtener_altura(nodo.izq), self._obtener_altura(nodo.der))
    #AVL ROTA

    def _rotacion_derecha(self, y):
        x = y.izq
        t2 = x.der

        
        x.der = y
        y.izq = t2

        
        self._actualizar_altura(y)
        self._actualizar_altura(x)
        return x

    def _rotacion_izquierda(self, x):
        y = x.der
        t2 = y.izq

    
        y.izq = x
        x.der = t2

    
        self._actualizar_altura(x)
        self._actualizar_altura(y)
        return y

    def _balancear(self, nodo):
        if nodo is None:
            return None

        self._actualizar_altura(nodo)
        balance = self._factor_balance(nodo)

        # Caso Izquierda - Izquierda
        if balance > 1 and self._factor_balance(nodo.izq) >= 0:
            return self._rotacion_derecha(nodo)

        # Caso Izquierda - Derecha
        if balance > 1 and self._factor_balance(nodo.izq) < 0:
            nodo.izq = self._rotacion_izquierda(nodo.izq)
            return self._rotacion_derecha(nodo)

        # Caso Derecha - Derecha
        if balance < -1 and self._factor_balance(nodo.der) <= 0:
            return self._rotacion_izquierda(nodo)

        # Caso Derecha - Izquierda
        if balance < -1 and self._factor_balance(nodo.der) > 0:
            nodo.der = self._rotacion_derecha(nodo.der)
            return self._rotacion_izquierda(nodo)

        return nodo
    
    #METODOS   
    def insertar(self, valor):
        """Inserta un valor numérico"""
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self.raiz = self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, actual, valor):
            if actual is None:
                return Nodo(valor)
    
            if valor < actual.valor:
                actual.izq = self._insertar_recursivo(actual.izq, valor)
            elif valor > actual.valor:
                actual.der = self._insertar_recursivo(actual.der, valor)
            else:
                return actual 
    
            return self._balancear(actual)

    def hoja(self, valor):
        """Busqueda y verificacion de si es hoja
           Retorna un valor booleano """
        nodo = self._buscar_nodo(self.raiz, valor)
        if nodo is None:
            return False  
        return nodo.es_hoja()

    def _buscar_nodo(self, actual, valor):
        if actual is None or actual.valor == valor:
            return actual
        if valor < actual.valor:
            return self._buscar_nodo(actual.izq, valor)
        return self._buscar_nodo(actual.der, valor)

    #ELIMINAR

    def _nodo_con_valor_minimo(self, nodo):
        """Encuentra el sucesor inorden (el nodo más a la izquierda)."""
        actual = nodo
        while actual.izq is not None:
            actual = actual.izq
        return actual

    def eliminar(self, valor):
        try:
            valor = float(valor) if '.' in str(valor) else int(valor)
        except ValueError:
            pass
        self.raiz = self._eliminar_recursivo(self.raiz, valor)

    def _eliminar_recursivo(self, actual, valor):
        if actual is None:
            return None

        if valor < actual.valor:
            actual.izq = self._eliminar_recursivo(actual.izq, valor)
        elif valor > actual.valor:
            actual.der = self._eliminar_recursivo(actual.der, valor)
        else:
          
            if actual.izq is None:
                temp = actual.der
                return temp
            elif actual.der is None:
                temp = actual.izq
                return temp

        
            temp = self._nodo_con_valor_minimo(actual.der)
            actual.valor = temp.valor
            actual.der = self._eliminar_recursivo(actual.der, temp.valor)

       
        return self._balancear(actual)
   
    def to_dict(self):
        """Retorna el árbol como diccionario o None si está vacío."""
        return self.raiz.to_dict() if self.raiz else None
    #RECORRIDOS 

    def inorden(self):
        """Recorrido InOrden: Izquierda -> Raíz -> Derecha"""
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado

    def _inorden_recursivo(self, actual, resultado):
        if actual is not None:
            self._inorden_recursivo(actual.izq, resultado)
            resultado.append(actual.valor)
            self._inorden_recursivo(actual.der, resultado)

    def preorden(self):
        """Recorrido PreOrden: Raíz -> Izquierda -> Derecha"""
        resultado = []
        self._preorden_recursivo(self.raiz, resultado)
        return resultado

    def _preorden_recursivo(self, actual, resultado):
        if actual is not None:
            resultado.append(actual.valor)
            self._preorden_recursivo(actual.izq, resultado)
            self._preorden_recursivo(actual.der, resultado)

    def postorden(self):
        """Recorrido PostOrden: Izquierda -> Derecha -> Raíz"""
        resultado = []
        self._postorden_recursivo(self.raiz, resultado)
        return resultado

    def _postorden_recursivo(self, actual, resultado):
        if actual is not None:
            self._postorden_recursivo(actual.izq, resultado)
            self._postorden_recursivo(actual.der, resultado)
            resultado.append(actual.valor)