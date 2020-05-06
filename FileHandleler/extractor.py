import patoolib


def extract_files(files, path="C:\\Users\\Ella\\Downloads"):
    """
    Function to extract files of almost any file format.
    :param files: A list of files that can be extracted
    :param path: The path to the folder
    """
    print("Function starting using files", files)
    for file in files:
        print("Extracting....")
        patoolib.extract_archive(path + "\\" + file, outdir=path)
        print(file, " extracted")


