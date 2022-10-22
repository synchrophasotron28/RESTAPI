from app import app, client

#----------------------------------
# Проверка put
res = client.put('/tutorials/2', json = {'result': 'my_result_new'})
print(res.status_code)

#посмотреть результат res.get_json()