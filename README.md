# Dynamic Invoice Generator

A Python script that automatically generates and sends invoices to clients based on the data entered in a Google Sheet.

## Prerequisites

- Python 3.x installed on your system
- A Google Cloud Platform (GCP) project with Google Sheets API and Gmail API enabled
- A `credentials.json` file for your GCP project
- A Google Sheet containing invoice data with the following columns:
  1. Invoice ID
  2. Client Name
  3. Client Email
  4. Total Amount
  5. Send Invoice
  6. (optional) Other columns

## Setup

1. Clone the repository or download the `dynamic_invoice_generator.py` and `requirements.txt` files.

2. Install the required Python packages by running the following command:

   ```bash
   pip install -r requirements.txt
   ```

3. Update the `dynamic_invoice_generator.py` script with your `SERVICE_ACCOUNT_FILE`, `SPREADSHEET_ID`, and `INVOICE_TEMPLATE_PATH`.

## Usage

Run the script using the following command:

```bash
python dynamic_invoice_generator.py
```

The script will read the data from your Google Sheet, generate invoices as PDF files, and send them via email to the specified clients if the "Send Invoice" column is set to "YES."

## Automation

To automate the execution of the script, you can set up a scheduled task (e.g., using `cron` on a Linux system or Task Scheduler on Windows) to run it at regular intervals.
