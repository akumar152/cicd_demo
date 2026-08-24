# Data Engineering Exercise Notes

This folder contains the ingestion and outlier-detection logic for the exercise.

## Ingestion

The ingestion entry point is:

- `equalexperts_dataeng_exercise.ingest`

Run it with:

```bash
poetry run exercise ingest-data
```

## Testing

```bash
poetry run exercise check-ingestion
```

**What it does**
1. Creates the blog_analysis schema if it does not already exist.
2. Creates the blog_analysis.votes table if it does not already exist.
3. Loads the source JSONL file into a temporary staging table.
4. Performs an incremental upsert into blog_analysis.votes using Id as the primary key.
5. New records are inserted, while existing records with the same Id are updated.

## **Design Decisions**

### Incremental Upsert

`Id` is used as the unique key for each vote.  
`INSERT ... ON CONFLICT (Id) DO UPDATE` is used so that new records are inserted and existing records are updated.

This makes the ingestion idempotent and prevents duplicate records when the same data is processed multiple times.

### Temporary Staging Table

The incoming JSONL data is first loaded into a temporary table before being written to the target table. This keeps the source data separate from the final analytics table and allows the data to be transformed before loading.



### **Outlier detection**

The outlier entry point is:

- `equalexperts_dataeng_exercise.outliers`

Run it with:

```bash
poetry run exercise detect-outliers
```
Testing:

```bash
poetry run exercise check-outliers
```


**What it does:**
1. Creates or replaces the blog_analysis.outlier_weeks view.
2. Aggregates vote counts by year and week from blog_analysis.votes.
3. Calculates the average weekly vote count across the complete dataset.
4. Identifies outlier weeks using the required formula:
    ABS(1 - VoteCount / AverageVoteCount) > 0.2
5. Returns only the outlier weeks, ordered by year and week number.



**DB Test:**

```bash
poetry run pytest tests/db_test.py 
```








