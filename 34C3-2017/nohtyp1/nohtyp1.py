alphabet = [chr(n) for n in range(48,58)] + [chr(n) for n in range(65,91)] + [chr(n) for n in range(97,123)] + [chr(95)]
verif = [160,155,208,160,190,215,237,134,210,126,212,222,224,238,128,240,164,213,183,192,162,178,163,162]

def crypt(a,b):
	return a + (b ^ 21)

flaglength = len(verif) #24


start = "34C3_mo4r_"
end = "tzzzz" #tzzzz, remove _ for test my code

unknow = "X" * (flaglength - len(start) - len(end))

for i in range(10):
	found = False
	for c in alphabet:
		l = len(unknow)
		unknow = unknow[:l-1] + c

		pattern = start + unknow + end
		patternChrs = list(map(ord,pattern))
		lvl1 = [crypt(*chrs) for chrs in zip(patternChrs,patternChrs[::-1])]
		if lvl1[::-1][len(end)] == verif[len(end)]:
			#print(start + unknow + end)
			end = c + end
			unknow = unknow[:l-1]
			found = True
			break
	if found == False:
		break

'''
here the flag looks like 34C3_mo4r_XXXX4kes_tzzzz
I guess the n before 4kes and I found the s after mo4r_ with the same code at the top.

Now I can't go further I need some "brute force" :
'''

start = "34C3_mo4r_s"
end = "n4kes_tzzzz"

unknow = "XX"

for j in alphabet:
	for c in alphabet:
		unknow = j+c

		pattern = start + unknow + end
		patternChrs = list(map(ord,pattern))
		lvl1 = [crypt(*chrs) for chrs in zip(patternChrs,patternChrs[::-1])]
		flag = start + unknow + end
		if lvl1[::-1][len(start)] == verif[len(start)] and flag.split('_')[3] == 'tzzzz':
			print(flag)

'''
I got 20 uniq possibles flag:

34C3_mo4r_sajn4kes_tzzzz
34C3_mo4r_sbgn4kes_tzzzz
34C3_mo4r_schn4kes_tzzzz
34C3_mo4r_sdmn4kes_tzzzz
34C3_mo4r_senn4kes_tzzzz
34C3_mo4r_sfkn4kes_tzzzz
34C3_mo4r_sgln4kes_tzzzz
34C3_mo4r_shan4kes_tzzzz
34C3_mo4r_sibn4kes_tzzzz
34C3_mo4r_slen4kes_tzzzz
34C3_mo4r_smfn4kes_tzzzz
34C3_mo4r_sncn4kes_tzzzz
34C3_mo4r_sodn4kes_tzzzz
34C3_mo4r_spyn4kes_tzzzz
34C3_mo4r_sqzn4kes_tzzzz
34C3_mo4r_srwn4kes_tzzzz
34C3_mo4r_ssxn4kes_tzzzz
34C3_mo4r_sxqn4kes_tzzzz
34C3_mo4r_syrn4kes_tzzzz
34C3_mo4r_szon4kes_tzzzz

but only 34C3_mo4r_schn4kes_tzzzz looks likes to be good "moar schnakes tzzzz"
'''