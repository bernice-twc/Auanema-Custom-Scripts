# Function to filter orthogroups and count overlaps between species
def filter_orthogroups(input_file):
    # Counters for different categories of orthogroups
    count_oti = 0
    count_g = 0
    count_celegans = 0
    count_oti_g = 0
    count_oti_celegans = 0
    count_g_celegans = 0
    count_all_three = 0  # Counter for orthogroups with all three species

    with open(input_file, 'r') as infile, \
         open("Filtered_Orthogroups_Arhod_Otip.txt", 'w') as oti_g_outfile, \
         open("Filtered_Orthogroups_Arhod_Cele.txt", 'w') as g_celegans_outfile:
        
        for line in infile:
            # Split the line into orthogroup and gene list
            parts = line.strip().split(':')
            orthogroup = parts[0]
            genes = parts[1].split()

            # Flags for species
            has_oti = False
            has_g = False
            has_celegans = False

            # Check which species are represented in this orthogroup
            for gene in genes:
                if gene.startswith("Oti_"):
                    has_oti = True
                elif gene.startswith("g"):
                    has_g = True
                else:
                    has_celegans = True

            # Count orthogroups based on species presence
            if has_oti and not has_g and not has_celegans:
                count_oti += 1
            elif has_g and not has_oti and not has_celegans:
                count_g += 1
            elif has_celegans and not has_oti and not has_g:
                count_celegans += 1
            if has_oti and has_g and not has_celegans:
                count_oti_g += 1
                oti_g_outfile.write(line)  # Write to the Oti & g file
            if has_oti and not has_g and has_celegans:
                count_oti_celegans += 1
            if not has_oti and has_g and has_celegans:
                count_g_celegans += 1
                g_celegans_outfile.write(line)  # Write to the g & C. elegans file
            if has_oti and has_g and has_celegans:
                count_all_three += 1  # Orthogroups with all three species

    # Print summary counts
    print(f"Pure O. tipulae orthogroups: {count_oti}")
    print(f"Pure A. rhodense orthogroups: {count_g}")
    print(f"Pure C. elegans orthogroups: {count_celegans}")
    print(f"Overlap (Oti & g): {count_oti_g}")
    print(f"Overlap (Oti & C. elegans): {count_oti_celegans}")
    print(f"Overlap (g & C. elegans): {count_g_celegans}")
    print(f"Orthogroups with all three species (Oti, g, and C. elegans): {count_all_three}")


# Call the function with your file path
input_file = "Orthogroups_cleaned.txt"
filter_orthogroups(input_file)
