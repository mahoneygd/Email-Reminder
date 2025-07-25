import json
from datetime import datetime
from email_sender import send_email

EVENTS_FILE = 'data/events.json'
CONFIG_FILE = 'data/config.json'

def load_events():
    with open(EVENTS_FILE, 'r') as f:
        return json.load(f)

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def check_due_events(events):
    today = datetime.today().strftime('%Y-%m-%d')
    due_events = [event for event in events if event['date'] == today]
    return due_events

def process_reminders():
    events = load_events()
    config = load_config()
    due_events = check_due_events(events)

    for event in due_events:
        subject = f"Reminder: {event['title']}"
        body = f"Hi! This is a reminder for {event['title']} scheduled on {event['date']}."
        send_email(config, event['email'], subject, body)

if __name__ == '__main__':
    process_reminders()
