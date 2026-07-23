import pandas as pd
from collections import defaultdict

# File paths
aligned_file = "aligned.txt"
gff_file = "final2_nxAuaRhod1_1_prot_blasted.gff"

# Load somatic regions
def load_somatic_regions(aligned_file):
    somatic_regions = defaultdict(list)
    with open(aligned_file, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:
                chrom, start, end = parts[0], int(parts[1]), int(parts[2])
                somatic_regions[chrom].append((start, end))
    return somatic_regions

# Load mRNA annotations from GFF
def load_mrna_annotations(gff_file):
    mrna_annotations = []
    with open(gff_file, "r") as f:
        for line in f:
            if line.startswith("#"):  # Skip comments
                continue
            parts = line.strip().split("\t")
            if len(parts) < 9:
                continue
            feature_type, chrom, start, end, attributes = parts[2], parts[0], int(parts[3]), int(parts[4]), parts[8]
            if feature_type == "mRNA":  # Extract only mRNA
                gene_id = next((item.split("=")[1] for item in attributes.split(";") if item.startswith("ID=")), None)
                notes = next((item.split("=")[1] for item in attributes.split(";") if item.startswith("Note=")), "")
                if gene_id:
                    mrna_annotations.append((chrom, start, end, gene_id, notes))
    return mrna_annotations

# Check if an mRNA is in a somatic region
def is_somatic(chrom, start, end, somatic_regions):
    if chrom in somatic_regions:
        for s_start, s_end in somatic_regions[chrom]:
            if not (end < s_start or start > s_end):  # Overlapping condition
                return True
    return False

# Process files
somatic_regions = load_somatic_regions(aligned_file)
mrna_annotations = load_mrna_annotations(gff_file)

# Classify mRNA
somatic_mrna = []
germline_mrna = []
unclassified_mrna = []

for chrom, start, end, gene_id, notes in mrna_annotations:
    if is_somatic(chrom, start, end, somatic_regions):
        somatic_mrna.append((gene_id, notes))
    else:
        germline_mrna.append((gene_id, notes))

# Find unclassified mRNA
classified_ids = {gene_id for gene_id, _ in somatic_mrna} | {gene_id for gene_id, _ in germline_mrna}
for _, _, _, gene_id, notes in mrna_annotations:
    if gene_id not in classified_ids:
        unclassified_mrna.append((gene_id, notes))

# Save results
with open("somatic_mrna.txt", "w") as f:
    for gene_id, notes in somatic_mrna:
        f.write(f"{gene_id}\t{notes}\n")

with open("germline_mrna.txt", "w") as f:
    for gene_id, notes in germline_mrna:
        f.write(f"{gene_id}\t{notes}\n")

with open("unclassified_mrna.txt", "w") as f:
    for gene_id, notes in unclassified_mrna:
        f.write(f"{gene_id}\t{notes}\n")

# Print summary
print(f"Total mRNA: {len(mrna_annotations)}")
print(f"Classified as Somatic: {len(somatic_mrna)}")
print(f"Classified as Germline: {len(germline_mrna)}")
print(f"Unclassified: {len(unclassified_mrna)}")
print("Unclassified mRNA saved to unclassified_mrna.txt")