# Twitter アイコンを一括ダウンロードするやつ
Connpass などでイベントを企画したとき、Twitter アイコンを保存したくなる時があると思います。
しかし、API の廃止により困難になってしまったので、それを補助するスクリプトです。

[dat.tsv](dat.tsv) にダウンロードしたい Twitter ID を書いて、`python3 download_twitter_icon.py` をすると、`out` ディレクトリに twitter アイコンがダウンロードされます。

![image](https://github.com/user-attachments/assets/552083b0-3bec-4ba7-b6f7-fff989fa59ee)

## 環境
- Ubuntu 24.04 (WSL2)
- Python 3.12.3
- playwright==1.50.0
- pillow==11.1.0
で動作確認しています。

リポジトリを clone したあと、
```
pip3 install playwright pillow
playwright install
```
を行ってください。

## 仕組み
`https://x.com/{normalized_id}/photo` が、認証なしで画像にアクセスできるページなので、そこにスクレイピングでアクセスしています。
Twitter の仕様変更により変わるかもしれません。

## 免責注意事項
Twitter のみの対応です。X には対応していません。

良ければスターをしてくれると、開発の励みになります。
