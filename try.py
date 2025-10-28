# class All_tasks:
#     def __init__(self):
#         self.vector_of_all_tasks_objects = []

# # Create two different objects
# tasks1 = All_tasks()
# tasks2 = All_tasks()

# # Add something to the first object's list
# tasks1.vector_of_all_tasks_objects.append("Task A")

# # Now check what's in the second object's list
# print("tasks1 list:", tasks1.vector_of_all_tasks_objects)
# print("tasks2 list:", tasks2.vector_of_all_tasks_objects)

# my_list = ["apple", "banana",  "orange","banana"]
# my_list.remove("banana")
# print(my_list)
class Task:
    def __init__(self, name, date):
        self.name = name
        self.date = date

task1 = Task("homework", "today")
task2 = Task("homework", "today")  # Same content, different object
my_tasks = [task1, task2]
my_tasks.remove(task1)
