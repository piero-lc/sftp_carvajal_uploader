
class Config:
    LOCAL_PATH = "C:/ArchivosCarvajal"
    SUCCESS_PATH = "C:/ArchivosCarvajal/success"
    ERROR_PATH = "C:/ArchivosCarvajal/error"
    REMOTE_PATH = ""
    MAX_ATTEMPTS = 3
    BATCH_SIZE = 50

    EMAIL_CONFIG = {
        "user": "multifuncional@lindcorp.pe",
        "password": "Lindcorp2025*",
        "alias": "reportes.diario@lindcorp.pe",
        "to": [
            "piero.gallo@lindcorp.pe"
            #, "jesus.alvarez@lindcorp.pe"
        ],
        "cco": [
            # "francisco.esparza@lindcorp.pe"
        ],
        "subject": f"Error envio SFTP Carvajal",
        "body": "Buenos días. Se adjunta el reporte de errores en el envio automático al SFTP Carvajal. Saludos"
    }