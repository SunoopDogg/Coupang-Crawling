import csv

product_id = input('product_id: ')
user_id = input('user id: ')

review_list = []

with open('reviews\\'+product_id+'.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    for row in reader:
        review_list.append(row)

find_user = [review for review in review_list if review[1] == user_id]

if (len(find_user) == 0):
    print('No user')
else:
    print('User found')
    print('name:', find_user[0][0])
    print('id:', find_user[0][1])
    print('date:', find_user[0][2])
    print('star:', find_user[0][3])
