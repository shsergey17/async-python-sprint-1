import pytest
from unittest.mock import Mock, patch, MagicMock, call, mock_open
import builtins
import sys

from requests import patch

sys.path.append("../")

from src.file_types import IFileType, JsonFileType

def test_get_filenname():
    json_type = JsonFileType('test')
    assert json_type.get_filename_with_ext('json') == 'test.json'




@patch('builtins.open', new_callable=mock_open())
def test_dump(self, mock_open_file, mock_os):
    json_type = JsonFileType('test')
    data_writer = json_type.save()

    mock_os.path.exists.assert_called_once_with('/my/path/not/exists')
    mock_open_file.assert_called_once_with('/my/path/not/exists/output.text', 'w+')
    mock_open_file.return_value.__enter__().write.assert_called_once_with('Hello, Foo!')

# def test_save():

#     data = [['column1', 'column2'], ['row1_value1', 'row1_value2'], ['row2_value1', 'row2_value2']]
#     mock_file = Mock()
#     mock_open = Mock(return_value=mock_file)

#     # Patch the built-in open function with the mock open function
#     with patch('builtins.open', mock_open):
#         file_type = JsonFileType()
#         file_type.save(data)

#     mock_open.assert_called_once_with(file_type.get_filename_with_ext('json'), 'w')
#     mock_file.write.assert_called_once_with('[["column1", "column2"], ["row1_value1", "row1_value2"], ["row2_value1", "row2_value2"]]')


    