import math
import operator
import six

class NegativePopulationSize(ValueError):
    def __init__(self, typename):
        self.typename = typename
        ValueError.__init__(self)
    def __str__(self):
        return str(str(self))
    def __unicode__(self):
        return "More calls to %(type)s.remove() than to %(type)s.add()" % {"type": self.typename}

class NonPositivePopulationSize(ValueError):
    def __init__(self, typename):
        self.typename = typename
        ValueError.__init__(self)
    def __str__(self):
        return str(str(self))
    def __unicode__(self):
        return "Need more calls to %(type)s.add() than to %(type)s.remove()" % {"type": self.typename}


class AbstractStdDev(object):
    def get(self):
        return math.sqrt(self.getSqr())
    def __add__(self, other):
        return StdDevSum(self.getSqr() + other.getSqr())

class StdDevSum(AbstractStdDev):
    def __init__(self, sqr):
        self.sqr = sqr
    def getSqr(self):
        return self.sqr

class StdDev(AbstractStdDev):
    def __init__(self):
        self.count = 0
        self.sum = 0
        self.sqrsum = 0
    def add(self, value):
        self.count += 1
        self.sum += value
        self.sqrsum += value**2
    def remove(self, value):
        if self.count < 1:
            raise NonPositivePopulationSize("StdDev")
        self.count -= 1
        self.sum -= value
        self.sqrsum -= value**2
    def getSqr(self):
        if self.count < 1:
            raise NonPositivePopulationSize("StdDev")
        a = self.sqrsum/self.count
        b = (self.sum/self.count)**2
        # Handle rounding errors
        # FIXME: find out what values this happened for and make a test...
        if a < b: # pragma: no cover
            assert b - a < 1e-3
            return 0.0
        return a - b

class Avg(object):
    def __init__(self):
        self.count = 0
        self.sum = 0
    def add(self, value):
        self.count += 1
        self.sum += value
    def remove(self, value):
        if self.count <= 1:
            raise NonPositivePopulationSize("Avg")
        self.count -= 1
        self.sum -= value
    def get(self):
        if self.count < 1:
            raise NonPositivePopulationSize("Avg")
        return self.sum/self.count

class Sum(object):
    def __init__(self):
        self.count = 0
        self.sum = 0
    def add(self, value):
        self.count += 1
        self.sum += value
    def remove(self, value):
        if self.count <= 0:
            raise NegativePopulationSize("Sum")
        self.count -= 1
        self.sum -= value
    def get(self):
        return self.sum

class Count(object):
    def __init__(self):
        self.count = 0
    def add(self, value):
        self.count += 1
    def remove(self, value):
        # Fast failure
        if self.count <= 0:
            raise NegativePopulationSize("Sum")
        self.count -= 1
    def get(self):
        return self.count

class Stat(object):
    def __init__(self, source, cls):
        self.source = source
        self.value = cls()
    def add(self, value):
        if self.source in value:
            self.value.add(value[self.source])
    def remove(self, value):
        if self.source in value:
            self.value.remove(value[self.source])
    def get(self):
        return self.value.get()

class StatSum(object):
    def __init__(self, *stats):
        self.stats = stats
    def add(self, value):
        for stat in self.stats:
            stat.add(value)
    def remove(self, value):
        for stat in self.stats:
            stat.remove(value)
    def get(self):
        summed = self.stats[0].value
        for x in self.stats[1:]:
            summed = summed + x.value
        return summed.get()
        # return reduce(operator.add, [stat.value for stat in self.stats]).get()

class Stats(object):
    """
    stat = Stats({
        "latitude": Stat("latitude", Avg),
        "longitude": Stat("longitude", Avg),
        "sigma": StatSum(Stat("latitude", StdDev),
                         Stat("longitude", StdDev))})
    stat.add({'latitude': 4.3, 'longitude': 3.2})
    print stat.get()['sigma']
    """

    def __init__(self, fieldmap):
        self.fieldmap = fieldmap
    def add(self, value):
        for field in six.itervalues(self.fieldmap):
            field.add(value)
    def remove(self, value):
        for field in six.itervalues(self.fieldmap):
            field.remove(value)
    def get(self):
        return {
            key: value.get()
            for (key, value)
            in six.iteritems(self.fieldmap)}
