#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# <bitbar.title>Read Password Normen from Google Sheet</bitbar.title>
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
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

print("🔒")
print("---")
chrome_path = "/usr/local/bin/chrome"
pbcopy_path = "/usr/local/bin/ctrlc"

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1uosNcfw7vGXdXW0GhAD7oIS4DLwtEG4XVjCCGJVbvaA'
SAMPLE_RANGE_NAME = 'Principal!A2:E'


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    group0 = None
    group1 = None
    group2 = None
    group3 = None
    chg = None
    values = None
    connError = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(os.path.join(sys.path[0], 'token.pickle')):
        with open(os.path.join(sys.path[0], 'token.pickle'), 'rb') as token:
            creds = pickle.load(token)

    try:
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

        with open(os.path.join(sys.path[0], 'backup_values.txt'), 'w') as filehandle:
            json.dump(values, filehandle)

    except Exception as e:
        connError = True
        with open(os.path.join(sys.path[0], 'backup_values.txt'), 'r') as filehandle:
            values = json.load(filehandle)
    finally:

        if not values:
            print('No data found.')
        else:
            # print(values)
            #values.sort(key=lambda x:x[4])
            for row in values:
                chg = None
                try:
                    if (row[4]) == '':
                        continue
                    if (group0 != (row[0]) and (row[0]) != '') or (group0 == None):
                        group0 = row[0] if (row[0] != None or row[0] != '') else '-'
                        print('%s' % group0)
                        chg = True
                    if (group1 != (row[1]) and (row[1]) != '') or (group1 == None) or chg == True:
                        #group1 = row[1]
                        #print("--"+'%s' % (row[1]))
                        group1 = row[1] if (row[1] != None or row[1] != '') else '-'
                        print("--" + '%s' % group1)
                        chg = True
                    if (group2 != (row[2]) and (row[2]) != '') or (group2 == None) or chg == True:
                        group2 = row[2] if (row[2] != None or row[2] != '') else '-'
                        print("----" + '%s' % group2)

                    group3 = row[3] if (row[3] != None or row[3] != '') else '-'
                    print("------" + '%s' % group3 + "| trim=true, color=blue bash=" + pbcopy_path + " param1=" + (row[4]) + " terminal=false")
                except IndexError:
                    continue

        print("---")
        print("Reference Sheet | trim=true, color=green bash=" + chrome_path + " param1=-u param2=https://docs.google.com/spreadsheets/d/1uosNcfw7vGXdXW0GhAD7oIS4DLwtEG4XVjCCGJVbvaA/edit?pli=1#gid=666997044 terminal=false refresh=true")

        if connError == True:
            print("---")
            print("Connection Error | trim=true, color=red terminal=false refresh=true")


if __name__ == '__main__':
    main()
