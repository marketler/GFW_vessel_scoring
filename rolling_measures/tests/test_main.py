import unittest
import rolling_measures

class TestMain(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_StdDev(self):
        stddev = rolling_measures.StdDev()
        stddev.add(0)
        stddev.add(10)
        self.assertEqual(stddev.get(), 5.0)

        stddev = rolling_measures.StdDev()
        stddev.add(55)
        stddev.add(0)
        stddev.add(0)
        stddev.add(0)
        stddev.add(4)
        stddev.remove(55)
        self.assertEqual(stddev.getSqr(), 3)

        stddev = rolling_measures.StdDev()
        with self.assertRaises(rolling_measures.NonPositivePopulationSize):
            stddev.getSqr()

        stddev = rolling_measures.StdDev()
        stddev.add(0)
        stddev.remove(0)
        with self.assertRaises(rolling_measures.NonPositivePopulationSize):
            stddev.remove(0)

    def test_Avg(self):
        avg = rolling_measures.Avg()
        avg.add(0)
        avg.add(10)
        self.assertEqual(avg.get(), 5.0)

        avg = rolling_measures.Avg()
        avg.add(55)
        avg.add(0)
        avg.add(0)
        avg.add(0)
        avg.add(4)
        avg.remove(55)
        self.assertEqual(avg.get(), 1)

        avg = rolling_measures.Avg()
        with self.assertRaises(rolling_measures.NonPositivePopulationSize):
            avg.get()

        avg = rolling_measures.Avg()
        avg.add(0)
        with self.assertRaises(rolling_measures.NonPositivePopulationSize):
            avg.remove(0)

    def test_Sum(self):
        sum = rolling_measures.Sum()
        sum.add(0)
        sum.add(10)
        self.assertEqual(sum.get(), 10)

        sum = rolling_measures.Sum()
        sum.add(55)
        sum.add(0)
        sum.add(0)
        sum.add(0)
        sum.add(4)
        sum.remove(55)
        self.assertEqual(sum.get(), 4)

        sum = rolling_measures.Sum()
        self.assertEqual(sum.get(), 0)

        sum = rolling_measures.Sum()
        sum.add(0)
        sum.remove(0)
        with self.assertRaises(rolling_measures.NegativePopulationSize):
            sum.remove(0)

    def test_Count(self):
        count = rolling_measures.Count()
        count.add(0)
        count.add(10)
        self.assertEqual(count.get(), 2)

        count = rolling_measures.Count()
        count.add(55)
        count.add(0)
        count.add(0)
        count.add(0)
        count.add(4)
        count.remove(55)
        self.assertEqual(count.get(), 4)

        count = rolling_measures.Count()
        self.assertEqual(count.get(), 0)

        count = rolling_measures.Count()
        count.add(0)
        count.remove(0)
        with self.assertRaises(rolling_measures.NegativePopulationSize):
            count.remove(0)

    def test_Stats(self):
        stat = rolling_measures.Stats({
                "latitude": rolling_measures.Stat("latitude", rolling_measures.Avg),
                "longitude": rolling_measures.Stat("longitude", rolling_measures.Avg),
                "sigma": rolling_measures.StatSum(rolling_measures.Stat("latitude", rolling_measures.StdDev),
                                                  rolling_measures.Stat("longitude", rolling_measures.StdDev))})
        stat.add({'latitude': 47.0, 'longitude': 11.0})
        stat.add({'latitude': 1.0, 'longitude': 1.0})
        stat.add({'latitude': 3.0, 'longitude': 3.0})
        stat.remove({'latitude': 47.0, 'longitude': 11.0})

        self.assertEqual(stat.get()['latitude'], 2.0)
        self.assertEqual(stat.get()['longitude'], 2.0)
        self.assertAlmostEqual(stat.get()['sigma'], 1.41421356237)

        stat.remove({'latitude': 0.0, 'longitude': 0.0})
        with self.assertRaises(rolling_measures.NonPositivePopulationSize):
            stat.remove({'latitude': 0.0, 'longitude': 0.0})
