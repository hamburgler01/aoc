pwd_count = 0

for i in range(183564, 657474 + 1):
   si = str(i)

   adjacent = False
   decrease = True
   for a, b in zip(si[:len(si) - 1], si[1:len(si)]):
       if a > b:
           decrease = False
           break;
       if a == b:
           adjacent = True
   if adjacent and decrease:
        pwd_count += 1

print("Password Count = ",  pwd_count)
    
    
