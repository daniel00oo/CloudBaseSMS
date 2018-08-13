import psutil


class Cpuinfo(object):
    def __init__(self):
        pass

    @staticmethod
    def get():
        d = {}

        l = psutil.cpu_freq()
        aux = {}
        for i in range(len(l)):
            aux[l._fields[i]] = l[i]
        d['cpu_freq'] = aux

        l = psutil.cpu_times()
        aux = {}
        for i in range(len(l)):
            aux[l._fields[i]] = l[i]
        d['cpu_times'] = aux

        d['cpu_percent'] = psutil.cpu_percent(0.5)

        l = psutil.cpu_stats()

        aux = {}
        for i in range(len(l)):
            aux[l._fields[i]] = l[i]
        d['cpu_stats'] = aux

        return d
