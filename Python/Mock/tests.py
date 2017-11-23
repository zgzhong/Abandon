from mymodule import rm
from mymodule import RemovalService
from mymodule import get_status_code

import os.path
import unittest
from unittest import mock

class RmTestCase(unittest.TestCase):

    @mock.patch('mymodule.os.path')
    @mock.patch('mymodule.os')
    def test_rm(self, mock_os, mock_path):
        mock_path.isfile.return_value = False
        rm("any path")
        self.assertFalse(mock_os.remove.called, "Failed to not remove the file if not present")

        mock_path.isfile.return_value = True
        rm("any path")
        mock_os.remove.assert_called_with("any path")

    @mock.patch('mymodule.os.path')
    @mock.patch('mymodule.os')
    def test_class_remove(self, mock_os, mock_path):
        reference = RemovalService()
        mock_path.isfile.return_value = False
        reference.rm("any path")
        self.assertFalse(mock_os.rm.called, "failed not to remove file not presented")

        mock_path.isfile.return_value = True
        reference.rm("any path")
        mock_os.remove.assert_called_with("any path")


class PropertyClassTest(unittest.TestCase):

    @mock.patch("mymodule.PropertyClass.prop", new_callable=mock.PropertyMock)
    def test_prop_mock(self, mock_status_code):
        mock_status_code.return_value = 200
        status_code = get_status_code()
        self.assertEqual(status_code, 200)
        print(get_status_code())

    def test_prop_mock(self):
        with mock.patch("mymodule.PropertyClass.prop", new_callable=mock.PropertyMock) as prop_moc:
            prop_moc.return_value = 200
            status_code = get_status_code()
            self.assertEqual(status_code, 200)
            print(get_status_code())

if __name__ == "__main__":
    unittest.main()