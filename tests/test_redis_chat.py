from chat import app, redis_connection
import json
def test_wipe_redis():
    redis_connection.flushdb()


def test_add_channel():
    client = app.test_client()
    client.get('/add_channel/new_channel')
    response = client.get('/list_channels')
    assert json.loads(response.data)[0] == "new_channel"
