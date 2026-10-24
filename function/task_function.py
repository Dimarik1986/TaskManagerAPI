

def response_task(task):
    task_response = {
        "id": task[0],
        "title": task[1],
        "done": task[2]
    }
    return task_response

def response_tasks(tasks):
    return [response_task(task) for task in tasks]