from flask import Flask, render_template, request, redirect, url_for
import requests
import json
from pycoingecko import CoinGeckoAPI

app = Flask(__name__)

cg = CoinGeckoAPI()


def get_data():
    reqdata = cg.get_coins_markets(vs_currency='usd',
                                   order='market_cap_desc',
                                   per_page='100',
                                   price_change_percentage='1h,24h,7d')
    with open('Dataset/liveData.json', 'w') as f:
        json.dump(reqdata, f)
    print("data retrieved")


# --SCHEDULE API REQUEST--
# sch = scheduler()
# sch.add_job(get_data, 'interval', minutes=15, replace_existing=True)
# sch.start()

# with open('Dataset/trending.json') as json_file:
# trending = json.load(json_file)

# ************************************


@app.route('/')
def main():
    #get_data()
    with open('Dataset/liveData.json') as json_file:
        data = json.load(json_file)
    # Getting Coin ID FROM IMAGE SOURCE
    for i in range(0, 100):
        img_src = data[i]['image']

        idx1 = img_src.find('images')
        idx_st = idx1 + 7
        idx2 = img_src.find('/large')
        coin_id = img_src[idx_st:idx2]
        data[i]['cid'] = coin_id
    return render_template('index.html', data=data)


@app.route('/crypto/<int:rank>/<string:name>', methods=['GET'])
def crypto(rank, name):
    with open('Dataset/liveData.json') as json_file:
        data = json.load(json_file)
        index = rank - 1
        dic = data[index]
        ticker = dic["symbol"] + 'usd'

    return render_template('crypto.html', ticker=ticker, dic=dic)


@app.route('/news')
def news():
    with open('Dataset/news.json') as json_file:
        data = json.load(json_file)

    for i in range(len(data)):
        data[i]["ID"] = "news" + str(data[i]["index"])

    return render_template('news.html', news=data)


@app.route('/services', methods=['GET'])
def services():
    return render_template('services.html')


@app.route('/contacts', methods=['GET'])
def contacts():
    return render_template('contacts.html')


if __name__ == '__main__':
    app.run(debug=True)
