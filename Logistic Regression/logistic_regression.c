#define P 1000081
#define PREF 35000
float w[P];
unsigned dun[P], cookie;
float spamminess(unsigned char *page, int n){
	unsigned i, b, h;
	cookie++;
	if (n > PREF) n = PREF;
	float score=0;
	b = (page[0]<<16) | (page[1]<<8) | page[2];
	for (i=3;i<n;i++){
		b = (b<<8) | page[i];
		h=b%
		if (dun[h] == cookie) 
			continue; 
		dun[h] = cookie;
		score += w[h];
	}
   return score;
}

#define delta 0.002
train(unsigned char *page, int n, int IsSpam){
	unsigned i, b, h;
	if (n > PREF) n = PREF;
	float p=1/(1+exp(-spamminess(page,n))); 
	cookie++;
	b = (page[0]<<16) | (page[1]<<8) | page[2]; 
	for (i=3;i<n;i++){
		b = (b<<8) | page[i];
		h=b%
		if (dun[h] == cookie) 
			continue; 
		dun[h] = cookie;
		w[h] += (IsSpam-p) * delta;
	}
 }
