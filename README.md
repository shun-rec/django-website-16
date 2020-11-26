# マイグレーションをマスターしよう（後編） - djangoチュートリアル #16

普段何気なく使っているマイグレーションについてもう少し深く理解しましょう。

エラーが発生した時に柔軟に対応できるようになりましょう。

## 事前準備（前回までの状態の復元）

### サーバー起動

Paizaサーバーは、djangoとMySQLにチェックを入れて起動して下さい。

MySQLのチェックを忘れた人はphpMyAdminを起動するのと同じメニューからMySQL → Start を押すと起動できます。

### phpMyAdmin起動

メニューに「phpMyAdmin」という項目があるので、「Start」 を押して、終わったら次 「Open」を押します。

### プロジェクトのDLとフォルダ移動

```sh
git clone https://github.com/shun-rec/django-website-15.git
cd django-website-15
```

### 共通ライブラリのインストール

MySQLに接続する際に共通で必要になるライブラリを２つインストールします。  

```sh
pip install dj-database-url
pip install python-dotenv
pip install mysqlclient
```

### 環境設定ファイルを設置

プロジェクト直下に`.env`というファイル名でファイルを作り、以下の内容を入力。
  
※ドットから始まるファイル名は隠しファイルと言って、デフォルトでは非表示です。Paizaではプロジェクトフォルダで右クリックをすると、「隠しファイルを表示」することが出来ます。

`mysql`の`pj_migrate`というデータベースに`root`ユーザーでパスワード無しでアクセスするという意味。

パスワード有りの場合は`root:password`と書きます。

```
DATABASE_URL=mysql://root:@localhost/pj_migrate
```

