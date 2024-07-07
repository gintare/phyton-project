This project is written in Python language, it implements rules:
- Each type of measurement is sampled separately
- From a 5-minute interval only the last measurement is taken
- If a measurement timestamp will exactly match a 5-minute interval border, it is used for
the current interval
- The input values are not sorted by time
- The output is sorted by time ascending
