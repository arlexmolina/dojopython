import unittest

numeros = [1000,900,500,400,100,90,50,40,10,9,5,4,1]
valor_romano=['M','CM','D','CD','C','XC','L','XL','X','IX','V','IV','I']

class NumeroRomano(object):
    def test(self, numero):
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
        return resultado

# Creamos una clase heredando de TestCase
class TestMyCalculator(unittest.TestCase):

    # Creamos una prueba para probar un valor inicial
    def test_uno(self):
        claseRomana = NumeroRomano()
        numero = claseRomana.test(1)
        self.assertEqual('I', numero)

    def test_cuatro(self):
        claseRomana = NumeroRomano()
        numero = claseRomana.test(4)
        self.assertEqual('IV', numero)

    def test_cinco(self):
        claseRomana = NumeroRomano()
        numero = claseRomana.test(5)
        self.assertEqual('V', numero)

    def test_cien(self):
        claseRomana = NumeroRomano()
        numero = claseRomana.test(100)
        self.assertEqual('C', numero)

    def test_quinientos(self):
        claseRomana = NumeroRomano()
        numero = claseRomana.test(500)
        self.assertEqual('D', numero)

    def test_NOVECIENTOS(self):
        claseRomana = NumeroRomano()
        numero = claseRomana.test(900)
        self.assertEqual('CM', numero)

    def test_novecientoscincuenta(self):
        claseRomana = NumeroRomano()
        numero = claseRomana.test(950)
        self.assertEqual('CML', numero)

    def test_novecxinetonoventayocho(self):
        claseRomana = NumeroRomano()
        numero = claseRomana.test(998)
        self.assertEqual('CMXCVIII', numero)

if __name__ == '__main__':
    unittest.main()
