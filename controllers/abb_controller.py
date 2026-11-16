from flask import Blueprint, request, jsonify
from models.arbol_binario import ArbolBinarioBusqueda

abb_bp = Blueprint('abb_bp', __name__)

# Instancia del modelo en memoria para la sesión
arbol_abb = ArbolBinarioBusqueda()

@abb_bp.route('/api/abb/insertar', methods=['POST'])
def insertar():
    datos = request.get_json() or {}
    valor_raw = datos.get('valor')

    if valor_raw is None or str(valor_raw).strip() == "":
        return jsonify({"error": "Valor no proporcionado"}), 400

    try:
        arbol_abb.insertar(valor_raw)
        return jsonify({
            "mensaje": f"Nodo {valor_raw} insertado",
            "arbol": arbol_abb.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@abb_bp.route('/api/abb/eliminar', methods=['POST'])
def eliminar():
    datos = request.get_json() or {}
    valor = datos.get('valor')

    if valor is None:
        return jsonify({"error": "Valor no proporcionado"}), 400

    try:
        arbol_abb.eliminar(valor)
        return jsonify({
            "mensaje": f"Nodo {valor} eliminado",
            "arbol": arbol_abb.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@abb_bp.route('/api/abb/inorden', methods=['GET'])
def api_inorden():
    return jsonify({"recorrido": arbol_abb.inorden()}), 200

@abb_bp.route('/api/abb/preorden', methods=['GET'])
def api_preorden():
    return jsonify({"recorrido": arbol_abb.preorden()}), 200

@abb_bp.route('/api/abb/postorden', methods=['GET'])
def api_postorden():
    return jsonify({"recorrido": arbol_abb.postorden()}), 200