
from flask import Flask, jsonify, request
import json
# from db import connect_db_pg 
import db 
app = Flask(__name__)

#клиент (для теста)
client = app.test_client()

# http://127.0.0.1:5000/orders
# [[1,"order1","Fri, 31 Dec 1999 21:00:00 GMT"]]
'''

1) Создать задачу {order_name: "изготовить изделие", start_date: "01-01-2022"}, изменить, удалить

2) К задаче добавить работу {task: "задача 1", duration: 2, resource: 10}, удалить работу

3) К работе добавить массив предшествующих работ {pred: [1, 2, 3]}

'''

orders = [
    {
        "order_name": 'order1',
        'start_date': '01-01-2022'
    },
    {
        "order_name": 'order2',
        'start_date': '02-01-2022'
    }

]
tasks = [
    {
        'task_id': 1,
        'order_name': "order1",
        'task':'задача 1',
        'duration': 2,
        'resource': 10,
        'pred': []
    },
    {
        'task_id': 2,
        'order_name': "order1",
        'task':'задача 2',
        'duration': 5,
        'resource': 8,
        'pred': [1]
    },
    {
        'task_id': 3,
        'order_name': "order2",
        'task':'задача 3',
        'duration': 3,
        'resource': 15,
        'pred': []
    },
    # [[1,"order1","Fri, 31 Dec 1999 21:00:00 GMT"]]

]

#route обрабатывает запросы клиента к серверу
#сначала обработчик гет запросов
@app.route('/orders', methods=['GET'])
def get_list():
    db.cur.execute('''SELECT * FROM orders;''')
    arr_db = db.cur.fetchall()
    result_list=[]
    for curr_str in arr_db:
        result_list.append(
            {
                "order_id"  :curr_str[0],
                'order_name':curr_str[1],
                'start_date':curr_str[2],
            }
            )
    return jsonify(result_list)

#список туториалов обновляется на сервере
#в него будет добавляться новый элемент
#по request получаем, когда отправляем от клиента к серверу

@app.route('/orders', methods=['POST'])
def post_list():
    data = json.loads(request.data)
    print(data)
    db.cur.execute(f"insert into orders (order_name, start_date) values \
    (\'{data['order_name']}\', \'{data['start_date']}\')")
    # db.con.commit()
    #получим данные с сервера
    # new_one = request.json
    # orders.append(new_one)
    # return jsonify(orders)
    return "done"

#добавить элементы в список
#нужен id
@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_list(order_id):
    #получим тело запроса
    params = request.json
    #генератор возвращает соответствующее id или none, если соответствие не найдено
    item = next((i for i in orders if i['id'] == order_id), None)
    if not item:
        return{'message': 'No tutorials with this id'}, 400
    item.update(params)
    #возвращаем изм список
    return item

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_list(order_id):

    idx, _ = next((i for i in enumerate(orders) if i[1]['id'] == order_id), (None, None))

    orders.pop(idx)
    return '', 204


#route обрабатывает запросы клиента к серверу
#сначала обработчик гет запросов
@app.route('/tasks', methods=['GET'])
def get_list_tasks():
    return jsonify(tasks)# бд сюда
#список туториалов обновляется на сервере
#в него будет добавляться новый элемент
#по request получаем, когда отправляем от клиента к серверу

@app.route('/tasks', methods=['POST'])
def post_list_tasks():
    #получим данные с сервера
    new_one = request.json
    tasks.append(new_one)
    return jsonify(tasks)

#добавить элементы в список
#нужен id
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_list_tasks(task_id):
    #получим тело запроса
    params = request.json
    #генератор возвращает соответствующее id или none, если соответствие не найдено
    item = next((i for i in orders if i['id'] == task_id), None)
    if not item:
        return{'message': 'No tutorials with this id'}, 400
    item.update(params)
    #возвращаем изм список
    return item

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_list_tasks(task_id):

    idx, _ = next((i for i in enumerate(orders) if i[1]['id'] == task_id), (None, None))
    tasks.pop(idx)
    return '', 204


if __name__ == '__main__':# this is main!
    # connect_db_pg()
    # db.connect_db_pg()
    with db.connect_db_pg() as connection: #это вообще работает?
        app.run()
