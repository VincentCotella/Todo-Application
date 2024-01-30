import tkinter as tk
from tkinter import ttk, messagebox
import time 

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")

        # Frame for mandatory task entry
        self.entry_frame = tk.Frame(root)
        self.entry_frame.pack(pady=10)

        tk.Label(self.entry_frame, text="Task Name:").pack(side=tk.LEFT)
        self.task_name_entry = tk.Entry(self.entry_frame, width=20)
        self.task_name_entry.pack(side=tk.LEFT, padx=(0, 5))

        self.add_button = tk.Button(self.entry_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.LEFT)

        # Frame for optional task details
        self.optional_frame = tk.LabelFrame(root, text="Optional Details")
        self.optional_frame.pack(pady=10)

        tk.Label(self.optional_frame, text="Description:").pack(side=tk.LEFT)
        self.task_description_entry = tk.Entry(self.optional_frame, width=20)
        self.task_description_entry.pack(side=tk.LEFT, padx=(0, 5))

        # Due Date Entry with Placeholder
        tk.Label(self.optional_frame, text="Due Date:").pack(side=tk.LEFT)
        self.due_date_entry = tk.Entry(self.optional_frame, width=15, fg='grey')
        self.due_date_entry.insert(0, "YYYY-MM-DD")
        self.due_date_entry.bind("<FocusIn>", self.on_focus_in_due_date)
        self.due_date_entry.pack(side=tk.LEFT, padx=(0, 5))

        tk.Label(self.optional_frame, text="Importance:").pack(side=tk.LEFT)
        self.importance_combobox = ttk.Combobox(self.optional_frame, values=["Low", "Medium", "High"], width=10)
        self.importance_combobox.pack(side=tk.LEFT, padx=(0, 5))

        # Listbox for tasks
        self.tasks_listbox = tk.Listbox(root, width=80)
        self.tasks_listbox.pack(pady=10)
        self.tasks_listbox.bind("<Double-1>", self.show_task_details)  # Bind double-click event

        # Frame for task actions
        self.action_frame = tk.Frame(root)
        self.action_frame.pack(pady=10)

        self.complete_button = tk.Button(self.action_frame, text="Complete Task", command=self.complete_task)
        self.complete_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.action_frame, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # Sorting Buttons
        self.sorting_frame = tk.Frame(root)
        self.sorting_frame.pack(pady=5)

        self.sort_added_button = tk.Button(self.sorting_frame, text="Sort by Added Order", command=self.sort_by_added)
        self.sort_added_button.pack(side=tk.LEFT, padx=5)

        self.sort_date_button = tk.Button(self.sorting_frame, text="Sort by Due Date", command=self.sort_by_date)
        self.sort_date_button.pack(side=tk.LEFT, padx=5)

        self.sort_importance_button = tk.Button(self.sorting_frame, text="Sort by Importance", command=self.sort_by_importance)
        self.sort_importance_button.pack(side=tk.LEFT, padx=5)

        self.tasks = []

    def on_focus_in_due_date(self, event):
        if self.due_date_entry.get() == 'YYYY-MM-DD':
            self.due_date_entry.delete(0, tk.END)
            self.due_date_entry.config(fg='black')

    def add_task(self):
        task_name = self.task_name_entry.get()
        task_description = self.task_description_entry.get()
        due_date = self.due_date_entry.get()
        importance = self.importance_combobox.get()
    
        if task_name:
            task = {
                "name": task_name,
                "description": task_description,
                "due_date": due_date if due_date and due_date != 'YYYY-MM-DD' else "N/A",
                "importance": importance if importance else "Medium",
                "completed": False,
                "timestamp": time.time() 

            }
            self.tasks.append(task)
            self.update_tasks_listbox()
            self.task_name_entry.delete(0, tk.END)
            self.task_description_entry.delete(0, tk.END)
            self.due_date_entry.delete(0, tk.END)
            self.due_date_entry.insert(0, "YYYY-MM-DD")
            self.due_date_entry.config(fg='grey')
        else:
            messagebox.showwarning("Warning", "Task name is required.")
            
    def delete_task(self):
        selected_indices = self.tasks_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select a task to delete.")
            return

        # Confirmation dialog
        response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected task(s)?")
        if response:  # If user confirms deletion
            for index in selected_indices[::-1]:
                del self.tasks[index]
            self.update_tasks_listbox()

    def complete_task(self):
        selected_indices = self.tasks_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select a task to complete.")
            return
        for index in selected_indices:
            self.tasks[index]["completed"] = True
        self.update_tasks_listbox()

    def show_task_details(self, event):
        selected_index = self.tasks_listbox.curselection()
        if selected_index:
            selected_task = self.tasks[selected_index[0]]
            details = (
                f"Task Name: {selected_task['name']}\n"
                f"Description: {selected_task['description']}\n"
                f"Due Date: {selected_task['due_date']}\n"
                f"Importance: {selected_task['importance']}\n"
                f"Status: {'Completed' if selected_task['completed'] else 'Pending'}"
            )
            messagebox.showinfo("Task Details", details)

    def sort_by_added(self):
        self.tasks = sorted(self.tasks, key=lambda x: self.tasks.index(x))
        self.update_tasks_listbox()

    def sort_by_date(self):
        self.tasks = sorted(self.tasks, key=lambda x: x['timestamp'])
        self.update_tasks_listbox()

    def sort_by_importance(self):
        self.tasks = sorted(self.tasks, key=lambda x: ("Low", "Medium", "High").index(x["importance"]), reverse=True)
        self.update_tasks_listbox()

    def update_tasks_listbox(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.tasks:
            task_text = f"{task['name']} - {task['description']} - Due: {task['due_date']} - Importance: {task['importance']} [{'Completed' if task['completed'] else 'Pending'}]"
            self.tasks_listbox.insert(tk.END, task_text)

def main():
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
