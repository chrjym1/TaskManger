from task import TaskList


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
