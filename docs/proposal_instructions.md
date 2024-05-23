# Instructions for Proposals to Add New HPAI Detections to this repository

## GitHub Proposal Instructions

This repo follows [the open-source proposal model used to designate SARS-CoV-2 lineages](https://github.com/cov-lineages/pango-designation), which involves proposing updates through GitHub issues and pull requests.

For users who are less familiar with git and GitHub, we recommend you fill your results into the [proposal template](../assets/proposal_template.tsv) and open an issue in [the repo's Issues section](https://github.com/dholab/dairy-hpai-monitoring/issues). The maintainers will then review the issue. If your results pass review, they will be added to the proposals branch of the repo, run through our automated tests, and merged into the main branch. Eventually, these new results will be included in an official release.

For users who are familiar with git and open source collaboration, we recommend the following steps to add data our [line list](../DETECTION_RESULTS.tsv):

1. Clone or fork this resository.
2. `git checkout` the proposals branch.
3. Add rows with your results directly to the [line list](../DETECTION_RESULTS.tsv).
4. `git commit` and push your changes to the proposal branch.
5. Open a pull request (PR) to have your proposed additions added to the main branch.

On pull request, a series of automated GitHub workflows will run that validate and normalize your PR, as well as regenerate the formatted README file. If all of these workflows pass, a repo maintainer will review your PR and merge if everything looks right.

## Proposal template file

For ease of use, a template tsv file is provided here: [template file](../assets/proposal_template.tsv).

## Column Descriptions

Required columns are in bold.

**sample** - An identifier for the sample. The sample is what you have tested or sequenced. Multiple samples can come from the same carton (see carton below). Sample names may be re-used only if the primer_asset_file or probe_asset_file values are not the same as the previous instance of that sample name (for samples tested with multiple assays). The sample column should not contain sensitive information about the producer, company, or brand.

**carton** - A de-identified code for each individual unit of dairy product obtained (for example, each milk carton) that may be sampled from multiple times. This code allows multiple sample rows to be linked to the same de-identified starting dairy product unit/carton. DO NOT use any code actually on the product that could be used to identify it. We suggest a naming scheme of `submitter_carton_####`.

**date_purchased** - The date the dairy product was purchased from a vendor or store in the format YYYY-MM-DD. An example is “2024-04-24”.

date_expiration - The expiration date listed (if applicable) on the dairy product in the format YYYY-MM-DD. An example is “2024-03-23”.

assay - The kind of assay used to determine whether a product was positive. Currently, we allow qPCR, dPCR, empty, or NA in this column, but feel free to open a GitHub issue if you'd like us to support additional values.

average_cycle_threshold - The cycle threshold value of the sample in a PCR-based assay. This is the number of cycles performed before a positive signal is detected by the instrument. Format as a number with decimal points. An example is "27.3". If the sample is negative, insert "NA".

average_copies_per_uL - A calculated value of targets per uL of sample extract/isolate added to the assay reaction. This is not intended to be the concentration of the original milk sample. For qPCR, the average_copies_per_uL value should be calculated from the cycle threshold value compared to a standard curve. The copies per reaction value should then be divided by the number of uL of sample extract/isolate that was added to the reaction mix. This value is optional. Round to nearest whole number.

**primer_asset_file** - The name of the file of the primers used in the assay. A file with the same name should be present in the [assets directory](../assets) of this repository. If this is your first time committing with your data you may need to add these files when you commit. The primer file should be a single fasta or bed file with both the forward and reverse primer. If your primers are proprietary, this field can be filled with "redacted" to indicate this. This filename should be unique among files within the repository. An example is "HPAI_primers.fasta".

**probe_asset_file** - The name of the file of the probe used in the assay. A file with the same name should be present in the [assets directory](../assets) of this repository. If your probe is proprietary, this field can be filled with "redacted" to indicate this. This filename should be unique among files within the repository. An example is "HPAI_probe.fasta".

**processing_plant_state** - The state abbreviation of the location of the processing plant. On every dairy product, there is a 2 digit code followed by a dash (-) and another series of numbers (usually 2-3). The first 2 digit code can be used to find the state where the milk was processed. The state should ONLY be included if there are more than 3 processing plants throughout the state so as to protect sensitive information. If the state has 3 or less processing plants (as is the case for AK, AR, GA, LA, MS, ND, SC, and WV), the entry in this column should be “NA”. States should be entered in their abbreviated format. An example entry is “WI” for Wisconsin.

**positive_for_HPAI** - This column should be populated with TRUE or FALSE depending on whether the sample tested positive for influenza based on the primers used.

SRA_bioproject - The bioproject to which the sequences were uploaded in SRA, if sequences have been uploaded.

SRA_accession - The accession number of the uploaded sequence in SRA, if sequences have been uploaded.

**contributors** - The names of those contributing this data. This should be a string.

**date_contributed** - The date of the pull request. This should be in the format of YYYY-MM-DD.

RNA_extraction_method - A general description of the method used to extract the RNA. This field is optional.
