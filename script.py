dictVithVacancies = {}

def main():
    def write_chunk(part, lines):
        with open('newCSV//data_part_'+ str(part) +'.csv', 'w', encoding="utf-8-sig") as f_out:
            f_out.writelines(lines)
            f_out.close()
    
    with open('vacancies_by_year.csv', 'r', encoding="utf-8-sig") as fi_le:
        names = fi_le.readline()
        for string in fi_le:
            year = string.split(",")[len(string.split(",")) - 1][0:4]
            if(year in dictVithVacancies.keys()):
                dictVithVacancies[year].append(string)
            else: 
                dictVithVacancies[year] = [names, string]

        if len(dictVithVacancies) > 0:
            for vacancie in dictVithVacancies:
                write_chunk(vacancie, dictVithVacancies[vacancie])

if __name__ == '__main__':
    main()
