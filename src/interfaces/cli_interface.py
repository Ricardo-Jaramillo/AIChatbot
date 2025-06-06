from interfaces.base_interface import BaseInterface

class CLIInterface(BaseInterface):
    def display(self, message):
        print(message)

    def get_user_input(self, prompt):
        return input(prompt)

    def execute_task(self):
        task_name = self.get_user_input("Enter the task name: ")
        parameters = self.get_user_input("Enter the parameters for the task (comma-separated): ")
        # Placeholder for task execution logic
        print(f"Executing task '{task_name}' with parameters: {parameters}")