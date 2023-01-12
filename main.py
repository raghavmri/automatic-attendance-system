import time
a = []
b = []
for i in range(1000000):  # Adding 1000000 element to both the lists
    a.append(i)
    b.append(i+10)

start_time = time.time()
c = a+b # Adding The lists using + operator
print("Time Taken To Concatenate using + Operator {}s".format(round(time.time()-start_time, 4)))

start_time = time.time()
d = a.extend(b) # Adding the lists using the extend method
print("Time Taken To Concatenate using extend Method {}s".format(
    round(time.time()-start_time, 4)))

start_time = time.time()
for i in b: # Adding the lists using the for loop
    a.append(i)
print("Time Taken To Concatenate using For Loop Method {}s".format(
    round(time.time()-start_time, 4)))
