#!/bin/sh
setupIfNecessary() {
    # .pyenv が存在しない場合はダウンロード
    #  install 時に初回のみ実行される
    if [ ! -d "~/.pyenv" ]; then
        # github からクローンする
        git clone https://github.com/pyenv/pyenv.git ~/.pyenv

        # 必要な環境変数の設定
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
        echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
        echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
        exec "$SHELL"

        # anaconda3-4.3.0 をPython として利用するための設定
        pyenv install anaconda3-4.3.0
        pyenv local anaconda3-4.3.0
        pyenv rehash
    fi

    # genie 実行に必要なPython ライブラリのインストール
    pip install textx
    pip install pandas
    pip install jinja2
}
setupIfNecessary
