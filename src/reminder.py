import json
from datetime import datetime
from email_sender import send_email

EVENTS_FILE = 'data/events.json'
CONFIG_FILE = 'data/config.json'
NOTICE = -1


def load_events():
    with open(EVENTS_FILE, 'r') as f:
        return json.load(f)


def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)


def calculate_years_since(event_year, current_date, event_month, event_day):
    years = current_date.year - event_year
    if (event_month, event_day) < (current_date.month, current_date.day):
        years += 1
    return years


def format_event_line(event):
    days_left = event['days_left']
    years_since = event['years_since']
    event_type = event['type'].lower()

    if event_type == 'birthday':
        suffix = f"turning {years_since}"
    elif event_type == 'anniversary':
        suffix = f"{years_since} year anniversary"
    else:
        suffix = f"{years_since} years"

    if days_left == 0:
        line = f"- {event['title']}'s ({event['type']}) is today! ({suffix})"
    elif days_left == 1:
        line = f"- {event['title']}'s ({event['type']}) is in 1 day ({suffix})"
    else:
        line = f"- {event['title']}'s ({event['type']}) is in {days_left} days ({suffix})"

    return line


def check_due_events(events, notice):
    today = datetime.today().date()
    due_events = []

    for event in events:
        event_month = event['date']['month']
        event_day = event['date']['day']

        event_date = datetime(year=today.year, month=event_month, day=event_day).date()
        if event_date < today:
            event_date = datetime(year=today.year + 1, month=event_month, day=event_day).date()

        delta_days = (event_date - today).days

        if notice == -1 or delta_days <= notice:
            event_copy = event.copy()
            event_copy['days_left'] = delta_days
            event_copy['years_since'] = calculate_years_since(event['date']['year'], event_date, event_month, event_day)
            due_events.append(event_copy)

    return due_events

def process_reminders(notice):
    subject = "Upcoming Reminders"
    events = load_events()
    config = load_config()
    due_events = check_due_events(events, notice)

    if not due_events:
        return

    due_events_sorted = sorted(due_events, key=lambda e: e['days_left'])
    body_lines = [format_event_line(event) for event in due_events_sorted]

    body = "Upcoming reminders:\n\n" + "\n".join(body_lines)

    send_email(config, config['smtp_user'], subject, body)


if __name__ == '__main__':
    process_reminders(NOTICE)
