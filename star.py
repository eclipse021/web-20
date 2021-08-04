from flask import Flask, jsonify, request
from flask.globals import current_app
from sqlalchemy import create_engine, text

def create_app(test_config = None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database = create_engine(app.config['DB_URL'], encoding = 'utf-8', max_overflow = 0)
    app.database = database


    @app.route("/rating", methods=['POST'])
    def rating():
        new_star = request.json
        if not new_star['point'] >= 1 and new_star['point'] <= 5:
            return '잘못 입력하셨습니다.', 401
        else:
            current_app.database.execute(text("""
                    INSERT INTO star(
                        point
                    ) VALUES(
                        :point
                    )
                """), new_star)
        
            return '', 200

    @app.route("/showrating", methods=['POST'])
    def showrating():
        row1 = app.database.execute(text("""
            SELECT SUM(
                point)
            FROM star
        """))

        row2 = app.database.execute(text("""
            SELECT COUNT(
                id)
            FROM star
        """))

        star = row1/row2
        Total_star = {
            'star' : star
        }
        return Total_star
    
    @app.route("/modifyrating", methods=['POST'])
    def modifyrating():
        new_star = request.json
        current_app.database.execute(text("""
           UPDATE star SET point = :point WHERE id = :id

        """),new_star)        
        return '' , 200
       
