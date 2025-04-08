class System_Health:
    '''
    Shared Data
    '''
    py_stats = {}
    pi_stats = {}
    sys_stats = {}

    #        measurement             default status
    py_stats['init wifi connection'] = 'null'
    py_stats['wifi message tx'] = 'null'
    py_stats['wifi message rx'] = 'null'
    py_stats['v1 open command'] = 'null'
    py_stats['v2 open command'] = 'null'
    py_stats['v3 open command'] = 'null'
    py_stats['v4 open command'] = 'null'
    py_stats['v5 open command'] = 'null'
    py_stats['coil on command'] = 'null'
    py_stats['cal command'] = 'null'
    py_stats['test command'] = 'null'
    py_stats['BM command'] = 'null'

    pi_stats["valve 1 fb"] = 'null'
    pi_stats["valve 2 fb"] = 'null'
    pi_stats["valve 3 fb"] = 'null'
    pi_stats["valve 4 fb"] = 'null'
    pi_stats["valve 5 fb"] = 'null'
    pi_stats["coil fb"] = 'null'
    pi_stats["pt 1 fb"] = 'null'
    pi_stats["pt 2 fb"] = 'null'
    pi_stats["pt 3 fb"] = 'null'
    pi_stats["pt 4 fb"] = 'null'
    pi_stats["pt 5 fb"] = 'null'
    pi_stats["lc fb"] = 'null'
    pi_stats["thermo 1 fb"] = 'null'
    pi_stats["thermo 2 fb"] = 'null'
    pi_stats["abort pt 1 "] = 'null'
    pi_stats["abort pt 2 "] = 'null'
    pi_stats["abort pt 3 "] = 'null'
    pi_stats["abort pt 4 "] = 'null'
    pi_stats["abort pt 5 "] = 'null'
    pi_stats["abort pt 6 "] = 'null'
    py_stats['cal command fb'] = 'null'
    py_stats['test command fb'] = 'null'
    py_stats['BM command fb'] = 'null'

    sys_stats.update(py_stats, **pi_stats)

    def get_pi_status(self):
        return self.pi_stats

    def get_py_status(self):
        return self.py_stats

    @classmethod
    def get_sys_status(self):
        id = 0
        keys = list(self.sys_stats.keys())
        values = list(self.sys_stats.values())

        max_key_length = max(len(key) for key in keys)

        for i in range(len(keys)):
            print(f'{keys[i].ljust(max_key_length)} : {values[i]}')
        return self.sys_stats 