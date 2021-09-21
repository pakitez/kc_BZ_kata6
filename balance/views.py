from balance import app
from flask import render_template, request, redirect, url_for
from balance.models import ListaMovimientos, Movimiento, ValidationError

@app.route("/")
def inicio():
    lm = ListaMovimientos()
    lm.leer()
    print(lm.movimientos)
    return render_template("inicio.html", items=lm.movimientos)

@app.route("/nuevo", methods=['GET', 'POST'])
def nuevo():

    if request.method == 'GET':
        return render_template("nuevo_movimiento.html", errores=[], form={"fecha":"", "concepto": "", "cantidad":""})
    else:
        datos = request.form
        movimiento = Movimiento(datos)
        if len(movimiento.errores) > 0:
            return render_template("nuevo_movimiento.html", errores=movimiento.errores, form=datos)


        #TODO validar datos

        lm = ListaMovimientos()
        lm.leer()

        lm.anyadir(datos)
        lm.escribir()
        #return redirect(url_for("inicio"))
        return redirect('/')

