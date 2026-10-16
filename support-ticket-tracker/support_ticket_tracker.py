"""Support ticket tracker: create, assign, update, search, persist."""
import json
import logging

TICKETS = {}
OPEN_STATUSES = ("open", "in_progress")


def create_ticket(title, description, reporter, priority="medium",
                  category="general", audit_log=None):
    """Create a ticket and store it.

    Return the ticket, or None if the title is blank.
    """
    if not title or not title.strip():
        return None
    ticket_id = str(max((int(key) for key in TICKETS), default=0) + 1)
    ticket = {
        "id": ticket_id, "title": title, "description": description,
        "priority": priority, "category": category, "status": "open",
        "reporter": reporter, "assignee": None,
    }
    TICKETS[ticket_id] = ticket
    if audit_log is not None:
        audit_log.append(f"Created ticket {ticket_id} for {reporter}")
    return ticket


def assign_ticket(ticket_id, agent):
    """Assign a ticket to an agent. Return False if it does not exist."""
    try:
        TICKETS[ticket_id]["assignee"] = agent
    except KeyError:
        logging.warning("Cannot assign: no ticket with id %s", ticket_id)
        return False
    return True


def update_status(ticket_id, status):
    """Set a ticket's status. Return the ticket, or None if not found."""
    ticket = TICKETS.get(ticket_id)
    if ticket is None:
        logging.warning("Cannot update: no ticket with id %s", ticket_id)
        return None
    ticket["status"] = status
    return ticket


def search_tickets(status=None, priority=None):
    """Return tickets matching the given status and/or priority."""
    results = []
    for ticket in TICKETS.values():
        if status is not None and ticket["status"] != status:
            continue
        if priority and ticket["priority"] != priority:
            continue
        results.append(ticket)
    return results


def save_tickets(path="tickets.json"):
    """Write all tickets to a JSON file."""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(TICKETS, file)


def load_tickets(path="tickets.json"):
    """Replace the in-memory tickets with those read from a JSON file."""
    with open(path, "r", encoding="utf-8") as file:
        loaded = json.load(file)
    TICKETS.clear()
    TICKETS.update(loaded)


def print_ticket_report():
    """Print one line per ticket."""
    print("Support Tickets")
    if not TICKETS:
        print("No tickets yet")
    for ticket_id, ticket in TICKETS.items():
        print(ticket_id, ticket["title"], ticket["status"])


def close_ticket(ticket_id):
    """Close a ticket. Return False if the ticket does not exist."""
    return update_status(ticket_id, "closed") is not None


def is_open(ticket_id):
    """Return True if the ticket exists and is open or in progress."""
    ticket = TICKETS.get(ticket_id)
    return ticket is not None and ticket["status"] in OPEN_STATUSES


def main():
    """Run the demo."""
    logging.basicConfig(level=logging.INFO)
    create_ticket(
        "Cannot sign in", "Password reset link fails", "alex@example.com")
    create_ticket(
        "Billing question", "Charged twice", "lee@example.com", "high")
    assign_ticket("1", "agent-01")
    update_status("1", "in_progress")
    print_ticket_report()
    logging.info("Tickets created: %d", len(TICKETS))
    print("Ticket 1 open?", is_open("1"))
    ticket_id = input("Ticket id to close (Enter to skip): ")
    if ticket_id and not close_ticket(ticket_id):
        print(f"No ticket with id {ticket_id}")
    save_tickets()


if __name__ == "__main__":
    main()
