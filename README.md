    • PEAS framework:
        ◦ Performance: Task management accuracy, reminder timeliness.
        ◦ Environment: User commands via web or command-line.
        ◦ Actuators: Display task list, reminders.
        ◦ Sensors: Text input for commands.


To run the python streamlit project-
                        - Clone the github to personal device
                         - install dependencies with pip
                               -pip install spacy
                               -pip install dateparser
                               -pip install json
                               -pip install streamlit
- Run streamlit run app.py
All Done!



# AI To-Do CLI - Natural Language Task Manager

## Overview
This command-line interface (CLI) application lets you manage tasks using natural language commands. The system understands phrases like:

```bash
"Add finish project by Friday"
"Delete task 3" 
"Complete the budget report task"
```

Installation
Prerequisites:

    Python 3.7+
    spaCy language model

Setup:

    pip install spacy dateparser
    python -m spacy download en_core_web_sm


# Basic Commands

add complete sales report by tomorrow
```bash
Added: "complete sales report" (Due: 2023-11-16)
```

list
```bash
1. complete sales report [pending] (Due: 2023-11-16)
2. call client [completed]
```
complete 1
```bash
Marked task 1 as complete
```
delete 2
```bash
Deleted: "call client"
```

# Natural Language Examples

Adding tasks:
```bash
add book flights for vacation next Monday
create very important task: finish presentation ASAP
insert "call mom" Sunday at 2pm

```
Modifying tasks:
```bash
delete task number 3
complete the budget analysis
remove low priority tasks
```
Viewing:
```bash
show all tasks
list pending items  
display completed work
```
