class TaskExecutor:
    def __init__(self):
        pass

    def execute_task(self):
        task_name = input("Please enter the name of the task you want to execute: ")
        parameters = input("Please enter the parameters for the task (comma-separated): ")
        parameters_list = [param.strip() for param in parameters.split(",")]

        # Placeholder for task execution logic
        print(f"Executing task '{task_name}' with parameters: {parameters_list}")
        # Here you would add the logic to execute the task based on task_name and parameters_list.