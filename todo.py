import tkinter as tk
from tkinter import messagebox, simpledialog

TASKS_FILE = "tasks.txt"  # File to save tasks

def load_tasks():
    """Load tasks from a file when the app starts."""
    try:
        with open(TASKS_FILE, "r") as file:
            tasks = file.readlines()
            for task in tasks:
                task_listbox.insert(tk.END, task.strip())
    except FileNotFoundError:
        open(TASKS_FILE, "w").close()  # Create file if it doesn't exist

def save_tasks():
    """Save all tasks to a file."""
    with open(TASKS_FILE, "w") as file:
        tasks = task_listbox.get(0, tk.END)
        for task in tasks:
            file.write(task + "\n")

def add_task(event=None):
    """Add a new task to the list."""
    task = task_entry.get().strip()
    if task:
        task_listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)
        save_tasks()
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")

def remove_task(event=None):
    """Remove the selected task from the list."""
    try:
        selected_task_index = task_listbox.curselection()[0]
        task_listbox.delete(selected_task_index)
        save_tasks()
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to remove.")

def mark_complete():
    """Mark the selected task as complete."""
    try:
        selected_task_index = task_listbox.curselection()[0]
        task = task_listbox.get(selected_task_index)
        # Avoid duplicate marks by checking if the task already starts with the check mark
        if not task.startswith("✅"):
            task_listbox.delete(selected_task_index)
            task_listbox.insert(tk.END, "✅ " + task)
            save_tasks()
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to mark as complete.")

def edit_task(event=None):
    """Edit the selected task."""
    try:
        selected_task_index = task_listbox.curselection()[0]
        current_task = task_listbox.get(selected_task_index)
        new_task = simpledialog.askstring("Edit Task", "Modify task:", initialvalue=current_task)
        if new_task:
            task_listbox.delete(selected_task_index)
            task_listbox.insert(selected_task_index, new_task)
            save_tasks()
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to edit.")

def clear_tasks():
    """Remove all tasks from the list."""
    if messagebox.askyesno("Confirm", "Are you sure you want to delete all tasks?"):
        task_listbox.delete(0, tk.END)
        save_tasks()

def toggle_theme():
    """Toggle between light and dark mode."""
    global dark_mode
    dark_mode = not dark_mode

    if dark_mode:
        root.config(bg="black")
        task_listbox.config(bg="gray20", fg="white", selectbackground="gray40")
        task_entry.config(bg="gray20", fg="white", insertbackground="white")
    else:
        root.config(bg="white")
        task_listbox.config(bg="white", fg="black", selectbackground="lightgray")
        task_entry.config(bg="white", fg="black", insertbackground="black")

def main():
    global root, task_listbox, task_entry, dark_mode

    # Create main window
    root = tk.Tk()
    root.title("To-Do List")
    root.geometry("400x500")
    root.configure(bg="white")

    dark_mode = False  # Default theme is light

    # Task Entry widget
    task_entry = tk.Entry(root, width=40)
    task_entry.pack(pady=10)
    task_entry.bind("<Return>", add_task)  # Press Enter to add task

    # Buttons for various functionalities
    tk.Button(root, text="Add Task", width=20, command=add_task).pack(pady=5)
    tk.Button(root, text="Remove Task", width=20, command=remove_task).pack(pady=5)
    tk.Button(root, text="Mark as Complete", width=20, command=mark_complete).pack(pady=5)
    tk.Button(root, text="Edit Task", width=20, command=edit_task).pack(pady=5)
    tk.Button(root, text="Clear All Tasks", width=20, command=clear_tasks).pack(pady=5)
    tk.Button(root, text="Toggle Theme", width=20, command=toggle_theme).pack(pady=5)

    # Task Listbox widget
    task_listbox = tk.Listbox(root, width=40, height=10, selectmode=tk.SINGLE)
    task_listbox.pack(pady=10)

    # Scrollbar for the listbox
    scrollbar = tk.Scrollbar(root, orient="vertical", command=task_listbox.yview)
    scrollbar.pack(side="right", fill="y")
    task_listbox.config(yscrollcommand=scrollbar.set)

    # Keyboard shortcuts
    root.bind("<Delete>", remove_task)  # Delete key removes task
    root.bind("<Control-e>", edit_task)  # Ctrl+E edits task

    # Load tasks from file
    load_tasks()

    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main()