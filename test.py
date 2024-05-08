import os
import paramiko

def upload_files_to_sftp(local_folder, sftp_host, sftp_port, sftp_username, sftp_password, sftp_folder):
    transport = paramiko.Transport((sftp_host, sftp_port))
    transport.connect(username=sftp_username, password=sftp_password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    
    for filename in os.listdir(local_folder):
        local_path = os.path.join(local_folder, filename)
        if os.path.isfile(local_path):
            # subir archivo al SFTP
            sftp.put(local_path, f"{sftp_folder}/{filename}")
            #FALTA PROBAR
    
    sftp.close()
    transport.close()

local_folder = "C:\ArchivosCarvajal"
sftp_host = "apolo.cen.biz"
sftp_port = 22  # Puerto por defecto para SFTP
sftp_username = "4709"
sftp_password = "T13nd4s2021*"
sftp_folder = "/ORDERS/In/"

upload_files_to_sftp(local_folder, sftp_host, sftp_port, sftp_username, sftp_password, sftp_folder)
