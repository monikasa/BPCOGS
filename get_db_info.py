import os


FILES_NEEDED = ["cogs.txt"]
#separator voor de blast files
SEPARATOR = "_"


def get_proteomes():
    proteoom_list = {}
    JGI_connect()
    # Aspergillus clavatus
    proteoom_list[
        "asp-cl"] = "http://www.uniprot.org/uniprot/?query=proteome:UP000006701&force=no&limit=no&format=fasta"
    # Aspergillus(of Emericella) nidulans
    proteoom_list[
        "eme-ni"] = "http://www.uniprot.org/uniprot/?query=proteome:UP000000560&force=no&limit=no&format=fasta"
    # Aspergillus niger
    proteoom_list[">asp-ni"] = download_JGI_proteome("Aspni7")
    # Heterogastridium pycnidioideum
    proteoom_list[">het-py"] = download_JGI_proteome("Hetpy1")
    # Magnaporthe grisea
    proteoom_list[
        "mag-gr"] = "http://www.uniprot.org/uniprot/?query=proteome:UP000009058&force=no&limit=no&format=fasta"
    # Penicillium bilaiae
    proteoom_list[">pen-bi"] = download_JGI_proteome("Penbi1")
    # Penicillium brevicompactum
    proteoom_list[">pen-br"] = download_JGI_proteome("Penbr2")
    # Phanerochaete chrysosporium
    proteoom_list[">pha-ch"] = download_JGI_proteome("Phchr2")
    # Rhizoctonia solani
    proteoom_list[
        "rhi-so"] = "http://www.uniprot.org/uniprot/?query=proteome:UP000044841&force=no&limit=no&format=fasta"
    # Saccharomyces cerevisiae
    proteoom_list[
        "sac-ce"] = "http://www.uniprot.org/uniprot/?query=proteome:UP000002311&force=no&limit=no&format=fasta"


    return (proteoom_list, proteoom_list.keys())


def check_files(orgs):
    global FILES_NEEDED, SEPARATOR
    files_aanwezig = True
    missing_files = []
    for x in FILES_NEEDED:
        if not os.path.isfile(x):
            files_aanwezig = False
            missing_files.append(x)
    for x in orgs:
        for y in orgs:
            if x != y:
                file = "blasts/" + x + SEPARATOR + y
                if not os.path.isfile(file):
                    files_aanwezig = False
                    missing_files.append(file)
    if not files_aanwezig:
        print("een paar nodige bestanden zijn niet gevonden")
        print("afwezig:")
        for x in missing_files:
            print(x)
        return False
    return True

def JGI_connect():
    print("logging in to JGI")
    os.system("curl 'https://signon.jgi.doe.gov/signon/create' --data-urlencode 'login=sven@debijleveldjes.nl'" +
              " --data-urlencode 'password=bpcogs1617' -c cookies > /dev/null")

def download_JGI_proteome(org):
    print("donwloading file list of {}".format(org))
    os.system(
        "curl -s 'http://genome.jgi.doe.gov/ext-api/downloads/get-directory?organism=" + org + "' -b cookies > files.xml")
    file = open("files.xml", "r")
    directory = file.readlines()
    subdir = []
    for line in directory:
        if "all_proteins" in line and "GeneCatalog" in line:
            subdir.append(line)
    # print("~~~~subdir has", len(subdir), "items~~~~")
    if len(subdir) == 1:
        path = subdir[0].split("url=\"")[1].split("\"")[0]
        return ("http://genome.jgi.doe.gov" + path)
    elif len(subdir) == 0:
        print("could not find a donwload!!!!")
        print("trying to find a different donwload")
        second_test = []
        for x in directory:
            if "protein" in x and "aa" in x and int(x.split("size=\"")[1].split()[0]) < 100:
                print("found another download")
                second_test.append(x)
                print(x)
        if len(second_test) != 0:
            return("http://genome.jgi.doe.gov" + second_test[0].split("url=\"")[1].split("\"")[0])
        else:
            print("could not find any file with the names portein and filtered")
            return("error")
    else:
        print("there are multiple downloads!!!!")
        print("Downloads:")
        for x in subdir:
            print(x)
            print("choosing first flle for donwload")
        path = subdir[0].split("url=\"")[1].split("\"")[0]
        return ("http://genome.jgi.doe.gov" + path)

def get_pathway(orgs):
    pathway_info = []
    pathway_koppel = []
    os.system("curl http://rest.kegg.jp/list/pathway -b cookies > $(pwd)/pathway_ids")
    pathway_ids = [x.split("\t") for x in open("pathway_ids", "r").readlines()]
    for org in orgs:
        if org[0] == ">":
            prot_file = [x.split("|")[2] for x in open("prots/{}.fa".format(org[1:]), "r").readlines() if x[0] == ">"]
            os.system(
                "curl -s 'http://genome.jgi.doe.gov/ext-api/downloads/get-directory?organism=" + org + "' -b cookies > files.xml")
            file = open("files.xml", "r")
            directory = file.readlines()
            possible_files = []
            for dir_file in directory:
                if "KEGG" in dir_file and "tab" in dir_file:
                    possible_files.append(dir_file)
            if len(possible_files) < 1:
                print("no pathway info found for {}".format(org))
                break
            elif len(possible_files) > 1:
                print("multiple downloads found for {}\nUsing first file\n files:".format(org))
                for x in possible_files:
                    print(x)
            path = possible_files[0].split("url=\"")[1].split("\"")[0]
            url = "http://genome.jgi.doe.gov" + path
            os.system("curl {} -b cookies > $(pwd)/{}_pathway.tab.gz".format(url, org[1:]))
            os.system("gunzip -q {}_pathway.tab.gz".format(org[1:]))
            pathway_file = open("{}_pathway.tab".format(org[1:]), "r").readlines()
            pathway_header = pathway_file.pop(0).split("\t")
            for prot in prot_file:
                for pathway in pathway_file:
                    test = pathway.split("\t")
                    if prot == test[0]:
                        pathway_name = test[pathway_header.index("pathway")]
                        found = False
                        for x in pathway_ids:
                            if pathway_name == x[1]:
                                pathway_koppel.append(prot, x[0])
                                pathway_info.append([x])
    print(pathway_koppel[1:10])
    print(list(set(pathway_info))[1:10])



def main():
    JGI_connect()
    proteomes, orgs = get_proteomes()
    clean_orgs = []
    for x in orgs:
        if x[0] == ">":
            clean_orgs.append(x[1:])
        else:
            clean_orgs.append(x)
    if check_files(clean_orgs):
        get_pathway(orgs)


main()