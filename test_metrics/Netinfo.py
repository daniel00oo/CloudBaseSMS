import psutil


class Netinfo(object):
    def __init__(self):
        pass

    @staticmethod
    def get():
        d = {}

        l = psutil.net_io_counters()
        aux = {}
        for i in range(len(l)):
            aux[l._fields[i]] = l[i]
        d['net_io_counters'] = aux

        l = psutil.net_connections()
        j = 0
        for conn in l:
            aux = {}
            for i in range(len(conn)):
                aux[conn._fields[i]] = conn[i]
            d['net_connection{}'.format(j)] = aux
            j += 1

        d['net_if_addrs'] = psutil.net_if_addrs()
        d['net_if_stats'] = psutil.net_if_stats()
        
        return d
