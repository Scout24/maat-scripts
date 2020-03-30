import json

class JsonWriter(object):
    def __init__(self):
        self.first = True

    def print_header(self):
        print('{')

    def print_stats(self, filename, stats):
        values = {'lines': stats.n_revs, 
                  'c': stats.total, 
                  'mean': round(stats.mean(), 2),
                  'sdev': round(stats.sd(), 2),
                  'max': stats.max_value()}
        data = {filename: values}
        print((',' if not self.first else '')+'"'+filename+'": '+json.dumps(values))
        self.first = False

    def print_footer(self):
        print('}')
