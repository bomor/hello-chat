from flask import Flask, request, jsonify
import json, elasticsearch, redis
app = Flask(__name__)
redis_connection = redis.Redis()
redis_connection.sadd('channels', "Food", "Love", "Moshe")
elastic_connection = elasticsearch.Elasticsearch()
MESSAGES_INDEX = "messages"
#if !(elastic_connection.indices.exists(index=)

@app.route('/join_to_channel/<nickname>/<channel>')
def join_to_channel(nickname, channel):
    redis_connection.pubsub().subscribe(channel)
    return redis_connection.sadd('%s-channels' % nickname, channel)


@app.route('/add_channel/<new_channel>')
def add_channel(new_channel):
    return str(redis_connection.sadd('channels', new_channel))


@app.route('/list_user_channels/<nickname>')
def list_user_channels(nickname):
    return jsonify(list(redis_connection.smembers('%s-channels' % nickname)))


@app.route('/who_i_am')
def who_i_am():
    return jsonify({"name": "Mor"})


@app.route('/clear_redis')
def clear_redis():
    redis_connection.flushdb()
    return jsonify({"status": "ok"})


@app.route('/send_message/<channel>', methods=['POST'])
def send_message(channel):
    request_values = dict(request.form)
    print request.form
    print ""
    print request_values
    request_values["channel"] = channel
    print redis_connection.rpush(channel, json.dumps(request_values))
    elastic_connection.index(index=MESSAGES_INDEX, doc_type="private", body=json.dumps(request_values))
    return "OK"
    #return redis_connection.publish(channel, "%s @ %s" % (nickname, message))


@app.route('/search_messages/<search_word>')
def search_messages(search_word):
    elastic_response = elastic_connection.search(index=MESSAGES_INDEX, body={
    "query" : {
        "constant_score" : {
            "filter" : {
                "term" : {
                    "message" : search_word
                        }
                    }
                }
            }
        }
    )
    return_response = {"items" : []}
    for ans in elastic_response["hits"]["hits"]:
        return_response["items"].append({"name":ans["_source"]["message"], "description" : "from: {0} in channel: {1}".format(ans["_source"]["nickname"], ans["_source"]["channel"])})
    return jsonify(return_response)


@app.route('/messages_in_channel/<channel>')
def messages_in_channel(channel):
    return jsonify(map(json.loads, redis_connection.lrange(channel, 0, 1000)))


@app.route('/list_channels')
def list_channels():
    return jsonify(list(redis_connection.smembers('channels')))


if __name__ == '__main__':
    app.run(debug=True, threaded=True, host="0.0.0.0")
