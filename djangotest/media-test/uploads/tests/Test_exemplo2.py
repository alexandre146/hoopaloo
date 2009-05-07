import unittest 
from unittest import TestResult 
from pexpect import *

class Test_exemplo2 (unittest.TestCase): 

	def setUp(self):
		 pass


	def tearDown(self):
		pass

	def test_investimento(self):
		child = spawn('python %s/exemplo2.py')
		child.expect('Capital\?')
		child.sendline('30')
		child.expect('Tempo\?')
		child.sendline('12')
		child.expect('Juros: 53.88')
		child.expect('Capital Futuro: 413.88')
		
	def test_capitalMenor(self):
		child = spawn('python %s/exemplo2.py')
		child.expect('Capital\?')
		#child.sendline('10')
		#child.expect('.*')
		#assert 'Investimento minimo de R$ 30,00' in child.after
		#assert 'Capital\?' in child.after
	#	child.expect('Investimento minimo de R$ 30,00')
	#	child.expect('Capital\?')
		child.sendline('-1')
		#child.expect('Investimento minimo de R$ 30,00')
		#child.expect('Capital\?')
		child.sendline('30')
		child.expect('Tempo\?')
		child.sendline('5')
		child.expect('Juros: 38.29')
		child.expect('Capital Futuro: 188.29')
		#assert "38.29" in child.after
		#assert "188.29" in child.after

	def test_tempoForaLimite(self):
		child = spawn('python %s/exemplo2.py')
		child.expect('Capital\?')
		child.sendline('1500')
		child.expect('Tempo\?')
		#child.sendline('1')
		#child.expect('.*')
		#assert 'Periodo de tempo de 02 a 48 meses' in child.after
		#child.expect('Tempo\?')
		#child.sendline('50')
		#child.expect('.*')
		#assert 'Periodo de tempo de 02 a 48 meses' in child.after
		#child.expect('Tempo\?')
		child.sendline('30')
		child.expect('Juros: 6482.91')
		child.expect('Capital Futuro: 51482.91')
		#assert "6482.92" in child.after
		#assert "51482.92" in child.after
		
	def test_limiteTempo1(self):
		child = spawn('python %s/exemplo2.py')
		child.expect('Capital\?')
		child.sendline('1000')
		child.expect('Tempo\?')
		child.sendline('2')
		child.expect('Juros: 1102.50')
		child.expect('Capital Futuro: 3102.50')
		#assert "1102.50" in child.after
		#assert "3102.50" in child.after

	def test_limiteTempo2(self):
		child = spawn('python %s/exemplo2.py')
		child.expect('Capital\?')
		child.sendline('1000')
		child.expect('Tempo\?')
		child.sendline('48')
		child.expect('Juros: 10401.27')
		child.expect('Capital Futuro: 58401.27')
		#assert "10401.29" in child.after
		#assert "58401.29" in child.after



if __name__== '__main__':
	loader = unittest.TestLoader()
	suite = loader.loadTestsFromTestCase(%s)
	r = TestResult()
	suite.run(r)
	result_file = open('result.txt', 'wb')
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