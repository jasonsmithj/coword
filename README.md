# Co-Word

## 概要
共起語検索のためのデータ収集ツール

## 技術
Python 3.6.1
Flask
mecab(ipadic-neologd)
ES 5.5.2
Google Custom Search API

## 開発環境構築

[初回]
```
$ docker-compose build
$ docker-compose up -d
```

[停止]
```
$ docker-compose stop
```

[2回目以降起動]
```
$ docker-compose start
```

## 開発環境起動方法
こちらを参考にログインすると楽です。
http://qiita.com/Jason/items/b64e12b42c25dc2301a0

1. hosts登録(Mac)
```
$ sudo vi /etc/hosts
127.0.0.1 dev-coword.example.com
```

2. Docker ログイン
```
$ docker-login coword coword
```

3. dotenv設定
```
$ cd /var/www/coword
$ cp -pi .env.sample .env
$ vi .env
設定
```

4. pip install
```
$ cd /var/www
$ python3 -m venv coword
$ cd /var/www/coword
$ pip -r requirements.txt 
```


3. 起動(Docker)
```
$ cd /var/www/coword
$ FLASK_ENV python run.py
```

## 開発環境確認方法

1. coword
http://dev-coword.example.com

2. ElasticSearch
http://dev-coword.example.com:8080
