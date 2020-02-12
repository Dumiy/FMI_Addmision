import requests
import PyPDF2
import wget

def year_filter(variable):
    years = ['2016','2017','2018','2019']
    category = ['info', 'mate']
    license = ['admitere/licenta']
    type = ['admisi','asteptare','respinsi']
    if any(True if x in variable else False for x in years ) \
           and license[0] in variable \
           and any(True if x in variable else False for x in type) \
           and any(True if x in variable else False for x in category):
        return True
    else:
        return False

class document:
    def __init__(self,link,site):
        self.url = link
        self.content = []
        self.uri = site
    def __verify__(self):
        if self.url is None:
            return False
        return True
    def __start_parse__(self):
        if self.__verify__() is True:
            get_request = requests.get(self.url)
            self.content = str(get_request.content).split('\\n')
    def __sanitize__(self):
        if self.content is not None:
            self.content = map(lambda x: x[x.index('|')+1:-1],self.content)
            self.content = filter(year_filter,self.content)
        else:
            raise ('No input from the site')
    def output_parsed(self):
        for x in self.content:
            print(x)
    def categorize_data_and_donwload(self):
        self.dictionary = {'info':[[],[],[]],'mate':[[],[],[]]}
        path = './files'
        for x in self.content:
            try:
                if 'info' in x:
                    if 'buget' in x:
                        self.dictionary['info'][0].append(x)
                        wget.download(self.uri+ '/' + x,path+'/info/buget/' )
                    elif 'taxa' in x or 'TAXA' in x :
                        self.dictionary['info'][1].append(x)
                        wget.download(self.uri + '/' + x, path + '/info/taxa/')
                    else:
                        self.dictionary['info'][2].append(x)
                        wget.download(self.uri + '/' + x, path + '/info/altele/')
                if 'mate' in x:
                    if 'buget' in x:
                        self.dictionary['mate'][0].append(x)
                        wget.download(self.uri + '/' + x, path + '/mate/buget/')
                    elif 'taxa' in x or 'TAXA' in x :
                        self.dictionary['mate'][1].append(x)
                        wget.download(self.uri + '/' + x, path + '/mate/taxa/')
                    else:
                        self.dictionary['mate'][2].append(x)
                        wget.download(self.uri + '/' + x, path + '/mate/altele/')
            except Exception:
                print('It happened, ERROR at file ',x)
                continue

test = document('http://fmi.unibuc.ro/ro/documente.txt','http://fmi.unibuc.ro/ro')
test.__start_parse__()
test.__sanitize__()
test.categorize_data_and_donwload()
