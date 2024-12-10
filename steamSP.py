import requests
import json
import time
import urllib.parse

BASE_URL = "https://store.steampowered.com/appreviews/"


def fetch_reviews(appid, language="all", filter="all", day_range=30, review_type="all", purchase_type="steam",
                  num_per_page=20, max_reviews=100):
    reviews = []
    cursor = "*"  # 初始游标
    while cursor and len(reviews) < max_reviews:
        url = f"{BASE_URL}{appid}?json=1&language={language}&filter={filter}&day_range={day_range}&review_type={review_type}&purchase_type={purchase_type}&num_per_page={num_per_page}&cursor={urllib.parse.quote(cursor)}"

        response = requests.get(url)
        if response.status_code != 200:
            break

        data = response.json()

        if data.get('success') == 1:
            # 解析评测数据
            reviews.extend(data.get('reviews', []))
            # 重置游标
            cursor = data.get('cursor', None)
            print(f" {len(data.get('reviews', []))} 条。")
        else:
            break

        if len(reviews) >= max_reviews:
            break

        time.sleep(1)

    return reviews[:max_reviews]


def clean_review_data(reviews):
    return reviews.copy()


def save_reviews_to_file(reviews, filename="reviews_cleaned.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=4)
    print(f"成功保存 {len(reviews)}")


if __name__ == "__main__":
# todo
# 修改appid定位到不同游戏

# 参数上
# language过滤不同语言 schinese简体中文 all所有语言 其他语言参见https://partner.steamgames.com/doc/store/localization/languages?l=schinese
# day_range 从现在至 N 天前 仅适用于“all”filter。 最大值为 365。
# filter:
# recent – 以创建时间排序
# updated – 以最后更新时间排序
# all – steam默认排序
# review_type
# positive – 仅限正面评测
# negative – 仅限负面评测
# purchase_type
# non_steam_purchase – 在 Steam 上未付费获得产品的用户撰写的评测
# steam – 在 Steam 上付费获得产品的用户撰写的评测（默认设置）
# all 默认
#filter_offtopic_activity 是否返回无价值评价 传入0即返回

    appid = "570"
    reviews = fetch_reviews(appid, language="schinese", filter="recent", day_range=30, review_type="all",
                            purchase_type="steam", num_per_page=20, max_reviews=100)
    reviews = clean_review_data(reviews)
    save_reviews_to_file(reviews)
