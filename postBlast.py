import re

# File paths
old_gff_file = "all-annotations-with-blast-hits_with_ARH_prefix.gff3"
new_gff_file = "nxAuaRhod1_1_prot_braker.gff"
mapping_file = "blastp_cleaned.txt"
output_gff_file = "updated_nxAuaRhod1_1_prot_blasted.gff"

# Step 1: Extract Notes and Ontology terms from old annotation
annotations = {}
with open(old_gff_file, "r") as old_gff:
    for line in old_gff:
        if not line.startswith("#") and "\t" in line:
            fields = line.strip().split("\t")
            attributes = fields[-1]
            match = re.search(r"ID=([^;]+)", attributes)
            if match:
                gene_id = match.group(1)
                if gene_id.startswith("ARH_"):
                    gene_id = gene_id.replace("ARH_", "")  # Remove ARH_ prefix
                notes = re.findall(r"(Note=[^;]+|Ontology_term=[^;]+)", attributes)
                if notes:
                    annotations[gene_id] = ";".join(notes)

# Step 2: Read mapping file (old gene ID to new gene ID)
mapping = {}
with open(mapping_file, "r") as map_file:
    for line in map_file:
        old_id, new_id = line.strip().split("\t")
        old_id = old_id.replace("ARH_", "")  # Ensure consistency in IDs
        mapping[new_id] = annotations.get(old_id, "")  # Get notes if available

# Step 3: Update new annotation file with Notes and Ontology terms
with open(new_gff_file, "r") as new_gff, open(output_gff_file, "w") as output_gff:
    for line in new_gff:
        if line.startswith("#") or "\t" not in line:
            output_gff.write(line)
            continue
        
        fields = line.strip().split("\t")
        attributes = fields[-1]
        match = re.search(r"ID=([^;]+)", attributes)
        if match:
            gene_id = match.group(1)
            if gene_id in mapping and mapping[gene_id]:
                attributes += ";" + mapping[gene_id]  # Append Notes and Ontology terms
        
        fields[-1] = attributes
        output_gff.write("\t".join(fields) + "\n")

print("Updated GFF file saved to", output_gff_file)
