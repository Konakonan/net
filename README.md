# net




#メモ<br>
--仮想環境内でpipのversionアップをしてください<br>
--コマンド:python -m pip install --upgrade pip <br>
--その後にモジュールを入れて。pip install -r requirements.txt<br>
--version指定してないため、確認したかったらして。python -c "import <>; print(<>.__version__)"<br>
--git hub トークンまだ使えた。<br>
--readme.mdをgit hub上で作ってからpushしたらconflictする。<br>
--git config --global pull.rebase falseしてからpullしてpushした解決した。<br>

#toxコマンド<br>
-- !! cmd<br>
-- tox -e <テスト環境名> <br>