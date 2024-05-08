import os
import time

from ..config.config import Config
from ..services import email_service, sftp_service

class FileService:
    def __init__(self):
        self.config = Config 
        self.email_service = email_service.EmailService()
        self.sftp_service = sftp_service.SFTPService() 

    def move_file(self, source_path, destination_path):
        try:    
            new_path = os.path.join(destination_path, os.path.basename(source_path))
            print(f"Moviendo archivo: {source_path} -> {new_path}")
            os.rename(source_path, new_path)
            return new_path
        except Exception as e:
            print(f"Error al mover {source_path} -> {new_path}: {e}")


    # simulacion de envio
    # def send_file_SFTP(self, source_path):
    #     print("Simulando envío de archivos a SFTP...")
    #     simulated_sftp_path = os.path.join("C:/Users/piero.gallo/Documents/test_SFTP", os.path.basename(source_path))

    #     try:
    #         time.sleep(1) #
    #         raise Exception("**ERROR SIMULADO**")
    #         with open(source_path, 'rb') as source_file, open(simulated_sftp_path, 'wb') as destination_file:
    #             for data in iter(lambda: source_file.read(1024), b''):
    #                 destination_file.write(data)
    #         print(f"Archivo enviado a SFTP: {simulated_sftp_path}")
    #     except Exception as e:
    #         raise Exception(e)
        

    def process_files(self):
        print("Comenzando el procesamiento de archivos...")
        failed_files_list = []

        # Obtener lista de archivos txt en la carpeta local y ordenarla por fecha de modificación
        txt_files = sorted([filename for filename in os.listdir(self.config.LOCAL_PATH) if filename.endswith(".txt")],
                           key=lambda f: os.path.getmtime(os.path.join(self.config.LOCAL_PATH, f)))
        
        # Limitar a 50 archivos por ejecución
        files_to_process = txt_files[:50]

        for filename in files_to_process:
            file_path = os.path.join(self.config.LOCAL_PATH, filename)
            print(f"Accediendo archivo: {file_path}")

            attempts = 1
            while attempts <= self.config.MAX_ATTEMPTS:
                try:
                    #self.send_file_SFTP(file_path)
                    self.sftp_service.sendFile(localPath=file_path, remotePath=self.config.REMOTE_PATH)
                    time.sleep(1)
                    print(f"Enviando archivo: {file_path}")
                    self.move_file(file_path, self.config.SUCCESS_PATH)
                    break
                except Exception as e:
                    print(f"Error al enviar archivo {filename} (intento {attempts}/{self.config.MAX_ATTEMPTS}): {e}")
                    attempts += 1
            else:
                print(f"Error al enviar archivo {filename} (se ha llegado al máximo de intentos)")
                if attempts == self.config.MAX_ATTEMPTS + 1:
                    failed_files_list.append(filename)
                    print(failed_files_list)
                    
                self.move_file(file_path, self.config.ERROR_PATH)
        
        if len(failed_files_list) > 0:
            self.email_service.send_error_email(failed_files_list)
        
        print("Proceso de archivos finalizado.")
