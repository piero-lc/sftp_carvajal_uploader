from decouple import config

class SFTPConfig:
    SFTP_HOST = config('SFTP_DINET_HOST')
    SFTP_PORT = config('SFTP_DINET_PORT')
    SFTP_USERNAME = config('SFTP_DINET_USER')
    SFTP_PASSWORD = config('SFTP_DINET_PWD')