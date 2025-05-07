import pyperclip
import time
import json
import os
from datetime import datetime

history_file = "clipboard_history.json"

# Load clipboard history
def load_history():
    if os.path.exists(history_file):
        with open(history_file, 'r') as file:
            data = json.load(file)
            # Upgrade from old format (list of strings) to new format
            if isinstance(data, list) and all(isinstance(item, str) for item in data):
                return [{"text": item, "timestamp": "unknown"} for item in data]
            return data
    else:
        return []

# Save clipboard history
def save_history(history):
    with open(history_file, 'w') as file:
        json.dump(history, file, indent=4)

# Track clipboard with timestamps
def track_clipboard():
    previous_clip = pyperclip.paste()
    history = load_history()
    print("Clipboard Manager is running... Press Ctrl+C to stop.")

    while True:
        current_clip = pyperclip.paste()
        if (
            current_clip != previous_clip
            and current_clip != ""
            and not any(item["text"] == current_clip for item in history)
        ):
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
            print(f"New copy at {timestamp}: {current_clip[:30]}...")
            history.insert(0, {
                "text": current_clip,
                "timestamp": timestamp
            })
            save_history(history)
        previous_clip = current_clip
        time.sleep(1)


# Show clipboard history with timestamps
def display_history():
    history = load_history()
    if history:
        print("\nClipboard History:")
        for i, item in enumerate(history, 1):
            text_preview = item['text'][:30].replace("\n", " ")
            print(f"{i}. [{item['timestamp']}] {text_preview}...")
    else:
        print("No clipboard history found.")

# Menu
def main():
    while True:
        print("\nClipboard Manager Menu:")
        print("1. Start tracking clipboard")
        print("2. View clipboard history")
        print("3. Exit")

        choice = input("Choose an option (1/2/3): ")

        if choice == '1':
            track_clipboard()
        elif choice == '2':
            display_history()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()