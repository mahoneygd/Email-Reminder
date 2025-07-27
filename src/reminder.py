import json
from datetime import datetime
from email_sender import send_email

# Constants for file paths and notice days
EVENTS_FILE = 'data/events.json'
CONFIG_FILE = 'data/config.json'
NOTICE = 3  # Number of days ahead to notify, -1 means notify for all upcoming events regardless of days left

def load_events():
    """Load events data from the JSON file."""
    with open(EVENTS_FILE, 'r') as f:
        return json.load(f)

def load_config():
    """Load email configuration data from the JSON file."""
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def calculate_years_since(event_year, current_date, event_month, event_day):
    """
    Calculate how many years have passed since the event year,
    adjusted if the event hasn't happened yet this year.

    Parameters:
    - event_year: The year the event originally happened
    - current_date: The datetime.date object representing the event occurrence this year
    - event_month, event_day: Month and day of the event

    Returns:
    - Number of years since the event year, incremented if the event date has passed this year.
    """
    years = current_date.year - event_year

    if (event_month, event_day) < (datetime.today().month, datetime.today().day):
        years += 1

    return years

def format_event_line(event):
    """
    Format a single event line for the email body, including days left and suffix based on event type.

    Parameters:
    - event: Dictionary containing event details and calculated fields like 'days_left' and 'years_since'

    Returns:
    - Formatted string describing the event
    """
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
    """
    Filter events to those occurring within the notice period or all if notice == -1.
    Calculate days until event and years since the original event year.

    Parameters:
    - events: List of event dictionaries loaded from JSON
    - notice: Integer number of days to look ahead; -1 means all events

    Returns:
    - List of event dictionaries extended with 'days_left' and 'years_since' fields
    """
    today = datetime.today().date()
    due_events = []

    for event in events:
        event_month = event['date']['month']
        event_day = event['date']['day']

        # Create a date object for event
        event_date = datetime(year=today.year, month=event_month, day=event_day).date()

        # Recalculate date object if date has passed already this year
        if event_date < today:
            event_date = datetime(year=today.year + 1, month=event_month, day=event_day).date()

        delta_days = (event_date - today).days

        # Include the event if within notice period or notice is -1 (all events)
        if notice == -1 or delta_days <= notice:
            event_copy = event.copy()
            event_copy['days_left'] = delta_days
            event_copy['years_since'] = calculate_years_since(event['date']['year'], event_date, event_month, event_day)
            due_events.append(event_copy)

    return due_events

def process_reminders(notice):
    """
    Main process to load events, filter and format due events, then send email reminders.

    Parameters:
    - notice: Number of days ahead to notify (or -1 for all upcoming)
    """
    subject = "Upcoming Reminders"
    events = load_events()
    config = load_config()
    due_events = check_due_events(events, notice)

    if not due_events:
        return

    # Sort events by days_left ascending
    due_events_sorted = sorted(due_events, key=lambda e: e['days_left'])

    # Create body of email
    body_lines = [format_event_line(event) for event in due_events_sorted]
    body = "Upcoming reminders:\n\n" + "\n".join(body_lines)

    send_email(config, config['smtp_user'], subject, body)

if __name__ == '__main__':
    process_reminders(NOTICE)
