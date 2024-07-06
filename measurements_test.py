import unittest
import measurements
from datetime import datetime


def mapDictResultToList(result):
    resultToList = []
    for key, value in result.items():
        temp = [key, value]
        for item in value:
            resultToList.append(item)
    return resultToList


class LearnTest(unittest.TestCase):

    def test_sampleMeasurements(self):
        filename = 'unsampled_measurements_test.txt'
        records = measurements.readFileToDataclass(filename)
        records.sort(key=lambda measure: measure.measurementTime)
        measurementStartDate = records[0].measurementTime

        result = measurements.sampleMeasurements(startOfSampling=measurementStartDate, unsampledMeasurements=records)

        filename = 'sampled_measurements_test.txt'
        sampledRecords = measurements.readFileToDataclass(filename)
        resultToList = mapDictResultToList(result)

        i = 0
        for item in resultToList:
            self.assertEqual(item, sampledRecords[i])
            i += 1


if __name__ == "__main__":
    unittest.main()
