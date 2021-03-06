import os


FILES_NEEDED = ["cogs.txt"]
#separator voor de blast files
SEPARATOR = "_"
JGI_ORGS = {">asp-ni" : "Aspni7",
            ">het-py" : "Hetpy1",
            ">pen-bi" : "Penbi1",
            ">pen-br" : "Penbr2",
            ">pha-ch" : "Phchr2"}

JGI_ORGS_NAMES = {">asp-ni" : "Aspergillus niger",
                  ">het-py" : "Heterogastridium pycnidioideum",
                  ">pen-bi" : "Penicillium bilaiae",
                  ">pen-br" : "Penicillium brevicompactum",
                  ">pha-ch" : "Phanerochaete chrysosporium",
                  "asp-ni" : "Aspergillus niger",
                  "het-py" : "Heterogastridium pycnidioideum",
                  "pen-bi" : "Penicillium bilaiae",
                  "pen-br" : "Penicillium brevicompactum",
                  "pha-ch" : "Phanerochaete chrysosporium",
                  "asp-cl" : "Aspergillus clavatus",
                  "eme-ni" : "Aspergillus nidulans",
                  "mag-gr" : "Magnaporthe grisea",
                  "rhi-so" : "Rhizoctonia solani",
                  "sac-ce" : "Saccharomyces cerevisea"}

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
        if not os.path.isfile("prots/{}.fa".format(x)):
            files_aanwezig = False
            missing_files.append(file)
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
    os.system("curl -s 'https://signon.jgi.doe.gov/signon/create' --data-urlencode 'login=sven@debijleveldjes.nl'" +
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

def get_pathway(orgs, proteomes):
    print("pathway tabellen aan het maken...")
    global JGI_ORGS, JGI_ORGS_NAMES
    eiwiten = [x.split(";")[0:2] for x in open("db_eiwit", "r").readlines()]
    pathway_info, pathway_koppel, pathway_ids = [], [], {}
    os.system("curl -s http://rest.kegg.jp/list/pathway -b cookies > $(pwd)/pathway_ids")
    pathway_ids_temp = [x[:-1].split("\t") for x in open("pathway_ids", "r").readlines()]
    for x in pathway_ids_temp:
        pathway_ids[x[1]] = x[0]
    for org in orgs:
        print(org)
        if org[0] == ">":
            prot_file = [x.split("|")[2] for x in open("prots/{}.fa".format(org[1:]), "r").readlines() if x[0] == ">"]
            jgi_url = "http://genome.jgi.doe.gov/ext-api/downloads/get-directory?organism={}".format(JGI_ORGS[org])
            os.system(
                "curl -s '{}' -b cookies > files.xml".format(jgi_url))
            file = open("files.xml", "r")
            directory = file.readlines()
            possible_files = []
            for dir_file in directory:
                if "KEGG" in dir_file and "tab" in dir_file:
                    possible_files.append(dir_file)
            if len(possible_files) < 1:
                print("no pathway info found for {}".format(org))
                continue
            elif len(possible_files) > 1:
                print("multiple downloads found for {}\nUsing first file\n files:".format(org))
                for x in possible_files:
                    print(x)
            path = possible_files[0].split("url=\"")[1].split("\"")[0]
            url = "http://genome.jgi.doe.gov" + path
            os.system("curl {} -s -b cookies > $(pwd)/{}_pathway.tab.gz".format(url, org[1:]))
            os.system("gunzip -q -f {}_pathway.tab.gz".format(org[1:]))
            pathway_file = [x.split("\t")for x in open("{}_pathway.tab".format(org[1:]), "r").readlines()]
            pathway_header = pathway_file.pop(0)
            for pathway in pathway_file:
                if pathway[0] in prot_file:
                    pathway_name = pathway[pathway_header.index("pathway")].strip(" ")
                    if pathway_name in pathway_ids:
                        pathway_koppel.append([pathway[0], JGI_ORGS_NAMES[org], pathway_ids[pathway_name]])
                        pathway_info.append([pathway_ids[pathway_name], pathway_name])
        else:
            uniprot_up = proteomes[org].split("proteome:")[1].split("&")[0]
            url = "http://www.uniprot.org/uniprot/?query=proteome:{}&format=tab&columns=id,pathway".format(uniprot_up)
            #os.system("echo {} > test".format(url))
            os.system("curl -s \"{}\" -b cookies > {}_pathway.tab".format(url, org))
            pathway_file = [[x.split("\t")[0]] + x[:-1].split("\t")[1].split(";") for x in open("{}_pathway.tab".format(org), "r").readlines() if len(x[:-1].split(" ")) > 2]
            for x in pathway_file:
                for y in pathway_ids:
                    if x[1].strip(" ") == y and [x[0], JGI_ORGS_NAMES[org]] in eiwiten:
                        pathway_koppel.append([x[0], JGI_ORGS_NAMES[org], pathway_ids[y]])
                        pathway_info.append([pathway_ids[y], y])



    #print(pathway_koppel[1:10])
    pathway_info = list(map(list, set(map(tuple, pathway_info))))
    #print(pathway_info[1:10])
    pathway_koppel_file = open("db_pathway_koppel", "w")
    pathway_info_file = open("db_pathway", "w")
    for x in pathway_koppel:
        pathway_koppel_file.write(";".join(x) + "\n")
    for x in pathway_info:
        pathway_info_file.write(";".join(x) + "\n")

def get_eiwit(orgs):
    print("eiwit tabel aan het maken...")
    global JGI_ORGS_NAMES
    #cogs = [x[:-1].split("\t") for x in open("cogs.txt", "r").readlines()]
    cogs_temp = [x[:-1].split("\t") for x in open("cogs.txt", "r").readlines()]
    cogs = {}
    for x in cogs_temp:
        cogs[x[1].split("|")[2] if x[1].split("|")[0] == "jgi" else x[1].split("|")[1]] = x[0]
    db_eiwit = []
    used_ids = []
    for org in orgs:
        print(org)
        found, cog, database, prot_id = False, "", "", ""
        if org[0] == ">":
            #prot = [x[:-1] for x in open("prots/{}.fa".format(org[1:]), "r") if x[0] == ">"]
            prot_file = open("prots/{}.fa".format(org[1:]), "r")
            database = "JGI"
        else:
            #prot = [x[:-1] for x in open("prots/{}.fa".format(org), "r") if x[0] == ">"]
            prot_file = open("prots/{}.fa".format(org), "r")
            database = "UNIPROT"
        prot = [x[:-1] for x in prot_file.readlines() if x not in ["", "\n"]]
        prot_current = prot.pop(0)
        prot_sequence = ""
        for x in prot:
            if x[0] == ">" and prot_sequence != "":
                if org[0] == ">":
                    prot_id = prot_current.split("|")[2]
                else:
                    prot_id = prot_current.split("|")[1]
                cog = cogs[prot_id] if prot_id in cogs else "NULL"
                prot_list = [prot_id, JGI_ORGS_NAMES[org], database, cog, prot_sequence]
                db_eiwit.append(prot_list)
                used_ids.append(prot_list)
                prot_current = x
                prot_sequence = ""
            else:
                prot_sequence += x
        cog = cogs[prot_id] if prot_id in cogs else "NULL"
        if org[0] == ">":
            prot_id = prot_current.split("|")[2]
        else:
            prot_id = prot_current.split("|")[1]
        prot_list = [prot_id, JGI_ORGS_NAMES[org], database, cog, prot_sequence]
        db_eiwit.append(prot_list)
        used_ids.append(prot_list)




    db_eiwit_file = open("db_eiwit", "w")
    for x in db_eiwit:
        db_eiwit_file.write(";".join(x) + "\n")

def get_blasts(orgs):
    print("blast tabel aan het maken...")
    global SEPARATOR, JGI_ORGS_NAMES
    db_blast = []
    for org1 in orgs:
        for org2 in orgs:
            if org1 != org2:
                blasts = [x[:-1] for x in open("blasts/{}{}{}".format(org1, SEPARATOR, org2), "r").readlines()]
                for blast in blasts:
                    temp_blast = []
                    blast = blast.split("\t")
                    if blast[0].split("|")[0] == "jgi":
                        temp_blast.append(blast[0].split("|")[2])
                    else:
                        temp_blast.append(blast[0].split("|")[1])
                    temp_blast.append(JGI_ORGS_NAMES[org2])
                    if blast[1].split("|")[0] == "jgi":
                        temp_blast.append(blast[1].split("|")[2])
                    else:
                        temp_blast.append(blast[1].split("|")[1])
                    temp_blast.append(JGI_ORGS_NAMES[org1])
                    db_blast.append(temp_blast)
    db_blast_file = open("db_blast", "w")
    db_blast = list(map(list, set(map(tuple, db_blast))))
    for x in db_blast:
        line = ";".join(x) + "\n"
        db_blast_file.write(line)

def remove_file(filename):
    if os.path.isfile(filename):
        os.system("rm {}".format(filename))

def clean_files(orgs):
    print("onnodige files verwijderen...")
    files = ["pathway_ids", "cookies", "files.xml", "test"]
    for file in files:
        remove_file(file)
    for org in orgs:
        remove_file("{}_pathway.tab".format(org))

def main():
    proteomes, orgs = get_proteomes()
    clean_orgs = []
    for x in orgs:
        if x[0] == ">":
            clean_orgs.append(x[1:])
        else:
            clean_orgs.append(x)
    if check_files(clean_orgs):
        get_eiwit(orgs)
        get_pathway(orgs, proteomes)
        get_blasts(clean_orgs)
        clean_files(clean_orgs)
        print("database files gemaakt!")



main()
