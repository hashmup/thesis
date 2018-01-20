# qstatを用いる場合にjobIDを取得するための正規表現
job_cluster_exp = re.compile(
    "(?P<id>\d+).\w+\s+\w+.\w+\s+\w+\s+\d+:\d+:\d+\s+(?P<state>\w+)\s+\w+\s+")
# pjstatを用いる場合にjobIDを取得するための正規表現
job_k_exp = re.compile(
    "(?P<id>\d+)\s+\w+.\w+\s+\w+\s+(?P<state>\w+)\s+[\s\w\d\[\]\/\:\-]+")
# サブミットされたジョブのIDをストアしておくディクショナリー
# サブミットした段階でrunning_jobs[job_id] = 0として初期化される
running_jobs = {}


def is_job_still_running(job_id, environment):
    # 環境がクラスタの場合
    if environment == "cluster":
        # qstatコマンドを実行
        res = execute("qstat")
        # qstatコマンドの返り値を改行で切り分ける
        job_lines = res.split('\n')
        for line in job_lines:
            # jobIDを取得する正規表現とqstatの各行を比較する
            m = job_cluster_exp.match(line)
            if m is not None:
                state = m.group("state")
                if job_id == m.group("id"):
                    # StateがC（Complete）であるならば完了している
                    if state == "C":
                        return False
                    else:
                        # jobIDの値が0,すなわち初期値ならばjobIDがqstatの返り値で
                        # 現れた時にマークする
                        if running_jobs[job_id] == 0:
                            running_jobs[job_id] = 1
                        return True
        # jobIDが以前のqstat実行時に現れ,今回のqstat実行時に一度も現れない場合
        # jobは完了しているとみなせる
        if running_jobs[job_id] > 0:
            return False
        else:
            return True
    # 環境が京の場合
    elif environment == "k":
        # pjstatコマンドを実行
        res = execute("pjstat")
        # pjstatコマンドの返り値を改行で切り分け
        job_lines = res.split('\n')
        for line in job_lines:
            # jobIDを取得する正規表現とpjstatの各行を比較する
            m = job_k_exp.match(line)
            if m is not None:
                if job_id == m.group("id"):
                    # pjstatでは,StateがRUNからSTOに切り替わり表示されなくなるまでの
                    # 間隔が非常に短いため,Stateでの判定は行わずともジョブが完了してから
                    # 結果を集約するまでの時間の差は無視できるほど小さい
                    # ここではjobIDのマークのみを行う
                    if running_jobs[job_id] == 0:
                        running_jobs[job_id] = 1
                    return True
        if running_jobs[job_id] > 0:
            return False
        else:
            return True
