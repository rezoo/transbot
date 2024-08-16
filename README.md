# Transbot

Transbotは、選択した文章を素早く翻訳するためのシンプルなPythonプログラムです。日本語から英語、または英語から日本語への翻訳をサポートしています。

## 概要

Transbotは、バックグラウンドで動作し、選択した文章を瞬時に翻訳します。以下の機能を備えています。

- **簡単操作**: 文章を選択して、Command-Cを2回連続で押すだけで翻訳が完了します。
- **自動判別**: 選択された文章が日本語であれば英語に翻訳し、英語であれば日本語に翻訳します。
- **リアルタイム翻訳**: 翻訳作業を中断することなく、シームレスに作業を続けられます。

## インストール方法

1. リポジトリをクローンします。
    ```bash
    $ git clone https://github.com/rezoo/transbot.git
    ```
2. プロジェクトディレクトリに移動し、パッケージをインストールします。

    ```bash
    cd transbot
    pip install -e .
    ```
3. `OPENAI_API_KEY` の環境変数に、OpenAIから発行されたAPIキーを設定します。
4. `transbot` で起動します。Transbotを停止するには、Ctrl-Cを押します。

## 注意事項

Macの設定: Macで使用する場合、プライバシーとセキュリティ設定で入力監視の許可が必要です。以下の手順で設定を行ってください。

* システム環境設定を開き、「セキュリティとプライバシー」メニューに移動します。
* 「プライバシー」タブを選択し、左側のリストから「入力監視」を選びます。
* 「＋」ボタンをクリックし、Transbotを実行するターミナルアプリケーションを追加します。

# ライセンス

このプロジェクトはMITライセンスのもとで公開されています。
