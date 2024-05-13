# Instructions for Proposals to Add New HPAI Detections to this repository

## Proposal template file

For ease of use, a template tsv file is provided at here.

## Column Descriptions

Required columns are in bold.

**sample** - An identifier for the sample. This should contain no sensitive information about the producer, company, or brand. When combined with the replicate, it must form a unique value in the table. For example, a lab could sample milk from store 1 ("MILK1") and milk from store 2 ("MILK2"). These are different products, therefore different samples.  

**replicate** - A number assigned to each sample to differentiate between replicates of the same dairy sample. Each replicate number will have three digits (XXX) and the first replicate should start with 001 and each following replicate should increase by 1 (002, 003, etc.) For example, a lab may run qPCR on a sample of milk ("MILK1"). Later, the same lab may run a qPCR using different primers on the same sample ("MILK1"). The new qPCR assay on the old sample would receive a replicate number of "002". Note - we are not collecting within experiment replicates. Please report an average cycle threshold value and only use the replicate column when the same sample has undergone multiple separate assays.

**date_purchased** - The date the dairy product was purchased from a vendor or store in the format YYYY-MM-DD. An example is “2024-04-24”.

date_expiration - The expiration date listed (if applicable) on the dairy product in the format YYYY-MM-DD. An example is “2024-03-23”.

**average_cycle_threshold** - The cycle threshold value of the sample in a qPCR assay. This is the number of cycles performed before a positive signal is detected by the instrument. Format as a number with decimal points. An example is "27.3".

copies_per_mL - A calculated value of qPCR targets per mL. This should be calculated from the cycle threshold value compared to a standard curve. This value is optional.

**primer_asset_file** - The name of the file of the primers used in the qPCR assay. A file with the same name should be present in the /assets/primers_and_probes directory of this repository. If this is your first time committing with your data you may need to add these files when you commit. The primer file should be a single fasta or bed file with both the forward and reverse primer. If your primers are proprietary, this field can be filled with "redacted" to indicate this. This filename should be unique among files within the repository. An example is "HPAI_primers.fasta". 

**probe_asset_file** - The name of the file of the probe used in the qPCR assay. A file with the same name should be present in the /assets/primers_and_probes directory of this repository. If your probe is proprietary, this field can be filled with "redacted" to indicate this. This filename should be unique among files within the repository. An example is "HPAI_probe.fasta".

**qPCR_cycle_condition** - The name of the file of the cycling conditions used in the qPCR assay. A file with the same name should be present in the /assets/cycling_conditions directory of the repository. The cycling conditions file should be a txt file.

**processing_plant_state** - The state abbreviation of the location of the processing plant. On every dairy product, there is a 2 digit code followed by a dash (-) and another series of numbers (usually 2-3). The first 2 digit code can be used to find the state where the milk was processed. The state should ONLY be included if there are more than 3 processing plants throughout the state so as to protect sensitive information. If the state has 3 or less processing plants, the entry in this column should be “NA”. States should be entered in their abbreviated format. An example entry is “WI” for Wisconsin.

**positive_for_HPAI** - This column should be populated with TRUE or FALSE depending on whether the sample tested positive for influenza based on the primers used.

SRA_bioproject - The bioproject to which the sequences were uploaded in SRA, if sequences have been uploaded.

SRA_accession - The accession number of the uploaded sequence in SRA, if sequences have been uploaded.

**contributors** - The names of those contributing this data. This should be a string. 

**date_contributed** - The date of the pull request. This should be in the format of YYYY-MM-DD. 

RNA_extraction_method - A general description of the method used to extract the RNA. This field is optional.