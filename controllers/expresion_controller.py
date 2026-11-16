from flask import Blueprint, request, jsonify
from models.arbol_expresion import ArbolExpresion

expresion_bp = Blueprint('expresion_bp', __name__)

# Instancia del modelo en memoria para la sesión
arbol_expresion = ArbolExpresion()

NOTACION_INFIJA = "1"
NOTACION_POSTFIJA = "2"
NOTACION_PREFIJA = "3"

@expresion_bp.route('/api/expresion/calcular', methods=['POST'])
def calcular():
    datos = request.get_json() or {}
    expresion = datos.get('expresion')
    notacion = str(datos.get('notacion', NOTACION_INFIJA))

    if expresion is None or str(expresion).strip() == "":
        return jsonify({"error": "Expresión no proporcionada"}), 400

    if notacion not in (NOTACION_INFIJA, NOTACION_POSTFIJA, NOTACION_PREFIJA):
        return jsonify({"error": "Notación aún no soportada"}), 400

    try:
        if notacion == NOTACION_POSTFIJA:
            arbol_expresion.insertar_postfija(expresion)
        elif notacion == NOTACION_PREFIJA:
            arbol_expresion.insertar_prefija(expresion)
        else:
            arbol_expresion.insertar_infija(expresion)
        return jsonify({
            "resultado": arbol_expresion.evaluar(),
            "arbol": arbol_expresion.to_dict()
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

RECORRIDOS = {
    "inorden": "inorden",
    "preorden": "preorden",
    "postorden": "postorden",
}

@expresion_bp.route('/api/expresion/<recorrido>', methods=['GET'])
def recorrido(recorrido):
    if recorrido not in RECORRIDOS:
        return jsonify({"error": "Recorrido no válido"}), 404
    try:
        return jsonify({"recorrido": getattr(arbol_expresion, RECORRIDOS[recorrido])()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
