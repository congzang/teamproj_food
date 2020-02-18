from PIL import Image
import numpy as np

# 업로드 경로(폴더)
UPLOAD_PATH = "static/upload/"

class Food_classification:

    # 초기화
    def __init__(self, model, sess, graph, filename):
        self.model = model
        self.graph = graph
        self.sess = sess
        self.filename = filename

    # 모델을 통해 사진 속의 음식 예측 후 분류
    def predict_food(self):
        model = self.model
        image_w = 128
        image_h = 128
        X = []
        categories = ['갈치구이',
                      '계란찜',
                      '고사리나물',
                      '메추리알장조림',
                      '소세지볶음',
                      '애호박볶음',
                      '연근조림',
                      '오징어채볶음',
                      '제육볶음',
                      '콩자반']

        image_path = UPLOAD_PATH + self.filename

        img = Image.open(image_path)
        img = img.convert("RGB")
        img = img.resize((image_w, image_h))
        img_to_array = np.asarray(img)
        X.append(img_to_array)
        X = np.array(X)

        print(model.summary())

        with self.sess.as_default():
            with self.graph.as_default():
                predict_result = model.predict(X)[0]
                pred_max_idx = predict_result.argmax()

                self.predicted_food_name = categories[pred_max_idx]
                self.predicted_probabilty = str(round(predict_result[pred_max_idx] * 100, 3))

    # 예측된 음식명, 확률 가져오기
    def get_predicted(self):
        self.predict_food()
        return self.predicted_food_name, self.predicted_probabilty