import re

# Input file paths
gff_file = "final_nxAuaRhod1_1_prot_blasted.gff"
desc_file = "updated_gene_ids_with_desc_cleaned.txt"
output_gff = "final2_nxAuaRhod1_1_prot_blasted.gff"

# Load gene descriptions into a dictionary
gene_desc = {}

with open(desc_file, "r") as f:
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) == 3:
            gene_id, alt_id, description = parts
            if description != "---NA---":  # Ignore NA descriptions
                gene_desc[gene_id] = description

# Process the GFF file
with open(gff_file, "r") as infile, open(output_gff, "w") as outfile:
    for line in infile:
        if line.startswith("#"):  # Preserve comments and headers
            outfile.write(line)
            continue

        fields = line.strip().split("\t")
        if len(fields) < 9:  # Ensure valid GFF format
            outfile.write(line)
            continue

        # Extract the gene ID from the attributes column
        attributes = fields[8]
        match = re.search(r"ID=([^;]+)", attributes)
        if match:
            gene_id = match.group(1)
            if gene_id in gene_desc:
                description = gene_desc[gene_id]
                # Append or update the Note attribute
                if "Note=" in attributes:
                    attributes = re.sub(r"Note=[^;]+", f"Note={description}", attributes)
                else:
                    attributes += f";Note={description}"
                
                fields[8] = attributes  # Update attributes column

        # Write updated line
        outfile.write("\t".join(fields) + "\n")

print(f"Updated GFF file saved as {output_gff}")
