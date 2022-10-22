from app import app, client

#----------------------------------
# Проверка delete
res = client.delete('/tutorials/1')
print(res.status_code)