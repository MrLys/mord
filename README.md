# Mord the password manager.
This is a very simple password manager made as a fun side project. It is fittingly named after the
petty, dimwitted and cruel turnkey from [A Song of Ice and Fire].

[A Song of Ice and Fire]: http://gameofthrones.wikia.com/wiki/Mord

## Install
Clone repository, navigate to project folder.
1. Install pip3 if you have not already.
2. Run
```bash
pip3 install pycryptodome pyperclip
```
3. Add this to your bashrc file.
```bash
export MORD_HOME='<Path-To-mord>'
```

## Usage
### Using python/ipython shell:
```python
import database
a = database.database('<Path-To-database-file>') # Can be empty, but must exist
a.add()
a.save()
```
If you want to migrate from lastpass:

```python
import database
a = database.database('<Path-To-database-file>') # Can be empty, but must exist
a.import_from_lastpass('<Path-To-lastpass-database-file>')
a.save()
```

### Running the mord application
Just navigate to the src folder.
```bash
python3 mord.py
```

# Q&A

* Is it secure? Given a sufficiently complex password, that is not forgotten, one can assume that the
passwords are safely stored locally. It uses AES CBC mode with a 256 bit key, and sha512 for the
password digest.
* When decrypted in memory can it then be accessed by a malicious actor? Probably, but if your
  machine has been breached and someone with malicious intent can access its memory, a different
  password manager wouldn't have done any better.


# TODO
- [ ] Make openssl compatible. Changing from pyCrypto to pyCryptoDome broke the compatibility.
- [ ] Improve interface/options.
- [ ] Add update option.
- [ ] Improve duplicate entry handler.
- [ ] Fix problem with saving backup database.
- [ ] Make the output from the list command into a `|less` like view.
- [ ] Make possible to type `q` or `x` to exit the password/entry viewing screen.
- [ ] Make possible to enter non-existing file, and create it.
- [ ] Make possible to import from 1password.
- [ ] Make possible to import from KeePass.
- [ ] Make possible to import from Dashlane.
