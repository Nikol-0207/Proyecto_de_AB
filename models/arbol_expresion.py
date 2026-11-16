from models.nodo import Nodo


class ArbolExpresion:
    OPERADORES = {'+', '-', '*', '/'}
    PRECEDENCIA = {'+': 1, '-': 1, '*': 2, '/': 2}

    def __init__(self):
        self.raiz = None

    # --- ENTRADA INFIJA ---

    def insertar_infija(self, expresion):
        """Construye el árbol a partir de una expresión infija. Ej: '(3 + 4) * 2'"""
        tokens = self._tokenizar(expresion)
        postfija = self._infija_a_postfija(tokens)
        self.raiz = self._construir_desde_postfija(postfija)
        return self.raiz

    # --- ENTRADA POSTFIJA ---

    def insertar_postfija(self, expresion):
        """Construye el árbol a partir de una expresión postfija. Ej: '2 3 5 * +' o '235*+'"""
        tokens = self._tokenizar_operandos(expresion)
        self.raiz = self._construir_desde_postfija(tokens)
        return self.raiz

    def _tokenizar_operandos(self, expresion):
        """Separa por espacios; los bloques sin espacios ('235*+') se separan carácter a carácter."""
        if expresion is None or str(expresion).strip() == "":
            raise ValueError("La expresión está vacía")

        tokens = []
        for bloque in str(expresion).split():
            if bloque in self.OPERADORES or self._es_operando(bloque):
                tokens.append(bloque)
                continue
            for c in bloque:
                if c in self.OPERADORES or c.isalnum():
                    tokens.append(c)
                elif c in '()':
                    raise ValueError("La notación postfija y prefija no usan paréntesis")
                else:
                    raise ValueError(f"Carácter no válido: '{c}'")
        return tokens

    def _es_operando(self, token):
        """Indica si el token es un número (con signo o decimales) o una variable."""
        try:
            float(token)
            return True
        except ValueError:
            return token[0].isalpha() and token.isalnum()

    def insertar_prefija(self, expresion):
        """Construye el árbol a partir de una expresión prefija. Ej: '* 2 + 3 5'"""
        tokens = self._tokenizar_operandos(expresion)
        self.raiz, pos = self._construir_desde_prefija(tokens, 0)
        if pos != len(tokens):
            raise ValueError("Expresión mal formada: sobran operandos")
        return self.raiz

    def _construir_desde_prefija(self, tokens, pos):
        """Arma el árbol recursivamente desde la notación prefija."""
        if pos >= len(tokens):
            raise ValueError("Expresión mal formada: faltan operandos")

        token = tokens[pos]
        nodo = Nodo(token)
        if token in self.OPERADORES:
            nodo.izq, pos = self._construir_desde_prefija(tokens, pos + 1)
            nodo.der, pos = self._construir_desde_prefija(tokens, pos)
            return nodo, pos
        return nodo, pos + 1

    def _tokenizar(self, expresion):
        """Separa la expresión en números/variables, operadores y paréntesis."""
        if expresion is None or str(expresion).strip() == "":
            raise ValueError("La expresión está vacía")

        tokens = []
        i = 0
        expresion = str(expresion)
        while i < len(expresion):
            c = expresion[i]

            if c.isspace():
                i += 1
                continue

            # Signo negativo unario: al inicio, tras un operador o tras '('
            es_unario = c == '-' and (not tokens or tokens[-1] in self.OPERADORES or tokens[-1] == '(')

            if c.isdigit() or c == '.' or (es_unario and i + 1 < len(expresion)
                                           and (expresion[i + 1].isdigit() or expresion[i + 1] == '.')):
                inicio = i
                i += 1
                while i < len(expresion) and (expresion[i].isdigit() or expresion[i] == '.'):
                    i += 1
                tokens.append(expresion[inicio:i])
            elif c.isalpha():
                inicio = i
                while i < len(expresion) and expresion[i].isalnum():
                    i += 1
                tokens.append(expresion[inicio:i])
            elif c in self.OPERADORES or c in '()':
                tokens.append(c)
                i += 1
            else:
                raise ValueError(f"Carácter no válido: '{c}'")

        return tokens

    def _infija_a_postfija(self, tokens):
        """Convierte la lista de tokens infijos a postfija (algoritmo Shunting-yard)."""
        salida = []
        pila = []

        for token in tokens:
            if token in self.OPERADORES:
                while (pila and pila[-1] in self.OPERADORES
                       and self.PRECEDENCIA[pila[-1]] >= self.PRECEDENCIA[token]):
                    salida.append(pila.pop())
                pila.append(token)
            elif token == '(':
                pila.append(token)
            elif token == ')':
                while pila and pila[-1] != '(':
                    salida.append(pila.pop())
                if not pila:
                    raise ValueError("Paréntesis desbalanceados")
                pila.pop()
            else:
                salida.append(token)

        while pila:
            tope = pila.pop()
            if tope == '(':
                raise ValueError("Paréntesis desbalanceados")
            salida.append(tope)

        return salida

    def _construir_desde_postfija(self, postfija):
        """Arma el árbol usando una pila de nodos a partir de la notación postfija."""
        pila = []
        for token in postfija:
            nodo = Nodo(token)
            if token in self.OPERADORES:
                if len(pila) < 2:
                    raise ValueError("Expresión mal formada: faltan operandos")
                nodo.der = pila.pop()
                nodo.izq = pila.pop()
            pila.append(nodo)

        if len(pila) != 1:
            raise ValueError("Expresión mal formada: sobran operandos")
        return pila[0]

    # --- EVALUACIÓN ---

    def evaluar(self):
        """Calcula el valor numérico de la expresión almacenada en el árbol."""
        if self.raiz is None:
            raise ValueError("El árbol está vacío")
        resultado = self._evaluar_recursivo(self.raiz)
        return int(resultado) if float(resultado).is_integer() else resultado

    def _evaluar_recursivo(self, nodo):
        if nodo.valor not in self.OPERADORES:
            try:
                return float(nodo.valor)
            except ValueError:
                raise ValueError(f"No se puede calcular con la variable '{nodo.valor}'")

        izq = self._evaluar_recursivo(nodo.izq)
        der = self._evaluar_recursivo(nodo.der)

        if nodo.valor == '+':
            return izq + der
        if nodo.valor == '-':
            return izq - der
        if nodo.valor == '*':
            return izq * der
        if der == 0:
            raise ValueError("División entre cero")
        return izq / der

    def to_dict(self):
        """Retorna el árbol como diccionario o None si está vacío."""
        return self.raiz.to_dict() if self.raiz else None

    # --- RECORRIDOS ---

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
