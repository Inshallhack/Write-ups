flagCrypted = [160,155,208,160,190,215,237,134,210,126,212,222,224,238,128,240,164,213,183,192,162,178,163,162]

def crypt(a,b):
	return a + (b ^ 21)

flagInput=input()

fnc=lambda a,b:a+(b^21)

flagInputChrs = list(map(ord,flagInput)) #convert input to char array

flagInputCrypted = [crypt(*chrs) for chrs in zip(flagInputChrs,flagInputChrs[::-1])]

flagInputCrypted = flagInputCrypted[::-1] #flip array

if flagInputCrypted == flagCrypted:
	if 'mo4r' in flagInput and '34C3_' in flagInput: 
		if flagInput.split('_')[3] == 'tzzzz':
			print('Correct!')
else:
	print('Almost!!')
