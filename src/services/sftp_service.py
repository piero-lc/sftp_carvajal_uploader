import os
import paramiko
from typing import Generator, Literal
from src.config.sftp_config import SFTPConfig
from paramiko import SFTPClient, Transport
from contextlib import contextmanager

class SFTPService:
    def __init__(self):
        self.transport: Transport = None
        self.__config = SFTPConfig()

    def connect(self):
        try:
            if not self.transport or not self.transport.is_active():
                sftp_host = self.__config.SFTP_HOST
                sftp_port = self.__config.SFTP_PORT
                sftp_username = self.__config.SFTP_USERNAME
                sftp_password = self.__config.SFTP_PASSWORD

                self.transport = paramiko.Transport((sftp_host, int(sftp_port)))
                self.transport.default_max_packet_size = 100000000
                self.transport.default_window_size = 100000000
                self.transport.connect(username=sftp_username, password=sftp_password)
        except Exception as error:
            raise error

    def disconnect(self):
        try:
            if self.transport:
                self.transport.close()
        except Exception as error:
            raise error

    @contextmanager
    def _get_sftp_client_context(self) -> Generator[SFTPClient, None, None]:
        try:
            self.connect()
            yield paramiko.SFTPClient.from_transport(self.transport)
        finally:
            self.disconnect()

    def sendFile(self, localPath: str, remotePath: str):
        try:
            with self._get_sftp_client_context() as sftp:

                sftp.put(localPath, remotePath)
        except Exception as e:
            raise e

    def getFile(self, remotePath: str, localPath: str):
        try:
            with self._get_sftp_client_context() as sftp:
                sftp.get(remotePath, localPath)
        except Exception as e:
            raise e

    def downloadFileSelected(self, routeRemote, routeLocal, field: str, typeFile: Literal[".txt", ".pdf", ".trg"] = ".txt", cantFiles: int = 0):
        try:
            filesDownload = []
            
            with self._get_sftp_client_context() as sftp:
                filesToDownload = [
                    file
                    for file in sftp.listdir(routeRemote)
                    if file.startswith(field) and file.endswith(typeFile)
                ]

                maxFilesToDown = len(filesToDownload) if cantFiles == 0 else cantFiles

                for index, filename in enumerate(filesToDownload):
                    remoteFilePath = routeRemote + "/" + filename
                    localFilePath = os.path.join(routeLocal, filename)
                    self.getFile(remotePath=remoteFilePath, localPath=localFilePath)
                    filesDownload.append(localFilePath)

                    if index == (maxFilesToDown - 1):
                        break

            return filesDownload
        except Exception as e:
            raise e

    def getAllFiles(self, remoteDirectory: str):
        try:
            with self._get_sftp_client_context() as sftp:
                return [fileAttr.filename for fileAttr in sftp.listdir_attr(remoteDirectory)]
        except Exception as e:
            raise e

    def moveFile(self, fileName: str, originRoute: str, destinRoute: str):
        try:
            with self._get_sftp_client_context() as sftp:
                sourcePath = f"{originRoute}/{fileName}"
                destinPath = f"{destinRoute}/{fileName}"
                sftp.rename(sourcePath, destinPath)
        except Exception as e:
            raise e

    def sendToFolder(self, filename: str, folder: Literal["BACKUP", "ERROR"] = "BACKUP"):
        try:
            originRoute = "/SALIDA"
            destinRoute = f"/SALIDA/{folder}"
            route, extent = os.path.splitext(filename)
            filenameTrg = route + ".trg"
            self.moveFile(fileName=filename, originRoute=originRoute, destinRoute=destinRoute)
            self.moveFile(fileName=filenameTrg, originRoute=originRoute, destinRoute=destinRoute)
        except Exception as e:
            raise e

