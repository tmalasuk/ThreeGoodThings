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
    return render_template('index.html', entries=entries, entry_count=entry_count)

@app.route('/submit', methods=['POST'])
def submit():
    try:
        good_thing = request.form.get('good_thing')
        date = datetime.now().strftime("%B %d, %Y %H:%M")
        new_entry = {'text': good_thing, 'date': date}
        entries.insert(0, new_entry)  # Insert new entry at the beginning of the list
        save_entries(entries)  # Save entries to JSON file
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error submitting entry: {e}")
        return "An error occurred while submitting your entry.", 500

if __name__ == '__main__':
    app.run(debug=True)
