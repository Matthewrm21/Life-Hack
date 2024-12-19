import os
import json
from datetime import datetime

# relative location of script
folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "task_manager")
file_path = os.path.join(folder_path, "tasks.json")

# check the folder exists
def setup():
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Check the file exists
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump([], f)

# load tasks from the file
def load_tasks():
    with open(file_path, 'r') as f:
        return json.load(f)

# save tasks to the file
def save_tasks(tasks):
    with open(file_path, 'w') as f:
        json.dump(tasks, f, indent=4)

# add a new task
def add_task():
    task = input("What task do you need to remember? ")
    date_input = input("Enter the date (mm/dd) or leave blank for no date: ")
    task_date = None

    # ensure correct date format
    if date_input:
        try:
            task_date = datetime.strptime(date_input, "%m/%d").strftime("%m/%d")
        except ValueError:
            print("Invalid date format. Task will be added without a date.")
            task_date = None

    tasks = load_tasks()
    tasks.append({"task": task, "completed": False, "date": task_date})
    save_tasks(tasks)
    print("Task added successfully.")

# view all tasks
def view_tasks():
    tasks = load_tasks()
    if not tasks:
        print("Your schedule is empty.")
        return

    # separate tasks with and without dates
    dated_tasks = [t for t in tasks if t.get("date")]
    no_date_tasks = [t for t in tasks if not t.get("date")]

    # sort tasks by date
    try:
        dated_tasks.sort(key=lambda x: datetime.strptime(x["date"], "%m/%d"))
    except ValueError:
        pass

    # show all tasks
    print("Your schedule:")
    sorted_tasks = dated_tasks + no_date_tasks
    for i, task in enumerate(sorted_tasks, 1):
        status = "[Completed]" if task["completed"] else "[Pending]"
        date_str = f" (Due: {task['date']})" if task.get("date") else ""
        print(f"{i}. {task['task']}{date_str} {status}")

# mark a task as complete
def mark_task_complete():
    tasks = load_tasks()
    if not tasks:
        print("No tasks to mark as complete.")
        return

    # separate and sort tasks
    dated_tasks = [t for t in tasks if t.get("date")]
    no_date_tasks = [t for t in tasks if not t.get("date")]
    try:
        dated_tasks.sort(key=lambda x: datetime.strptime(x["date"], "%m/%d"))
    except ValueError:
        pass

    sorted_tasks = dated_tasks + no_date_tasks

    # display tasks
    print("Your schedule:")
    for i, task in enumerate(sorted_tasks, 1):
        status = "[Completed]" if task["completed"] else "[Pending]"
        date_str = f" (Due: {task['date']})" if task.get("date") else ""
        print(f"{i}. {task['task']}{date_str} {status}")

    # mark a task as complete
    try:
        task_number = int(input("Enter the task number to mark as complete: "))
        if 1 <= task_number <= len(sorted_tasks):
            # update the original task in the unsorted list
            selected_task = sorted_tasks[task_number - 1]
            for task in tasks:
                if task == selected_task:
                    task["completed"] = True
                    break
            save_tasks(tasks)
            print("Task marked as complete.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

# delete a task
def delete_task():
    tasks = load_tasks()
    if not tasks:
        print("No tasks to delete.")
        return

    # separate and sort tasks
    dated_tasks = [t for t in tasks if t.get("date")]
    no_date_tasks = [t for t in tasks if not t.get("date")]
    try:
        dated_tasks.sort(key=lambda x: datetime.strptime(x["date"], "%m/%d"))
    except ValueError:
        pass

    sorted_tasks = dated_tasks + no_date_tasks

    # display tasks
    print("Your schedule:")
    for i, task in enumerate(sorted_tasks, 1):
        status = "[Completed]" if task["completed"] else "[Pending]"
        date_str = f" (Due: {task['date']})" if task.get("date") else ""
        print(f"{i}. {task['task']}{date_str} {status}")

    # delete a task
    try:
        task_number = int(input("Enter the task number to delete: "))
        if 1 <= task_number <= len(sorted_tasks):
            # remove the original task from the unsorted list
            selected_task = sorted_tasks[task_number - 1]
            tasks.remove(selected_task)
            save_tasks(tasks)
            print(f"Task '{selected_task['task']}' has been deleted.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

# main menu
def main():
    setup()
    while True:
        print("\nTask Manager")
        print("1. Add a new task")
        print("2. View schedule")
        print("3. Mark a task as complete")
        print("4. Delete a task")
        print("5. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            mark_task_complete()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()