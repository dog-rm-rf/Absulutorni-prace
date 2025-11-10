import sys
from pathlib import Path
import os
# Fix Windows console encoding for Czech characters
sys.stdout.reconfigure(encoding='utf-8')

class GUI:

    def __init__(self, allTasks, goal):
        self.allTasks = allTasks
        self.goal = goal


    def menu(self):
        self.head()
        # with open('number_timer.txt', 'r') as f:
        #     self.x = int(f.read())  
        
          
        #the progarm
        while True:
            for x in self.goal.list_of_all_goals_objects:
                print(f"Your goals for your 12 weeks are {x}\n")
            print(  
                    "setting your goal for 12 weeks press 0\n" +
                    "If you want add task press 1\n" + 
                    "if you want remove press 2\n" +
                    "if you want to see all tasks press 3\n" + 
                    "if you want to see tasks for one day press 4\n" +
                    "if you want to setting tasks press 5\n" +
                    "if you want to update tasks press 6\n" +
                    "if you want remove column press 7\n" +
                    "if you want to set the timer press 8\n" +
                    "if you want to - timer press 9\n" +
                    "if you want quit press q")
            answer = input()
            match answer:
                case "0":
                    self.add_goal()
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
                    self.setting_task()
                case "6":
                    self.update_task()    
                case "7":
                    self.delete_column()
                case "8":
                    self.set_timer()
                case "9":
                    self.change_timer()
                case "q":
                    self.allTasks.save_data_frame()
                    break
                case _:
                    print("The language doesn't matter, what matters is solving problems.")
    def head(self):
        print("Hello welcome to 12 week app")  

        
    # def set_timer(self):
    #     print("set the timer")
    #     timer = input()
    #     self.x = self.allTasks.setting_timer(timer)

    def add_goal(self):
        print("add a goal name")
        goal = input()
        print("set timer")
        time_input = input()
        print("set avrage score you find succesfull")
        avrage_score = int(input())
        goals = [goal, time_input, avrage_score]
        self.goal.add_goal(goals)
        
        
    def add_task(self):  
        print("give name to task:")
        task_name = input()
        print("give me name of subclass")
        task_sub_class = input()
        print("give me date:")
        date = input()
        print("give me how much hours you want to spent on the task")
        desired_time_spent = int(input())
        #variables for review
        score = None
        learnt = ""
        dont_understand = ""
        next_step = ""
        review = [learnt, dont_understand, next_step]
        #list
        task = [task_name, task_sub_class, date, desired_time_spent, score, review]
        self.allTasks.add_new_task(task)
        
    def setting_task(self):
        #chtel bych mit reviews a v tom what i leartn what i dont understand, what should be next setp
        print("select the task by name")
        name = input()
        print(self.allTasks.data_frame.loc[self.allTasks.data_frame['activity'] == name])
        print("select the index")
        index_to_use = int(input())
        print("select score 0/10")
        score = int(input())
        print("type key notes(review = what you learnt, what you dont understand, what should be your next step)")
        print("what you learnt")
        learnt = input()
        print("what do you not understand")
        dont_understand = input()
        print("what is your next step")
        next_step = input()
        self.allTasks.setting_task(name, index_to_use, score, learnt, dont_understand, next_step)
        
    def update_task(self):
        print("select the task by name")
        name = input()
        print(self.allTasks.data_frame.loc[self.allTasks.data_frame['activity'] == name])
        print("select the index")
        index_to_use = int(input())
        print("do you want to change the name pres y/n")
        yn0 = input()
        if(yn0 == "y"):
            print("type new name")
            new_name = input()
            self.allTasks.list_of_all_tasks_objects[index_to_use][0] = new_name
            self.allTasks.update_data_frame()
        else:
            pass
        print("do you want to change the subclass press y/n")
        yn1 = input()
        
        if(yn1 == "y"):
            print("type new subclass")
            subclass = input()
            self.allTasks.list_of_all_tasks_objects[index_to_use][1] = subclass
            self.allTasks.update_data_frame()
        else:
            pass
        print("do you want to change the date press y/n")
        yn2 = input()
        
        if(yn2 == "y"):
            print("type new date")
            date = input()
            self.allTasks.list_of_all_tasks_objects[index_to_use][2] = date
            self.allTasks.update_data_frame()
        else:
            pass
        print("do you want to change the desired_time_spent press y/n, also it will change the main timer")
        yn3 = input()
        
        if(yn3 == "y"):
            print("type new desired_time_spent")
            desired_time_spent = int(input())
            self.allTasks.list_of_all_tasks_objects[index_to_use][3] = desired_time_spent
            self.allTasks.update_data_frame()
            self.change_timer(desired_time_spent)
        else:
            self.change_timer(self.allTasks.list_of_all_tasks_objects[index_to_use][3])
            pass
        print("do you want to change the score press y/n")
        yn4 = input()
        
        if(yn4 == "y"):
            print("type new score")
            score = int(input())
            self.allTasks.list_of_all_tasks_objects[index_to_use][4] = score
            self.allTasks.update_data_frame()
        else:
            pass
        print("do you want to change the learnt press y/n")
        yn5 = input()
        
        if(yn5 == "y"):
            print("type new learnt")
            learnt = input()
            self.allTasks.list_of_all_tasks_objects[index_to_use][5][0] = learnt
            self.allTasks.update_data_frame()
        else:
            pass
        print("do you want to change the dont_understand press y/n")
        yn6 = input()
        
        if(yn6 == "y"):
            print("type new dont_understand")
            dont_understand = input()
            self.allTasks.list_of_all_tasks_objects[index_to_use][5][1] = dont_understand
            self.allTasks.update_data_frame()
        else:
            pass
        print("do you want to change the next_step press y/n")
        yn7 = input()
        
        if(yn7 == "y"):
            print("type new next_step")
            next_step = input()
            self.allTasks.list_of_all_tasks_objects[index_to_use][5][2] = next_step
            self.allTasks.update_data_frame()
        else:
            pass
        

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
        
    def delete_column(self):
        self.allTasks.delete_column()
        
   #q
   #def add_column


        


