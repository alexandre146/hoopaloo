import unittest 
from unittest import TestResult 
from <module solution> import <function name>

class TesteExercicio1_2 (unittest.TestCase): 

	def setUp(self):
		 pass


	def tearDown(self):
		pass

        def testAlgumteste(self):
                child = spawn('python %s/es.py')
                child.expect('.*')
                assert "3.0" in child.after.split()
                assert "2.0" in child.after.split()

if __name__== '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TesteExercicio1_2)
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