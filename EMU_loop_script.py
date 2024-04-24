import os
import subprocess

def analyze_barcodes(input_folder, output_folder, emu_database_dir, num_threads):
    # Get a list of all files in the input folder
    barcode_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through each barcode file
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

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run EMU analysis on a folder of barcode files")
    parser.add_argument("input_folder", type=str, help="Path to the folder containing barcode files")
    parser.add_argument("output_folder", type=str, help="Path to the folder where output will be saved")
    parser.add_argument("emu_database_dir", type=str, help="Path to the EMU database directory")
    parser.add_argument("--threads", type=int, default=1, help="Number of threads to use (default: 1)")
    args = parser.parse_args()

    analyze_barcodes(args.input_folder, args.output_folder, args.emu_database_dir, args.threads)
