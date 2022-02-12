from flask import request, json

from app import app

with app.test_client() as c:
    # положительный тест
    rv = c.get('/category/2')
    data = json.loads(rv.data)
    status = rv.status_code
    print('Результаты проведения положительного теста:\n', data, '\nСтатус ответа:', status)
    assert status == 200

    # негативный тест
    rv = c.get('/category/255')
    data = json.loads(rv.data)
    status = rv.status_code
    print('Результаты проведения негативного теста:\n', data, '\nСтатус ответа:', status)
    assert status == 404, 'При запросе к не существующему id категории, должен выдаваться статус 404'



