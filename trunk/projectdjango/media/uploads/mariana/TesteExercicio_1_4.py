import unittest 
from unittest import TestResult 
from pexpect import *

class TesteEx1_4 (unittest.TestCase): 

	def testDuasRaizes1(self):
	        child = spawn('python %s/es.py')
        	child.sendline('1')
        	child.sendline('-5')
        	child.sendline('6')
        	child.expect('.*')
        	assert "3.0" in child.after
        	assert "2.0" in child.after

	def testDuasRaizes2(self):
        	child = spawn('python %s/es.py')
        	child.sendline('4')
        	child.sendline('-8')
        	child.sendline('0')
        	child.expect('.*')
        	assert "0.0" in child.after
        	assert "32.0" in child.after

	def testRaizesNulas(self):
        	child = spawn('python %s/es.py')
        	child.sendline('4')
        	child.sendline('0')
        	child.sendline('0')
        	child.expect('.*')
        	assert "0.0" in child.after

	def testUmaRaizNegativa(self):
        	child = spawn('python %s/es.py')
        	child.sendline('1')
        	child.sendline('6')
        	child.sendline('0')
        	child.expect('.*')
	        assert "0.0" in child.after
	        assert "-6.0" in child.after

	def testDuasRaizesNegativas(self):
        	child = spawn('python %s/es.py')
        	child.sendline('2')
	        child.sendline('7')
        	child.sendline('5')
        	child.expect('.*')
        	assert "-4.0" in child.after
        	assert "-10.0" in child.after



if __name__== '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TesteEx1_4)
	r = TestResult()
	suite.run(r)
	result_file = open(/home/mariana/www/projectdjango/media/uploads/mariana/ + 'result.txt', 'wb')
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