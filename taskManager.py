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

class Queue:
    def __init__(self):
        self.quadrant_1 = TaskList()
        self.quadrant_2 = TaskList()
        self.quadrant_3 = TaskList()
        self.quadrant_4 = TaskList()

    def add_task_to_queue(self, title, priority, quadrant):
        try:
            if quadrant == 1:
                return self.quadrant_1.add_task(title, priority, quadrant)
            elif quadrant == 2:
                return self.quadrant_2.add_task(title, priority, quadrant)
            elif quadrant == 3:
                return self.quadrant_3.add_task(title, priority, quadrant)
            elif quadrant == 4:
                return self.quadrant_4.add_task(title, priority, quadrant)
            else:
                print("Invalid quadrant. Please choose between 1, 2, 3, and 4.")
                return None
        except ValueError as e:
            print(e)
            return None

    def remove_task_from_queue(self, task_id, quadrant):
        try:
            if quadrant == 1:
                return self.quadrant_1.remove_task(task_id)
            elif quadrant == 2:
                return self.quadrant_2.remove_task(task_id)
            elif quadrant == 3:
                return self.quadrant_3.remove_task(task_id)
            elif quadrant == 4:
                return self.quadrant_4.remove_task(task_id)
            else:
                print("Invalid quadrant. Please choose between 1, 2, 3, and 4.")
                return None
        except ValueError as e:
            print(e)
            return None

    def display_queue(self):
        print("Quadrant 1: Urgent and Important")
        self.quadrant_1.display_tasks()
        print("\nQuadrant 2: Not Urgent but Important")
        self.quadrant_2.display_tasks()
        print("\nQuadrant 3: Urgent but Not Important")
        self.quadrant_3.display_tasks()
        print("\nQuadrant 4: Not Urgent and Not Important")
        self.quadrant_4.display_tasks()
