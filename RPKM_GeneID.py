import os
import csv

# Load extracted gene info into dictionaries
gene_info_file = "extracted_gene_info.csv"

gene_map = {}
gene_length = {}

# Read gene info CSV
with open(gene_info_file, "r") as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        if len(row) < 3:
            continue
        gene_id, gene_name, length = row[0], row[1], row[2]
        gene_map[gene_id] = gene_name if gene_name.strip() else gene_id  # Use Gene_ID if name is empty
        gene_length[gene_id] = int(length) if length.isdigit() else 1  # Default length to 1 if missing

# Define folders
count_folder = "4_Counts_Pablo"
output_folder = "RPKM_Calculated"
os.makedirs(output_folder, exist_ok=True)

# Define unwanted entries (modify if needed)
unwanted_entries = {"__no_feature", "__ambiguous", "__too_low_aQual", "__not_aligned", "__alignment_not_unique"}

# Process each count file
for count_file in os.listdir(count_folder):
    if not count_file.endswith(".txt"):
        continue

    file_path = os.path.join(count_folder, count_file)
    output_file = os.path.join(output_folder, count_file.replace(".txt", "_RPKM.txt"))

    count_data = []
    total_counts = 0  # To compute total mapped reads

    # Read raw count file
    with open(file_path, "r") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) != 2:
                continue  # Skip malformed lines

            gene_id, raw_count = parts
            if gene_id in unwanted_entries or not gene_id.strip():
                continue  # Skip unwanted entries and lines without a valid gene_id

            try:
                raw_count = int(raw_count)
            except ValueError:
                continue  # Skip invalid counts

            count_data.append((gene_id, raw_count))
            total_counts += raw_count  # Update total mapped reads

    if not count_data or total_counts == 0:
        print(f"Skipping empty or invalid file: {count_file}")
        continue

    # Compute RPKM and write output
    with open(output_file, "w", newline="") as out_f:
        writer = csv.writer(out_f, delimiter="\t")

        for gene_id, raw_count in count_data:
            length = gene_length.get(gene_id, 1)  # Default length to 1 if missing
            rpkm = (raw_count * 1e9) / (total_counts * length)  # Compute RPKM

            writer.writerow([gene_id, f"{rpkm:.2f}"])  # Write output with 2 decimal places

    print(f"Processed: {count_file} -> {output_file}")

print("All files processed successfully!")
