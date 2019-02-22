fname='files_with_unequal_no_of_columns.dat'
with open(fname) as f:
    content = f.readlines()
content = [x.strip() for x in content] 
# you may also want to remove whitespace characters like `\n` at the end of each line
