# Lang-chainとllama-indexを使って独自データを使ったWebチャットアプリケーションを作成します。

## 必要なもの
Python 3.10  
OpenAIのAPIキー  

## 環境構築
python 3.10環境で必要なモジュールをインストール  
コマンドプロンプト またはターミナルでこのフォルダへ移動し、

''' python -m pip install -r requirements.txt '''

## OpenAIキーを入力

secret_keys.pyにOpenAIキーを入力

## インデックスの作成

Dataフォルダに独自データ（テキストデータ)を配置
コマンドプロンプト またはターミナルでcreate_index.pyを実行

''' python create_index.py '''

## streamlitを実行して、Webアプリケーションの実行

コマンドプロンプト またはターミナルで

''' python -m streamlit run app.py '''
