```
import json, ssdeep

text = open('file-20171020T1500').read()

data = [json.loads(x) for x in text.split('\n')]  

number = {}


for i in range(len(data)):	
	number[str(i)] = data[i]['positives']


numberr = sorted(number.items(), key=lambda x:x[1], reverse=True)

index = int(numberr[3][0])


high = [0,'']
for i in range(len(data)):
	if i != index:
		fuzza = data[index]['ssdeep']
		fuzzb = data[i]['ssdeep']
		try:
			score = ssdeep.compare(fuzza,fuzzb)
			if score > high[0]:
				high[0] = score
				high[1] = data[i]['md5']
		except Exception as e:
			pass
		

print str(high[0])+":"+high[1]
#74:58eecc3d74637728a102f43072b49502
```
