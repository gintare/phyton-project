import unittest
import measurements
from datetime import datetime

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'


def mapDictResultToList(result: dict[measurements.MeasType,
                        list[measurements.Measurement]]) -> list[measurements.Measurement]:
    resultToList = []
    for key, value in result.items():
        temp = [key, value]
        for item in value:
            resultToList.append(item)
    return resultToList


def getListByMeasurements() -> list[measurements.Measurement]:
    measurementTime = datetime.strptime('2024-07-07T12:06:20', DATETIME_FORMAT)
    measurementTime1 = datetime.strptime('2024-07-07T12:07:20', DATETIME_FORMAT)
    measurementTime2 = datetime.strptime('2024-07-07T12:08:20', DATETIME_FORMAT)
    listByMeasurements = [measurements.Measurement(measurementTime=measurementTime,
                                                   measurementType=measurements.MeasType.SPO2,
                                                   value=1),
                          measurements.Measurement(measurementTime=measurementTime1,
                                                   measurementType=measurements.MeasType.SPO2,
                                                   value=2),
                          measurements.Measurement(measurementTime=measurementTime2,
                                                   measurementType=measurements.MeasType.TEMP,
                                                   value=3),
                          ]
    return listByMeasurements


class MeasurementTest(unittest.TestCase):

    def test_parseLine(self):
        measurement = measurements.parseLine('{2017-01-03T10:04:45, HR, 35.79}')
        self.assertEqual(measurement.measurementTime, datetime.strptime('2017-01-03T10:04:45', DATETIME_FORMAT))
        self.assertEqual(measurement.measurementType, measurements.MeasType.HR)
        self.assertEqual(measurement.value, 35.79)

    def test_readFileToDataclass(self):
        listLines = measurements.readFileToDataclass("unsampled_measurements_test.txt")
        self.assertGreater(len(listLines), 1)

    def test_listByMeasurementType(self):
        listByMeasType = measurements.listByMeasurementType(measurements.MeasType.SPO2, getListByMeasurements())
        self.assertEqual(len(listByMeasType), 2)
        self.assertEqual(listByMeasType[0].measurementTime, datetime.strptime('2024-07-07T12:06:20', DATETIME_FORMAT))
        self.assertEqual(listByMeasType[0].measurementType, measurements.MeasType.SPO2)
        self.assertEqual(listByMeasType[0].value, 1)
        self.assertEqual(listByMeasType[1].measurementTime, datetime.strptime('2024-07-07T12:07:20', DATETIME_FORMAT))
        self.assertEqual(listByMeasType[1].measurementType, measurements.MeasType.SPO2)
        self.assertEqual(listByMeasType[1].value, 2)

    def test_dictByMeasurementType(self):
        dictByMeas = measurements.dictByMeasurementType(getListByMeasurements())
        self.assertEqual(len(dictByMeas), 3)
        self.assertEqual(len(dictByMeas[measurements.MeasType.SPO2]), 2)
        self.assertEqual(len(dictByMeas[measurements.MeasType.TEMP]), 1)
        self.assertEqual(len(dictByMeas[measurements.MeasType.HR]), 0)

    def test_listByDateMeasurements(self):
        startDate = datetime.strptime('2024-07-07T12:10:00', DATETIME_FORMAT)
        measurementTime = datetime.strptime('2024-07-07T12:06:20', DATETIME_FORMAT)
        measurementTime1 = datetime.strptime('2024-07-07T12:07:20', DATETIME_FORMAT)
        listByMeasurements = [measurements.Measurement(measurementTime=measurementTime,
                                                       measurementType=measurements.MeasType.SPO2,
                                                       value=1),
                              measurements.Measurement(measurementTime=measurementTime1,
                                                       measurementType=measurements.MeasType.SPO2,
                                                       value=2),
                              ]
        dateList = measurements.listByDateMeasurements(startDate, listByMeasurements)
        self.assertEqual(len(dateList), 1)
        self.assertEqual(dateList[0].measurementTime, startDate)
        self.assertEqual(dateList[0].measurementType, measurements.MeasType.SPO2)
        self.assertEqual(dateList[0].value, 2)

    def test_correctStartOfSamplingDate(self):
        startOfSamplingDate = datetime.strptime('2024-07-07T12:06:20', DATETIME_FORMAT)
        correctedDate = measurements.correctStartOfSamplingDate(startOfSamplingDate)
        self.assertEqual(datetime.strptime('2024-07-07T12:10:00', DATETIME_FORMAT), correctedDate)
        pass

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
