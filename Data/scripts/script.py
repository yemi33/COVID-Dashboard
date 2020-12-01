import zipfile
import os
import fnmatch
import shutil
import pandas as pd

#--------------code------------------
print ("hello world!")
os.system("rm -r nssac-ncov-data-country-state")
with zipfile.ZipFile('nssac-ncov-data-country-state.zip', 'r') as zip_ref:
        zip_ref.extractall()
os.chdir(r"nssac-ncov-data-country-state")
files = [f for f in os.listdir("./") if f.endswith(".csv")]
for i in files:
    print(i)
    data = pd.read_csv(i)
    newdata = data.rename(columns ={'Last Update' : 'Date'})
    newdata = newdata.reset_index(drop=True)
    newname = i[14:]
    newname = "a" + newname.replace("-", "_")
    newdata.to_csv(newname, header = False, index = False)
    os.remove(i)
os.remove("README.txt")
os.system("echo hello")
files_csv = [f for f in os.listdir("./") if f.endswith(".csv")]
os.chdir(r"..")
#shutil.move("table.sql" , "nssac-ncov-data-country-state/" + files_csv[0] + ".sql")
os.chdir(r"nssac-ncov-data-country-state")
os.system("psql -c 'DROP TABLE IF EXISTS alltables'")
os.system("psql -c  'CREATE TABLE alltables ( place varchar, region varchar, Date varchar, confirmed int, death int, recovered int );'")
for i in files_csv:
    name = i[:-4]
    os.system("psql -c 'DROP TABLE IF EXISTS '" + name +"';'")
    os.system("psql -c  'CREATE TABLE '" + name + "'( place varchar, region varchar, Date varchar, confirmed int, death int, recovered int );'")
    os.system('psql -c "\copy "'+ name +'" FROM "' + i + '" DELIMITER \',\' CSV"')
    os.system('psql -c "\copy alltables FROM "' + i + '" DELIMITER \',\' CSV"')


                                                                    
