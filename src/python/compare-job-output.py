# シミュレーション結果でそれぞれのスパイクに関わる行の正規表現
spike_exp = re.compile(
    "SPIKE : \t (?P<val>\d+\.*\d*)\t (?P<idvec>[0-9]+) \[(?P<pid>\d+)\]")
# シミュレーションでスパイク情報を集計した行の正規表現
spike_stat_exp = re.compile(
    "\[(?P<pid>\d+)\] NC = (?P<nc>\d+), SYN = (?P<syn>\d+), \
    tmp_pre = (?P<tmp_pre>\d+), tmp_post = (?P<tmp_post>\d+)")
# シミュレーション結果で各々のプロセスに関わる行の正規表現
end_exp = re.compile(
    "\[(?P<pid>\d+)\] nsendmax=(?P<nsendmax>\d+) nsend=(?P<nsend>\d+) \
    nrecv=(?P<nrecv>\d+) nrecv_useful=(?P<nrecv_useful>\d+)")


def verify(self, files):
    # ハッシュ値を保存するセット
    s = set()
    # ファイルを一つずつ読み込み,ソートしたのちハッシュ値をセットに追加する
    for filename in files:
        f = open(filename)
        lines = f.readlines()
        f.close()
        s.add(self.sort_and_hash_log(lines))
    # すべてのファイルの内容が同じなのであれば,セットの大きさは1である
    return len(s) == 1


def sort_and_hash_log(self, lines):
    _lines = []
    spike_stat = {}
    end = {}
    spike = {}
    # processIDの最大値を記憶しておくための変数
    maxid = 0
    # ファイルないのすべての行に対して正規表現と合致するものを抜き出す
    for line in lines:
        m = spike_stat_exp.match(line)
        if m:
            pid = int(m.group("pid"))
            spike_stat[pid] = line
            maxid = max(maxid, pid)
            continue
        m = spike_exp.match(line)
        # 各Spikeに関してのみ複数行あるため,2次元で情報をストアする
        if m:
            pid = int(m.group("pid"))
            idvec = int(m.group("idvec"))
            if pid in spike:
                spike[pid][idvec] = line
            else:
                spike[pid] = {}
                spike[pid][idvec] = line
            continue
        m = end_exp.match(line)
        if m:
            pid = int(m.group("pid"))
            end[pid] = line
    # spike, spikeの統計量,そのプロセスの統計量をprocessID順に並べ替える
    for pid in range(maxid + 1):
        _lines.append(spike_stat[pid])
        for line in spike[pid]:
            _lines.append(spike[pid][line])
        _lines.append(end[pid])
    # ソートし終えたファイルの中身のハッシュ値を計算する
    return hash(tuple(_lines))
