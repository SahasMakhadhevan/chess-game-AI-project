from board.move import move
from pieces.nullpiece import nullpiece
from pieces.queen import queen
import random

class AI:

    global tp
    tp=[]


    def __init__(self):
        pass


    def evaluate(self,gametiles):
        min=100000
        count=0
        count2=0
        chuk=[]
        movex=move()
        tp.clear()
        xp=self.minimax(gametiles,3,-1000000000,1000000000,False)

        for zoom in tp:
            if zoom[4]<min:
                chuk.clear()
                chuk.append(zoom)
                min=zoom[4]
            if zoom[4]==min:
                chuk.append(zoom)
        fx=random.randrange(len(chuk))
        print(tp)
        return chuk[fx][0],chuk[fx][1],chuk[fx][2],chuk[fx][3]


    def reset(self,gametiles):
        for x in range(8):
            for y in range(8):
                if gametiles[x][y].pieceonTile.tostring()=='k' or gametiles[x][y].pieceonTile.tostring()=='r':
                    gametiles[x][y].pieceonTile.moved=False


    def updateposition(self,x,y):
        a=x*8
        b=a+y
        return b

    def checkmate(self,gametiles):
        movex=move()
        if movex.checkw(gametiles)[0]=='checked':
            array=movex.movesifcheckedw(gametiles)
            if len(array)==0:
                return True

        if movex.checkb(gametiles)[0]=='checked' :
            array=movex.movesifcheckedb(gametiles)
            if len(array)==0:
                return True

    def stalemate(self,gametiles,player):
        movex=move()
        if player==False:
            if movex.checkb(gametiles)[0]=='notchecked':
                check=False
                for x in range(8):
                    for y in range(8):
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                            lx1=movex.pinnedb(gametiles,moves1,y,x)
                            if len(lx1)==0:
                                continue
                            else:
                                check=True
                            if check==True:
                                break
                    if check==True:
                        break

                if check==False:
                    return True

        if player==True:
                if movex.checkw(gametiles)[0]=='notchecked':
                    check=False
                    for x in range(8):
                        for y in range(8):
                            if gametiles[y][x].pieceonTile.alliance=='White':
                                moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                                lx1=movex.pinnedw(gametiles,moves1,y,x)
                                if len(lx1)==0:
                                    continue
                                else:
                                    check=True
                                if check==True:
                                    break
                        if check==True:
                            break

                    if check==False:
                        return True






    def minimax(self,gametiles, depth,alpha , beta ,player):
        if depth==0 or self.checkmate(gametiles)==True or self.stalemate(gametiles,player)==True:
            return self.calculateb(gametiles)
        if not player:
            minEval=100000000
            kp,ks=self.eva(gametiles,player)
            for lk in kp:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.move(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,True)
                    if evalk<minEval and depth==3:
                        tp.clear()
                        tp.append(move)
                    if evalk==minEval and depth==3:
                        tp.append(move)
                    minEval=min(minEval,evalk)
                    beta=min(beta,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break

                if beta<=alpha:
                    break
            return minEval

        else:
            maxEval=-100000000
            kp,ks=self.eva(gametiles,player)
            for lk in ks:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.movew(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,False)
                    maxEval=max(maxEval,evalk)
                    alpha=max(alpha,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break
                if beta<=alpha:
                    break

            return maxEval



    def printboard(self,gametilles):
        count = 0
        for rows in range(8):
            for column in range(8):
                print('|', end=gametilles[rows][column].pieceonTile.tostring())
            print("|",end='\n')


    def checkeva(self,gametiles,moves):
        arr=[]
        for move in moves:
            lk=[[move[2],move[3]]]
            arr.append(self.calci(gametiles,move[0],move[1],lk))

        return arr



    def eva(self,gametiles,player):
        lx=[]
        moves=[]
        kp=[]
        ks=[]
        movex=move()
        for x in range(8):
            for y in range(8):
                    if gametiles[y][x].pieceonTile.alliance=='Black' and player==False:
                        if movex.checkb(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedb(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            kp=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='K'):
                                ax=movex.castlingb(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([0,6])
                                        if l=='qs':
                                            moves.append([0,2])
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            lx=movex.pinnedb(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        kp.append(self.calci(gametiles,y,x,moves))


                    if gametiles[y][x].pieceonTile.alliance=='White' and player==True:
                        if movex.checkw(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedw(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            ks=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if moves==None:
                            print(y)
                            print(x)
                            print(gametiles[y][x].pieceonTile.position)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='k'):
                                ax=movex.castlingw(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([7,6])
                                        if l=='qs':
                                            moves.append([7,2])
                        if gametiles[y][x].pieceonTile.alliance=='White':
                            lx=movex.pinnedw(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        ks.append(self.calci(gametiles,y,x,moves))

        return kp,ks



    def calci(self,gametiles,y,x,moves):
        arr=[]
        jk=object
        for move in moves:
            jk=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            mk=self.calculateb(gametiles)
            gametiles[y][x].pieceonTile=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=jk
            arr.append([y,x,move[0],move[1],mk])
        return arr


    def calculateb(self, gametiles):
        # TODO: Fix Pawn Promotion
        # TODO: write past moves to a file and then read them to see if the same position has been repeated 3 times?

        value, bvalue, wvalue = 0, 0, 0
        num_P, num_p, num_N, num_n, num_R, num_r, num_B, num_b, num_Q, num_q = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        pawn_multiplier = {
            0: 0,
            1: 1,
            2: 1.1,
            3: 1.2,
            4: 1.6,
            5: 1.8,
            6: 2,
            7: 9
        }

        # Impl taken from move.py
        def is_checked(alliance, r, c, gametiles):
            for m in range(8):
                for k in range(8):
                    tmp_piece = gametiles[m][k].pieceonTile
                    if tmp_piece.alliance is not None:
                        if tmp_piece.alliance != alliance:
                            # print(m, k)
                            moves = gametiles[m][k].pieceonTile.legalmoveb(gametiles)
                            if moves is None:
                                continue
                            for move in moves:
                                if move[0] == r and move[1] == c:
                                    return True
            return False

        def is_checkmate(piece, r, c, gametiles):
            movex = move()
            if is_checked(piece.alliance, r, c, gametiles):
                array = movesifchecked(piece.alliance, r, c, gametiles)
                if len(array) == 0:
                    return True
            return False

        def is_pawn_diagonal(piece, r, c, gametiles):
            if piece.alliance == 'Black' and r <= 6 and 6 >= c >= 1:
                if gametiles[r + 1][c + 1].pieceonTile.tostring() == 'P' or gametiles[r + 1][c - 1].pieceonTile.tostring() == 'P':
                    return True
            elif piece.alliance == 'White' and r >= 1 and 6 >= c >= 1:
                if gametiles[r - 1][c + 1].pieceonTile.tostring() == 'p' or gametiles[r - 1][c - 1].pieceonTile.tostring() == 'p':
                    return True
            return False

        def center_control(row):
            if row is 3 or row is 4:
                return 20
            return 0
        def is_stalemate(gametiles, player):
            movex = move()
            if not player:
                # Alliance is Black
                r, c, = None, None
                for i in range(8):
                    for j in range(8):
                        if gametiles[i][j].pieceonTile.tostring == 'K':
                            r = j
                            c = i
                if is_checked('Black', r, c, gametiles):
                    check = False
                    for x in range(8):
                        for y in range(8):
                            if gametiles[y][x].pieceonTile.alliance == 'Black':
                                moves1 = gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                                if moves1 is None:
                                    continue
                                lx1 = movex.pinnedb(gametiles, moves1, y, x)
                                if len(lx1) == 0:
                                    continue
                                else:
                                    check = True
                                if check:
                                    break
                        if check:
                            break

                    if not check:
                        return True

            if player:
                # Alliance is Black
                r, c, = None, None
                for i in range(8):
                    for j in range(8):
                        if gametiles[i][j].pieceonTile.tostring == 'k':
                            r = j
                            c = i
                if is_checked('White', r, c, gametiles):
                    check = False
                    for x in range(8):
                        for y in range(8):
                            if gametiles[y][x].pieceonTile.alliance == 'White':
                                moves1 = gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                                if moves1 is None:
                                    continue
                                lx1 = movex.pinnedw(gametiles, moves1, y, x)
                                if len(lx1) == 0:
                                    continue
                                else:
                                    check = True
                                if check == True:
                                    break
                        if check == True:
                            break

                    if check == False:
                        return True

        def movesifchecked(alliance, r, c, gametiles):
            movi = []
            piece = None
            for m in range(8):
                for k in range(8):
                    if gametiles[m][k].pieceonTile.alliance == alliance:
                        moves = gametiles[m][k].pieceonTile.legalmoveb(gametiles)
                        for move in moves:
                            x = move[0]
                            y = move[1]
                            piece = gametiles[x][y].pieceonTile
                            gametiles[x][y].pieceonTile = gametiles[m][k].pieceonTile
                            gametiles[m][k].pieceonTile = nullpiece()
                            s = self.updateposition(x, y)
                            gametiles[x][y].pieceonTile.position = s
                            if not is_checked(alliance, r, c, gametiles):
                                movi.append([m, k, x, y])
                                gametiles[m][k].pieceonTile = gametiles[x][y].pieceonTile
                                gametiles[x][y].pieceonTile = piece
                                s = self.updateposition(m, k)
                                gametiles[m][k].pieceonTile.position = s
                            else:
                                gametiles[m][k].pieceonTile = gametiles[x][y].pieceonTile
                                gametiles[x][y].pieceonTile = piece
                                s = self.updateposition(m, k)
                                gametiles[m][k].pieceonTile.position = s
            return movi

        def num_moves(piece, gametiles):
            moves = piece.legalmoveb(gametiles)
            return 0 if moves is None else len(moves) * 10

        for row in range(8):
            for col in range(8):
                piece = gametiles[row][col].pieceonTile
                match piece.tostring():
                    case 'P':
                        bvalue -= (100 * pawn_multiplier[row])
                        bvalue -= num_moves(piece, gametiles)
                        num_P += 1
                        if is_pawn_diagonal(piece, row, col, gametiles):
                            bvalue -= (20 * pawn_multiplier[row])
                    case 'N':
                        bvalue -= 300
                        bvalue -= num_moves(piece, gametiles)
                        num_N += 1
                        bvalue -= center_control(row)
                    case 'B':
                        bvalue -= 300
                        bvalue -= num_moves(piece, gametiles)
                        bvalue -= center_control(row)
                        num_B += 1
                    case 'R':
                        bvalue -= 500
                        bvalue -= num_moves(piece, gametiles)
                        num_R += 1
                        bvalue -= center_control(row)
                    case 'Q':
                        bvalue -= 950
                        bvalue -= num_moves(piece, gametiles) / 10
                        bvalue -= center_control(row)
                        num_Q += 1
                    case 'K':
                        bvalue -= 10000
                        bvalue -= num_moves(piece, gametiles)

                        # is king checkmate?
                        if is_checkmate(piece, row, col, gametiles):
                            bvalue += 1000000

                        # Is the king checked?
                        elif is_checked(piece.alliance, row, col, gametiles) == 'Checked':
                            bvalue += 450

                        # Is there a pawn in front of the king?
                        if gametiles[row - 1][col].pieceonTile.tostring() == 'P':
                            # is the rook next to the king?
                            if col is not (0 or 7):
                                if gametiles[row][col - 1].pieceonTile.tostring() == 'R' or gametiles[row][col + 1].pieceonTile.tostring() == 'R':
                                    bvalue -= 400
                    case 'p':
                        wvalue += (100 * pawn_multiplier[7 - row])
                        wvalue += num_moves(piece, gametiles)
                        num_p += 1
                        if is_pawn_diagonal(piece, row, col, gametiles):
                            wvalue += (20 * pawn_multiplier[row])

                    case 'n':
                        wvalue += 300
                        wvalue += num_moves(piece, gametiles)
                        num_n += 1
                        wvalue += center_control(row)
                    case 'b':
                        wvalue += 300
                        wvalue += center_control(row)
                        wvalue += center_control(row)
                        num_b += 1
                    case 'r':
                        wvalue += 500
                        wvalue += num_moves(piece, gametiles)
                        wvalue += center_control(row)
                        num_r += 1
                    case 'q':
                        wvalue += 950
                        wvalue += num_moves(piece, gametiles) / 10
                        wvalue += center_control(row)
                        num_q += 1
                    case 'k':
                        wvalue += 10000
                        wvalue += num_moves(piece, gametiles)

                        # if stalemate
                        # if is_stalemate(gametiles, True):
                        #     wvalue += 1000000

                        # is king checkmate?
                        if is_checkmate(piece, row, col, gametiles):
                            wvalue -= 1000000

                        # Is the king checked?
                        elif is_checked(piece.alliance, row, col, gametiles) == 'Checked':
                            wvalue -= 450

                        # Is there a pawn in front of the king?
                        if gametiles[row - 1][col].pieceonTile.tostring() == 'p':
                            # is the rook next to the king?
                            if col is not (0 or 7):
                                if gametiles[row][col - 1].pieceonTile.tostring() == 'r' or gametiles[row][col + 1].pieceonTile.tostring() == 'r':
                                    wvalue += 400
                    case '_':
                        pass
        if (bvalue + wvalue) < 0:
            # Black is winning
            if is_stalemate(gametiles, False):
                value = 1000000
        elif (bvalue + wvalue) > 0:
            # White is winning
            if bvalue > -11000 and is_stalemate(gametiles, True):
                value = -1000000
        #pair bonus:
        if num_N == 2:
            bvalue -= 10
        if num_n == 2:
            wvalue += 10
        if num_R == 2:
            bvalue -= 10
        if num_r == 2:
            wvalue += 10
        if num_B == 2:
            bvalue -= 10
        if num_b == 2:
            wvalue += 10
        if num_Q >= 2:
            bvalue -= 500*num_Q
        if num_q >= 2:
            wvalue += 500*num_q

        value += (bvalue + wvalue)
        return value


    def move(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='K' or gametiles[y][x].pieceonTile.tostring()=='R':
            gametiles[y][x].pieceonTile.moved=True

        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='P' and y+1==n and y==6:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='P':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('Black',self.updateposition(n,m))
                promotion=False

        return gametiles



    def revmove(self,gametiles,x,y,n,m,mts):
        if gametiles[x][y].pieceonTile.tostring()=='K':
            if m==y-2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[n][7].pieceonTile.moved=False

                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            elif m==y+2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(m,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[n][0].pieceonTile.moved=False
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts

            return gametiles

        if gametiles[x][y].pieceonTile.tostring()=='k':
            if m==y-2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            elif m==y+2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(n,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts


            return gametiles

        gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
        s=self.updateposition(n,m)
        gametiles[n][m].pieceonTile.position=s
        gametiles[x][y].pieceonTile=mts

        return gametiles



    def movew(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='k' or gametiles[y][x].pieceonTile.tostring()=='r':
            pass

        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='p' and y-1==n and y==1:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='p':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('White',self.updateposition(n,m))
                promotion=False

        return gametiles
























                        
