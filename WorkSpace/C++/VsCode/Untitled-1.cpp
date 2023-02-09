void back(i) {

if (i ==n) 

show

return

C = {1, 2,…n} \ {a1, a2, ..ai} 

for (c in C) {

a[i+1] = c;

back(i+1)

}

used[n] = false

void back(i) {

if  (i ==n) 

show 

return 

for (c = 1, c< N; c++) {

if( used[c] == false) {

a[i+1] = c

used[i+1] = true

back(i+1)

used[c] = false

}