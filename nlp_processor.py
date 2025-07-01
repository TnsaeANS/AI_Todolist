import spacy
import dateparser

NLP = spacy.load("en_core_web_sm")

def process_command(command):
    doc = NLP(command.lower())

    intent = None
    entities = {
        "task_description": "",
        "task_id": None,
        "due_date": None,
        "due_time": None,         # NEW
        "importance": "medium importance"  # NEW default
    }

    if any(token.lemma_ in ["add", "create", "insert"] for token in doc):
        intent = "add_task"
    elif any(token.lemma_ in ["delete", "remove", "erase"] for token in doc):
        intent = "delete_task"
    elif any(token.lemma_ in ["complete", "finish", "done"] for token in doc):
        intent = "complete_task"
    elif any(token.lemma_ in ["list", "show", "display"] for token in doc):
        intent = "list_tasks"
    elif any(token.lemma_ in ["exit", "quit", "bye"] for token in doc):
        return "exit", {}

    task_description_parts = []
    for token in doc:
        if token.lemma_ not in [
            "add", "create", "insert", "delete", "remove", "erase",
            "complete", "finish", "done", "list", "show", "display",
            "reminder", "due", "exit", "quit", "bye", "task"
        ]:
            task_description_parts.append(token.text)

    # Extract task ID if mentioned
    if intent in ["delete_task", "complete_task"]:
        for ent in doc.ents:
            if ent.label_ == "CARDINAL":
                entities["task_id"] = ent.text
                break

    # Extract due date/time and remove those words from description
    if intent == "add_task":
        for ent in doc.ents:
            if ent.label_ in ["DATE", "TIME"]:
                parsed = dateparser.parse(ent.text, settings={'PREFER_DATES_FROM': 'future'})
                if parsed:
                    entities["due_date"] = parsed.strftime("%Y-%m-%d")
                    entities["due_time"] = parsed.strftime("%H:%M") if parsed.time() else None
                    for part in ent.text.split():
                        if part in task_description_parts:
                            task_description_parts.remove(part)

        # Detect importance level
        importance_keywords = {
            "very important": ["very important", "urgent", "asap"],
            "low": ["low", "not urgent"],
            "medium importance": ["medium", "normal"]
        }

        for level, keywords in importance_keywords.items():
            if any(word in command.lower() for word in keywords):
                entities["importance"] = level
                for word in keywords:
                    if word in task_description_parts:
                        task_description_parts.remove(word)
                break

    entities["task_description"] = " ".join(task_description_parts).strip()
    return intent, entities
