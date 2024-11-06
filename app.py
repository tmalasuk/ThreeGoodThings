from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "data.json"

# Load entries from JSON file
def load_entries():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

GOOD_DAYS_FILE = "good_days.json"

# Load or save good days to JSON
def load_good_days():
    if os.path.exists(GOOD_DAYS_FILE):
        with open(GOOD_DAYS_FILE, 'r') as file:
            return json.load(file)
    return []

def save_good_days(date_str):
    good_days = load_good_days()
    if date_str not in good_days:
        good_days.append(date_str)
        with open(GOOD_DAYS_FILE, 'w') as file:
            json.dump(good_days, file)


# Save entries to JSON file
def save_entries(entries):
    with open(DATA_FILE, 'w') as file:
        json.dump(entries, file)

# Initialize entries from file
entries = load_entries()

# Function to count entries for current day
def count_entries_today():
    today = datetime.now().date()
    count = sum(1 for entry in entries if datetime.strptime(entry['date'], "%B %d, %Y %H:%M").date() == today)
    return count

@app.route('/', methods=['GET'])
def index():
    entry_count = count_entries_today()
    good_days = load_good_days()
    return render_template('index.html', entries=entries, entry_count=entry_count, good_days=good_days)


@app.route('/submit', methods=['POST'])
def submit():
    good_thing = request.form.get('good_thing')
    date = datetime.now().strftime("%B %d, %Y %H:%M")
    new_entry = {'text': good_thing, 'date': date}
    entries.insert(0, new_entry)
    save_entries(entries)

    # Check if we have 3 entries for today
    if count_entries_today() >= 3:
        today_str = datetime.now().strftime("%Y-%m-%d")
        save_good_days(today_str)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
