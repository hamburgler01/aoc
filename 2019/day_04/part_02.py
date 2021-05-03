import itertools

pwd_count = 0

for i in range(183564, 657474 + 1):
   si = str(i)

   decrease = True
   for a, b in zip(si[:len(si) - 1], si[1:len(si)]):
       if a > b:
           decrease = False
           break;

   repeats = [len(list(g)) for k,g in itertools.groupby(si)]

   if decrease and 2 in repeats:
        pwd_count += 1

print("Password Count = ",  pwd_count)
