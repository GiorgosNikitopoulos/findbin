import argparse
import os
import subprocess
import glob
from pathlib import Path
import pdb
import shutil

def main(args):
    #For all tar files input
    for tar_file in glob.glob(f"{args.input_path}/*"):
        print(tar_file)
        #Untar file in temp
        temp = args.temp_dir
        result = subprocess.run(["tar", "-xf", tar_file, "-C", f"{temp}"], capture_output=True, text=True)

        #Depackage all the debs out of the directory to temp
        for deb_file in glob.glob(f"{temp}/**/*.deb", recursive = True):
            result = subprocess.run(["dpkg-deb", "-x", deb_file, temp], capture_output=True, text=True)

        elf_files = []
        #File all files in directory and extract all the executables
        for each_file in glob.glob(f"{temp}/**", recursive = True):
            result = subprocess.run(["file", each_file], capture_output=True, text=True)
            print(result)
            #Get the stdout of the process call 
            output = result.stdout
            #Check if it mentions an ELF 
            if "ELF" in output:
                elf_files.append(each_file)

        #If at least an ELF file is found
        if len(elf_files) > 0:
            #Create an output directory in the output_path
            output_directory = os.path.join(args.output_path, os.path.basename(tar_file))
            os.makedirs(output_directory, exist_ok = True)

        print(elf_files)
        #Copy all ELF files to the output path 
        for elf in elf_files:
            shutil.copy(elf, os.path.join(output_directory, os.path.basename(elf)))

        #Clean up directory 
        subprocess.run(f'rm -r {temp}/*', shell=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find executable ELFs')
    parser.add_argument("--input_path", type=str, default = "/input_data", help="Input path")
    parser.add_argument("--output_path", type=str, default = "/output_data", help="Output path")
    parser.add_argument("--temp_dir", type=str, default="./tmp", help="Output path")

    args = parser.parse_args()
    main(args)

