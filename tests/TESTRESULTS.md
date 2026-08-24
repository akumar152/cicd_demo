# Assignment Test Result


## 1. Test check-ingestion
```bash
poetry run exercise check-ingestion
```

```text
============================================= test session starts =============================================
platform linux -- Python 3.11.16, pytest-7.3.1, pluggy-1.0.0
rootdir: /home/dataeng
configfile: setup.cfg
plugins: cov-4.1.0
collected 3 items                                                                                             

tests/exercise_tests/test_ingestion.py ...                                                              [100%]

============================================== 3 passed in 0.28s ==============================================
```
## 2. Test check-outliers

```bash
poetry run exercise check-outliers
```

```text
============================================= test session starts =============================================
platform linux -- Python 3.11.16, pytest-7.3.1, pluggy-1.0.0
rootdir: /home/dataeng
configfile: setup.cfg
plugins: cov-4.1.0
collected 2 items                                                                                             

tests/exercise_tests/test_outliers.py ..                                                                [100%]

============================================== 2 passed in 0.14s ==============================================
```

## 3. Test detect-outliers

```bash
poetry run exercise detect-outliers
```

```text
┌───────┬────────────┬───────────┐
│ Year  │ WeekNumber │ VoteCount │
│ int64 │   int32    │   int64   │
├───────┼────────────┼───────────┤
│  2017 │          8 │      1422 │
│  2017 │          9 │      1102 │
│  2017 │         10 │       454 │
│  2017 │         11 │       425 │
│  2017 │         12 │       485 │
│  2017 │         13 │       417 │
│  2017 │         14 │       304 │
│  2017 │         15 │       410 │
│  2017 │         16 │       323 │
│  2017 │         18 │       131 │
│    ·  │          · │        ·  │
│    ·  │          · │        ·  │
│    ·  │          · │        ·  │
│  2021 │         24 │       244 │
│  2021 │         25 │        56 │
│  2021 │         26 │       239 │
│  2021 │         27 │       134 │
│  2021 │         28 │        78 │
│  2021 │         30 │        55 │
│  2021 │         31 │       110 │
│  2021 │         32 │       109 │
│  2021 │         33 │        91 │
│  2021 │         34 │       130 │
├───────┴────────────┴───────────┤
│ 166 rows (20 shown)  3 columns │
└────────────────────────────────┘
```

## 4. test custom outliers_test

```bash
poetry run pytest tests/outliers_test.py
```

```text
platform linux -- Python 3.11.16, pytest-7.3.1, pluggy-1.0.0
rootdir: /home/dataeng
configfile: setup.cfg
plugins: cov-4.1.0
collected 1 item                                                                                              

tests/outliers_test.py .                                                                                [100%]

============================================== 1 passed in 0.03s ==============================================
```

## 5. Test custom ingest_test

```bash
poetry run pytest tests/ingest_test.py 
```

```text
============================================= test session starts =============================================
platform linux -- Python 3.11.16, pytest-7.3.1, pluggy-1.0.0
rootdir: /home/dataeng
configfile: setup.cfg
plugins: cov-4.1.0
collected 3 items                                                                                             

tests/ingest_test.py ...                                                                                [100%]

============================================== 3 passed in 0.07s ==============================================
```

## 6. Test db_test

```bash
poetry run pytest tests/db_test.py 
```

```text
============================================= test session starts =============================================
platform linux -- Python 3.11.16, pytest-7.3.1, pluggy-1.0.0
rootdir: /home/dataeng
configfile: setup.cfg
plugins: cov-4.1.0
collected 1 item                                                                                              

tests/db_test.py .                                                                                      [100%]

============================================== 1 passed in 0.02s ==============================================
```