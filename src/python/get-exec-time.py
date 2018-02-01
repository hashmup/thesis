# シミュレーションにかかった時間を取得するための正規表現
time_exp = re.compile(
    "\s+\* core time : (?P<decimal>\d+).(?P<float>\d+) sec\s+")


def obtain_time(self, filename):
    f = open(filename)
    lines = f.readlines()
    f.close()
    # シミュレーション時間を出力しているのはファイルの中でも1行のみだが,
    # 並列で実行している場合表示される順番がランダムになっているため
    # すべての行を確認する必要がある
    for line in lines:
        m = time_exp.match(line)
        if m:
            time = int(m.group("decimal")) +\
                int(m.group("float")) * 10**(-len(m.group("float")))
            return time
