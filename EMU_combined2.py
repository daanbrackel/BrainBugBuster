import os
import argparse
import pandas as pd
import plotly.graph_objects as go

def process_tsv(input_folder, output_folder):
    for barcode_folder in os.listdir(input_folder):
        barcode_path = os.path.join(input_folder, barcode_folder)
        if os.path.isdir(barcode_path):
            for file in os.listdir(barcode_path):
                if file.endswith(".tsv") and "threshold" not in file:
                    tsv_path = os.path.join(barcode_path, file)
                    output_path = os.path.join(output_folder, f"{barcode_folder}_processed.tsv")
                    process_file(tsv_path, output_path)

def process_file(input_file, output_file):
    data = pd.read_csv(input_file, sep='\t')
    processed_data = data[['abundance', 'species', 'genus']]
    processed_data.to_csv(output_file, sep='\t', index=False)

def merge_processed_tsv_files(processed_folder):
    dfs = []
    for file in os.listdir(processed_folder):
        if file.endswith("_processed.tsv"):
            tsv_file_path = os.path.join(processed_folder, file)
            barcode = file.split("_processed.tsv")[0]  # Extract barcode from file name
            df = pd.read_csv(tsv_file_path, sep='\t')
            df['Barcode'] = barcode  # Assign barcode to a new column
            dfs.append(df)
    if not dfs:
        raise ValueError("No processed TSV files found in the processed folder.")

    merged_df = pd.concat(dfs, ignore_index=True)
    return merged_df

def save_merged_dataframe(merged_dataframe, output_file):
    merged_dataframe.to_csv(output_file, index=False)
    print("Merged dataframe saved as '{}'.".format(output_file))

def plot_abundance(input_csv, output_species_html, output_genus_html):
    df = pd.read_csv(input_csv)

    species_df = df.drop(columns=['genus'])
    species_df['abundance'] *= 100
    species_df['genus'] = species_df['species']
    species_df.drop(columns=['species'], inplace=True)
    species_df_grouped = species_df.groupby(['Barcode', 'genus']).sum().reset_index()

    species_df_grouped.loc[species_df_grouped['abundance'] < 1, 'genus'] = 'Other species <1%'
    species_df_grouped = species_df_grouped.groupby(['Barcode', 'genus']).sum().reset_index()
    species_pivot_table = species_df_grouped.pivot(index='Barcode', columns='genus', values='abundance').fillna(0)

    genus_df = df.drop(columns=['species'])
    genus_df['abundance'] *= 100
    genus_df_grouped = genus_df.groupby(['Barcode', 'genus']).sum().reset_index()

    genus_df_grouped.loc[genus_df_grouped['abundance'] < 1, 'genus'] = 'Other genera <1%'
    genus_df_grouped = genus_df_grouped.groupby(['Barcode', 'genus']).sum().reset_index()
    genus_pivot_table = genus_df_grouped.pivot(index='Barcode', columns='genus', values='abundance').fillna(0)

    fig_species = go.Figure()
    for column in species_pivot_table.columns:
        fig_species.add_trace(go.Bar(x=species_pivot_table.index, y=species_pivot_table[column], name=column))

    fig_species.update_layout(title='Species Abundance per Barcode',
                               xaxis_title='Barcode',
                               yaxis_title='Abundance (%)',
                               barmode='stack')
    fig_species.write_html(output_species_html)

    fig_genus = go.Figure()
    for column in genus_pivot_table.columns:
        fig_genus.add_trace(go.Bar(x=genus_pivot_table.index, y=genus_pivot_table[column], name=column))

    fig_genus.update_layout(title='Genus Abundance per Barcode',
                            xaxis_title='Barcode',
                            yaxis_title='Abundance (%)',
                            barmode='stack')
    fig_genus.write_html(output_genus_html)

def main():
    parser = argparse.ArgumentParser(description="Process EMU output files, merge them, and plot abundance")
    parser.add_argument("input_folder", type=str, help="Path to the folder containing barcode output folders (these output folders contain the .tsv files)")
    parser.add_argument("output_folder", type=str, help="Path to the folder where all results will be placed")
    args = parser.parse_args()

    processed_folder = os.path.join(args.output_folder, "processed_files")
    os.makedirs(processed_folder, exist_ok=True)

    # Process TSV files
    process_tsv(args.input_folder, processed_folder)

    # Merge processed TSV files
    merged_dataframe = merge_processed_tsv_files(processed_folder)
    merged_csv_path = os.path.join(args.output_folder, "merged.csv")
    save_merged_dataframe(merged_dataframe, merged_csv_path)

    # Plot abundance
    species_html_path = os.path.join(args.output_folder, "species_abundance.html")
    genus_html_path = os.path.join(args.output_folder, "genus_abundance.html")
    plot_abundance(merged_csv_path, species_html_path, genus_html_path)

if __name__ == "__main__":
    main()
