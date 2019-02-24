from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import sys
from datetime import timedelta

#DATE FORMAT : 2019-02-23 20:53:32.846516


def agendar(email,descricao,titulo,start,end):
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('./apps/calendar/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('./apps/calendar/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    end = end.isoformat()
    start = start.isoformat()
    event_body = {
      'summary': titulo,
	    'location':"Não especificado",
	    'description': descricao,
	    'start': {
	      'dateTime': start,
	      'timeZone': 'America/Bahia',
	    },
	    'end': {
	      'dateTime': end,
	      'timeZone': 'America/Bahia',
	    },
	    'recurrence': [
	      'RRULE:FREQ=DAILY;COUNT=1'
	    ],
	    'attendees': [
	      {'email': email},
	    ],
	    'reminders': {
	      'useDefault': False,
	      'overrides': [
	        {'method': 'email', 'minutes': 24 * 60},
	        {'method': 'popup', 'minutes': 10},
	      ],
	    },
	}

    event = service.events().insert(calendarId='primary', body=event_body).execute()
    return 1