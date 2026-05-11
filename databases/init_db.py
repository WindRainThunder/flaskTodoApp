import sqlite3

connection = sqlite3.connect(".\\databases\\todo.db")

with open(".\\schemas\\schema.sql", "r", encoding="utf-8") as f:
    connection.executescript(f.read())

tasks = [
    ("Buy milk and bread", "Stop by the store after work and pick up a few basic groceries.", "todo"),
    ("Reply to emails", "Check your inbox and respond to messages from the client and team.", "todo"),
    ("Refill water bottle", "Keep yourself hydrated and make sure your bottle stays full.", "todo"),
    ("Plan the week", "Write down your main tasks and set priorities for the next few days.", "todo"),
    ("Take out the trash", "Bring the trash bag outside before you forget in the evening.", "todo"),
    ("Do grocery shopping", "Buy vegetables, fruit, breakfast items, and something for lunch.", "todo"),
    ("Clean the desk", "Put away unnecessary items, organize papers, and leave only what you need.", "todo"),
    ("Review meeting notes", "Go over the decisions and add any missing action items.", "todo"),
    ("Call mom", "Take a few minutes to catch up and ask how she is doing.", "todo"),
    ("Finish the project", "Focus on the final edits and close it out today.", "todo"),
    ("Book a dentist appointment", "Check available times and reserve the earliest slot.", "todo"),
    ("Prepare lunch for tomorrow", "Make a simple meal to take with you in the morning.", "todo"),
    ("Check the budget", "Review your spending and see how much is left for the week.", "todo"),
    ("Send the documents", "Attach the needed files and send them before the deadline.", "todo"),
    ("Do 20 minutes of exercise", "Take a short walk, stretch, or do a quick home workout.", "todo"),
    ("Read 10 pages", "Set aside some time to read before going to bed.", "todo"),
    ("Update the task list", "Remove finished items and add new priorities.", "todo"),
    ("Pick up the package", "Check the pickup code and stop by the parcel locker.", "todo"),
    ("Prepare materials for tomorrow", "Gather everything you’ll need for the morning.", "todo"),
    ("Take a break", "Step away from the screen, rest a little, and come back refreshed.", "todo"),
]

connection.executemany(
    "INSERT INTO tasks (title, description, status, user_id) VALUES (?, ?, ?, 1)",
    tasks
)

connection.commit()
connection.close()

