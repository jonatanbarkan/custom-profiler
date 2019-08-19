import inspect
from collections import defaultdict
from time import time

import numpy as np


class TimeLogger:
    def __init__(self, base_time='ms', outliers_m=4):
        self.logger = defaultdict(list)
        if base_time == 'ms':
            self.base = 1000
        elif base_time == 's':
            self.base = 1
        else:
            raise AttributeError
        self.m = outliers_m

    def timeit(self, method):
        def timed(*args, **kw):
            ts = time()
            result = method(*args, **kw)
            es = time()
            # cls = get_class_that_defined_method(method)
            # if cls is None:
            #     pass
            # else:
            #     pass
            self.logger[method.__name__.upper()].append((es - ts) * self.base)
            return result

        return timed

    def print(self):
        for k, v in self.logger.items():
            v = np.array(v)
            print(
                'all        ' + '{} total {:8.2f} ms, times executed {}, mean {:6.2f} ms, std {:6.2f} ms'.format(
                    k, sum(v), len(v), np.mean(v), np.std(v)))
            v_ = v[10:]
            print(
                'after10    ' + '{} total {:8.2f} ms, times executed {}, mean {:6.2f} ms, std {:6.2f} ms'.format(
                    k, sum(v_), len(v_), np.mean(v_), np.std(v_)))
            wo_v = self.reject_outliers(np.array(v))
            print(
                'w/outliers ' + '{} total {:8.2f} ms, times executed {}, mean {:6.2f} ms, std {:6.2f} ms'.format(
                    k, sum(wo_v), len(wo_v), np.mean(wo_v), np.std(wo_v)))
            print()

    def reject_outliers(self, data: np.ndarray):
        d = data[abs(data - np.mean(data)) < self.m * np.std(data)]
        # print('{} outliers'.format(len(data) - len(d)))
        return d


# def get_class_that_defined_method(meth):
#     if inspect.ismethod(meth):
#         for cls in inspect.getmro(meth.__self__.__class__):
#             if cls.__dict__.get(meth.__name__) is meth:
#                 return cls
#         meth = meth.__func__  # fallback to __qualname__ parsing
#     if inspect.isfunction(meth):
#         cls = getattr(inspect.getmodule(meth),
#                       meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
#         if isinstance(cls, type):
#             return cls
#     return getattr(meth, '__objclass__', None)
