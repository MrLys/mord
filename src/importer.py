from password_generator import *
import secrets
import string
import re

def import_from_lastpass(location):
    # url,username,password,extra,name,grouping,fav
    import sys
    if sys.maxunicode == 65535:
        print('You have a narrow build. Bummer.')
    regex_string = '(.*),(.*),(.*),(.*),(.*),(.*),(.*)'
    db = dict()
    with open(location,'r') as ifp:
        f = ifp.read().replace('ø','oe').replace('æ','ae').replace('å','aa')
        re_compiled = re.compile(regex_string)
        matches = re_compiled.findall(f)
        for match in matches:
            entry = dict()
            entry['url'] = match[0]
            entry['username'] = match[1]
            entry['password'] = match[2]
            entry['extra'] = match[3]
            entry['grouping'] = match[5]
            entry['fav'] = match[6]
            if(len(match[4]) > 0):
                name = match[4]
                if db.get(name,''):
                    name = name + '-' + match[1][:5]
                db[name] = entry
            else:
                continue
    return db

if __name__ == '__main__':
    main()
