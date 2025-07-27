# Email-Reminder
A Python script that sends email reminders for upcoming events like birthdays and anniversaries. You can configure how many days in advance you want to be reminded. The events are pulled from a JSON file and the emails are sent via SMTP.

For privacy reasons the real events.json file is passed securely using a GitHub Secret. Since Actions can't upload files directly, the contents of events.json are Base64-encoded and stored as a secret (EVENTS_JSON_B64). During the workflow, this secret is decoded and written back into data/events.json so the Python script can read it and send reminders as usual. This ensures sensitive event data stays secure while still being accessible during the workflow run.


## Example Email

Subject: Upcoming Reminders

Upcoming reminders:

- John's (Birthday) is today! (turning 34)
- Wedding Anniversary's (Anniversary) is in 2 days (15 year anniversary)
- Jane's (Birthday) is in 10 days (turning 29)
