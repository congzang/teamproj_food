import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import quote
import re

class Recipe:

    # 초기화
    def __init__(self, food_name):
        self.food_name = food_name
        self.recipe_step = []

    # 만개의 레시피에서 조리법 크롤링
    def crawling_recipe(self):
        keyword = quote(self.food_name)

        site_url = "http://www.10000recipe.com"

        # 1. 사이트에서 음식 검색
        search_url = site_url + "/recipe/list.html?q={keyword}&order=reco&page=1".format(**{"keyword": keyword})

        res = urllib.request.urlopen(search_url).read().decode("utf-8")
        bsp = BeautifulSoup(res, "lxml")

        # 2. 검색된 목록에서 제일 첫번째 조리법 선택(추천순으로 되어있음)
        first_food_detail_element = bsp.find("a", {"class": "thumbnail"})

        save_step = ""

        if first_food_detail_element != None and len(first_food_detail_element) > 0:
            first_food_url = site_url + first_food_detail_element["href"]  # 검색한 음식의 첫번째 조리법(추천순)

            res = urllib.request.urlopen(first_food_url).read().decode("utf-8")
            bsp = BeautifulSoup(res, "lxml")

            # 조리법 글자만 추출
            step_list = bsp.find_all("div", {"id": re.compile("^stepdescr")})

            for step in step_list:
                self.recipe_step.append(step.text)

    # 조리법 얻어오기
    def get_recipe(self):
        self.crawling_recipe()
        return self.recipe_step

# 만개의 레시피에서 조리법 크롤링
# def get_recipe_site1(keyword):
#     keyword = quote(keyword)  # 한글 사용
#
#     site_url = "http://www.10000recipe.com"
#
#     # 1. 사이트에서 음식 검색
#     search_url = site_url + "/recipe/list.html?q={keyword}&order=reco&page=1".format(**{"keyword": keyword})
#
#     res = urllib.request.urlopen(search_url).read().decode("utf-8")
#     bsp = BeautifulSoup(res, "lxml")
#
#     # 2. 검색된 목록에서 제일 첫번째 조리법 선택(추천순으로 되어있음)
#     first_food_detail_element = bsp.find("a", {"class": "thumbnail"})
#
#     save_step = ""
#
#     if first_food_detail_element != None and len(first_food_detail_element) > 0:
#         first_food_url = site_url + first_food_detail_element["href"]  # 검색한 음식의 첫번째 조리법(추천순)
#
#         res = urllib.request.urlopen(first_food_url).read().decode("utf-8")
#         bsp = BeautifulSoup(res, "lxml")
#
#         # 조리법 글자만 추출
#         step_list = bsp.find_all("div", {"id": re.compile("^stepdescr")})
#
#         for step in step_list:
#             save_step += step.text + "@"
#
#     return save_step

# 실행
# food_categories는 실제 데이터로 변경할 것
#food_categories = ["제육볶음", "ㅁㄴㅇㄴ"]  # 분류가능한 음식
#food_recipe = {}

# 분류되어있는 음식별로 조리법 크롤링
#for food_name in food_categories:
    #    recipe_text = get_recipe_site1(food_name)  # 음식명
#    food_recipe[food_name] = recipe_text  # 조리법 text

# 음식명, 조리법 데이터 저장
#food_recipe_to_list = {"recipe_name": list(food_recipe.keys()), "recipe_text": list(food_recipe.values())}
#df = pd.DataFrame(food_recipe_to_list)


