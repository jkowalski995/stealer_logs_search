import os
import subprocess
import yaml
import re
import pandas as pd
import time


def get_list_of_archives() -> list:
    """
    Lists archives in dir. It assumes that in the dir are only archives.
    :return: lst with files from dir
    """
    arch_list = os.listdir()
    return arch_list


def check_password(archive: str, password: str) -> bool:
    """
    Check if provided password fits to the archive
    :param archive: str archive to check
    :param password: str password to check
    :return: Print "Everything is Ok" when password fits archive and False if not
    """
    try:
        output = subprocess.check_output(["7z", "t", "-p" + password, archive], stderr=subprocess.STDOUT,
                                         universal_newlines=True)
        return "Everything is Ok" in output
    except subprocess.CalledProcessError:
        return False


def unpack_with_pass(dict_arch_pass: dict, dest_to_unpack: str) -> None:
    """
    Unpack archives based on previously found pairs - pass:arch
    :param dict_arch_pass: dict with archives and passwords
    :param dest_to_unpack: str directory for unpacking the archives
    :return: None
    """
    for archive, password in dict_arch_pass.items():
        dst = dest_to_unpack + "/" + archive
        print(archive, password)
        try:
            subprocess.run(["7z", "x", "-y", "-p" + password, "-mmt3", archive, "-o" + dst], check=True)
            print(f"wypakowano {archive} {dst}")
        except subprocess.CalledProcessError:
            print(f"wypakowanie {archive} nie powiodło się")


def unpack_without_pass(arch_list: list, dest_to_unpack: str) -> None:
    """
    Unpack archives without password protection
    :param arch_list: lst with archives
    :param dest_to_unpack: str directory for unpacking the archives
    :return: None
    """
    for arch in arch_list:
        dst = dest_to_unpack + "/" + arch
        print(arch)
        try:
            subprocess.run(["7z", "x", "-y", "-mmt3", arch, "-o" + dst], check=True)
            print(f"wypakowano {arch} {dst}")
        except subprocess.CalledProcessError:
            print(f"wypakowanie {arch} nie powiodło się")


def pass_check(passwords: list) -> dict:
    """
    Function for searching archive:password pairs
    :param passwords: lst with known passwords
    :return: dict with archives and passwords
    """
    passwords = passwords
    dict_arch_pass = {}

    for archive in os.listdir("."):
        if archive.endswith(".7z") or archive.endswith(".rar"):
            for password in passwords:
                if check_password(archive, password):
                    dict_arch_pass[archive] = password
                    break

    print(dict_arch_pass)
    return dict_arch_pass


def filter_list(arch_list_raw: dict) -> list:
    """
    Filtering raw list of archives to left only that without passwords. So, if archive from dict (archive:pass) is in
    raw list than remove it from raw list.
    :param arch_list_raw: dict raw dict of archives in directory
    :return: lst with archives without passwords
    """
    archives = get_list_of_archives()
    for a in arch_list_raw.keys():
        if a in archives:
            archives.remove(a)
    # Do not try to unpack dir
    if 'wypakowane' in archives:
        archives.remove('wypakowane')
    # Do not try to unpack this script
    if 'stealer_search.py' in archives:
        archives.remove('stealer_search.py')
    # Do not try to unpack results in *.txt file
    if 'WYNIKI.txt' in archives:
        archives.remove('WYNIKI.txt')
    # Do not try to unpack results in *.html file
    if 'WYNIKI.html' in archives:
        archives.remove('WYNIKI.html')
    # Do not try to unpack instruction file
    if 'Instrukcja_stealer_search' in archives:
        archives.remove('Instrukcja_stealer_search')
    print(f"filter {archives}")
    return archives


def get_part_lists(filtered_archives: list) -> tuple:
    """
    Get list of archives divided into parts based on commonly known patterns of parts in zip, rar and 7z archives.
    :param filtered_archives: lst of archives after filtering out these with passwords
    :return: lst with 7z parts; lst with rar parts; lst with zip parts
    """
    z_parts = []
    for a in filtered_archives:
        if "7z.0" in a:
            z_parts.append(a)

    rar_parts = []
    for a in filtered_archives:
        if ".part" in a and ".rar" in a:
            rar_parts.append(a)

    zip_parts = []
    for a in filtered_archives:
        if ".zip.0" in a:
            zip_parts.append(a)
    return z_parts, rar_parts, zip_parts


def unpack_parts(z_parts: list, rar_parts: list, zip_parts: list, dest_to_unpack: str, archives_with_pass: dict) -> None:
    """
    Unpacking archives that are divided into parts to make sure that unpacking will start from first part. It tries
    both options with or without password based on occurrence of first part in dict with archive:pass pairs.
    :param z_parts: lst with 7z parts
    :param rar_parts: lst with rar parts
    :param zip_parts; lst with zip parts
    :param dest_to_unpack: str directory for unpacking the archives
    :param archives_with_pass: dict with archives and passwords
    :return: None
    """
    for a in z_parts:
        if "7z.001" in a:
            dst = dest_to_unpack + "/" + a
            try:
                if a in archives_with_pass:
                    subprocess.run(["7z", "x", "-y", "-p" + archives_with_pass[a], "-mmt3", a, "-o" + dst], check=True)
                    print(f"wypakowano {a}")
                else:
                    subprocess.run(["7z", "x", "-y", "-mmt3", a, "-o" + dst], check=True)
                    print(f"wypakowano {a}")
            except subprocess.CalledProcessError:
                print(f"wypakowanie {a} nie powiodło się")

    for a in rar_parts:
        if ".part1.rar" in a:
            dst = dest_to_unpack + "/" + a
            try:
                if a in archives_with_pass:
                    subprocess.run(["7z", "x", "-y", "-p" + archives_with_pass[a], "-mmt3", a, "-o" + dst], check=True)
                    print(f"wypakowano {a}")
                else:
                    subprocess.run(["7z", "x", "-y", "-mmt3", a, "-o" + dst], check=True)
                    print(f"wypakowano {a}")
            except subprocess.CalledProcessError:
                print(f"wypakowanie {a} nie powiodło się")

    for a in zip_parts:
        if ".zip.001" in a:
            dst = dest_to_unpack + "/" + a
            try:
                if a in archives_with_pass:
                    subprocess.run(["7z", "x", "-y", "-p" + archives_with_pass[a], "-mmt3", a, "-o" + dst], check=True)
                    print(f"wypakowano {a}")
                else:
                    subprocess.run(["7z", "x", "-y", "-mmt3", a, "-o" + dst], check=True)
                    print(f"wypakowano {a}")
            except subprocess.CalledProcessError:
                print(f"wypakowanie {a} nie powiodło się")


def search_for_keywords(keywords: str, dest_to_unpack: str) -> None:
    """
    Running the ripgrep (rg) function for searching keywords. Search is limited to *.txt files (--type-add "txt:*.txt")
    and also find only perfect match (-w). It prints out 3 lines before and after the match and also save colored
    output with ansi formatting.
    :param keywords: str of keywords, each split with pipe (|)
    :param dest_to_unpack: str directory for unpacking the archives
    :return: None
    """
    output = subprocess.check_output(
        ["rg", "--color=ansi", keywords, "-B", "3", "-A", "3", "-w", "--type-add", "txt:*.txt", dest_to_unpack],
        stderr=subprocess.STDOUT,
        universal_newlines=True)
    with open("WYNIKI.txt", "w") as f:
        f.write(output)


def beautify_output() -> None:
    """
    Beautifying output for better user experience. Save results to *.html files in 3 categories: passwords, cookies,
    other. Works on results from *.txt file.
    :return: None
    """

    def replace_ansi_with_css(text: str, mapping: dict) -> str:
        """
        Replacing ansi tags with css tags for further conversion into html file.
        :param text: str lines from *.txt file with ansi tags
        :param mapping: mapping for converting from ansi tags into css tags
        :return: str inside css tags
        """
        if text is None:
            return ""

        for ansi_code, css_style in mapping.items():
            text = text.replace(ansi_code, f'<span style="{css_style}">')
        return text.replace("[0m", "</span>")

    def add_category(val: str) -> str:
        """
        This function is added due to the adding extra column with Category of it content based on keyword inside
        the file path.
        :param val: str from column 'Ścieżka do pliku'
        :return: str Based of resolving the if statement
        """
        if "Cookies" in val or "cookies" in val or "Cookie" in val or "cookie" in val:
            return "Cookies"
        elif "Passwords" in val or "passwords" in val or "Password" in val or "password" in val or "Pass" in val or "pass" in val:
            return "Passwords"
        else:
            return "Other"

    def get_folder_path(file_path: str) -> str:
        """
        Change file path into dir path.
        :param file_path: str with file path
        :return: str with dir path
        """
        return os.path.dirname(file_path)

    # ANSI to CSS mapping
    ansi_to_css = {
        "[30m": "color: black;",
        "[31m": "color: red;",
        "[32m": "color: green;",
        "[33m": "color: yellow;",
        "[34m": "color: blue;",
        "[35m": "color: magenta;",
        "[36m": "color: cyan;",
        "[37m": "color: white;",
        "[1m": "font-weight: bold;",
    }

    # Extract data
    with open("WYNIKI.txt", "r") as file:
        raw_content = file.read()

    lines = raw_content.splitlines()
    data = [re.split(r'(?<=\.txt)', line) for line in lines]
    df_raw = pd.DataFrame(data, columns=['Ścieżka do pliku', 'Zawartość'])

    # Clean up ANSI tags from 'Ścieżka do pliku' column
    df_raw['Ścieżka do pliku'] = df_raw['Ścieżka do pliku'].apply(lambda x: re.sub(r'\x1B\[\d+m', '', x))

    # Apply ANSI-to-CSS transformation only to the 'Zawartość' column
    df_raw['Zawartość'] = df_raw['Zawartość'].apply(lambda content: replace_ansi_with_css(content, ansi_to_css))

    # Grouping, making links and saving as HTML
    grouped = df_raw.groupby('Ścieżka do pliku')['Zawartość'].apply(
        lambda x: '<br>'.join(filter(None, x))).reset_index()
    grouped.columns = ['Ścieżka do pliku', 'Zawartość']
    grouped['Ścieżka do folderu'] = grouped['Ścieżka do pliku'].apply(get_folder_path)
    grouped['Ścieżka do pliku'] = grouped['Ścieżka do pliku'].apply(lambda x: f'<a href="{x}">{x}</a>')
    grouped['Ścieżka do folderu'] = grouped['Ścieżka do folderu'].apply(lambda x: f'<a href="{x}">{x}</a>')
    grouped['Category'] = grouped['Ścieżka do pliku'].apply(add_category)
    grouped = grouped[['Ścieżka do pliku', 'Ścieżka do folderu', 'Category', 'Zawartość']]

    for value in grouped['Category'].unique():
        subset_grouped = grouped[grouped['Category'] == value]
        subset_grouped = subset_grouped.drop(columns=['Category'])
        html_table = subset_grouped.to_html(index=False, escape=False, classes='dataframe')

        html_string = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.21/css/jquery.dataTables.css">
            <script type="text/javascript" charset="utf8" src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
            <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.21/js/jquery.dataTables.js"></script>
        </head>
        <body>

        {html_table}

        <script>
        $(document).ready( function () {{
            $('.dataframe').DataTable();
        }});
        </script>

        </body>
        </html>
        '''

        with open(f"{value}.html", "w") as f:
            f.write(html_string)


def change_permissions(dest: str) -> None:
    """
    In default after executing the script as root only root can access files, so this is why changing the permissions
    is added.
    :param: dest: str path for changin permissions
    :return: None
    """
    files = ['WYNIKI.html', 'WYNIKI.txt', 'Passwords.html', 'Cookies.html', 'Other.html']
    for elem in files:
        try:
            subprocess.run(["chmod", "777", elem], check=True)
            print(f"Zmieniono uprawnienia dla {elem}")
        except subprocess.CalledProcessError:
            print(f"Nie zmieniono uprawnień dla {elem}")

    try:
        subprocess.run(["chmod", "-R", "777", dest], check=True)
        print(f"Zmieniono uprawnienia dla {dest}")
    except subprocess.CalledProcessError:
        print(f"Nie zmieniono uprawnień dla {dest}")


def main() -> None:
    """
    Main function for launching the other functions:
        1. Match passwords witch archives
        2. Create a list of archives without passwords
        3. Create a list of parts
        4. Unpack archives without passwords from 2.
        5. Unpack parts from 3.
        6. Unpack archives with passwords from 1.
        7. Search using rg for provided keywords
        8. Beautify output and save it into *.html file
    :return: None
    """
    start_time = time.time()
    # If You want to ommit any step just comment it out
    archives_with_pass = pass_check(passwords)
    filtered_archives = filter_list(archives_with_pass)
    z_parts, rar_parts, zip_parts = get_part_lists(filtered_archives)
    unpack_without_pass(filtered_archives, dest_to_unpack)
    unpack_parts(z_parts, rar_parts, zip_parts, dest_to_unpack, archives_with_pass)
    unpack_with_pass(archives_with_pass, dest_to_unpack)
    search_for_keywords(keywords, dest_to_unpack)
    beautify_output()
    change_permissions(dest_to_unpack)
    end_time = time.time()
    exec_time = end_time - start_time
    print (f"Script execution took: {exec_time: .2f} seconds")


passwords = ["pass1", "pass2"]
dest_to_unpack = "/path/to/unpack"

# Keywords without "@". For not known reason providing keyword with @ make keyword not matching even if values inside
# files consist @ with keyword.
keywords = 'keyword1|keyword2|keyword3'

if __name__ == "__main__":
    main()
