from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

INTERVAL_IN_MINUTES = 5


class MeasType(Enum):
    SPO2 = 1
    HR = 2
    TEMP = 3

    @staticmethod
    def from_str(label):
        if label == 'SPO2':
            return MeasType.SPO2
        elif label == 'HR':
            return MeasType.HR
        elif label == 'TEMP':
            return MeasType.TEMP
        else:
            raise NotImplementedError


@dataclass
class Measurement:
    measurementTime: datetime = datetime.min
    measurementType: MeasType = MeasType.SPO2
    value: float = 0.0


def parseLine(line: str) -> Measurement:
    strippedString = line.strip("{").strip()
    strippedString = strippedString[:-1]
    parts = strippedString.strip().split(',')
    date = datetime.strptime(parts[0], "%Y-%m-%dT%H:%M:%S")
    measType = MeasType.from_str(parts[1].strip())
    value = float(parts[2].strip())
    return Measurement(measurementTime=date, measurementType=measType, value=value)


def readFileToDataclass(filename: str) -> list[Measurement]:
    records = []
    with open(filename, 'r') as file:
        for line in file:
            parseLine(line)
            record = parseLine(line)
            records.append(record)
    return records


def listByMeasurementType(measurementType: MeasType,
                          unsampledMeasurements: list[Measurement]) -> list[Measurement]:
    sampledList = []
    for unsMeas in unsampledMeasurements:
        if unsMeas.measurementType == measurementType:
            sampledList.append(unsMeas)
    sampledList.sort(key=lambda measure: measure.measurementTime)
    return sampledList


def dictByMeasurementType(unsampledMeasurements: list[Measurement]) -> dict[MeasType, list[Measurement]]:
    sampledMeasurements = {}
    listByMeasType = listByMeasurementType(MeasType.TEMP, unsampledMeasurements)
    sampledMeasurements.update({MeasType.TEMP: listByMeasType})
    listByMeasType = listByMeasurementType(MeasType.SPO2, unsampledMeasurements)
    sampledMeasurements.update({MeasType.SPO2: listByMeasType})
    listByMeasType = listByMeasurementType(MeasType.HR, unsampledMeasurements)
    sampledMeasurements.update({MeasType.HR: listByMeasType})
    return sampledMeasurements


def listByDateMeasurements(startOfSamplingDate: datetime,
                           listByMeasType: list[Measurement]) -> list[Measurement]:
    start = startOfSamplingDate
    listByDate = []
    prev = None
    if len(listByMeasType) > 0:
        prev = listByMeasType[0]
    for unsMeas in listByMeasType:
        measurementAdded = False
        if unsMeas.measurementTime > start:
            mes = Measurement(start, prev.measurementType, prev.value)
            listByDate.append(mes)
            timeDelta = timedelta(days=0, hours=0, minutes=INTERVAL_IN_MINUTES)
            start = start + timeDelta
        elif unsMeas.measurementTime == start:
            mes = Measurement(start, unsMeas.measurementType, unsMeas.value)
            listByDate.append(mes)
            timeDelta = timedelta(days=0, hours=0, minutes=INTERVAL_IN_MINUTES)
            start = start + timeDelta
            measurementAdded = True
        if unsMeas == listByMeasType[-1] and not measurementAdded:
            mes = Measurement(start, unsMeas.measurementType, unsMeas.value)
            listByDate.append(mes)
        prev = unsMeas
    return listByDate


def correctStartOfSamplingDate(startOfSampling: datetime) -> datetime:
    startMinute = (int(startOfSampling.minute / INTERVAL_IN_MINUTES) + 1) * INTERVAL_IN_MINUTES
    if startOfSampling.minute % INTERVAL_IN_MINUTES == 0:
        startMinute = int(startOfSampling.minute / INTERVAL_IN_MINUTES) * INTERVAL_IN_MINUTES
    startOfSampling = startOfSampling.replace(minute=startMinute, second=0, microsecond=0)
    return startOfSampling


def sampleMeasurements(startOfSampling: datetime,
                       unsampledMeasurements: list[Measurement]) -> dict[MeasType, list[Measurement]]:
    sampledMeasurements = dictByMeasurementType(unsampledMeasurements)
    startOfSampling = correctStartOfSamplingDate(startOfSampling)

    for key, value in sampledMeasurements.items():
        listByDate = listByDateMeasurements(startOfSampling, sampledMeasurements[key])
        sampledMeasurements.update({key: listByDate})

    return sampledMeasurements


def main():
    filename = 'unsampled_measurements_test.txt'
    records = readFileToDataclass(filename)
    records.sort(key=lambda measure: measure.measurementTime)
    measurementStartDate = records[0].measurementTime
    result = sampleMeasurements(startOfSampling=measurementStartDate, unsampledMeasurements=records)
    print(result)


if __name__ == "__main__":
    main()
