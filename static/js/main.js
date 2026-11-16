document.addEventListener("DOMContentLoaded", () => {
    const inputNodo = document.getElementById("insert-nodo");
    const btnInsertar = document.getElementById("btn-insertar");
    const btnEliminar = document.getElementById("btn-eliminar");
    const canvas = document.getElementById("main-canvas");
    const ctx = canvas.getContext("2d");

    // Parámetros de renderizado
    const RADIO = 18;
    const DISTANCIA_Y = 60;
    const COLOR_NODO_FONDO = "#16161f";
    const COLOR_BORDE = "#f8bb4a";
    const COLOR_TEXTO = "#f8bb4a";
    const COLOR_LINEA = "#7b7b93";
    
    const btnInorden = document.getElementById("btn-inorden");
    const btnPreorden = document.getElementById("btn-preorden");
    const btnPostorden = document.getElementById("btn-postorden");
    const inputResultado = document.getElementById("result-record");

    // Eventos de los botones 
    btnInorden.addEventListener("click", () => solicitarRecorrido("/api/abb/inorden"));
    btnPreorden.addEventListener("click", () => solicitarRecorrido("/api/abb/preorden"));
    btnPostorden.addEventListener("click", () => solicitarRecorrido("/api/abb/postorden"));
    btnInsertar.addEventListener("click", () => enviarAccion("/api/abb/insertar"));
    btnEliminar.addEventListener("click", () => enviarAccion("/api/abb/eliminar"));

    // Árbol de expresiones
    const selectNotacion = document.getElementById("notacion");
    const inputExpresion = document.getElementById("input-expresion");
    const btnCalcular = document.getElementById("btn-calcular");
    const inputResultadoExp = document.getElementById("result-exp");
    const btnMostrarArbol = document.getElementById("show-tree");

    const btnExpInorden = document.getElementById("exp-inorden");
    const btnExpPreorden = document.getElementById("exp-preorden");
    const btnExpPostorden = document.getElementById("exp-postorden");
    const inputResultadoRec = document.getElementById("result-exp-rec");

    btnExpInorden.addEventListener("click", () => solicitarRecorridoExpresion("inorden"));
    btnExpPreorden.addEventListener("click", () => solicitarRecorridoExpresion("preorden"));
    btnExpPostorden.addEventListener("click", () => solicitarRecorridoExpresion("postorden"));

    function solicitarRecorridoExpresion(recorrido) {
        fetch(`/api/expresion/${recorrido}`)
            .then(res => {
                if (!res.ok) throw new Error("Error al obtener recorrido");
                return res.json();
            })
            .then(data => {
                if (data.recorrido && data.recorrido.length > 0) {
                    inputResultadoRec.value = data.recorrido.join(", ");
                } else {
                    inputResultadoRec.value = "Árbol vacío";
                }
            })
            .catch(err => {
                console.error("Error en recorrido:", err);
                inputResultadoRec.value = "Error al consultar";
            });
    }

    btnCalcular.addEventListener("click", () => procesarExpresion(false));
    btnMostrarArbol.addEventListener("click", () => procesarExpresion(true));
    inputExpresion.addEventListener("keydown", (e) => {
        if (e.key === "Enter") procesarExpresion(false);
    });

    function procesarExpresion(mostrarArbol) {
        const expresion = inputExpresion.value.trim();
        if (expresion === "") {
            inputResultadoExp.value = "Ingrese una expresión";
            return;
        }

        fetch("/api/expresion/calcular", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ expresion: expresion, notacion: selectNotacion.value })
        })
        .then(res => res.json().then(data => ({ ok: res.ok, data })))
        .then(({ ok, data }) => {
            if (!ok) {
                inputResultadoExp.value = data.error || "Error al calcular";
                return;
            }
            inputResultadoExp.value = data.resultado;

            if (mostrarArbol) {
                limpiarCanvas();
                if (data.arbol) {
                    dibujarArbol(data.arbol, canvas.width / 2, 45, canvas.width / 4);
                }
            }
        })
        .catch(err => {
            console.error("Error en expresión:", err);
            inputResultadoExp.value = "Error al consultar";
        });
    }
    
    function solicitarRecorrido(urlEndpoint) {
        fetch(urlEndpoint)
            .then(res => {
                if (!res.ok) throw new Error("Error al obtener recorrido");
                return res.json();
            })
            .then(data => {
                // Si la lista está vacía muestra corchetes vacíos, si no, los valores separados por coma
                if (data.recorrido && data.recorrido.length > 0) {
                    inputResultado.value = data.recorrido.join(", ");
                } else {
                    inputResultado.value = "Árbol vacío";
                }
            })
            .catch(err => {
                console.error("Error en recorrido:", err);
                inputResultado.value = "Error al consultar";
            });
    }

    inputNodo.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            enviarAccion("/api/abb/insertar");
        }
    });

    // 3. Función unificada para insertar y eliminar
    function enviarAccion(urlEndpoint) {
        const texto = inputNodo.value.trim();
        if (texto === "") return;

        const numero = Number(texto);
        if (isNaN(numero)) {
            alert("Por favor, introduce un número válido.");
            return;
        }

        fetch(urlEndpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ valor: numero })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Error en la respuesta del servidor");
            }
            return response.json();
        })
        .then(data => {
            limpiarCanvas();
            // Si tras eliminar el árbol queda vacío, simplemente se queda limpio
            if (data.arbol) {
                const xInicial = canvas.width / 2;
                const yInicial = 45;
                const separacionInicialX = canvas.width / 4;

                dibujarArbol(data.arbol, xInicial, yInicial, separacionInicialX);
            }
            inputNodo.value = "";
            inputNodo.focus();
        })
        .catch(error => console.error("Error en la operación:", error));
    }

    // 4. Dibujado en Canvas
    function limpiarCanvas() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }

    function dibujarArbol(nodo, x, y, separacionX) {
        if (!nodo) return;

        if (nodo.izq) {
            const hijoX = x - separacionX;
            const hijoY = y + DISTANCIA_Y;
            dibujarConexion(x, y, hijoX, hijoY);
            dibujarArbol(nodo.izq, hijoX, hijoY, separacionX / 2);
        }

        if (nodo.der) {
            const hijoX = x + separacionX;
            const hijoY = y + DISTANCIA_Y;
            dibujarConexion(x, y, hijoX, hijoY);
            dibujarArbol(nodo.der, hijoX, hijoY, separacionX / 2);
        }

        dibujarNodo(nodo.valor, x, y);
    }

    function dibujarConexion(xOrigen, yOrigen, xDestino, yDestino) {
        ctx.beginPath();
        ctx.moveTo(xOrigen, yOrigen);
        ctx.lineTo(xDestino, yDestino);
        ctx.strokeStyle = COLOR_LINEA;
        ctx.lineWidth = 2;
        ctx.stroke();
    }

    function dibujarNodo(valor, x, y) {
        ctx.beginPath();
        ctx.arc(x, y, RADIO, 0, 2 * Math.PI);
        ctx.fillStyle = COLOR_NODO_FONDO;
        ctx.fill();
        ctx.strokeStyle = COLOR_BORDE;
        ctx.lineWidth = 2;
        ctx.stroke();

        ctx.fillStyle = COLOR_TEXTO;
        ctx.font = "18px 'VT323', monospace";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(valor, x, y);
    }
});