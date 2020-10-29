import gspread

# create a client to interact with the Google Drive API
gc = gspread.service_account(filename='client_secret.json')

# Open spreadsheet by name
humidity = gc.open_by_url('https://docs.google.com/spreadsheets/d/1WF35JEkQr129Cluj2MAp6fM3QjogUusoJytuiqaXZZs').worksheet("Humidity")

# Extract and print row 1
print(humidity.row_values(1))
