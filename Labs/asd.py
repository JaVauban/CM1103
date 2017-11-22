def sqrt(s, acc):
	x = s
	for i in range(acc):
		x = 0.5 * (x + s/x)
	return x
    
print(sqrt(49, 10))
print(sqrt(49, 50))
print(sqrt(30, 15))
print(sqrt(-64, 10))