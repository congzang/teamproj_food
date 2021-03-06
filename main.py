import logging
import os
import time
import tensorflow as tf
from keras.models import load_model
from keras.backend import set_session
from PIL import Image

from flask import Flask, render_template, request, send_from_directory
import json

from predict import Food_classification
from recipe import Recipe

app = Flask(__name__)

# 업로드 허용된 확장자
ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png"]

# 업로드 경로(폴더)
UPLOAD_PATH = "static/upload/"


# main
@app.route("/")
def main():
    return render_template("run.html")

# 파일 확장자 체크
def check_file_ext(ext):
    return ext in ALLOWED_EXTENSIONS

# 썸네일 이미지 생성
def create_thumbnail_image(filename):
    thumbnail_path = UPLOAD_PATH + "thumb_" + filename  # 썸네일 이미지 저장 경로 + 파일명

    try:
        # 원본 이미지에서 썸네일 이미지를 생성
        img = Image.open(UPLOAD_PATH + filename)  # 원본 이미지 열기
        img = img.convert("RGB")
        img.thumbnail((500, 500), Image.ANTIALIAS)

        # 썸네일 이미지 저장
        img.save(thumbnail_path)

    except Exception as e:
        logging.error("썸네일 생성 Error : " + str(e))
        raise e

    return "thumb_" + filename


# 썸네일 다운로드
@app.route("/thumbnail/<filename>")
def download_thumbnail(filename):
    print("download_thumbnail : " + filename)
    return send_from_directory(UPLOAD_PATH, filename, as_attachment=True, mimetype="image/jpeg")


# 파일 업로드
@app.route("/fileUpload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        img_file = request.files["img_file"]
        user_lang = request.form["user_lang"]

        o_file_ext = os.path.splitext(img_file.filename)[1].lower()  # 원본파일 확장자
        thumbnail_filename = ""

        # 파일 존재여부와 파일 확장자 체크
        if img_file and check_file_ext(o_file_ext):
            timestamp_str = time.strftime("%Y%m%d-%H%M%S")  # 파일명 생성을 위한 timestamp
            save_file_name = timestamp_str + o_file_ext
            save_path = UPLOAD_PATH + save_file_name  # 저장할 경로

            # 파일 저장
            img_file.save(save_path)

            # 화면에 출력하기 위한 thumbnail 생성
            thumbnail_filename = create_thumbnail_image(save_file_name)

        return render_template("run.html", thumb_img_name=thumbnail_filename, user_lang=user_lang)

# 음식 예측하기
@app.route("/predict", methods=["GET", "POST"])
def predict():
    filename = request.form["in_filename"].replace("thumb_", "")
    trans_lang = request.form["sel_user_lang"]

    food_name, probability = Food_classification(model, sess, graph, filename).get_predicted()

    recipe_txt =  Recipe(food_name, trans_lang).get_recipe()

    result = {"food_name" : food_name,
              "probability" : probability,
              "recipe_step_list" : recipe_txt}

    return json.dumps(result, ensure_ascii=False)

# 조리법 가져오기
def get_recipe(food_name):
    return Recipe(food_name).get_recipe()

# 실행
if __name__ == "__main__":
    global model
    print("******* 모델이 로딩된 후에 서비스를 시작합니다. *******")

    global graph
    global sess
    sess = tf.Session()
    set_session(sess)
    graph = tf.get_default_graph()
    model = load_model("./model/food_classification.model")

    app.run(host="0.0.0.0", port="5555")  # http://127.0.0.1:5555