from flask import Flask, request, jsonify   
app = Flask(__name__)
app.rating = 0 #평균 점수를 의미함
app.rating_count = 0 #별점에 참여하는 사람 수를 의미함

@app.route("/rating",methods=['POST'])
def CalcuateRating():
    app.rating_count += 1
    d_rating = request.json
    app.rating = int(d_rating['rate']) + app.rating
    result_rating = app.rating/app.rating_count
    return '', 200