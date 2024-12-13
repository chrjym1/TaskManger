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
            return new_task.task_id

        current = self.head
        while current.next and current.next.task.priority <= priority:
            current = current.next
        new_node.next = current.next
        current.next = new_node
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
                return current.task
            previous = current
            current = current.next
        return None

    def display_tasks(self):
        if not self.head:
            print("No tasks available.")
            return

        current = self.head
        while current:
            print(current.task)
            current = current.next

    def get_task_by_id(self, task_id):
        current = self.head
        while current:
            if current.task.task_id == task_id:
                return current.task
            current = current.next
        return None

class Queue:
    def __init__(self):
        self.quadrant_1 = TaskList()
        self.quadrant_2 = TaskList()
        self.quadrant_3 = TaskList()
        self.quadrant_4 = TaskList()
        self.undo_stack = []
        self.redo_stack = []

    def add_action(self, action, task):
        """Adds an action to the undo stack and clears the redo stack."""
        self.undo_stack.append((action, task))
        self.redo_stack.clear()

    def get_quadrant(self, quadrant):
        """Returns the TaskList for the specified quadrant."""
        if quadrant == 1:
            return self.quadrant_1
        elif quadrant == 2:
            return self.quadrant_2
        elif quadrant == 3:
            return self.quadrant_3
        elif quadrant == 4:
            return self.quadrant_4
        else:
            raise ValueError("Invalid quadrant. Please choose between 1, 2, 3, and 4.")

    def add_task_to_queue(self, title, priority, quadrant):
        """Adds a task to the appropriate quadrant and logs the action."""
        try:
            quadrant_list = self.get_quadrant(quadrant)
            task_id = quadrant_list.add_task(title, priority, quadrant)
            task = quadrant_list.get_task_by_id(task_id)
            self.add_action('add', task)
            return task
        except ValueError as e:
            print(f"Error adding task: {e}")
        return None

    def remove_task_from_queue(self, task_id, quadrant):
        """Removes a task from the specified quadrant and logs the action."""
        try:
            quadrant_list = self.get_quadrant(quadrant)
            task = quadrant_list.remove_task(task_id)
            if task:
                self.add_action('remove', task)
                return task
        except ValueError as e:
            print(f"Error removing task: {e}")
        return None

    def undo(self):
        """Undoes the last action by reverting its effects."""
        if not self.undo_stack:
            print("No actions to undo.")
            return

        action, task = self.undo_stack.pop()

        if action == 'add':
            # Reverse an 'add' action by removing the task
            self.get_quadrant(task.quadrant).remove_task(task.task_id)
            self.redo_stack.append(('remove', task))
        elif action == 'remove':
            # Reverse a 'remove' action by adding the task back
            self.get_quadrant(task.quadrant).add_task(task.title, task.priority, task.quadrant)
            self.redo_stack.append(('add', task))

    def redo(self):
        """Redoes the last undone action."""
        if not self.redo_stack:
            print("No actions to redo.")
            return

        action, task = self.redo_stack.pop()

        if action == 'add':
            # Reapply an 'add' action
            self.get_quadrant(task.quadrant).add_task(task.title, task.priority, task.quadrant)
            self.undo_stack.append(('add', task))
        elif action == 'remove':
            # Reapply a 'remove' action
            self.get_quadrant(task.quadrant).remove_task(task.task_id)
            self.undo_stack.append(('remove', task))

    def display_queue(self):
        """Displays all tasks grouped by quadrants."""
        print("Quadrant 1: Urgent and Important")
        self.quadrant_1.display_tasks()
        print("\nQuadrant 2: Not Urgent but Important")
        self.quadrant_2.display_tasks()
        print("\nQuadrant 3: Urgent but Not Important")
        self.quadrant_3.display_tasks()
        print("\nQuadrant 4: Not Urgent and Not Important")
        self.quadrant_4.display_tasks()

    def display_history(self):
        """Displays the undo and redo history."""
        print("\nUndo Stack (most recent first):")
        for action, task in reversed(self.undo_stack):
            print(f"Action: {action}, Task: {task}")

        print("\nRedo Stack (most recent first):")
        for action, task in reversed(self.redo_stack):
            print(f"Action: {action}, Task: {task}")
