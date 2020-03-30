class CsvWriter(object):
    def print_header(self):
        print('file_path,n,total,mean,sd,max')

    def print_stats(self, filename, stats):
        fields_of_interest = [stats.n_revs, stats.total, round(stats.mean(), 2), round(stats.sd(), 2),
                              stats.max_value()]
        printable = [str(field) for field in fields_of_interest]
        print(filename + ',' + ','.join(printable))

    def print_footer(self):
        pass
