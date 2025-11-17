from flask import Flask, render_template, request

# Crear la aplicación
app = Flask(__name__)

# Almacenamiento en memoria
registros_notas = []     # Para guardar los resultados del ejercicio 1
registros_nombres = []   # Para guardar los resultados del ejercicio 2


# Ruta principal
@app.route("/")
def index():
    return render_template("index.html")  # Carga la plantilla

# Ruta para Ejercicio 1
@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    # Inicializamos errores y valores
    errors = {}
    nota1 = nota2 = nota3 = asistencia = ""

    if request.method == "POST":
        # Intentar convertir los valores a float
        try:
            nota1 = float(request.form.get("nota1", ""))
        except ValueError:
            errors["nota1"] = "Ingresa un número válido"
        try:
            nota2 = float(request.form.get("nota2", ""))
        except ValueError:
            errors["nota2"] = "Ingresa un número válido"
        try:
            nota3 = float(request.form.get("nota3", ""))
        except ValueError:
            errors["nota3"] = "Ingresa un número válido"
        try:
            asistencia = float(request.form.get("asistencia", ""))
        except ValueError:
            errors["asistencia"] = "Ingresa un número válido"

        # Validación de rango si no hay error de conversión
        if "nota1" not in errors and not (10 <= nota1 <= 70):
            errors["nota1"] = "La nota 1 debe estar entre 10 y 70"
        if "nota2" not in errors and not (10 <= nota2 <= 70):
            errors["nota2"] = "La nota 2 debe estar entre 10 y 70"
        if "nota3" not in errors and not (10 <= nota3 <= 70):
            errors["nota3"] = "La nota 3 debe estar entre 10 y 70"
        if "asistencia" not in errors and not (0 <= asistencia <= 100):
            errors["asistencia"] = "La asistencia debe estar entre 0 y 100"

        # Si hay errores, volvemos a mostrar el formulario con ellos
        if errors:
            return render_template(
                "ejercicio1.html",
                errors=errors,
                nota1=request.form.get("nota1", ""),
                nota2=request.form.get("nota2", ""),
                nota3=request.form.get("nota3", ""),
                asistencia=request.form.get("asistencia", "")
            )

        # Calcular promedio y mensaje
        promedio = (nota1 + nota2 + nota3) / 3
        mensaje = "APROBADO" if promedio >= 40 and asistencia >= 75 else "REPROBADO"

        # Guardar registro
        registros_notas.append({
            "nota1": nota1,
            "nota2": nota2,
            "nota3": nota3,
            "promedio": round(promedio, 1),
            "asistencia": asistencia,
            "mensaje": mensaje
        })

        # Mostrar resultado
        return render_template(
            "ejercicio1.html",
            promedio=round(promedio, 1),
            asistencia=asistencia,
            mensaje=mensaje,
            errors={},  # no hay errores ahora
            nota1=nota1,
            nota2=nota2,
            nota3=nota3,
            asistencia_val=asistencia
        )

    # GET: mostrar formulario vacío
    return render_template(
        "ejercicio1.html",
        errors={},
        nota1="",
        nota2="",
        nota3="",
        asistencia=""
    )


# Ruta para Ejercicio 2
@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    if request.method == "POST":
        nombre1 = request.form["nombre1"].strip()
        nombre2 = request.form["nombre2"].strip()
        nombre3 = request.form["nombre3"].strip()

        #creamos lista
        nombres = [nombre1, nombre2, nombre3]

        #obtener nombre mas largo
        nombre_mas_largo = max(nombres, key=len)
        cantidad_caracteres = len(nombre_mas_largo)

        #guardar en memoria
        registros_nombres.append({  "nombre1": nombre1,
                                    "nombre2": nombre2,
                                    "nombre3": nombre3,
                                    "nombre_mas_largo": nombre_mas_largo,
                                    "caracteres": cantidad_caracteres})
        #enviar nombres a plantilla
        return render_template("ejercicio2.html",
                               nombre=nombre_mas_largo,
                               caracteres=cantidad_caracteres)

    return render_template("ejercicio2.html")

@app.route("/memoria")
def memoria():
    return render_template("memoria.html",
                           registros_notas=registros_notas,
                           registros_nombres=registros_nombres)


# Ejecutar la app


if __name__ == "__main__":
    app.run(debug=True)
