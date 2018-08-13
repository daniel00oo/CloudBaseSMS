import psutil


class Meminfo(object):
    def __init__(self):
        pass

    @staticmethod
    def get():
        d = {}
        l = psutil.virtual_memory()

        aux = {}
        for i in range(len(l)):
            aux[l._fields[i]] = l[i]
        d['virtual_memory'] = aux

        l = psutil.swap_memory()
        aux = {}
        for i in range(len(l)):
            aux[l._fields[i]] = l[i]
        d['swap_memory'] = aux

        return d
