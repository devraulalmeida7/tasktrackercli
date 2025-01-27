import argparse
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

# Function to load the files from JSON
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    return []

# Function to save tasks on JSON
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# func to add a task
def add_task(name,description):
    tasks = load_tasks()
    today: str = datetime.today().isoformat()
    tasks.append({
        "id": len(tasks) + 1,
        "name": name,
        "description": description,
        "status":'to-do',
        "createdAt": today,
        "updateAt": today
    })
    save_tasks(tasks)
    print(f"Tarefa adicionada: {name} ")

#  func to list tasks
def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("Nenhuma tarefa encontrada.")
    else:
        print("Tarefas:")
        for task in tasks:
            print(f"[{task['id']}] Name:{task['name']} Description:{task['description']} Status:{task['status']}")
# func to list tasks by status
def list_tasks_status(status):
    tasks = load_tasks()
    if not tasks:
        print("No task found!")
    else:
        for task in tasks:
            if(status == task['status']):
                print(f"[{task['id']}], {task['name']} {task['description']} {task['status']}")
                break



    
# func to remove a task
def remove_task(task_id):
    tasks = load_tasks()
    updated_tasks = [task for task in tasks if task["id"] != task_id]
    if len(updated_tasks) == len(tasks):
        print(f"Nenhuma tarefa encontrada com o ID: {task_id}")
    else:
        save_tasks(updated_tasks)
        print(f"Tarefa {task_id} removida com sucesso.")

# func to update a task using ID
def update_task(taskId, taskName, taskDescription, taskStatus):
    today: str = datetime.today().isoformat()
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == taskId:
            if taskDescription is not None and taskName is not None and taskStatus is not None:
                task['name'] = taskName
                task['description'] = taskDescription
                task['status'] = taskStatus
                task['updateAt'] = today
            

    save_tasks(tasks)
 
# Configuration argparse
def main():
    parser = argparse.ArgumentParser(description="Gerenciador de Tarefas")
    subparsers = parser.add_subparsers(dest="command", help="Commands available:")

    # command to add a task
    add_parser = subparsers.add_parser("add", help="Adiciona uma nova tarefa")
    add_parser.add_argument("name", help="Add the name of the task")
    add_parser.add_argument("description", type=str, help="Descrição da tarefa")

    #Command to update a task
    update_parser = subparsers.add_parser("update", help="Atualiza uma tarefa")
    update_parser.add_argument("id", type=int, help="Id a ser atualizada")
    update_parser.add_argument("name", help="Add the name of the task")
    update_parser.add_argument("description", type=str, help="Descrição a ser atualizada")
    update_parser.add_argument("status", type=str, help="Status of the task")
    

    # Command to list the tasks
    subparsers.add_parser("list", help="Lista todas as tarefas")
    list_parser = subparsers.add_parser("list-status", help="List tasks using status")
    list_parser.add_argument("status", type=str, help="Use status of task to filter it")

    # Command to remove a task
    remove_parser = subparsers.add_parser("remove", help="Remove uma tarefa pelo ID")
    remove_parser.add_argument("id", type=int, help="ID da tarefa a ser removida")

    # Command to export tasks
    export_parser = subparsers.add_parser("export", help="Exporta as tarefas para um arquivo JSON")
    export_parser.add_argument("filename", type=str, help="Nome do arquivo JSON para exportação")

    args = parser.parse_args()

    # Execute the commands
    if args.command == "add":
        add_task(args.name,args.description)
    elif args.command == "list":
        list_tasks()
    elif args.command == "list-status":
        list_tasks_status(args.status)
    elif args.command == "update":
        update_task(args.id, args.name, args.description, args.status)
    elif args.command == "remove":
        remove_task(args.id)
    elif args.command == "export":
        tasks = load_tasks()
        with open(args.filename, "w") as file:
            json.dump(tasks, file, indent=4)
        print(f"Tarefas exportadas para {args.filename}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
