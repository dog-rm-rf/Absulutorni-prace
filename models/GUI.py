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
                    "if you want to see tasks for one day press 4\n" +
                    "if you want to add score to task press 5\n" +
                    "if you want quit press q")
            answer = input()
            match answer:
                    # add
                case "1":
                    self.add_task()
                    #remove
                case "2":
                    self.remove_task_gui()
                case "3":
                    self.show_all_tasks()
                case "4":
                    self.show_tasks_for_one_date()
                case "5":
                    self.add_score()
                case "q":
                    self.allTasks.save_data_frame()
                    break
                case _:
                    print("The language doesn't matter, what matters is solving problems.")

    def head(self):
        print("Hello welcome to 12 week app")  

    def add_task(self):  
        print("give name to task:")
        task_name = input()
        print("give me date:")
        date = input()
        print("give me how much hours you want to spent on the task")
        desired_time_spent = input()
        #variables for review
        learnt = ""
        dont_undersand = ""
        next_step = ""
        review = [learnt, dont_undersand, next_step]
        #list
        task = [task_name, date, desired_time_spent, None, review]
        self.allTasks.add_new_task(task)

    def remove_task_gui(self):
        print("which task you want to remove\n type name of task ")
        task_remove_name = input()
        print("I found these tasks with given name, give me the row number that you want to remove\n")
        print(self.allTasks.data_frame.loc[self.allTasks.data_frame['activity'] == task_remove_name])
        index_to_remove = int(input())
        self.allTasks.remove_task_df(index_to_remove)

    def show_all_tasks(self):
        print(self.allTasks.data_frame)
        # for task in self.list_of_all_tasks_objects:
        #     print(f"Task: {task[0]}, Date: {task[1]}")
    
    def show_tasks_for_one_date(self):
        date_to_find = input("What date do you want to see?\n")
        print(self.allTasks.data_frame.loc[self.allTasks.data_frame['date'] == date_to_find])

    def add_score(self):
        print("select the task by name")
        name = input()
        print(self.allTasks.data_frame.loc[self.allTasks.data_frame['activity'] == name])
        print("select the index")
        index_to_use = int(input())
        print("select score 0/10")
        score = int(input())
        #chtel bych mit reviews a v tom what i leartn what i dont understand, what should be next setp
        print("type key notes(review = what you learnt, what you dont understand, what should be your next step)")
        print("what you learnt")
        learnt = input()
        print("what do you not understand")
        dont_understand = input()
        print("what is your next step")
        next_step = input()
        self.allTasks.add_score_to_task(index_to_use, score, learnt, dont_understand, next_step)





        


