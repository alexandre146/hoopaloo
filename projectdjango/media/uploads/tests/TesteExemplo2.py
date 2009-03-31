import unittest 
from unittest import TestResult 
from pexpect import *

class MinhaClasse(unittest.TestCase):
    def testAlgumteste(self):
        child = spawn('python %s/es.py')
        child.expect('num1\? ')
        child.sendline('10')

        child.expect('num2\? ')
        child.sendline('8')

        child.expect('num3\? ')
        child.sendline('15')

        child.expect('soma = 33')
        child.expect('.*')


if __name__== '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(MinhaClasse)
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
	for e in r.errors:
		result_file.write(e[1])
	for f in r.failures:
		result_file.write(f[1])
	result_file.close()