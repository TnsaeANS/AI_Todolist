import spacy
import dateparser

NLP = spacy.load("en_core_web_sm")

def process_command(command):
    doc = NLP(command.lower())

    intent = None
    entities = {"task_description": "", "task_id": None, "due_date": None}

    if any(token.lemma_ in ["add", "create", "insert"] for token in doc):
        intent = "add_task"
    elif any(token.lemma_ in ["delete", "remove", "erase"] for token in doc):
        intent = "delete_task"
    elif any(token.lemma_ in ["complete", "finish", "done"] for token in doc):
        intent = "complete_task"
    elif any(token.lemma_ in ["list", "show", "display"] for token in doc):
        intent = "list_tasks"
    elif any(token.lemma_ in ["reminder", "due"] for token in doc):
        intent = "show_reminders"
    elif any(token.lemma_ in ["exit", "quit", "bye"] for token in doc):
        return "exit", {}

    task_description_parts = []
    for token in doc:
        if token.lemma_ not in ["add", "create", "insert", "delete", "remove", "erase", "complete", "finish", "done", "list", "show", "display", "reminder", "due", "exit", "quit", "bye", "task"]:
            task_description_parts.append(token.text)

    if intent in ["delete_task", "complete_task"]:
        for ent in doc.ents:
            if ent.label_ == "CARDINAL":
                entities["task_id"] = ent.text
                break

    if intent == "add_task":
        for ent in doc.ents:
            if ent.label_ in ["DATE", "TIME"]:
                parsed_date = dateparser.parse(ent.text, settings={'PREFER_DATES_FROM': 'future'})
                if parsed_date:
                    entities["due_date"] = parsed_date.strftime("%Y-%m-%d")
                    for part in ent.text.split():
                        if part in task_description_parts:
                            task_description_parts.remove(part)
                    break

    entities["task_description"] = " ".join(task_description_parts).strip()
    return intent, entities
