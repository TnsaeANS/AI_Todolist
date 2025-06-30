    • PEAS framework:
        ◦ Performance: Task management accuracy, reminder timeliness.
        ◦ Environment: User commands via web or command-line.
        ◦ Actuators: Display task list, reminders.
        ◦ Sensors: Text input for commands.


To run the python project- Clone the github to personal device
                         - install dependencies with pip
                               -pip install spacy
                               -pip install dateparser
                               -pip install json
- Run python main.py
All Done!


# AI To-Do List Assistant - Usage Guide

This guide provides examples of how to interact with the AI To-Do List Assistant. The assistant uses natural language processing, so you can phrase your commands in various ways.

## Adding a Task

You can add tasks with or without due dates.

- **Simple task:**
  ```
  > add buy groceries
  Task added: 'buy groceries'
  ```
- **Task with a due date:**
  ```
  > add submit the report by next Friday
  Task added: 'submit the report', due 2025-07-11
  ```
- **Different phrasing:**
  ```
  > create a new task: call the bank tomorrow
  Task added: 'call the bank', due 2025-07-01
  ```
- **More complex command:**
  ```
  > I need to add a task to prepare the presentation for August 1st
  Task added: 'prepare the presentation', due 2025-08-01
  ```

## Listing Tasks

You can ask to see your tasks in different ways.

- **Simple list:**
  ```
  > list
  ```
- **Alternative phrasing:**
  ```
  > show me all my tasks
  ```

## Completing a Task

Reference the task by its number.

- **Simple command:**
  ```
  > complete 3
  ```
- **More descriptive command:**
  ```
  > mark task number 1 as done
  ```

## Deleting a Task

Reference the task by its number.

- **Simple command:**
  ```
  > delete 2
  ```
- **Alternative phrasing:**
  ```
  > remove task 4
  ```

## Getting Reminders

Check for tasks that are due.

- **Simple command:**
  ```
  > reminders
  ```
- **Alternative phrasing:**
  ```
  > show me what's due
  ```

## Exiting the Application

You can use any of the following commands to exit:

- `exit`
- `quit`
- `bye`
