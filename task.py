class Task:
    """
    Represents a task with unique ID, title, priority, and quadrant.
    Quadrant indicates the task's categorization based on urgency and importance.
    """
    def __init__(self, task_id, title, priority, quadrant):
        self.task_id = task_id
        self.title = title
        self.priority = priority
        self.quadrant = quadrant

    def __str__(self):
        """
        Returns a formatted string representation of the task for easy display.
        """
        return f"{self.task_id}: {self.title} - Priority: {self.priority} - Quadrant: {self.quadrant}"


class Node:
    """
    Represents a node in a linked list structure, holding a Task object and a pointer to the next node.
    """
    def __init__(self, task):
        self.task = task
        self.next = None


class TaskList:
    """
    Implements a linked list to manage tasks, sorted by priority.
    Lower priority numbers indicate higher importance.
    """
    def __init__(self):
        self.head = None  # Points to the first node in the list
        self.task_counter = 1  # Auto-incrementing counter for assigning unique task IDs

    def add_task(self, title, priority, quadrant):
        """
        Adds a new task to the list, maintaining sorted order by priority.
        Parameters:
        - title: Title of the task
        - priority: Integer representing task priority (lower is more important)
        - quadrant: Integer (1-4) indicating task urgency/importance category
        """
        # Input validation
        if not isinstance(priority, int) or priority < 1:
            raise ValueError("Priority must be a positive integer.")
        if quadrant not in [1, 2, 3, 4]:
            raise ValueError("Quadrant must be between 1 and 4.")

        # Create a new task and wrap it in a Node
        new_task = Task(self.task_counter, title, priority, quadrant)
        new_node = Node(new_task)
        self.task_counter += 1

        # Insert the new task in the correct position in the list
        if not self.head or self.head.task.priority > priority:
            new_node.next = self.head
            self.head = new_node
            print("Task added successfully!")
            return new_task.task_id

        # Traverse the list to find the appropriate insertion point
        current = self.head
        while current.next and current.next.task.priority <= priority:
            current = current.next
        new_node.next = current.next
        current.next = new_node
        print("Task added successfully!")
        return new_task.task_id

    def remove_task(self, task_id):
        """
        Removes a task from the list by its task ID.
        Parameters:
        - task_id: Unique ID of the task to be removed
        """
        # Input validation
        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer.")

        current = self.head
        previous = None

        # Traverse the list to locate the task
        while current:
            if current.task.task_id == task_id:
                if previous:  # If task is in the middle or end of the list
                    previous.next = current.next
                else:  # If task is at the head
                    self.head = current.next
                print(f"Task {task_id} removed successfully!")
                return current.task
            previous = current
            current = current.next

        # If task was not found
        print("Task not found.")
        return None

    def display_tasks(self):
        """
        Displays all tasks in the list in order of their priority.
        """
        if not self.head:
            print("No tasks available.")
            return

        # Traverse the list and print each task
        current = self.head
        while current:
            print(current.task)
            current = current.next
