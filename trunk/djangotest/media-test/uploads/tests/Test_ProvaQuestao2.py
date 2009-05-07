import unittest 
from unittest import TestResult 


class Test_ProvaQuestao2 (unittest.TestCase): 

	def setUp(self):
		 pass


	def tearDown(self):
		pass

        def test_dalton(self):
                pass


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