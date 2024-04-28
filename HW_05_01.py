import os
import shutil
import asyncio
import argparse
import logging

logging.basicConfig(filename='file_copy.log', level=logging.ERROR)

async def read_folder(source_folder, output_folder):
    for root, _, files in os.walk(source_folder):
        for file in files:
            source_path = os.path.join(root, file)
            extension = os.path.splitext(file)[1]
            destination_folder = os.path.join(output_folder, extension[1:])
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
            destination_path = os.path.join(destination_folder, file)
            await copy_file(source_path, destination_path)

async def copy_file(source_path, destination_path):
    try:
        shutil.copyfile(source_path, destination_path)
        print(f"Copied {source_path} to {destination_path}")
    except Exception as e:
        error_message = f"Error copying {source_path}: {e}"
        print(error_message)
        logging.error(error_message)

async def main(source_folder, output_folder):
    await read_folder(source_folder, output_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Copy files from source folder to output folder.')
    parser.add_argument('source_folder', type=str, help='Path to the source folder')
    parser.add_argument('output_folder', type=str, help='Path to the output folder')
    args = parser.parse_args()

    asyncio.run(main(args.source_folder, args.output_folder))
