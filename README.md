## :warning: Please read these instructions carefully and entirely first
* Clone this repository to your local machine.
* Use your IDE of choice to complete the assignment.
* When you have completed the assignment, you need to  push your code to this repository and [mark the assignment as completed by clicking here](https://app.snapcode.review/submission_links/5a2a2dda-90ce-4c5d-9a79-b48a5dc89ba4).
* Once you mark it as completed, your access to this repository will be revoked. Please make sure that you have completed the assignment and pushed all code from your local machine to this repository before you click the link.

**Table of Contents**
1. [Before you start](#before-you-start), a brief explanation for the exercise and software prerequisites/setup.  
2. [Tips for what we are looking for](#tips-on-what-were-looking-for) provides clear guidance on solution qualities we value 
3. [The Challenge](#begin-the-two-part-challenge) explains the data engineering code challenge to be tackled.
4. [Follow-up Questions](#follow-up-questions) related to the challenge which you should address  
5. [Your approach and answers to follow-up questions](#your-approach-and-answers-to-follow-up-questions-) is where you should include the answers to the follow-up question and clarify your solution approach any assumptions you have made.

## Before you start
### Why complete this task?

We want to make the interview process as simple and stress-free as possible. That’s why we ask you to complete 
the first stage of the process from the comfort of your own home.

Your submission will help us to learn about your skills and approach. If we think you’re a good fit for our 
network, we’ll use your submission in the next interview stages too.

### About the task

You’ll be creating an ingestion process to ingest files containing vote data. You’ll also create a means to 
query the ingested data to determine outlier weeks.

There’s no time limit for this task, but we expect it to take less than 2 hours.

### Setup Instructions

For instructions on how to set up and run the exercise, please see [SETUP.md](SETUP.md).

### Tips on what we’re looking for


* ✅  **Test coverage**

    Demonstrate your ability to write well-structured tests that verify behavior, not just execute code for coverage.

* ✅  **Self-contained tests**

    Your tests should be self-contained, with no dependency on being run in a specific order.

* ✅  **Simplicity**

    We value simplicity as an architectural virtue and a development practice. Solutions should reflect the difficulty of the assigned task, and shouldn’t be overly complex. We prefer simple, well tested solutions over clever solutions. 

    Please avoid:

   * ❌ unnecessary layers of abstraction
   * ❌ patterns
   * ❌ custom test frameworks
   * ❌ architectural features that aren’t called for
   * ❌ libraries like **pandas** or **polars** or frameworks like **PySpark** or **ballista**
  
     We know that this exercise can be
     solved fairly trivially using these libraries and a Dataframe approach, and we'd encourage appropriate 
     use of these in daily work contexts. But for this small exercise we really 
     want to know more about how you structure, write and test your Python code,
     and want you to show some fluency in SQL -- a **pandas**
     solution won't allow us to see much of that.

* ✅  **Self-explanatory code**

    The solution you produce must speak for itself. Multiple paragraphs explaining the solution is a sign 
    that the code isn’t straightforward enough to understand on its own.
    However, please do explain your non-obvious _choices_ e.g. perhaps why you decided to load
    data a specific way.

* ✅ **Demonstrate fluency with data engineering concepts**
   
   Even though this is a toy exercise, treat DuckDB as you would an OLAP 
   data warehouse. Choose datatypes, data loading methods, optimisations and data models that 
   are suited for resilient analytics processing at scale, not transaction processing.

* ✅ **Dealing with ambiguity**

    If there’s any ambiguity, please add this in a section at the bottom of the README. 
    You should also make a choice to resolve the ambiguity and proceed.

Our review process starts with a very simplistic test set in the `tests/exercise_tests` folder which you should also
check before submission. You can run these with:
```shell
poetry run exercise check-ingestion
poetry run exercise check-outliers
```

Expect these to fail until you have completed the exercise.

You should not change the `tests/exercise-tests` folder and your solution should be able to pass both tests.


## Download the dataset for the exercise
Run the command
```
poetry run exercise fetch-data
```

which will fetch the dataset, uncompress it and place it in `uncommitted/votes.jsonl` for you.
Explore the data to see what values and fields it contains (no need to show how you explored it).

## Begin the two-part challenge
There are two parts to the exercise, and you are expected to complete both. 
A user should be able to execute each task independently of the other. 
For example, ingestion shouldn't cause the outliers query to be executed.

### Part 1: Ingestion

Create a schema called `blog_analysis`.
Create an on-demand ingestion process that can handle incremental loads from files containing vote data. The process should be designed to run multiple times and must handle:
- **New records**: Insert records that don't exist in the target table
- **Updated records**: Reflect changes when a record with the same ID has different values

You should ensure that data scientists, who will be consumers of the data, do not need to consider duplicate records in their queries. The data should be stored in a table called `votes` in the `blog_analysis` schema.

### Part 2: Outliers calculation
Create a view named `outlier_weeks`  in the `blog_analysis` schema. It will contain the output of a SQL calculation for which weeks are regarded as outliers based on the vote data that was ingested.
The view should contain the year, week number and the number of votes for the week _for only those weeks which are determined to be outliers_, according to the following rule:

NB! If you're viewing this Markdown document in a viewer
where the math isn't rendering, try viewing this README in GitHub on your web browser, or [see this pdf](docs/calculating_outliers.pdf).

> 
> **A week is classified as an outlier when the total votes for the week deviate from the average votes per week for the complete dataset by more than 20%.**</br>  
> For the avoidance of doubt, _please use the following formula_: 
>  
> > Say the mean votes is given by $\bar{x}$ and this specific week's votes is given by $x_i$. 
> > We want to know when $x_i$ differs from $\bar{x}$ by more than $20$%. 
> > When this is true, then the ratio $\frac{x_i}{\bar{x}}$ must be further from $1$ by more than $0.2$, i.e.: </br></br> 
> > $\big|1 - \frac{x_i}{\bar{x}}\big| > 0.2$

The data should be sorted in the view by year and week number, with the earliest week first.

Running `outliers.py` should recreate the view and 
just print the contents of this `outlier_weeks` view to the terminal - don't do any more calculations after creating the view.

## Example

The sample dataset below is included in the test-resources folder and can be used when creating your tests.

Assuming a file is ingested containing the following entries:

```
{"Id":"1","PostId":"1","VoteTypeId":"2","CreationDate":"2022-01-02T00:00:00.000"}
{"Id":"2","PostId":"1","VoteTypeId":"2","CreationDate":"2022-01-09T00:00:00.000"}
{"Id":"4","PostId":"1","VoteTypeId":"2","CreationDate":"2022-01-09T00:00:00.000"}
{"Id":"5","PostId":"1","VoteTypeId":"2","CreationDate":"2022-01-09T00:00:00.000"}
{"Id":"6","PostId":"5","VoteTypeId":"3","CreationDate":"2022-01-16T00:00:00.000"}
{"Id":"7","PostId":"3","VoteTypeId":"2","CreationDate":"2022-01-16T00:00:00.000"}
{"Id":"8","PostId":"4","VoteTypeId":"2","CreationDate":"2022-01-16T00:00:00.000"}
{"Id":"9","PostId":"2","VoteTypeId":"2","CreationDate":"2022-01-23T00:00:00.000"}
{"Id":"10","PostId":"2","VoteTypeId":"2","CreationDate":"2022-01-23T00:00:00.000"}
{"Id":"11","PostId":"1","VoteTypeId":"2","CreationDate":"2022-01-30T00:00:00.000"}
{"Id":"12","PostId":"5","VoteTypeId":"2","CreationDate":"2022-01-30T00:00:00.000"}
{"Id":"13","PostId":"8","VoteTypeId":"2","CreationDate":"2022-02-06T00:00:00.000"}
{"Id":"14","PostId":"13","VoteTypeId":"3","CreationDate":"2022-02-13T00:00:00.000"}
{"Id":"15","PostId":"13","VoteTypeId":"3","CreationDate":"2022-02-20T00:00:00.000"}
{"Id":"16","PostId":"11","VoteTypeId":"2","CreationDate":"2022-02-20T00:00:00.000"}
{"Id":"17","PostId":"3","VoteTypeId":"3","CreationDate":"2022-02-27T00:00:00.000"}
```

Then the following should be the content of your `outlier_weeks` view:


| Year | WeekNumber | VoteCount |
|------|------------|-----------|
| 2022 | 0          | 1         |
| 2022 | 1          | 3         |
| 2022 | 2          | 3         |
| 2022 | 5          | 1         |
| 2022 | 6          | 1         |
| 2022 | 8          | 1         |

**Note that we strongly encourage you to use this data as a test case to ensure that you have the correct calculation!**

## Follow-up Questions

Please include instructions about your strategy and important decisions you made in the README file. You should also include answers to the following questions, please make sure these are answered without the use AI tools as we would like to understand your thought process:

1. What kind of data quality measures would you apply to your solution in production?
2. What would need to change for the solution scale to work with a 10TB dataset with 5GB new data arriving each day?
3. Please tell us in your modified README about any assumptions you have made in your solution (below).


## Your Approach and answers to follow-up questions 

My approach was to keep the solution intentionally small and SQL-native, matching the exercise scope and the evaluation rubric. 
### Incremental Upsert

`Id` is used as the unique key for each vote.  
`INSERT ... ON CONFLICT (Id) DO UPDATE` is used so that new records are inserted and existing records are updated.

This makes the ingestion idempotent and prevents duplicate records when the same data is processed multiple times.

### Temporary Staging Table

The incoming JSONL data is first loaded into a temporary table before being written to the target table. This keeps the source data separate from the final analytics table and allows the data to be transformed before loading.

## Outlier detection
 The outlier calculation is then implemented as a SQL view over the ingested data, grouping by year and week and filtering on the percentage-difference rule in the README.


 ### Test Coverage

1. The ingestion tests verify:
    • initial data loading
    • insertion of new records
    • updating of existing records
    • prevention of duplicate records
    • idempotent ingestion

2. The outlier test uses known sample data and verifies that the `outlier_weeks` view produces the expected outlier weeks and vote counts.

# 1. Data quality measures I would apply in production

The most important checks for this pipeline would be schema validation, null and uniqueness checks on Id, duplicate detection, record-count reconciliation, and monitoring for failed or rejected records.
    • Row count reconciliation
    • Data reconciliation (validation)
    • Schema and record validation
    • Validate each JSON line against a strict JSON Schema (Id, PostId, VoteTypeId, CreationDate types and required fields)
    • Null checks
    • Timeliness
    • Data Type checks
    • Deduplication & idempotency
    • Quarantine and error handling
    • Proper audit columns
    • View and analytic checks (outliers)
    • Negative scanerio(bad records/wrong datatype)
    • schema evolution(strict/allowed based on buisness requirement)

# 2. What would need to change for a 10TB dataset with 5GB new data arriving each day?

### 2. What would need to change for the solution to scale to a 10TB dataset with 5GB new data arriving each day?

The current solution uses DuckDB and is suitable for the exercise, but I would change the architecture for a 10TB dataset.
    • **Storage** – Store the raw and curated data in scalable object storage such as S3 or ADLS rather than relying on a local DuckDB database file.
    • **File format** – Store the data in Parquet because it is columnar and supports efficient analytical reads.
    • **Incremental processing** – Process only the new 5GB of data each day instead of scanning the complete 10TB dataset.
    • **Distributed processing** – Use a distributed processing engine such as Spark when the data volume or transformation complexity requires it.
    • **Partitioning** – Partition the data by an appropriate date column, such as `CreationDate`, to reduce the amount of data scanned.
    • **Upserts** – Use a scalable table format such as Delta Lake to efficiently handle inserts and updates rather than repeatedly rewriting
        large portions of the dataset.
    • **Data quality** – Run validation checks on each incremental batch and quarantine invalid records.
    • **Monitoring** – Track records received, inserted, updated, rejected records, processing time, and failures.
    • **Idempotency and recovery** – Maintain checkpoints or processing metadata so that a failed daily load can be safely retried without creating
        duplicates.

# 3. Assumptions made in this solution

The following assumptions were made for this solution:
    • `Id` uniquely identifies a vote and is therefore used as the key for upserts.
    • The input file is a JSONL file containing `Id`, `PostId`, `VoteTypeId`, and `CreationDate`.
    • `CreationDate` is a valid timestamp and is used to determine the year and week of a vote.
    • A week is considered an outlier when it differs from the average weekly vote count by more than 20%, using the formula specified in the exercise.
    • The week numbering follows the Sunday-based numbering required by the provided test data.
    • Invalid or malformed source records are outside the scope of this exercise and would be handled through data-quality validation in a production
      implementation.


## AI Tool Usage

While we encourage the use of AI tools as part of the learning process but to ensure transparency, please provide the following information regarding the use of AI tools in this submission:

1.  **Specific Use Cases:** Describe for what purposes tool was used (e.g., code generation, debugging assistance, query generation etc.).
2.  **Percentage of Code Generated by AI:** Provide an estimate of the percentage of the submitted code that was generated by AI.
3.  **How AI-Generated Code Was Reviewed:** Explain how you reviewed and verified the AI-generated code to ensure its correctness and quality.

Please note, during the technical interview, which will build upon this exercise, we'll focus on your coding abilities and problem-solving skills without the use of AI tools. This will allow us to see your direct approach and thought process.


## AI Tool Usage: I used copilot for this assignment. 

1. ***Specific Use Cases**
    • I used copilot for rephrasing README file.
    • i used copilot for duckDB syntax and useage as it is new to me.
    • I used copilot for debugging assistance.
    
2. ***Percentage of Code Generated by AI:** I would say 20% (mainly for duckDB usage)
3. ***How AI-Generated Code Was Reviewed:** Manually and Also by running tests