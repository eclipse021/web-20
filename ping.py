from flask import Flask, request, jsonify

app = Flask(__name__)
app.users = {}
app.id_count = 1
app.tweets = []
app.follow = []

@app.route("/follow",methods=['POST'])
def follow():
    requesting = request.json
    me_id = int(requesting['id'])
    friend_id = int(requesting['follow'])
    app.follow.append({me_id:friend_id})
    return '', 200
    
def unfollow():
    requesting = request.json
    me_id = int(requesting['id'])
    friend_id = int(requesting['unfollow'])
    app.follow.remove({me_id : friend_id})
    return '', 200

@app.route("/ping",methods=['GET'])
def ping():
    return "pong"

@app.route("/sign-up", methods=['POST'])
def sign_up():
    new_user = request.json
    new_user["id"] = app.id_count
    app.users[app.id_count] = new_user
    app.id_count = app.id_count + 1

    return jsonify(new_user)

@app.route('/tweet',methods=['POST'])
def tweet():
    writing = request.json
    user_id = int(writing['id'])
    document = writing['tweet']

    if user_id not in app.users:
        return '사용자가 존재 하지 않습니다.' , 400

    elif len(document) > 300:
        return '글자 수를 초과했습니다.', 400

    else:
        app.tweets.append({'user_id':user_id, 'tweet':document})
        return '', 200
