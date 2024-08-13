from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

tasks = []
task_id_control = 1

#CREATE
@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control, title=data['title'], description=data.get('description', ""))
    task_id_control += 1
    tasks.append(new_task)
    print(tasks)
    return jsonify({"message": "Nova tarefa criada com sucesso!", "id":new_task.id})
#READ
@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]
    # for task in tasks:
    #     task_list.append(task.to_dict())
    output = {
                "tasks": task_list,
                "total_tasks": len(task_list)
             }
    return jsonify(output)
#READ BY ID
@app.route('/tasks/<int:id>', methods=['GET'])
def get_by_id(id):
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
        break
    return jsonify({"messege":"Não foi possível encontrar a atividade"}), 404
#UPDATE            
@app.route('/tasks/<int:id>', methods=['PUT'])
def update(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break
    if task == None:
        return jsonify({"messege":"Não foi possível encontrar a atividade"}), 404
    
    data = request.get_json()
    task.title = data['title']
    task.description = data['description']
    task.completed = data['completed']
    return jsonify({"message:": "Tarefa atualizada com sucesso!"}), 200
#DELETE
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break
    if not task:
        return jsonify({"message": "Não foi possível encontrar a atividade"}), 404

    tasks.remove(task)
    return jsonify({"message": "Tarefa deletada com sucesso!"})

if __name__ == "__main__":
    app.run(debug=True)

