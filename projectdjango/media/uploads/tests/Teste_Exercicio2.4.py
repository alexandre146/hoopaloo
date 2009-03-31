import unittest 
from unittest import TestResult 


class Exercicio2_4 (unittest.TestCase): 

	def setUp(self):
		 pass


	def tearDown(self):
		pass


if __name__== '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(Exercicio2_4)
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