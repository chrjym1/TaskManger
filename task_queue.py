from task import TaskList

class Queue:
    def __init__(self):
        self.quadrant_1 = TaskList()
        self.quadrant_2 = TaskList()
        self.quadrant_3 = TaskList()
        self.quadrant_4 = TaskList()
        self.undo_stack = []
        self.redo_stack = []

    def add_action(self, action):
        self.undo_stack.append(action)
        self.redo_stack.clear()  # Clear redo stack on new action

    def add_task_to_queue(self, title, priority, quadrant):
        try:
            if quadrant == 1:
                task = self.quadrant_1.add_task(title, priority, quadrant)
            elif quadrant == 2:
                task = self.quadrant_2.add_task(title, priority, quadrant)
            elif quadrant == 3:
                task = self.quadrant_3.add_task(title, priority, quadrant)
            elif quadrant == 4:
                task = self.quadrant_4.add_task(title, priority, quadrant)
            else:
                print("Invalid quadrant. Please choose between 1, 2, 3, and 4.")
                return None

            # Record the action
            self.add_action(('add', task))
            return task
        except ValueError as e:
            print(e)
            return None

    def remove_task_from_queue(self, task_id, quadrant):
        try:
            if quadrant == 1:
                task = self.quadrant_1.remove_task(task_id)
            elif quadrant == 2:
                task = self.quadrant_2.remove_task(task_id)
            elif quadrant == 3:
                task = self.quadrant_3.remove_task(task_id)
            elif quadrant == 4:
                task = self.quadrant_4.remove_task(task_id)
            else:
                print("Invalid quadrant. Please choose between 1, 2, 3, and 4.")
                return None
            
            # Record the action
            if task:
                self.add_action(('remove', task))
            return task
        except ValueError as e:
            print(e)
            return None

    def undo(self):
        if not self.undo_stack:
            print("No actions to undo.")
            return
        
        action, task = self.undo_stack.pop()
        if task is None:
            print("No valid task to undo.")
            return
        if action == 'add':
            self.remove_task_from_queue(task.id, task.quadrant)
            self.redo_stack.append(('remove', task))
        elif action == 'remove':
            self.add_task_to_queue(task.title, task.priority, task.quadrant)
            self.redo_stack.append(('add', task))

    def redo(self):
        if not self.redo_stack:
            print("No actions to redo.")
            return
        
        action, task = self.redo_stack.pop()
        if task is None:
            print("No valid task to redo.")
            return
        if action == 'add':
            self.add_task_to_queue(task.title, task.priority, task.quadrant)
            self.undo_stack.append(('add', task))
        elif action == 'remove':
            self.remove_task_from_queue(task.id, task.quadrant)
            self.undo_stack.append(('remove', task))

    def display_queue(self):
        print("Quadrant 1: Urgent and Important")
        self.quadrant_1.display_tasks()
        print("\nQuadrant 2: Not Urgent but Important")
        self.quadrant_2.display_tasks()
        print("\nQuadrant 3: Urgent but Not Important")
        self.quadrant_3.display_tasks()
        print("\nQuadrant 4: Not Urgent and Not Important")
        self.quadrant_4.display_tasks()
