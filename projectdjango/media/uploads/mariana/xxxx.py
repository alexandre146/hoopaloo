import unittest 
from unittest import TestResult 
from <module solution> import <function name>

class <TestName> (unittest.TestCase): 

	def setUp(self):
		 pass


	def tearDown(self):
		pass


if __name__== '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(<TestName>)
	r = TestResult()
	suite.run(r)
	result_file = open('/home/mariana/www/projectdjango/media/uploads/mariana/' + 'result.txt', 'wb')
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