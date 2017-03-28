def main():
    cog = input("voer een cog in:")
    cogs = [x[:-1].split(";") for x in open("db_eiwit", "r").readlines()]
    fasta = []
    for x in cogs:
        if x[3] == cog:
            seq = x.pop(4)
            fasta.append(">" + "|".join(x) + "\n")
            line_length = 70
            for y in range(0, len(seq), line_length):
                fasta.append(seq[y:y+line_length] + "\n")
    fasta_file = open("cog_{}.fa".format(cog), "w")
    for x in fasta:
        fasta_file.write(x)

main()