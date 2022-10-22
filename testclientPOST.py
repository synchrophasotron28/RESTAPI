from app import app, client

#----------------------------------
# Проверка post
res = client.post('/orders', json = {'title':'video1', 'desc':'trev'})

print(res.status_code)
#200 - успех

