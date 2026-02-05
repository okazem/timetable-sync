import datetime
import os.path

from fastapi import FastAPI

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

app = FastAPI()


def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # token.jsonがあるなら読み込む
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    tomorrow = datetime.datetime.now().date() + datetime.timedelta(days=1)
    start_time = f"{tomorrow}T09:00:00"
    end_time = f"{tomorrow}T10:30:00"

    event = {
      "summary": "テスト授業",
      "location": "テスト教室",
      "start": {
        'dateTime': start_time,
        'timeZone': 'Asia/Tokyo',
      },
      'end': {
            'dateTime': end_time,
            'timeZone': 'Asia/Tokyo',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'popup', 'minutes': 10}]
        }
    }

    event_result = service.events().insert(calendarId='primary', body=event).execute()

    print(event_result)

  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()