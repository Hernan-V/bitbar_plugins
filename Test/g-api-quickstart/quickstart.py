#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# <bitbar.title>Test read spreadsheet</bitbar.title>
# <bitbar.author>Hernan Valenzuela</bitbar.author>
# <bitbar.author.github>Hernan-V</bitbar.author.github>
# <bitbar.image></bitbar.image>
# <bitbar.desc>How to read a Google Sheet</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>
# <bitbar.version>v1.0</bitbar.version>


from __future__ import print_function
import sys
import os
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import numpy as np


print("🔒")
print("---")
chrome_path = "/usr/local/bin/chrome"
pbcopy_path = "/usr/local/bin/ctrlc"

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    group = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(os.path.join(sys.path[0], 'token.pickle')):
        with open(os.path.join(sys.path[0], 'token.pickle'), 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(sys.path[0], "credentials.json"), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(os.path.join(sys.path[0], 'token.pickle'), 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        values.sort(key=lambda x: x[4])
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            if group != (row[4]):
                group = row[4]
                print('%s' % (row[4]))
            print("--" + '%s' % (row[0]) + "| trim=true, color=blue bash=" + pbcopy_path + " param1=" + (row[0]) + " terminal=false")

    print("---")
    print("Reference Sheet | trim=true, color=green bash=" + chrome_path + " param1=-u param2=https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit#gid=0 terminal=false refresh=true")


if __name__ == '__main__':
    main()
