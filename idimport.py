from assessment_app.models import IDNumbers

import csv

with open("import.csv", "r") as f:
    a = csv.reader(f)

    for i in a: 
        print(i[0])
        new = IDNumbers(idnum=i[0])
        new.save()