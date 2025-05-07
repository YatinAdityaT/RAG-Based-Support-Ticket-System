import csv
import os
import datetime

def save_feedback(query: str, ticket_id: str, feedback: str) -> None:
    """Save user feedback for ticket relevance to a CSV file."""
    feedback_file = "feedback.csv"
    file_exists = os.path.isfile(feedback_file)
    
    with open(feedback_file, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Query", "Ticket ID", "Feedback", "Timestamp"])
        writer.writerow([query, ticket_id, feedback, datetime.datetime.now().isoformat()])