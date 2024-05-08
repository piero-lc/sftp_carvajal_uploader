from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO
import smtplib
import openpyxl

from ..config.config import Config

class EmailService:
    def send_error_email(self, failed_files_list: list):
        message = MIMEMultipart()
        message['Subject'] = Config.EMAIL_CONFIG['subject']
        message['From'] = f"{Config.EMAIL_CONFIG['alias']} <{Config.EMAIL_CONFIG['user']}>"
        message['To'] = ', '.join(Config.EMAIL_CONFIG['to'])

        try:
            message.attach(MIMEText(Config.EMAIL_CONFIG["body"], 'plain'))
        except Exception as e:
            print(f"Error al adjuntar cuerpo del mensaje: {e}")

        if failed_files_list:
            try:
                excel_file = BytesIO()
                workbook = openpyxl.Workbook()
                worksheet = workbook.active

                row = 1
                for filename in failed_files_list:
                    worksheet.cell(row=row, column=1).value = filename
                    row += 1

                workbook.save(excel_file)
                excel_data = excel_file.getvalue()
                excel_file.close()
                    
                # Attach Excel to message
                excel_part = MIMEBase('application', 'octet-stream')
                excel_part.set_payload(excel_data)
                encoders.encode_base64(excel_part)
                excel_part.add_header('Content-Disposition', 'attachment; filename="ArchivosFallidos.xlsx"')
                message.attach(excel_part)

            except Exception as e:
                print(f"Error al crear o adjuntar archivo Excel: {e}")

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                print("Conectando a servidor SMTP...")
                server.starttls()
                print("Iniciando TLS...")
                server.login(Config.EMAIL_CONFIG['user'], Config.EMAIL_CONFIG['password'])
                print("Iniciando sesión...")
                print("Enviando correo electrónico...")
                server.sendmail(Config.EMAIL_CONFIG['user'], Config.EMAIL_CONFIG['to'], message.as_string())
                print("Correo electrónico enviado!")

        except Exception as e:
            print(f"Error al enviar correo electrónico: {e}")
