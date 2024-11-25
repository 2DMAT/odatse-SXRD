odatse-SXRD のインストール
================================

実行環境・必要なパッケージ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- python 3.9 以上

    - 必要なpythonパッケージ

        - numpy (>= 1.14)
        - pydantic (>= 2.0)

- ODAT-SE version 3.0 以降

- sxrdcalc

    - Cコンパイラおよび GNU Scientific Library が必要

ダウンロード・インストール
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. ODAT-SE をインストールする

   - ソースコードからのインストール

     リポジトリから ODAT-SE のソースファイルを取得します。

     .. code-block:: bash

        $ git clone https://github.com/issp-center-dev/ODAT-SE.git

     pip コマンドを実行してインストールします。

     .. code-block:: bash

	$ cd ODAT-SE
	$ python3 -m pip install .

     ``--user`` オプションを付けるとローカル (``$HOME/.local``) にインストールできます。

     ``python3 -m pip install .[all]`` を実行するとオプションのパッケージも同時にインストールします。

2. sxrdcalc をインストールする

   - sxrdcalc は GitHubの以下のURLで公開されています。

     https://github.com/sxrdcalc/sxrdcalc

     サイトにアクセスし、「Code」-「Download ZIP」よりソースコード一式をダウンロードします。以下のコマンドで取得することもできます。

     .. code-block:: bash

        $ wget -O sxrdcalc.zip https://github.com/sxrdcalc/sxrdcalc/archive/refs/heads/main.zip

   - ソースパッケージを展開し、コンパイルします。必要に応じて sxrdcalc-main/ 内の Makefile を編集してください。コンパイルには GNU Scientific Library が必要です。

     .. code-block:: bash

	$ unzip sxrdcalc.zip
	$ cd sxrdcalc-main
	$ make

     コンパイルが成功すると実行形式 ``sxrdcalc`` が作成されます。 ``sxrdcalc`` を PATH の通ったディレクトリ (環境変数 PATH に列挙された、実行プログラムを探索するディレクトリ) に配置するか、実行時にディレクトリ名をつけて指定します。

3. odatse-SXRD をインストールする

   odatse-SXRD のソースファイルは GitHub リポジトリから取得できます。以下の手順でリポジトリをクローンした後、pip コマンドを実行してインストールします。

     .. code-block:: bash

	$ git clone https://github.com/2DMAT/odatse-SXRD.git
	$ cd odatse-SXRD
	$ python3 -m pip install .

     ``--user`` オプションを付けるとローカル (``$HOME/.local``) にインストールできます。

     odatse-SXRD のライブラリと、実行コマンド ``odatse-SXRD`` がインストールされます。


実行方法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ODAT-SE では順問題ソルバーと逆問題解析アルゴリズムを組み合わせて解析を行います。
SXRDの解析を行うには次の2通りの方法があります。

1. このパッケージに含まれる odatse-SXRD プログラムを利用して解析を行います。ユーザは、プログラムの入力となるパラメータファイルを TOML 形式で作成し、プログラムの引数に指定してコマンドを実行します。逆問題解析のアルゴリズムはパラメータで選択できます。

2. odatse-SXRD ライブラリと ODAT-SE フレームワークを用いてプログラムを作成し、解析を行います。逆問題解析アルゴリズムは import するモジュールで選択します。プログラム中に入力データの生成を組み込むなど、柔軟な使い方ができます。

パラメータの種類やライブラリの利用方法については以降の章で説明します。


アンインストール
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

odatse-SXRD モジュールおよび ODAT-SE モジュールをアンインストールするには、以下のコマンドを実行します。

.. code-block:: bash

    $ python3 -m pip uninstall odatse-SXRD ODAT-SE
