time_exp = re.compile(
    "\s+\* core time : (?P<decimal>\d+).(?P<float>\d+) sec\s+")


def obtain_time(self, filename):
        f = open(filename)
        lines = f.readlines()
        f.close()
        for line in lines:
            m = time_exp.match(line)
            if m:
                time = int(m.group("decimal")) +\
                    int(m.group("float")) * 10**(-len(m.group("float"))+1)
                return time
