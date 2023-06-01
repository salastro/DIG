import base64
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from fpdf import FPDF

# Update these with your own values
SERVICE_ACCOUNT_FILE = 'path/to/your/credentials.json'
SPREADSHEET_ID = 'your_spreadsheet_id'
INVOICE_TEMPLATE_PATH = 'path/to/your/invoice_template.pdf'

# Set up Google Sheets API and Gmail API credentials
scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/gmail.send']
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)

# Create API clients
sheets_service = build('sheets', 'v4', credentials=credentials)
gmail_service = build('gmail', 'v1', credentials=credentials)

def read_data_from_sheet():
    try:
        range_name = 'Sheet1!A1:H'
        result = sheets_service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
        rows = result.get('values', [])

        if not rows:
            print('No data found.')
            return []

        return rows

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

def create_invoice_pdf(data, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add your desired invoice template and layout here
    pdf.cell(200, 10, txt="Invoice", ln=1, align="C")

    for i, item in enumerate(data):
        for j, value in enumerate(item):
            pdf.cell(30, 10, txt=str(value), border=1)
        pdf.ln()

    pdf.output(output_path)

def send_email(to, subject, body, attachment_path):
    message = MIMEMultipart()
    message['to'] = to
    message['subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    with open(attachment_path, 'rb') as attachment_file:
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(attachment_file.read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))
        message.attach(attachment)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

    try:
        gmail_service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
        print(f"Email sent to {to}")
    except HttpError as error:
        print(f"An error occurred: {error}")

def main():
    data = read_data_from_sheet()

    for row in data[1:]:
        invoice_id, client_name, client_email, total_amount, send_invoice = row[:5]

        if send_invoice.lower() == "yes":
            output_path = f"{invoice_id}.pdf"
            create_invoice_pdf(data, output_path)

            subject = f"Invoice #{invoice_id}"
            body = f"Dear {client_name},\n\nPlease find attached the invoice #{invoice_id} for the total amount of {total_amount}.\n\nThank you for your business.\n\nBest regards,\nYour Company"
            send_email(client_email, subject, body, output_path)

            os.remove(output_path)

if __name__ == '__main__':
    main()
