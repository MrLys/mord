from mord_crypto import *
from mord_utils import *
import yaml
import importer

class database():
    def __init__(self, db_location):
        self.db_location = db_location
        ret = self.__read_db()
        if ret  < 0:
            print("Could not initiate database!")
            return None
        elif ret == 0:
            if self.__decrypt_db() < 0:
                raise EOFError


    def __decrypt_db(self):
        db_password = safe_getpass("Database password:")
        if db_password == -1:
            print("Could not initiate database")
            return -1
        self.__db = decrypt(self.encrypted_db,db_password)
        if not self.__verify_password():
            self.__decrypt_db()

    def __read_db(self):
        try:
            with open(self.db_location,'r+') as in_file:
                raw_data = in_file.read().replace('\n', '')
                if len(raw_data) > 0:
                    self.__encrypted_backup = raw_data
                    self.encrypted_db = raw_data
                else:
                    self.new_database()
                    return 1
        except FileNotFoundError as efnf:
            print(efnf)
            return -1
        return 0

    def __verify_password(self):
        try:
            self.__db  = yaml.load(self.__db)
            if self.__db is None:
                print("Incorrect password or empty database!")
                return False
            return True
        except yaml.YAMLError as exc:
            print("Incorrect password!")
            return False
        except UnicodeError as ude:
            print("Incorrect password!")
            return False

    def find(self, name):
        return self.__db.get(name,'')

    def add(self, name, entry):
        if not db.find(entry['name']) is '':
            self.__db[entry['name']] = entry
        else: # make sure to not overwrite existing entry.
            # TODO. Implement a better solution.
            self.add(self,name + entry['username'][:5], entry)

    def get_keys(self):
        for key in self.__db:
            print(key)

    def save(self):
        if not self.__db:
            print("No database to save")
            return
        db_password = safe_getpass("Database password:")
        if db_password == -1:
            print("Could not save database")
            return -1
        verify_db_password = safe_getpass("Verify database password:")
        if not db_password == verify_db_password:
            print("Passwords did not match, please try again!")
            return self.save()

        encrypted_db = encrypt(self.__db,db_password)
        try:
            if self.__encrypted_backup:
                with open(self.db_location+'_backup','wb') as out:
                    out.write(self.__encrypted_backup)
        except TypeError as ete:
            print(ete)
            print("Something went wrong with saving backup database")
        with open(self.db_location,'wb') as out:
            out.write(encrypted_db)

    def new_database(self):
        print("Created new database")
        self.__encrypted_backup = dict()
        self.__db = dict()

    def import_from_lastpass(self, location):
        new_data = importer.import_from_lastpass(location)
        self.__db.update(new_data)

