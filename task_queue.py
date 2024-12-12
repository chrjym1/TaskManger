from task import TaskList

class Queue:
    def __init__(self):
        # Initialize task lists for each quadrant and stacks for undo/redo
        self.quadrant_1 = TaskList()
        self.quadrant_2 = TaskList()
        self.quadrant_3 = TaskList()
        self.quadrant_4 = TaskList()
        self.undo_stack = []
        self.redo_stack = []

    def add_action(self, action):
        """Record an action and clear the redo stack on new actions."""
        self.undo_stack.append(action)
        self.redo_stack.clear()  # Clear redo stack on new action

    def get_quadrant(self, quadrant):
        """Helper method to return the appropriate quadrant."""
        if quadrant == 1:
            return self.quadrant_1
        elif quadrant == 2:
            return self.quadrant_2
        elif quadrant == 3:
            return self.quadrant_3
        elif quadrant == 4:
            return self.quadrant_4
        else:
            print("Invalid quadrant. Please choose between 1, 2, 3, and 4.")
            return None

    def get_task_by_id(self, task_id, quadrant):
        """Retrieve a task by its ID from a specific quadrant."""
        quadrant_list = self.get_quadrant(quadrant)
        if quadrant_list:
            return quadrant_list.get_task_by_id(task_id)
        return None

    def add_task_to_queue(self, title, priority, quadrant):
        """Add a task to a specified quadrant."""
        try:
            quadrant_list = self.get_quadrant(quadrant)
            if quadrant_list:
                task = quadrant_list.add_task(title, priority, quadrant)
                # Record the action
                self.add_action(('add', task))
                return task
        except ValueError as e:
            print(f"Error adding task: {e}")
        return None

    def remove_task_from_queue(self, task_id, quadrant):
        """Remove a task by its ID from a specific quadrant."""
        try:
            quadrant_list = self.get_quadrant(quadrant)
            if quadrant_list:
                task = quadrant_list.remove_task(task_id)
                if task:
                    self.add_action(('remove', task))
                return task
        except ValueError as e:
            print(f"Error removing task: {e}")
        return None

    def undo(self):
        """Undo the last action."""
        if not self.undo_stack:
            print("No actions to undo.")
            return
        
        action, task = self.undo_stack.pop()
        if not task:
            print("No valid task to undo.")
            return
        
        if action == 'add':
            self.remove_task_from_queue(task.task_id, task.quadrant)
            self.redo_stack.append(('remove', task))
        elif action == 'remove':
            self.add_task_to_queue(task.title, task.priority, task.quadrant)
            self.redo_stack.append(('add', task))

    def redo(self):
        """Redo the last undone action."""
        if not self.redo_stack:
            print("No actions to redo.")
            return
        
        action, task = self.redo_stack.pop()
        if not task:
            print("No valid task to redo.")
            return
        
        if action == 'add':
            self.add_task_to_queue(task.title, task.priority, task.quadrant)
            self.undo_stack.append(('add', task))
        elif action == 'remove':
            self.remove_task_from_queue(task.task_id, task.quadrant)
            self.undo_stack.append(('remove', task))

    def display_queue(self):
        """Display all tasks in the queue, grouped by quadrant."""
        print("Quadrant 1: Urgent and Important")
        self.quadrant_1.display_tasks()
        print("\nQuadrant 2: Not Urgent but Important")
        self.quadrant_2.display_tasks()
        print("\nQuadrant 3: Urgent but Not Important")
        self.quadrant_3.display_tasks()
        print("\nQuadrant 4: Not Urgent and Not Important")
        self.quadrant_4.display_tasks()

    def display_history(self):
        """Display the history of actions in the undo and redo stacks."""
        print("\nUndo Stack (most recent first):")
        for action, task in reversed(self.undo_stack):
            print(f"Action: {action}, Task: {task}")

        print("\nRedo Stack (most recent first):") 
        for action, task in reversed(self.redo_stack): 
            print(f"Action: {action}, Task: {task}")
