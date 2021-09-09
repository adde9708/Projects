lst = ['How', 'do', 'you', 'do']
print()
print('Here is the list:')
print(' '.join(lst))
print()
print('Here we print various subsets of the list')
print(' '.join(lst[:3]))
print(' '.join(lst[1:]))
print(' '.join(lst[::2]))
print(' '.join(lst[::3]))

print()

print('Here we print the entire list one item at a time')
for item in lst:
    print(item)
