import psutil


class Diskinfo(object):
    def __init__(self):
        pass

    @staticmethod
    def get():
        d={}

        l = psutil.disk_partitions()
        
        j = 0
        for disk in l:
            aux = {}
            for i in range(len(disk)):
                aux[disk._fields[i]] = disk[i]
            d['disk_partition{}'.format(j)] = aux
            j += 1

        l = psutil.disk_usage('/')
        aux = {}
        for i in range(len(l)):
            aux[l._fields[i]] = l[i]
        d['disk_usage'] = aux

        l = psutil.disk_io_counters()
        aux = {}
        for i in range(len(l)):
            aux[l._fields[i]] = l[i]
        d['disk_io_counters'] = aux

        return d
