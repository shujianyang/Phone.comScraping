import json

input = open('PhoneNumsCan.json', 'r')
phone_list = json.load(input)

for loc, nums in phone_list:
    found = False
    for n in nums:
        if n[1:4] == '705':
            if not found:
                print(loc)
                found = True
            print(n)
    if found: print()

input.close()
print('Search completed.')
