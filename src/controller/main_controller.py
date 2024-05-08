import os
from ..services import file_service, sftp_service

class MainController:
    def __init__(self):
        self.file_service = file_service.FileService()
        self.sftp_service = sftp_service.SFTPService()

    def run(self):
        try:
            self.file_service.process_files()
        except Exception as e:
            print(f"Error general: {e}")