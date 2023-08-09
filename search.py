import os
import subprocess
# import yaml


def get_list_of_archives():
    arch_list = os.listdir()
    return arch_list


def check_password(archive, password):
    try:
        output = subprocess.check_output(["7z", "t", "-p" + password, archive], stderr=subprocess.STDOUT,
                                         universal_newlines=True)
        return "Everything is Ok" in output
    except subprocess.CalledProcessError:
        return False


# def create_dir(arch_name):
#     try:
#         os.mkdir(arch_name)
#     #    except FileExistsError:
#     #        os.mkdir(arch_name+"_")
#     except OSError as e:
#         print(f"Nie można utworzyc folderu {arch_name}")


def unpack_with_pass(dict_arch_pass, dest_to_unpack):
    for archive, password in dict_arch_pass.items():
        dst = dest_to_unpack + "/" + archive
        # create_dir(archive)
        print(archive, password)
        try:
            subprocess.run(["7z", "x", "-y", "-p" + password, archive, "-o" + dst], check=True)
            print(f"wypakowano {archive}")
        except subprocess.CalledProcessError:
            print(f"wypakowanie {archive} nie powiodło się")


# def main(passwords):
#    with open("confirmed.txt", "w") as confirmed_file, open("failed.txt", "w") as failed_file:
#        passwords = passwords
#        dict_arch_pass = {}
# with open("passwords.yaml", "r") as passwords_file:
# passwords = [line.strip() for line in passwords_file]

#        for archive in os.listdir("."):
#            if archive.endswith(".7z") or archive.endswith(".rar"):
#                for password in passwords:
#                    if check_password(archive, password):
#                        confirmed_file.write(f"{archive} : {password}\n")
#                        dict_arch_pass[archive] = password

#                        break
#                else:
#                    failed_file.write(f"{archive}\n")
#    print(dict_arch_pass)

def pass_check(passwords):
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


def filter_list(arch_list_raw):
    archives = get_list_of_archives()
    for a in arch_list_raw.keys():
        if a in archives:
            archives.remove(a)
    print(archives)
    return archives


def get_part_lists(content):
    z_parts = []
    for a in content:
        if "7z.0" in a:
            z_parts.append(a)

    rar_parts = []
    for a in content:
        if ".part" in a and ".rar" in a:
            rar_parts.append(a)
    return z_parts, rar_parts


def unpack_parts(z_parts, rar_parts, dest_to_unpack, archives_with_pass):
    for a in z_parts:
        if "7z.001" in a:
            dst = dest_to_unpack + "/" + a
            try:
                if a in archives_with_pass:
                    subprocess.run(["7z", "x", "-y", "-p" + archives_with_pass[a], a, "-o" + dst], check=True)
                    print(f"wypakowano {a}")
                else:
                    subprocess.run(["7z", "x", "-y", a, "-o" + dst], check=True)
                    print(f"wypakowano {a}")
            except subprocess.CalledProcessError:
                print(f"wypakowanie {a} nie powiodło się")

    for a in rar_parts:
        if "part1.rar" in a:
            dst = dest_to_unpack + "/" + a
            try:
                if a in archives_with_pass:
                    subprocess.run(["7z", "x", "-y", "-p" + archives_with_pass[a], a, "-o" + dst], check=True)
                    print(f"wypakowano {a}")
                else:
                    subprocess.run(["7z", "x", "-y", a, "-o" + dst], check=True)
                    print(f"wypakowano {a}")
            except subprocess.CalledProcessError:
                print(f"wypakowanie {a} nie powiodło się")


# def get_rid_fo_unnecessary_files(dest_to_unpack):
#     TMP_DIR = "/path/to/archives/tmp"
#     os.mkdir("tmp")
#     command = f'find "{dest_to_unpack}" -type f ! -name "*.txt" ! -name "*.TXT" ! -name "*.jpg" -exec rm {{}} \\;'
#
#     try:
#         subprocess.run(command, shell=True, check=True)
#         print("Pomyślnie wykonano komendę.")
#     except subprocess.CalledProcessError as e:
#         print(f"Wystąpił błąd podczas wykonania komendy: {e}")


passwords = ["123", "log", "xls", "zip", "qwe", "log1234"]

dest_to_unpack = "/path/to/archives/wypakowane"

keywords = 'keyword1|keyword2|keyword3'


def search_for_keywords(keywords, dest_to_unpack):
    output = subprocess.check_output(["rg", keywords, "-B", "2", "-A", "2", "-w", "--type-add", "txt:*.txt", dest_to_unpack], stderr=subprocess.STDOUT,
                                     universal_newlines=True)
    with open("/path/to/archives/WYNIKI.txt", "w") as f:
        f.write(output)


def beautify_output():
    with open('WYNIKI.txt', 'r') as input_file:
        lines = input_file.readlines()

    with open('WYNIKI.html', 'w') as output_file:
        # output_file.write('<html><head><title>Wyniki wyszukiwania</title></head><body><table>\n')
        # output_file.write('<tr><th>Ścieżka do pliku</th><th style="text-align: left;">Zawartość pliku</th></tr>\n')

        output_file.write(
            '<html><head><title>Wyniki wyszukiwania</title></head><body><table style="border-collapse: collapse; border: 1px solid black;">\n')
        output_file.write(
            '<tr><th style="border: 1px solid black;">Ścieżka do pliku</th><th style="border: 1px solid black; text-align: left;">Zawartość pliku</th></tr>\n')

        for line in lines:
            line = line.strip()
            parts = line.split('.txt', 1)
            if len(parts) > 1:
                # output_file.write(f'<tr><td><a href="{parts[0]}.txt">{parts[0]}.txt</a></td><td>{parts[1]}</td></tr>\n')

                output_file.write(
                    f'<tr><td style="border: 1px solid black;"><a href="{parts[0]}.txt">{parts[0]}.txt</a></td><td style="border: 1px solid black; text-align: left;">{parts[1]}</td></tr>\n')

        output_file.write('</table></body></html>\n')


def main():
    archives_with_pass = pass_check(passwords)
    filtered_archives = filter_list(archives_with_pass)
    z_parts, rar_parts = get_part_lists(filtered_archives)
    unpack_parts(z_parts, rar_parts, dest_to_unpack, archives_with_pass)
    unpack_with_pass(archives_with_pass, dest_to_unpack)
    #get_rid_fo_unnecessary_files(dest_to_unpack)
    search_for_keywords(keywords, dest_to_unpack)
    beautify_output()


if __name__ == "__main__":
    main()
