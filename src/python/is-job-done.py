# qstat を用いる場合に jobID を取得するための正規表現
job_cluster_exp = re.compile(
    "(?P<id>\d+).\w+\s+\w+.\w+\s+\w+\s+\d+:\d+:\d+\s+(?P<state>\w+)\s+\w+\s+")
# pjstat を用いる場合に jobID を取得するための正規表現
job_k_exp = re.compile(
    "(?P<id>\d+)\s+\w+.\w+\s+\w+\s+(?P<state>\w+)\s+[\s\w\d\[\]\/\:\-]+")
# サブミットされたジョブの ID をストアしておくディクショナリー
# サブミットした段階でrunning_jobs[job_id] = 0として初期化される
running_jobs = {}


def is_job_still_running(job_id, environment):
    # 環境がクラスタの場合
    if environment == "cluster":
        # qstat コマンドを実行
        res = execute("qstat")
        # qstat コマンドの返り値を改行で切り分ける
        job_lines = res.split('\n')
        for line in job_lines:
            # jobID を取得する正規表現と qstat の各行を比較する
            m = job_cluster_exp.match(line)
            if m is not None:
                state = m.group("state")
                if job_id == m.group("id"):
                    # StateがC（Complete）であるならば完了している
                    if state == "C":
                        return False
                    else:
                        # jobID の値が 0 ,すなわち初期値ならば jobID が qstat の返り値で
                        # 現れた時にマークする
                        if running_jobs[job_id] == 0:
                            running_jobs[job_id] = 1
                        return True
        # jobID が以前の qstat 実行時に現れ,今回の qstat 実行時に一度も現れない場合
        # job は完了しているとみなせる
        if running_jobs[job_id] > 0:
            return False
        else:
            return True
    # 環境が京の場合
    elif environment == "k":
        # pjstat コマンドを実行
        res = execute("pjstat")
        # pjstat コマンドの返り値を改行で切り分け
        job_lines = res.split('\n')
        for line in job_lines:
            # jobID を取得する正規表現と pjstat の各行を比較する
            m = job_k_exp.match(line)
            if m is not None:
                if job_id == m.group("id"):
                    # pjstat では,State が RUN から STO に切り替わり表示されなくなるまでの
                    # 間隔が非常に短いため,State での判定は行わずともジョブが完了してから
                    # 結果を集約するまでの時間の差は無視できるほど小さい
                    # ここでは jobID のマークのみを行う
                    if running_jobs[job_id] == 0:
                        running_jobs[job_id] = 1
                    return True
        if running_jobs[job_id] > 0:
            return False
        else:
            return True
