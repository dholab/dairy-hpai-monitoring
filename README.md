# Real-Time Monitoring of HPAI Detections in Dairy Products in the United States

[![Still Validation](https://github.com/dholab/dairy-hpai-monitoring/actions/workflows/validate.yml/badge.svg)](https://github.com/dholab/dairy-hpai-monitoring/actions/workflows/validate.yml)

HPAI (highly-pathogenic avian influenza) RNA has been detected in consumer dairy products in the United States. Many labs around the country have been using these products to monitor the extent of the ongoing H5N1 outbreak in dairy cattle. Due to the dual threat this outbreak poses to public health and industry, it is imperative that HPAI positivity data for dairy products is shared in both a transparent and responsible manner. The purpose of this repository is to gather and make available dairy product HPAI PCR and sequencing data to coordinate monitoring efforts while also setting a standard for sensitive metadata stewardship.

To submit results of your own, read over our [proposal instructions](docs/proposal_instructions.md) and then open [a new issue](https://github.com/dholab/dairy-hpai-monitoring/issues/new).

## Table of Contents

- [Real-Time Monitoring of HPAI Detections in Dairy Products in the United States](#real-time-monitoring-of-hpai-detections-in-dairy-products-in-the-united-states)
  - [Table of Contents](#table-of-contents)
  - [Positivity Tally by State](#positivity-tally-by-state)
  - [Sampling Dairy Products for HPAI RNA](#sampling-dairy-products-for-hpai-rna)
    - [Extracting HPAI RNA from Dairy Products](#extracting-hpai-rna-from-dairy-products)
      - [Milk and Cream](#milk-and-cream)
    - [Quantifying and Sequencing HPAI RNA from Dairy Products](#quantifying-and-sequencing-hpai-rna-from-dairy-products)
  - [Metadata Stewardship](#metadata-stewardship)
    - [Geolocation Data](#geolocation-data)
    - [Naming Conventions](#naming-conventions)
  - [Data Submission](#data-submission)

## Recent Results by State

Recent results in the 90 days preceding 31 January 2025

Processing Plant State  |  Total Cartons  |  Negative Cartons  |  Positive Cartons  |  Latest Date Sampled
------------------------|-----------------|--------------------|--------------------|---------------------
CA                      |  6              |  1                 |  5                 |  2025-01-21
CO                      |  5              |  5                 |  0                 |  2025-01-21
IA                      |  2              |  1                 |  1                 |  2024-12-17
IN                      |  1              |  1                 |  0                 |  2024-12-17
MI                      |  7              |  7                 |  0                 |  2025-01-21
MN                      |  1              |  1                 |  0                 |  2024-11-19
MO                      |  1              |  1                 |  0                 |  2024-12-17
WI                      |  72             |  63                |  9                 |  2025-01-21

## All-time Results by State

Full results across the history of the project (24 April 2024-Present)

Processing Plant State  |  Total Cartons  |  Negative Cartons  |  Positive Cartons  |  Latest Date Sampled
------------------------|-----------------|--------------------|--------------------|---------------------
CA                      |  9              |  4                 |  5                 |  2025-01-21
CO                      |  19             |  11                |  9                 |  2025-01-21
FL                      |  1              |  1                 |  0                 |  2024-05-20
IA                      |  12             |  11                |  1                 |  2024-12-17
ID                      |  1              |  1                 |  0                 |  2024-05-20
IL                      |  3              |  3                 |  0                 |  2024-06-17
IN                      |  7              |  6                 |  1                 |  2024-12-17
KS                      |  2              |  2                 |  0                 |  2024-07-02
KY                      |  4              |  3                 |  1                 |  2024-07-02
MI                      |  27             |  12                |  16                |  2025-01-21
MN                      |  7              |  7                 |  0                 |  2024-11-19
MO                      |  4              |  3                 |  1                 |  2024-12-17
NC                      |  2              |  2                 |  0                 |  2024-09-24
NY                      |  5              |  4                 |  1                 |  2024-09-24
OH                      |  3              |  3                 |  0                 |  2024-07-28
OR                      |  1              |  1                 |  0                 |  2024-05-20
TX                      |  2              |  1                 |  1                 |  2024-06-05
UT                      |  1              |  1                 |  0                 |  2024-05-02
VA                      |  2              |  2                 |  0                 |  2024-07-02
WI                      |  192            |  172               |  20                |  2025-01-21

## Sampling Dairy Products for HPAI RNA

Dairy products can be easily obtained from grocery stores and/or other vendors. All dairy products registered on the [FDA Interstate Milk Shippers List](https://www.fda.gov/food/federalstate-food-programs/interstate-milk-shippers-list#rules) have an Interstate Milk Shippers (IMS) code that can be used to trace each unit back to the dairy plant where it was processed. IMS codes consist of a two letter state code and a four letter plant code separated by a hyphen. This code, used in tandem with the website [whereismymilkfrom.com](https://www.whereismymilkfrom.com), can help inform sampling strategy. While IMS codes identify the exact locations of specific dairy processing plants, it is mandatory that only state-level information is shared on this repository (see Metadata Stewardship).

This repository is intended for dairy samples only. Other sample types are outside the scope of this project.

### Extracting HPAI RNA from Dairy Products

#### Milk and Cream

We have published an HPAI RNA extraction protocol tested on milk and cream on protocols.io: [protocol](https://www.protocols.io/view/rna-extraction-from-milk-for-hpai-surveillance-dczp2x5n.html)

### Quantifying and Sequencing HPAI RNA from Dairy Products

We have published an HPAI 250bp tiled amplicon sequencing protocol compatible with Oxford Nanopore and Illumina sequencing platforms on protocols.io: [protocol](https://www.protocols.io/view/whole-genome-sequencing-of-h5n1-from-dairy-product-dev43e8w.html)

## Metadata Stewardship

This repository aims to share information about broad trends in HPAI across the US milk supply, not to investigate individual plants, brands, or farms. Please keep this aim in mind as you name your samples. Any pull requests that include geographic information at a level below state, plant IDs, or brand abbreviations will not be approved.

### Geolocation Data

Because the following states have less than three dairy processing plants, to avoid identifying individual plants please replace the following states with “NA” in the “processing_plant_state” column: AK, AR, GA, LA, MS, ND, SC, WV. Again, do not include ANY sample geolocation information below state level in any submission column.

### Naming Conventions

In the “sample” column, "carton" column, or any other column, DO NOT include:

-   Geolocation information below state level (or state level info from one of the states specifically mentioned under Geolocation Data)
-   Any reference to the brand of dairy product tested
-   Any reference to the type of dairy product tested (this is to protect dairy producers that may be the only location in their state to process a specific product)
-   Any code (such as the IMS code) that can be used to identify a specific brand, product, or location

## Data Submission

We invite any labs able to test dairy products for HPAI and willing to abide by our metadata standards to submit their PCR and sequencing data to this repository. Further information on how to submit your data can be found in the [proposal_instructions.md](docs/proposal_instructions.md).
