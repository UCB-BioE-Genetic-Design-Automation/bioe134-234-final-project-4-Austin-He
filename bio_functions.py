def reverse_complement(sequence):
    """
    Calculates the reverse complement of a DNA sequence.
    
    Args:
        sequence (str): A string representing the DNA sequence.

    Returns:
        str: The reverse complement of the DNA sequence.

    Raises:
        ValueError: If the DNA sequence contains invalid characters.
    """
    valid_nucleotides = {'A', 'T', 'C', 'G'}
    if any(char not in valid_nucleotides for char in sequence):
        raise ValueError("DNA sequence contains invalid characters. Allowed characters: A, T, C, G.")

    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join(complement[base] for base in reversed(sequence))

def translate(sequence):
    """
    Translates a DNA sequence into a protein sequence based on the standard genetic code.

    Args:
        sequence (str): A string representing the DNA sequence.

    Returns:
        str: The corresponding protein sequence.

    Raises:
        ValueError: If the DNA sequence contains invalid characters or is not a multiple of three.
    """
    valid_nucleotides = {'A', 'T', 'C', 'G'}
    if any(char not in valid_nucleotides for char in sequence):
        raise ValueError("DNA sequence contains invalid characters. Allowed characters: A, T, C, G.")
    if len(sequence) % 3 != 0:
        raise ValueError("Length of DNA sequence is not a multiple of three, which is required for translation.")

    codon_table = {
        'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
        'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
        'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
        'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
        'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
        'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
        'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
        'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
        'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
        'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
        'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
        'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
        'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
        'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
        'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
        'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W',
    }
    protein = ""
    for i in range(0, len(sequence), 3):
        codon = sequence[i:i+3]
        protein += codon_table.get(codon, '_')  # Using '_' for unknown or stop codons
    return protein


import requests

def query_uniprot(uniprot_id):
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}"
    headers = {"Accept": "application/json"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()

def query_alphafold(uniprot_id):
    url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

def query_interpro_by_uniprot(uniprot_id):
    url = f"https://www.ebi.ac.uk/interpro/api/protein/uniprot/{uniprot_id}/"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()
import requests

import requests

def query_go_annotations_uniprot(uniprot_id):
    base_url = "https://www.ebi.ac.uk/QuickGO/services/annotation/search"
    params = {
        "geneProductId": f"UniProtKB:{uniprot_id}",
        "fields": "goId,evidenceCode,geneProductId",  # keep fields minimal for clarity
        "limit": "50"
    }
    r = requests.get(base_url, params=params)
    r.raise_for_status()
    return r.json()

def get_go_term_details(go_id):
    url = f"https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/{go_id}"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()
    results = data.get("results", [])
    if results:
        # The name field is typically here
        return results[0].get("name", None)
    return None

def enrich_go_annotations_with_names(annotations):
    for ann in annotations.get("results", []):
        go_id = ann.get("goId")
        if go_id:
            go_name = get_go_term_details(go_id)
            ann["goName"] = go_name
    return annotations

    

if __name__ == "__main__":
    # Example DNA sequence for demonstration
    dna_example = "ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG"

    try:
        # Perform reverse complement
        rc_result = reverse_complement(dna_example)
        print(f"Reverse Complement of '{dna_example}': {rc_result}")

        # Perform translation
        translation_result = translate(dna_example)
        print(f"Translation of '{dna_example}': {translation_result}")
    except Exception as e:
        print(f"Error: {str(e)}")

    test_id = "P69905"  # Human Hemoglobin subunit alpha, should return data reliably
    
    print("Querying UniProt...")
    uniprot_data = query_uniprot(test_id)
    print("UniProt data:", uniprot_data, "\n")

    print("Querying AlphaFold...")
    alphafold_data = query_alphafold(test_id)
    print("AlphaFold data:", alphafold_data, "\n")

    print("Querying InterPro...")
    interpro_data = query_interpro_by_uniprot(test_id)
    print("InterPro data:", interpro_data, "\n")

    print("Querying GO annotations...")
    annotations = query_go_annotations_uniprot(test_id)
    print("GO annotations data:", annotations, "\n")
    enriched_annotations = enrich_go_annotations_with_names(annotations)
    print("Enriched GO annotations with GO names:", enriched_annotations)


