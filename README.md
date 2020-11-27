# マイグレーションをマスターしよう（後編） - djangoチュートリアル #16

普段何気なく使っているマイグレーションについてもう少し深く理解しましょう。

エラーが発生した時に柔軟に対応できるようになりましょう。

## 事前準備（前回までの状態の復元）

### サーバー起動

Paizaサーバーは、djangoとMySQLにチェックを入れて起動して下さい。

MySQLのチェックを忘れた人はphpMyAdminを起動するのと同じメニューからMySQL → Start を押すと起動できます。

### phpMyAdmin起動

メニューに「phpMyAdmin」という項目があるので、「Start」 を押して、終わったら次 「Open」を押します。

### データベース作成

phpMyAdmin上で`pj_migrate`という新規データベースを作成して下さい。

※詳しくは前回の動画を参照

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

### マイグレーションの実行

前回までのマイグレーションを実行しましょう。

```sh
python manage.py migrate
```

## マイグレーションはどこに記録されているか

phpMyAdminのdjango_migrationsというテーブルを見てみましょう。

## 複数のマイグレーションを１つにまとめる

`blog/models.py`のBlogモデルの一番下に以下のフィールドを追加しましょう。

```py
    field1 = models.CharField(max_length=250, default="")
```

その状態で一度マイグレーションファイルを作りましょう。

以下を実行します。

```sh
python manage.py makemigrations blog
```

マイグレーションも実行してDBにまで反映させます。

```sh
python manage.py migrate
```

仮にマイグレーションを実行した後にもう１つフィールドを追加したくなったとします。

以下のfield2をfield1の下に追加しましょう。

```py
    field2 = models.CharField(max_length=250, default="")
```

その状態でもう１つマイグレーションファイルを作りましょう。

以下を実行します。

```sh
python manage.py makemigrations blog
```

マイグレーションももう一度実行してDBにまで反映させます。

```sh
python manage.py migrate
```

今マイグレーションファイルが２つ追加された状態です。

実務ではこれを１つにまとめたい、まとめて欲しいと言われることがよくあります。

本番のDBの変更は巻き戻しが難しく（ユーザーデータが消えてしまうためです）、管理しやすくするためです。

この２つのマイグレーションファイルをまとめて１つにするには`squashmigrations`というコマンドを使用します。

```sh
python manage.py squashmigrations blog 0004_blog_field1 0005_blog_field2
```

確認メッセージが出るので`y`（Yesの意味）とタイプして進めます。

もとの２つのマイグレーションファイルは削除しましょう。

* `blog/migrations/0004_blog_field1.py`
* `blog/migrations/0005_blog_field2.py`

これで完成です。

`showmigrations`コマンドでマイグレーション一覧を表示してみましょう。

```sh
python manage.py showmigrations blog
```

## まとめた後を残さずに1つのファイルにまとめる

`blog/models.py`のBlogモデルの一番下に以下のフィールドを追加しましょう。

```py
    field3 = models.CharField(max_length=250, default="")
```

その状態で一度マイグレーションファイルを作りましょう。

以下を実行します。

```sh
python manage.py makemigrations blog
```

もう１度以下のfield4をfield3の下に追加しましょう。

```py
    field4 = models.CharField(max_length=250, default="")
```

その状態でもう１つマイグレーションファイルを作りましょう。

以下を実行します。

```sh
python manage.py makemigrations blog
```

マイグレーションも実行してDBにまで反映させます。

```sh
python manage.py migrate
```

これで0005と0006の２つのマイグレーションファイルが出来ました。

そして、その内容はDBにも同期されています。

これを`squashmigrations`を使わずに１つのマイグレーションファイルにまとめてみましょう。

`squashmigrations`を使うと１つにまとめた後が残ってしまいます。

また、たまにエラーで実行できないこともあります。

それらが嫌だという方は今から紹介する方法が向いています。

まずは、0005と0006の２つのマイグレーションファイルを削除します。

その状態でマイグレーションファイルを作りましょう。

以下を実行します。

```sh
python manage.py makemigrations blog
```

すると、0005のマイグレーションファイルが出来ます。

これで１つにまとめた後が残らずに、もとあった0005と0006を合わせた内容のマイグレーションファイルの完成です。

ここで注意点として、もとあった0005と0006の内容がすでにDBに同期されてしまっています。

試しに新しいマイグレーションファイルでマイグレーションを実行してみましょう。

```sh
python manage.py migrate
```

すでにDBに`field3`と`field4`が存在するというエラーが出ます。

この0005が実行できないと今後すべてマイグレーションが実行できないので解決する必要があります。

このようにすでにDBには適用済みのマイグレーションを後から事実上実行済み状態にしたい場合には`--fake`というオプションを使用します。

以下のコマンドを実行しましょう。

```sh
python manage.py migrate --fake
```

すると、DB上のBlogテーブルは変わらずにマイグレーションだけが実行済みの状態になります。

それ以降はまたこれまでと同じようにマイグレーションしていくことが出来ます。

## 分岐した際のマージ

複数人で開発していると同じ番号のマイグレーションが複数出来ることがあります。

この場合の解消方法を紹介します。

`blog/models.py`のBlogモデルの一番下に以下のフィールドを追加しましょう。

```py
    field5 = models.CharField(max_length=250, default="")
```

その状態で一度マイグレーションファイルを作りましょう。

以下を実行します。

```sh
python manage.py makemigrations blog
```

`0006_blog_field5.py`というマイグレーションファイルが出来ます。

これを一旦削除したことにしましょう。

ファイル名を`_`から始めるとマイグレーションファイルとして認識されなくなります。

`_0006_blog_field5.py`と名前を変更しましょう。

もう１人の開発者が同時に`field6`を追加したと仮定して以下のように追記しましょう。

```py
    field6 = models.CharField(max_length=250, default="")
```

その状態でマイグレーションファイルを作りましょう。

以下を実行します。

```sh
python manage.py makemigrations blog
```

`0006_blog_field6.py`というマイグレーションファイルが出来ます。

ここで先程名前を変えておいたマイグレーションファイルを`0006_blog_field5.py`と再度変えて認識されるように戻します。

この状態でマイグレーションを実行してみましょう。

```py
python manage.py migrate
```

同じ番号をもったマイグレーションファイルが２つあるというエラーが出ます。

これを解消するには0006で２つに分かれてしまったマイグレーションファイルを0007でもとの１本道に戻す必要があります。

これには`--merge`というオプションと一緒に`makemigrations`コマンドを使用します。

以下のコマンドを実行しましょう。

```
python manage.py makemigrations --merge
```

確認メッセージが出るので`y`とタイプし、Enterを押します。

0007が出来ます。

この中には２つの0006が依存関係として追加されています。

この0007がまとめてくれていることによって、0006が２つある状態が許されているのです。

マイグレーションを実行してみましょう。

```
python manage.py migrate
```

エラー無く実行できました。

## 複数人が矛盾するマイグレーションファイルを作った場合

先程は`field4`と`field5`という互いに矛盾しない独立した変更をしたのでマイグレーションがうまくいきました。

一方で矛盾する変更が同時にされると`--merge`を使って自動でマイグレーションファイルを作ることは出来ません。

そのプロジェクトがどういう方向性でいくかdjangoは当然知らないからです。

そういう場合にはチームでコミュニケーションをとって、ソースコードを正しい形に修正する必要があります。

本番適用前のマイグレーションファイルであれば一旦削除してソースコードを修正してマイグレーションファイルを作り直します。

本番適用後であれば、必要なコードの修正を行ってから追加のマイグレーションファイルとして作成します。

その上でマイグレーションを実行します。
