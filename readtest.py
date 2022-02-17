fname = 'testlist.txt'
count = 0
with open(fname) as fp:
    line = fp.readline()
    while line:
        count += 1
        # print(line.strip())
        line = fp.readline()

file = open(fname, 'r')

wordbank = [line.strip() for line in file if len(line.strip())==5]


print(wordbank)
print(count==len(wordbank))


#
# file = open(fname, 'r')
# wordbank = [line for line in file if (len(line) == 5)]
# for line in file:
#     line.strip()
#     print("z")
#     print(type(line))
#
# print (counter)
# print (len(wordbank))
# file.close()