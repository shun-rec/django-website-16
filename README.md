# マイグレーションをマスターしよう（前編） - djangoチュートリアル #15

普段何気なく使っているマイグレーションについてもう少し深く理解しましょう。

エラーが発生した時に柔軟に対応できるようになりましょう。

## 事前準備

### サーバー起動

Paizaサーバーは、djangoとMySQLにチェックを入れて起動して下さい。

MySQLのチェックを忘れた人はphpMyAdminを起動するのと同じメニューからMySQL → Start を押すと起動できます。

### phpMyAdmin起動

メニューに「phpMyAdmin」という項目があるので、「Start」 を押して、終わったら次 「Open」を押します。

### 新規プロジェクトの作成

```sh
django-admin startproject pj_migrate
cd pj_migrate
```

全体設定のALLOWED_HOSTSを以下のように修正します。

どのドメイン名でアクセスしてもアクセス出来るように許可する設定です。

```py
ALLOWED_HOSTS = ['*']
```

### 新規アプリ作成

```sh
python manage.py startapp blog
```

全体設定にblogアプリを追加します。

`pj_migrate/settings.py`のINSTALLED_APPSの最後に以下を追記します。

```py
    'blog',
```

### データベースとの接続

詳しくは第5回を参照。

今回はPaiza上で使いやすいMySQLと接続してみます。  

※ SQLに慣れている方はデフォルトのSQLite3のままでも構いません。

#### 共通ライブラリのインストール

MySQLとPostgreSQLなど、データベースに接続する際に共通で必要になるライブラリを２つインストールします。  

* dj-database-url: データベースの接続設定が１行で楽に書けるライブラリ
* python-dotenv: `.env`という環境設定ファイルを使ってプロジェクトの設定が出来るライブラリ

```sh
pip install dj-database-url
pip install python-dotenv
```

##### 全体設定ファイルの編集

もともとあるDATABASESの欄を削除して以下を追記。  

```py
import dj_database_url
from dotenv import (
    find_dotenv,
    load_dotenv,
)
load_dotenv(find_dotenv())
DATABASES = {
    'default': dj_database_url.config(conn_max_age=600),
}
```

* load_dotenvで環境設定ファイルを読み込み、
* dj_database_url.configで自動的に設定されます。
* conn_max_age=600というのは今は理解不要ですが、高速化の設定です。

#### MySQL用ライブラリのインストール

```
pip install mysqlclient
```

#### MySQL上にプロジェクト用データベースを作成

phpMyAdmin上で作成します。  
`pj_migrate`という新しいデータベースを作成します。

#### 環境設定ファイルを設置

プロジェクト直下に`.env`というファイル名でファイルを作り、以下の内容を入力。
  
※ドットから始まるファイル名は隠しファイルと言って、デフォルトでは非表示です。Paizaではプロジェクトフォルダで右クリックをすると、「隠しファイルを表示」することが出来ます。

`mysql`の`pj_migrate`というデータベースに`root`ユーザーでパスワード無しでアクセスするという意味。

パスワード有りの場合は`root:password`と書きます。

```
DATABASE_URL=mysql://root:@localhost/pj_migrate
```

## 最初のマイグレーションの動きをDB上で見てみよう

何もない状態のphpMyAdminを開いてみましょう。

次にプロジェクトのデータベースを作成しましょう。

`migrate`コマンドは全体設定のINSTALLED_APPSに指定されたアプリのすべてのマイグレーションファイルをデータベースに反映させます。

```sh
python manage.py migrate
```

もう一度phpMyAdminを開いてみましょう。テーブルが作成されています。

`django_migrations`というテーブルを開いて実行済みのマイグレーション一覧を見てみましょう。

次にスーパーユーザーを追加してみましょう。

```sh
python manage.py createsuperuser
```

* ユーザー名: admin
* パスワード: admin

phpMyAdmin上でデータを閲覧したり、編集することが出来ます。

## 独自のマイグレーションファイルを作って実行してみよう

### モデルの定義

`blog/models.py`を以下の内容に編集します。

```py
from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=250)
```

* 文字列の`title`だけを持った`Blog`モデルを作ります。

### マイグレーションファイルの作成

```sh
python manage.py makemigrations blog
```

### マイグレーションで実行されるSQLの確認

データベースに変更を加えるにはSQL（エスキューエル）という言語を使用します。  
これはdjangoに限らず、データベースを使うために共通の言語です。

先程作ったマイグレーションファイルが最終的にどのようなSQLとなって実行されるのかは以下のコマンドで確認出来ます。

`sqlmigrate`のコマンドでアプリ名とマイグレーションファイルIDを指定します。

```py
python manage.py sqlmigrate blog 0001_initial
```

### マイグレーションの適用

```sh
python manage.py migrate
```

phpMyAdmin上でBlogテーブルが作成され、titleカラムが追加されていることを確認しましょう。

### データベースで直接データを追加して、管理サイトから確認しよう

#### phpMyAdmin上でレコードの追加

phpMyAdmin上でBlogテーブルにレコードを追加しましょう。

データベース上の１つのデータをレコードと言います。

#### Blogを管理サイトに登録

`blog/admin.py`を以下の内容に編集します。

```py
from django.contrib import admin

from .models import Blog

admin.site.register(Blog)
```

内容は前回までの管理サイトの回を参照して下さい。

#### 管理サイトで確認

追加したら、開発サーバーを立ち上げます。

```sh
python manage.py runserver
```

管理サイトにアクセスして、Blogが１つ作成されていることを確認しましょう。

このように、普段はdjangoが自動的にデータベースと同期してくれていますが、データベース上でデータを変更することも可能です。

## テーブルにカラムを追加してみよう

それでは一度作ったモデル（テーブル）を変更してみましょう。

### モデルの変更

`pj_migrate/models.py`のBlogクラスのtitleフィールドの下に以下を追記します。

```py
    body = models.TextField()
```

* body ブログの本文となる文章です。

### マイグレーションファイルの作成

ここからは最初にモデルを作ったときと同様の手順です。

```sh
python manage.py makemigrations blog
```

何も問題が無いときにはそのままマイグレーションファイルが作成されます。

今回はdjangoに追加の質問をされます。

今回はbodyにデフォルト値を設定していません。

そしてbodyは`null=True`を指定していないので、空にすることも出来ません。

なので、既存のBlogについてはbodyはどうするのか？という質問をdjangoにされます。

```
You are trying to add a non-nullable field 'body' to blog without a default; we can't do that (the database needs something to populate existing rows).
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit, and let me add a default in models.py
Select an option:
```

1を選択すると、その場で既存のBlogにのみ使われるデフォルト値の入力画面が開始します。  
2を選択すると、マイグレーションが中止されます。

今回はBlogモデルにはデフォルト値を設定したくないので、既存のBlogにのみ使われる今だけのデフォルト値を使うことにします。

`1`と入力してEnterキーを押します。

すると、Pythonコンソールが開くのでデフォルト値を入力してEnterキーを押します。

今回は既存のBlogについてはbodyは空文字列`""`としますので、それを入力してEnterキーを押します。

これでマイグレーションファイルが作成されます。

### SQLの確認

マイグレーションファイルを作成するとその作成したファイル名が表示されます。

その`.py`を除いた部分がIDです。

そのIDを指定して以下のように`sqlmigrate`コマンドを実行します。

```sh
python manage.py sqlmigrate blog 0002_blog_body
```

### マイグレーション実行

```sh
python manage.py migrate
```

### phpMyAdminで確認しよう

bodyカラムが追加されています。

先程追加したレコードも自動で修正され、空文字列のbodyが追加されています。

## 適用したマイグレーションをもとに戻してみよう（ロールバック）

本番ではこのようなロールバックを使用することは実はありません。

本番では、データベース全体のバックアップ（スナップショット）を定期的にとっておきます。

何か問題が生じた時にはそのバックアップを使用してもとに戻します。

今回はそのようなバックアップなどが存在しない場合や、テスト・開発用にdjangoの機能でもとに戻す方法です。

### マイグレーションIDの確認

まずは戻したい時点のマイグレーションIDを確認します。

候補となるマイグレーションIDの一覧は以下の`showmigrations`コマンドで確認出来ます。

```sh
python manage.py showmigrations blog
```

### ロールバックの実行

今回は`0001_initial`時点まで戻してみましょう。

```sh
python manage.py migrate blog 0001_initial
```

### マイグレーションファイルの削除

次のマイグレーションで間違って実行されないように、不要になったマイグレーションファイルは削除しましょう。

```sh
rm blog/migrations/0002_blog_body.py
```

### モデルからもbodyを削除

モデルからも不要になったbodyは削除しましょう。

```py
from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=250)
```

### phpMyAdminで確認しよう

bodyカラムがたしかに削除されていることが確認出来ます。

## ユニーク制約を持ったフィールドを追加する

他のレコードとデータが被っていけないという制約をユニーク制約といいます。

これを使うと誰かと同じメールアドレスやユーザー名で登録しようとした場合にエラーを出し、必ず皆が異なるメールアドレスやユーザー名をもつようにできます。

これは便利なので、本番でも途中から追加したい場面はよくあります。

今回はブログ記事のURLを表すスラッグを追加してみましょう。

ブログ記事のURLはそれぞれ異なっている必要があるので、ユニーク制約が必要です。

ここで単にマイグレーションファイルを作ろうとすると、問題が起こります。

既存のブログ記事はそもそもスラッグを持っていないので先ほどと同じようにデフォルト値を設定したいです。

ところが、ユニーク制約があるのですべてに同じ値を設定するわけにはいきません。

こういう場合の設定方法です。

### 全体の手順

1. ユニーク制約無しでスラッグフィールドを追加し、マイグレーションを実行します
2. 既存のブログにそれぞれ異なるスラッグを設定します
3. スラッグフィールドにユニーク制約を追加し、マイグレーションを再度実行します

### ユニーク制約無しでスラッグフィールドを追加し、マイグレーションを実行

`blog/models.py`のBlogモデルのtitleの下に以下を追記します。

```py
    slug = models.SlugField(unique=False, default="")
```

マイグレーションファイルを作成します。

```sh
python manage.py makemigrations blog
```

マイグレーションを実行します。

```sh
python manage.py migrate
```

### 既存のブログにそれぞれ異なるスラッグを設定

phpMyAdminを開いてブログ記事それぞれに異なるスラッグを設定しましょう。

### スラッグフィールドにユニーク制約を追加し、マイグレーションを再度実行

`blog/models.py`のBlogモデルのslugフィールドを以下のように変更します。

```py
    slug = models.SlugField(unique=True)
```

マイグレーションファイルを作成します。

```sh
python manage.py makemigrations blog
```

マイグレーションを実行します。

```sh
python manage.py migrate
```

これで無事ユニーク制約をもったスラッグフィールドを追加できました。
