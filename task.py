class Task:
    def __init__(self, task_id, title, priority, quadrant):
        self.task_id = task_id
        self.title = title
        self.priority = priority
        self.quadrant = quadrant

    def __str__(self):
        return f"{self.task_id}: {self.title} - Priority: {self.priority} - Quadrant: {self.quadrant}"

class Node:
    def __init__(self, task):
        self.task = task
        self.next = None

class TaskList:
    def __init__(self):
        self.head = None
        self.task_counter = 1

    def add_task(self, title, priority, quadrant):
        if not isinstance(priority, int) or priority < 1:
            raise ValueError("Priority must be a positive integer.")
        if quadrant not in [1, 2, 3, 4]:
            raise ValueError("Quadrant must be between 1 and 4.")

        new_task = Task(self.task_counter, title, priority, quadrant)
        new_node = Node(new_task)
        self.task_counter += 1

        if not self.head or self.head.task.priority > priority:
            new_node.next = self.head
            self.head = new_node
            print("Task added successfully!")
            return new_task.task_id

        current = self.head
        while current.next and current.next.task.priority <= priority:
            current = current.next
        new_node.next = current.next
        current.next = new_node
        print("Task added successfully!")
        return new_task.task_id

    def remove_task(self, task_id):
        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer.")

        current = self.head
        previous = None
        while current:
            if current.task.task_id == task_id:
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next
                print(f"Task {task_id} removed successfully!")
                return current.task
            previous = current
            current = current.next
        print("Task not found.")
        return None

    def display_tasks(self):
        if not self.head:
            print("No tasks available.")
            return

        current = self.head
        while current:
            print(current.task)
            current = current.next
