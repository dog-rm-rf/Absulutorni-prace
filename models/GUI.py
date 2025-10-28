import sys

# Fix Windows console encoding for Czech characters
sys.stdout.reconfigure(encoding='utf-8')

class GUI:

    def __init__(self, allTasks):
        self.allTasks = allTasks

    def menu(self):
        self.head()
        #the progarm
        while True:
            print("If you want add task press 1\n" + 
                    "if you want remove press 2\n" +
                    "if you want to see all tasks press 3\n" +
                    "if you want quit press q")
            answer = input()
            match answer:
                    # add
                case "1":
                    self.addTask()
                    #remove
                case "2":
                    self.removeTask()
                case "3":
                    self.show_all_tasks()
                case "4":
                    self.show_tasks_for_one_date()
                case "q":
                    self.allTasks.saveDataFrame()
                    break
                case _:
                    print("The language doesn't matter, what matters is solving problems.")

    def head(self):
        print("Hello welcome to 12 week app")  

    def addTask(self):  
        print("give name to task:")
        task_name = input()
        print("give me date:")
        date = input()
        # p1 = Task(task_name, date)
        task = [task_name, date]
        self.allTasks.add_new_task(task)

    def removeTask(self):
        print("which task you want to remove\n type name of task ")
        task_remove_name = input()
        print("I found these tasks with given name, give me the row number that you want to remove\n")
        print(self.allTasks.tasks_dataframe.loc[self.allTasks.tasks_dataframe['activity'] == task_remove_name])
        index_to_remove = int(input())
        self.allTasks.removeTask(index_to_remove)

    def show_all_tasks(self):
        print(self.allTasks.tasks_dataframe)
        # for task in self.list_of_all_tasks_objects:
        #     print(f"Task: {task[0]}, Date: {task[1]}")
    
    def show_tasks_for_one_date(self):
        date_to_find = input("What date do you want to see?\n")
        print(self.allTasks.tasks_dataframe.loc[self.allTasks.tasks_dataframe['date'] == date_to_find])
