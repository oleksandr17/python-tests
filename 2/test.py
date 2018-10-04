import os.path
import tempfile
import unittest
from unittest import mock

import main


class RmTestCase(unittest.TestCase):

    def test_rm(self):
        # create file
        tmpfilepath = os.path.join(tempfile.gettempdir(), "tmp-testfile")
        with open(tmpfilepath, "wt") as f:
            f.write("Delete me!")

        # remove the file
        main.rm(tmpfilepath)
        # test that it was actually removed
        self.assertFalse(os.path.isfile(tmpfilepath), "Failed to remove the file.")

    @mock.patch('main.path')
    @mock.patch('main.os')
    def test_rm_mock_patch(self, mock_os, mock_path):
        # test that the remove call was NOT called
        mock_path.isfile.return_value = False
        main.rm("any path")
        self.assertFalse(mock_os.remove.called, "Failed to not remove the file if not present.")
        
        # make the file 'exist'
        mock_path.isfile.return_value = True
        main.rm("any path")
        mock_os.remove.assert_called_with("any path")


class RemovalServiceTestCase(unittest.TestCase):
    
    @mock.patch('main.path')
    @mock.patch('main.os')
    def test_rm_mock_patch(self, mock_os, mock_path):
        # instantiate our service
        service = main.RemovalService()
        
        # test that the remove call was NOT called
        mock_path.isfile.return_value = False
        file_deleted = service.rm("any path")
        self.assertFalse(file_deleted)
        self.assertFalse(mock_os.remove.called, "Failed to not remove the file if not present.")
        
        # make the file 'exist'
        mock_path.isfile.return_value = True
        file_deleted = service.rm("any path")
        self.assertTrue(file_deleted)
        mock_os.remove.assert_called_with("any path")


class UploadServiceTestCase(unittest.TestCase):
    
    @mock.patch.object(main.RemovalService, 'rm')
    def test_upload_mock_patch_object(self, mock_rm):
        # build our dependencies
        removal_service = main.RemovalService()
        reference = main.UploadService(removal_service)
        
        # call upload_complete, which should, in turn, call `rm`:
        reference.upload_complete("my uploaded file")
        
        # check that it called the rm method of any RemovalService
        mock_rm.assert_called_with("my uploaded file")
        
        # check that it called the rm method of _our_ removal_service
        removal_service.rm.assert_called_with("my uploaded file")

    def test_upload_mock_create_autospec(self):
        # build our dependencies
        mock_removal_service = mock.create_autospec(main.RemovalService)
        reference = main.UploadService(mock_removal_service)
        
        # call upload_complete, which should, in turn, call `rm`:
        reference.upload_complete("my uploaded file")
        
        # test that it called the rm method
        mock_removal_service.rm.assert_called_with("my uploaded file")
