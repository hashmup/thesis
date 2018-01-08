job_exp = re.compile(
    "(?P<id>\d+).\w+\s+\w+.\w+\s+\w+\s+\d+:\d+:\d+\s+(?P<state>\w+)\s+\w+\s+")


def is_job_still_running(self, job_id):
    res = self.shell.execute("qstat", [], [], "")[0]
    if type(res) is bytes:
        res = res.decode('utf-8')
    job_lines = res.split('\n')
    if len(job_lines) > 2:
        for line in job_lines[2:]:
            m = job_exp.match(line)
            if m is not None:
                state = m.group("state")
                if job_id == m.group("id") and state == "C":
                    return False
    return True
