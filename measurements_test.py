import unittest
import measurements
from datetime import datetime


# def parseLine(line: str) -> measurements.Measurement:
#     stripped_string = line.strip("{").strip()
#     stripped_string1 = stripped_string[:-1]
#     parts = stripped_string1.strip().split(',')
#     date = datetime.strptime(parts[0], "%Y-%m-%dT%H:%M:%S")
#     measType = measurements.MeasType.from_str(parts[1].strip())
#     value = float(parts[2].strip())
#     return measurements.Measurement(measurementTime=date, measurementType=measType, value=value)
#
#
# def readFileToDataclass(filename: str) -> list[measurements.Measurement]:
#     records = []
#     with open(filename, 'r') as file:
#         for line in file:
#             parseLine(line)
#             record = parseLine(line)
#             records.append(record)
#     return records


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
