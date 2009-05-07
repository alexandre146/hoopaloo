import unittest
from unittest import TestResult
import pexpect


class Output:
    def __init__(self, buffer):
        self.buffer = buffer
        
    def __getitem__(self, number):
        return self.buffer.split('\n')[number].strip('\n\r')

class PexpectTestCase(unittest.TestCase):

    def setUp(self):
        self.f = "/home/mariana/www/djangotest/media-test/uploads/under_tests//Questao7_1.py"
        self.child = pexpect.spawn('python ' + self.f, timeout=1, maxread=2000)

    def input(self, inputs):
        for a in inputs:
            self.child.sendline(str(a))
        index = self.child.expect([pexpect.EOF, pexpect.TIMEOUT])
        if index == 1:
            testcase.fail("TIMEOUT: Programa pendurou quando era esperado finalizar.")
            
        self.child.close()

    def output(self):
        return Output(self.child.before)

class UnderTest_Questao7_2(PexpectTestCase):

    def test_entrada_capital(self):
        self.input([30,12])
        o = self.output()
        self.assertEquals("capital? 30", o[0])

    def test_entrada_tempo(self):
        self.input([30,12])
        o = self.output()
        self.assertEquals("tempo? 12", o[1])

    def test_saida(self):
        self.input([30, 12])
        o = self.output()
        self.assertEqual(o[2], 'Juros: 53.88')
        self.assertEqual(o[3], 'Capital Futuro: 413.88')
   
    def test_investimento(self, input=(30,12), juros="53.88", futuro="413.88", base=0):
        self.input(input)
        o = self.output()
        s1 = o[base + 2]
        s2 = o[base + 3]
        self.assertEqual(s1[-len(juros)-1:], ' ' + juros)
        self.assertEqual(s2[-len(futuro)-1:], ' ' + futuro)

    def test_capital_menor(self):
        self.test_investimento((10, 30, 12), base=2)
        o = self.output()
        self.assertEqual(o[1], 'Investimento minimo de R$ 30,00')

    def test_outro_investimento(self):
        self.test_investimento((30, 5), '38.29', '188.29')

    def test_mais_outro_investimento(self):
        self.test_investimento((50, 30), '216.10', '1716.10')

    def test_tempoForaLimite1(self):
        self.test_investimento((30, 1500, 30, 12), base=3)
        o = self.output()
        self.assertEqual(o[2], 'Periodo de tempo de 02 a 48 meses')

    def test_tempoForaLimite2(self):
        self.test_investimento((30, 1, 30, 12), base=3)
        o = self.output()
        self.assertEqual(o[2], 'Periodo de tempo de 02 a 48 meses')

    def test_limiteTempo1(self):
        self.test_investimento((1000, 2), '1102.50', '3102.50')

    def test_limiteTempo2(self):
        self.test_investimento((1000, 48), '10401.27', '58401.27')


if __name__== '__main__':
	loader = unittest.TestLoader()
	loader.testMethodPrefix = 'undertest'
	suite = loader.loadTestsFromTestCase(UnderTest_Roteiro7_1)
	r = TestResult()
	suite.run(r)
	result_file = open('/home/mariana/www/djangotest/media-test/uploads/under_tests/' + 'result.txt', 'wb')
	result_file.write(str(len(r.errors)))
	result_file.write('\n')
	result_file.write(str(len(r.failures)))
	result_file.write('\n')
	result_file.write(str(r.testsRun))
	result_file.write('\n')
	result_file.write(str(r.wasSuccessful()))
	result_file.write('\n')
	for e in r.errors:
		result_file.write(e[1])
	for f in r.failures:
		result_file.write(f[1])
	result_file.close()