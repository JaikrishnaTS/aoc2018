
claims = []

maxx, maxy = 0, 0
with open('inp3.txt') as f:
    for claim_line in f:
        cid, _, pos, size = claim_line.split()
        posx, posy = map(int, pos[:-1].split(','))
        sizex, sizey = map(int, size.split('x'))
        maxx = max(maxx, posx + sizex)
        maxy = max(maxy, posy + sizey)
        claims.append((posx, posy, sizex, sizey))

mat = [[0] * maxy for _ in range(maxy)]

for posx, posy, sizex, sizey in claims:
    for y in range(posy, posy + sizey):
        for x in range(posx, posx + sizex):
            mat[y][x] += 1

multiple = sum(1 for line in mat for c in line if c > 1)
print(multiple)

for cid, cline in enumerate(claims, 1):
    posx, posy, sizex, sizey = cline
    if all(mat[y][x] == 1 
           for y in range(posy, posy + sizey) 
           for x in range(posx, posx + sizex)):
        print(cid)
