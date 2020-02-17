from PIL import Image
import numpy as np
from keras.models import load_model

# 업로드 경로(폴더)
UPLOAD_PATH = "static/upload/"
#caltech_dir = "D:/final_test"

class Food_classification:

    # 초기화
    def __init__(self, filename):
        self.filename = filename

    # 모델을 통해 사진 속의 음식 예측 후 분류
    def predict_food(self):
        # image_w = 128
        # image_h = 128
        #
        # image_path = UPLOAD_PATH + self.filename
        # print("predict() -> image_path :  " + image_path)
        # img = Image.open(image_path)
        # img = img.convert("RGB")
        # img = img.resize((image_w, image_h))
        # img_to_array = np.asarray(img)
        #
        # model = load_model("./model/food_classification.model")
        #
        # prediction = model.predict(img_to_array)
        # print(len(prediction))

        # TODO : prediction에서 레이블명, 확률 뽑아내깅...ㅠㅠ

        self.predicted_food_name = "김치찌개"
        self.predicted_probabilty = "99.8"

    # 예측된 음식명, 확률 가져오기
    def get_predicted(self):
        return self.predicted_food_name, self.predicted_probabilty



# image_w = 128
# image_h = 128
#
# img = Image.open(f)
# img = img.convert("RGB")
# img = img.resize((image_w, image_h))
# data = np.asarray(img)
# filenames.append(f)
# X.append(data)
#
# X = []
# filenames = []
# files = glob.glob(caltech_dir+"/*.*")
#
# for i, f in enumerate(files):
#     print(f)
#     img = Image.open(f)
#     img = img.convert("RGB")
#     img = img.resize((image_w, image_h))
#     data = np.asarray(img)
#     filenames.append(f)
#     X.append(data)
#
# X = np.array(X)
# model = load_model('./model/food_classification.model')
#
# prediction = model.predict(X)
# np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
# cnt = 0
#
# for i in prediction:
#     pre_ans = i.argmax()  # 예측 레이블
#     print(i)
#     print(pre_ans)
#     #pre_ans_str = categories[pre_ans]
#     pre_ans_str = pre_ans
#     print("해당 "+"이미지는 "+pre_ans_str+"로 추정됩니다.")