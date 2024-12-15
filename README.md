# BioE 134 Final Project Submission
# Project Overview
This project provides a set of bioinformatics utilities and integrations:

Queries:
query_uniprot: Fetches UniProtKB entry data for a given UniProt ID.
query_alphafold: Retrieves predicted protein structure information from the AlphaFold API for a given UniProt ID.
query_interpro_by_uniprot: Obtains protein domain and family annotations from InterPro for a given UniProt ID.
query_go_annotations_uniprot: Fetches Gene Ontology (GO) annotations for a given UniProt ID.
enrich_go_annotations_with_names: Enhances GO annotation results by retrieving GO term names via QuickGO.

Protein Language Model Integration:
generate_with_protein_model: Uses a fine-tuned large language model ("basil2115/llama2-qlora-proteins") to generate text related to protein science queries.

# Scope of Work
For the BioE 134 final project, the core functionality developed includes the reverse_complement and translate functions. These form the foundation for sequence analysis tasks. Additional functionalities were implemented to interface with popular bioinformatics services (UniProt, AlphaFold, InterPro, QuickGO) and to use a custom fine-tuned language model for protein-related queries.

# Core functions:

Bioinformatics Database Queries

Query Functions:
1. **query_uniprot(uniprot_id)**:
Queries the UniProt REST API for detailed protein information by UniProt ID.

Example:
data = query_uniprot("P69905")
print(data)

2. **query_alphafold(uniprot_id)**:
Retrieves AlphaFold predicted structure information for a given UniProt ID.

Example:
structure = query_alphafold("P69905")
print(structure)

3. **query_interpro_by_uniprot(uniprot_id)**:
Fetches protein domain and family annotations from InterPro based on a UniProt ID.

Example:
interpro_data = query_interpro_by_uniprot("P69905")
print(interpro_data)

4. **query_go_annotations_uniprot(uniprot_id)**:
Retrieves GO annotations (molecular function, biological process, cellular component) associated with a given UniProt ID from QuickGO.

Example:
go_data = query_go_annotations_uniprot("P69905")
print(go_data)

5. **enrich_go_annotations_with_names(annotations)**:
Enhances GO annotations by fetching the human-readable GO term names using the QuickGO ontology service.

Example:
enriched_go = enrich_go_annotations_with_names(go_data)
print(enriched_go)

Protein Language Model Generation

6. **generate_with_protein_model(prompt, max_length=128)**
Description:
Uses a fine-tuned language model ("basil2115/llama2-qlora-proteins") to generate text related to protein science. This can be helpful for summarizing information, explaining biological concepts, or generating hypotheses.

Input:

prompt: A string containing the prompt or question.
max_length: Maximum length of the generated output tokens.
Output:
A string containing the generated response from the model.

Example:
response = generate_with_protein_model("Tell me about Human Hemoglobin subunit alpha")
print(response)

# Error Handling:
Query Functions
Rely on requests.raise_for_status() to raise requests.HTTPError for invalid queries (e.g., invalid UniProt IDs).

Language Model Generation
If the model or tokenizer cannot be loaded, OSError or environment-related errors may be raised.

# Testing:
Testing is done using pytest. A suite of tests covers:

Query Functions:
Tests querying known UniProt IDs and handling invalid ones, ensuring results parse as expected.

Model Generation:
Tests prompt-response generation with both standard and empty prompts (if environment supports model loading).

# Usage Instructions:

Install Requirements:
pip install -r requirements.txt

Import and Use Functions:
from bio_functions import query_uniprot, query_alphafold, query_interpro_by_uniprot, query_go_annotations_uniprot, enrich_go_annotations_with_names
from bio_functions import generate_with_protein_model

# Querying databases
uni_data = query_uniprot("P69905")
print(uni_data)

# Model generation
response = generate_with_protein_model("Explain the fuctions of alpha hemoglobin y")
print(response)
Conclusion
This project delivers a set of tools for DNA sequence manipulation (reverse_complement, translate), integrates with major bioinformatics resources (UniProt, AlphaFold, InterPro, GO), and utilizes a fine-tuned protein-related language model for advanced text generation. All functionalities are tested and documented, ensuring a robust and versatile toolkit for bioinformatics analysis pipelines.

Additional Resources
UniProt: https://www.uniprot.org
AlphaFold: https://alphafold.ebi.ac.uk
InterPro: https://www.ebi.ac.uk/interpro/
QuickGO: https://www.ebi.ac.uk/QuickGO/
Hugging Face Model: basil2115/llama2-qlora-proteins (llama2 I finetuned on protein sequences using qlora)
