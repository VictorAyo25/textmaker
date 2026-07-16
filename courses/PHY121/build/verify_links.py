import fitz, os
d=fitz.open('full_manual.pdf')
# Contents likely pages 2-3
total=0; goto=0; samples=[]
for i in range(1,4):
    for lk in d[i].get_links():
        total+=1
        if lk.get('kind')==fitz.LINK_GOTO:
            goto+=1
            if len(samples)<8: samples.append((i+1, lk.get('page',-1)+1))
print(f'Contents link annotations: {total}, internal GoTo links: {goto}')
print('sample (from_page -> to_page):', samples)
