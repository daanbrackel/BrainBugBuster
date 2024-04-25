import os
import subprocess
import argparse
import pandas as pd
import plotly.graph_objects as go

def analyze_barcodes(input_folder, output_folder, emu_database_dir, num_threads):
    # Get a list of all files in the input folder
    barcode_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each barcode file
    for barcode_file in barcode_files:
        # Extract the barcode name (without extension)
        barcode_name = os.path.splitext(barcode_file)[0]

        # Define input and output paths
        input_path = os.path.join(input_folder, barcode_file)
        output_path = os.path.join(output_folder, f"{barcode_name}_output")

        # Create the output folder for this barcode if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Run EMU analysis for this barcode
        command = f"emu abundance {input_path} --db {emu_database_dir} --output-dir {output_path} --threads {num_threads}"
        run = subprocess.run(command, shell=True, text=True)
        print(run.stdout)

def merge_tsv_files_with_barcode(input_folder, output_folder):
    dfs = []
    for folder in os.listdir(input_folder):
        folder_path = os.path.join(input_folder, folder)
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith(".tsv"):
                    tsv_file_path = os.path.join(folder_path, file)
                    df = pd.read_csv(tsv_file_path, sep='\t')
                    df['Barcode'] = folder  # Assign barcode to a new column
                    dfs.append(df)

    if not dfs:
        raise ValueError("No processed TSV files found in the barcode folders.")

    merged_df = pd.concat(dfs, ignore_index=True)
    merged_tsv_path = os.path.join(output_folder, "merged_with_barcode.tsv")
    merged_df.to_csv(merged_tsv_path, sep='\t', index=False)
    print("Merged TSV files saved as '{}'.".format(merged_tsv_path))

    # Remove unnecessary columns
    modified_df = merged_df[['abundance', 'species', 'genus', 'Barcode']]
    modified_tsv_path = os.path.join(output_folder, "modified_merged.tsv")
    modified_df.to_csv(modified_tsv_path, sep='\t', index=False)
    print("Modified merged TSV file saved as '{}'.".format(modified_tsv_path))

    return modified_tsv_path

def plot_abundance_from_csv(input_csv, output_species_html, output_genus_html):
    # Read input CSV
    df = pd.read_csv(input_csv, sep='\t')

    # Species plot
    species_df = df.drop(columns=['genus'])  # Drop genus column
    species_df['abundance'] *= 100  # Multiply abundance by 100 to get percentage
    species_df['genus'] = species_df['species']  # Rename species column to genus for consistency
    species_df.drop(columns=['species'], inplace=True)  # Drop species column
    species_df_grouped = species_df.groupby(['Barcode', 'genus']).sum().reset_index()

    # Aggregate species with <1% abundance into 'Other species <1%'
    species_df_grouped.loc[species_df_grouped['abundance'] < 1, 'genus'] = 'Other species <1%'
    species_df_grouped = species_df_grouped.groupby(['Barcode', 'genus']).sum().reset_index()
    species_pivot_table = species_df_grouped.pivot(index='Barcode', columns='genus', values='abundance').fillna(0)

    # Genus plot
    genus_df = df.drop(columns=['species'])  # Drop species column
    genus_df['abundance'] *= 100  # Multiply abundance by 100 to get percentage
    genus_df_grouped = genus_df.groupby(['Barcode', 'genus']).sum().reset_index()

    # Aggregate genera with <1% abundance into 'Other genera <1%'
    genus_df_grouped.loc[genus_df_grouped['abundance'] < 1, 'genus'] = 'Other genera <1%'
    genus_df_grouped = genus_df_grouped.groupby(['Barcode', 'genus']).sum().reset_index()
    genus_pivot_table = genus_df_grouped.pivot(index='Barcode', columns='genus', values='abundance').fillna(0)

    # Plot species abundance
    fig_species = go.Figure()
    for column in species_pivot_table.columns:
        fig_species.add_trace(go.Bar(x=species_pivot_table.index, y=species_pivot_table[column], name=column))

    fig_species.update_layout(title='Species Abundance per Barcode',
                               xaxis_title='Barcode',
                               yaxis_title='Abundance (%)',
                               barmode='stack')
    # Save species plot as HTML
    fig_species.write_html(output_species_html)

    # Plot genus abundance
    fig_genus = go.Figure()
    for column in genus_pivot_table.columns:
        fig_genus.add_trace(go.Bar(x=genus_pivot_table.index, y=genus_pivot_table[column], name=column))

    fig_genus.update_layout(title='Genus Abundance per Barcode',
                            xaxis_title='Barcode',
                            yaxis_title='Abundance (%)',
                            barmode='stack')
    # Save genus plot as HTML
    fig_genus.write_html(output_genus_html)

def main():
    parser = argparse.ArgumentParser(description="Run EMU analysis on a folder of barcode files, merge processed TSV files, visualize abundance data, and save plots")
    parser.add_argument("input_folder", type=str, help="Path to the folder containing barcode files")
    parser.add_argument("output_folder", type=str, help="Path to the folder where all results will be placed")
    parser.add_argument("emu_database_dir", type=str, help="Path to the EMU database directory")
    parser.add_argument("--threads", type=int, default=1, help="Number of threads to use for EMU analysis (default: 1)")
    args = parser.parse_args()

    # Run EMU analysis
    analyze_barcodes(args.input_folder, args.output_folder, args.emu_database_dir, args.threads)

    # Merge TSV files from barcode folders and add barcode information
    merged_tsv_path = merge_tsv_files_with_barcode(args.output_folder, args.output_folder)

    # Plot abundance data and save plots
    output_species_html = os.path.join(args.output_folder, "species_abundance.html")
    output_genus_html = os.path.join(args.output_folder, "genus_abundance.html")
    plot_abundance_from_csv(merged_tsv_path, output_species_html, output_genus_html)

if __name__ == "__main__":
    main()
