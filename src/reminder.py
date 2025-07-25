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
    current_month = datetime.today().month
    current_day = datetime.today().day
    due_events = [event for event in events
                    if event['date']['day'] == current_day and event['date']['month'] == current_month]
    return due_events

def process_reminders():
    events = load_events()
    config = load_config()
    due_events = check_due_events(events)

    if not due_events:
        return

    subject = "Today's Reminders"
    body_lines = [f"- {event['title']}'s ({event['type']})" for event in due_events]
    body = "Hi! Here are your reminders for today:\n\n" + "\n".join(body_lines)

    send_email(config, config['smtp_user'], subject, body)

if __name__ == '__main__':
    process_reminders()
