# Project documentation files

This file is the entrypoint for the project's documentation files that live
outside of pure functionality specification. It lists each file and what their
contents and purpose are.

## Dataset Croissant

**File:** [GermanCreditCroissant.json]

The file contains a complete description of the project's dataset as a
standardized JSON file. A full description of this file can be found in the
[Croissant's specification page], and here we will keep the discussion focused
on the entries used directly by the code or that provide relevant context about
the data.

* `distribution`: here we find the URL to download the Parquet file directly
  from the internet. The full path is `distribution.contentUrl`. It also has
  a MD5 checksum to verify file integrity: `distribution.md5`.
* `recordSet`: here we find information about each column in the dataset. It
  is a list of objects, where each object represents a column. The entry
  `name` inside each object identifies each column by their name in the data
  file. The `description` gives a text definition of the information the column
  is representing.

## Dataset schema

**File:** [GermanCreditSchema.md]

This file contains a complete description of all columns contained in the
dataset, along with some auxiliary columns created in the project. The file thus
serves as a data dictionary for the project and frequent consultation is
recommended for it.

## Hypotheses

**File:** [Hypotheses.md]

This file lists and briefly describes each hypothesis proposed for the project,
alongside a marker about whether they were falsified or not and the evidence
for their falsification.

[GermanCreditCroissant.json]: GermanCreditCroissant.json
[Croissant's specification page]: https://docs.mlcommons.org/croissant/docs/croissant-spec-1.1.html
[GermanCreditSchema.md]: GermanCreditSchema.md
[Hypotheses.md]: Hypotheses.md
