import os
import sys
import unittest
from ip_tracker import csv_writer, csv_reader, ip_tracker


class TestIPTracker(unittest.TestCase):

    def setUp(self):
        self.columns_to_record = ['Column']
        self.encoding = 'utf-8-sig'
        self.environment_column = 'env'
        self.environment_name = 'test_env'
        self.combined_file_name = 'comb.csv'
        self.comb_file_path = os.path.join(sys.path[0],
                                           self.combined_file_name)

        self.test_env_file_1 = [
            {'Column': 'Test1'},
            {'Column': 'Test1'},
            {'Column': 'Test2'},
            {'Column': 'Test2'},
            {'Column': 'Test3'},
            {'Column': 'Test4'},
        ]
        self.test_env_file_path_1 = os.path.join(sys.path[0], 'test_env1.csv')
        csv_writer(self.test_env_file_path_1, self.test_env_file_1,
                   [], self.columns_to_record, False, self.encoding)

        self.test_env_file_2 = [
            {'Column': 'Test4'},
            {'Column': 'Test5'},
            {'Column': 'Test6'},
            {'Column': 'Test7'},
            {'Column': 'Test8'},
            {'Column': 'Test9'},
        ]
        self.test_env_file_path_2 = os.path.join(sys.path[0], 'test_env2.csv')
        csv_writer(self.test_env_file_path_2, self.test_env_file_2,
                   [], self.columns_to_record, False, self.encoding)

    def test_extraction(self):
        extracted_values = sum([csv_reader(self.test_env_file_path_1,
                                           self.columns_to_record,
                                           self.encoding,
                                           self.environment_column,
                                           self.environment_name, True)
                                for file in self.test_env_file_path_1], [])

        for value in self.test_env_file_1:
            self.assertIn(value, extracted_values)

        extracted_values = sum([csv_reader(self.test_env_file_path_2,
                                           self.columns_to_record,
                                           self.encoding,
                                           self.environment_column,
                                           self.environment_name, True)
                                for file in self.test_env_file_path_1], [])

        for value in self.test_env_file_2:
            self.assertIn(value, extracted_values)

    def test_ip_tracker(self):
        ip_tracker(self.environment_name, self.columns_to_record,
                   self.combined_file_name, self.environment_column,
                   False, self.encoding,
                   False)
        extracted_values = csv_reader(self.comb_file_path,
                                      self.columns_to_record +
                                      [self.environment_column],
                                      self.encoding,
                                      self.environment_column,
                                      self.environment_name, True)

        expected_result = [
            {'Column': 'Test1', 'env': 'test_env'},
            {'Column': 'Test2', 'env': 'test_env'},
            {'Column': 'Test3', 'env': 'test_env'},
            {'Column': 'Test4', 'env': 'test_env'},
            {'Column': 'Test5', 'env': 'test_env'},
            {'Column': 'Test6', 'env': 'test_env'},
            {'Column': 'Test7', 'env': 'test_env'},
            {'Column': 'Test8', 'env': 'test_env'},
            {'Column': 'Test9', 'env': 'test_env'},
        ]

        self.assertEqual(extracted_values, expected_result)

        os.remove(self.comb_file_path)

    def test_ip_tracker_new_env(self):
        ip_tracker(self.environment_name, self.columns_to_record,
                   self.combined_file_name, self.environment_column,
                   False, self.encoding,
                   False)

        test_env_file = [
            {'Column': 'Test10'},
            {'Column': 'Test11'},
            {'Column': 'Test12'},
            {'Column': 'Test13'},
            {'Column': 'Test14'},
            {'Column': 'Test15'},
        ]
        test_env_file_path = os.path.join(sys.path[0], 'test_new_env1.csv')
        csv_writer(test_env_file_path, test_env_file,
                   [], self.columns_to_record, False, self.encoding)

        ip_tracker('test_new_env', self.columns_to_record,
                   self.combined_file_name, self.environment_column,
                   False, self.encoding,
                   False)

        extracted_values = csv_reader(self.comb_file_path,
                                      self.columns_to_record +
                                      [self.environment_column],
                                      self.encoding,
                                      self.environment_column,
                                      self.environment_name, True)

        expected_result = [
            {'Column': 'Test1', 'env': 'test_env'},
            {'Column': 'Test2', 'env': 'test_env'},
            {'Column': 'Test3', 'env': 'test_env'},
            {'Column': 'Test4', 'env': 'test_env'},
            {'Column': 'Test5', 'env': 'test_env'},
            {'Column': 'Test6', 'env': 'test_env'},
            {'Column': 'Test7', 'env': 'test_env'},
            {'Column': 'Test8', 'env': 'test_env'},
            {'Column': 'Test9', 'env': 'test_env'},
            {'Column': 'Test10', 'env': 'test_new_env'},
            {'Column': 'Test11', 'env': 'test_new_env'},
            {'Column': 'Test12', 'env': 'test_new_env'},
            {'Column': 'Test13', 'env': 'test_new_env'},
            {'Column': 'Test14', 'env': 'test_new_env'},
            {'Column': 'Test15', 'env': 'test_new_env'},
        ]

        self.assertEqual(extracted_values, expected_result)

        os.remove(self.comb_file_path)
        os.remove(test_env_file_path)

    def tearDown(self):
        os.remove(self.test_env_file_path_1)
        os.remove(self.test_env_file_path_2)


if __name__ == '__main__':
    unittest.main()
