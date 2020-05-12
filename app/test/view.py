from flask import make_response, jsonify
from flask_cors import cross_origin

from . import test

numeros = [1000,900,500,400,100,90,50,40,10,9,5,4,1]
valor_romano=['M','CM','D','CD','C','XC','L','XL','X','IX','V','IV','I']

# nuevo metodo
@test.route('test1/<numero>', methods=['GET'])
@cross_origin() # allow all origins all methods.
def test(numero):
    numero = int(numero)
    pendiente = numero
    resultado = ''

    for i in range(len(numeros)):
        pendiente_aux = pendiente
        resultado_aux = resultado
        while pendiente_aux >= numeros[i]:
            resultado_aux = resultado_aux + valor_romano[i]
            pendiente_aux = pendiente_aux - numeros[i]
        pendiente = pendiente_aux
        resultado = resultado_aux

    r = make_response(jsonify(resultado))

    return r
