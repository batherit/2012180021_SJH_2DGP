import game_framework
import math
import random
from pico2d import *



#주인공의 공격 상태
enumerate(['NORAML', 'ATTACK' ])
#주인공의 공격 방향
enumerate(['DEFAULT','LEFT, RIGHT, UP, DOWN'])
#주인공의 공격 타입
enumerate(['SKILL1, SKILL2, SKILL3'])
#인질들의 계급
#enumerate(['KING', 'QUEEN', 'BUTLER', 'KNIGHT', 'SLAVE'])

#UI 클래스
class UI:
    def __init__(self):
        self.UITitle = load_image('UI/UITitle.png')
    def update(self):
        pass
    def draw(self):
        self.UITitle.draw(450, 350)
#맵 클래스 : carpet의 움직임에 종속적
class Map:
    global carpet
    def __init__(self):
        #self.mapCast = load_image('map/mapCast2.png')
        self.baseMap = load_image('map/baseMap.png')
        self.map1 = load_image('map/simpleMap1.png')
        self.map2 = load_image('map/simpleMap2.png')
        self.map3 = load_image('map/simpleMap3.png')
        self.map4 = load_image('map/simpleMap4.png')
        self.map5 = load_image('map/simpleMap5.png')
    def draw(self):
        self.baseMap.draw(450, 350)
        self.map1.draw(450-0.5*(carpet.x-350), 350-0.5*(carpet.y-350))
        self.map2.draw(450-0.25*(carpet.x-350), 350-0.25*(carpet.y-350))
        self.map3.draw(450-0.125*(carpet.x-350), 350-0.125*(carpet.y-350))
        self.map4.draw(450-0.0625*(carpet.x-350), 350-0.0625*(carpet.y-350))
        self.map5.draw(350-0.20*(carpet.x-350), 350-0.20*(carpet.y-350))
        #self.mapCast.draw(450, 350)
    pass


#주인공 클래스 : carpet 클래스와 cootTime 변수에 종속적
#속성값 : 주인공 위치 좌표, 현재 상태(기본, 공격), 공격 방향, 공격 타입
class Hero:
    global carpet
    global heroSkill1Box
    global heroSkill2Box

    def __init__(self): #속성 초기화
        self.x = 0
        self.y = 0
        self.state = 'NORMAL'
        self.attackDirect = 'DEFAULT'
        self.skillType = 'SKILL1'
        self.hero = load_image('hero/mainchar.png')
        self.attack = load_image('hero/mainchar_attack.png')
        self.attackAniFlag = 0
        self.frame = 0
        self.delay = 0
        self.skill1Delay = 0
        self.skill2Delay = 0
        self.skill3Delay = 0
    def update(self): #게임 로직
        #주인공이 공격 상태라면 탄환을 생성한다.
        if self.state == 'ATTACK':
            if self.skillType == 'SKILL1':
                self.skill1Delay+=1
                if self.skill1Delay == 8:
                    heroSkill1Box.append(Skill1())
                    self.skill1Delay = 0
            elif self.skillType == 'SKILL2':
                self.skill2Delay+=1
                if self.skill2Delay == 35:
                    heroSkill2Box.append(Skill2())
                    self.skill2Delay = 0
            elif self.skillType == 'SKILL3':
                self.skill3Delay+=1
                if self.skill3Delay == 10:
                    heroSkill3Box.append(Skill3())
                    self.skill3Delay = 0


    def draw(self): #게임 렌더링
        self.delay+=1
        if self.state == 'NORMAL': #아무런 입력이 없을 경우
            self.hero.clip_draw(self.frame*40, 0, 40,40, self.x+carpet.x, self.y+carpet.y)
            if self.delay == 10:
                self.frame = (self.frame+1) % 2
                self.delay = 0
        elif self.state == 'ATTACK': #스페이스키를 눌러 공격 형태가 됐을 경우
            if self.attackAniFlag == 0:
                self.attack.clip_draw(self.frame*40, 40, 40,40,self.x+carpet.x, self.y+carpet.y)
                if self.delay == 4:
                    self.frame = (self.frame+1) % 8
                    self.delay = 0
                    if self.frame == 0:
                        self.attackAniFlag = 1-self.attackAniFlag
            else:
                self.attack.clip_draw(self.frame*40, 0, 40,40, self.x+carpet.x, self.y+carpet.y)
                if self.delay == 4:
                    self.frame = (self.frame+1)%8
                    self.delay =0
                    #if self.frame == 0:
                    #    self.attackAniFlag = 1-self.attackAniFlag
            pass

def angle(startX,startY,directX, directY):
    axisDegree = (180.0 / math.pi)*math.atan2(0.0, 1.0)
    if axisDegree < 0: axisDegree += 360
    moveDegree = (180.0 / math.pi)*math.atan2((directY - startY), (directX - startX))
    if moveDegree < 0: moveDegree += 360
    return moveDegree - axisDegree
#주인공 마법 타입1 클래스 : 주인공 클래스에 종속적
#속성값 : 마법 초기 생성 위치, 마법 진행 방향, 마법 진행 방향각, 마법 이동 속도
#전제 : Skill1 인스턴스는 hero 내에서 생성된다. (hero.state == 'ATTACK' 상태 )
class Skill1:
    global hero
    global carpet
    global heroSkill1Box

    skill1 = None

    def __init__(self):
        if Skill1.skill1 == None:Skill1.skill1 = load_image('hero/heroSkill/skill1.png')
        #마법은 주인공 기준으로 생성된다.
        self.x = hero.x+carpet.x
        self.y = hero.y+carpet.y
        self.angle = 0.0
        self.frame = 0
        self.collision = False
        self.aniDelay = 0
        self.carpetX = carpet.x
        self.carpetY = carpet.y
        #마법 탄환 초기 생성 위치 초기화
        if hero.attackDirect=='UP':
            self.y += 30
            self.angle = angle(self.x, self.y, self.x+random.randint(-40, 40), self.y+500)
        elif hero.attackDirect == 'DOWN':
            self.y -= 30
            self.angle = angle(self.x, self.y, self.x+random.randint(-40, 40), self.y-500)
        elif hero.attackDirect == 'LEFT':
            self.x -= 30
            self.angle = angle(self.x, self.y, self.x-500, self.y+random.randint(-40, 40))
        elif hero.attackDirect == 'RIGHT':
            self.x += 30
            self.angle = angle(self.x, self.y, self.x+500, self.y+random.randint(-40, 40))
        self.direct = hero.attackDirect
        self.velocity = 10#random.randint(20,21)
    def update(self):
        if self.collision == False:
            self.x += self.velocity*math.cos(math.pi/180*self.angle)
            self.y += self.velocity*math.sin(math.pi/180*self.angle)
    def draw(self):
        if self.collision == False : self.skill1.clip_draw(0,0, 30, 30, self.x-0.7*(carpet.x-self.carpetX), self.y-0.7*(carpet.y-self.carpetY))
        else:
            self.aniDelay+=1
            self.skill1.clip_draw(self.frame*30, 0, 30, 30,self.x-0.7*(carpet.x-self.carpetX), self.y-0.7*(carpet.y-self.carpetY))
            if self.aniDelay == 3:
                self.frame = (self.frame+1)%8
                self.aniDelay = 0
                if self.frame == 0:
                    for i in range(-1, len(heroSkill1Box)-1):
                        if self == heroSkill1Box[i]:
                            del heroSkill1Box[i]
                            break

class Skill2:
    global hero
    global carpet
    global heroSkill2Box

    skill2_1LR, skill2_2LR, skill2_1UD, skill2_2UD = None, None, None, None

    def __init__(self):
        if Skill2.skill2_1LR == None:Skill2.skill2_1LR = load_image('hero/heroSkill/skill2_1LR.png')
        if Skill2.skill2_2LR == None:Skill2.skill2_2LR = load_image('hero/heroSkill/skill2_2LR.png')
        if Skill2.skill2_1UD == None:Skill2.skill2_1UD = load_image('hero/heroSkill/skill2_1UD.png')
        if Skill2.skill2_2UD == None:Skill2.skill2_2UD = load_image('hero/heroSkill/skill2_2UD.png')
        #마법은 주인공 기준으로 생성된다.
        self.x = hero.x+carpet.x
        self.y = hero.y+carpet.y
        self.frame = 0
        self.aniFlag = random.randint(0,1)
        self.aniDelay = 0
        self.direct = hero.attackDirect
        #마법 탄환 초기 생성 위치 초기화
        if hero.attackDirect=='UP':
            self.y += 430
        elif hero.attackDirect == 'DOWN':
            self.y -= 430
        elif hero.attackDirect == 'LEFT':
            self.x -= 430
        elif hero.attackDirect == 'RIGHT':
            self.x += 430

    def update(self):
        pass
    def draw(self):
        self.aniDelay+=1
        if self.direct == 'RIGHT' or self.direct == 'LEFT':
            if self.aniFlag == 0:
                self.skill2_1LR.clip_draw(0, 360-self.frame*60, 800,60, self.x, self.y)
                if self.aniDelay == 3:
                    self.frame = (self.frame+1)%7
                    self.aniDelay=0
                    if self.frame == 0:
                        for i in range(-1, len(heroSkill2Box)-1):
                                if self == heroSkill2Box[i]:
                                    del heroSkill2Box[i]
                                    break
            else:
                self.skill2_2LR.clip_draw(0, 360-self.frame*60, 800,60, self.x, self.y)
                if self.aniDelay == 3:
                    self.frame = (self.frame+1)%7
                    self.aniDelay=0
                    if self.frame == 0:
                        for i in range(-1, len(heroSkill2Box)-1):
                                if self == heroSkill2Box[i]:
                                    del heroSkill2Box[i]
                                    break
        elif self.direct == 'UP' or self.direct == 'DOWN':
            if self.aniFlag == 0:
                self.skill2_1UD.clip_draw(self.frame*60, 0, 60,800, self.x, self.y)
                if self.aniDelay == 3:
                    self.frame = (self.frame+1)%7
                    self.aniDelay=0
                    if self.frame == 0:
                        for i in range(-1, len(heroSkill2Box)-1):
                                if self == heroSkill2Box[i]:
                                    del heroSkill2Box[i]
                                    break
            else:
                self.skill2_2UD.clip_draw(self.frame*60, 0, 60,800, self.x, self.y)
                if self.aniDelay == 3:
                    self.frame = (self.frame+1)%7
                    self.aniDelay=0
                    if self.frame == 0:
                        for i in range(-1, len(heroSkill2Box)-1):
                                if self == heroSkill2Box[i]:
                                    del heroSkill2Box[i]
                                    break

class Skill3:
    global hero
    global carpet
    global heroSkill1Box

    skill3 = None
    skill3Boom = None
    KIND1, KIND2, KIND3, KIND4, KIND5 = 0, 1, 2, 3, 4
    skill3_kind = { KIND1 : 0, KIND2 : 1, KIND3 : 2, KIND4 : 3, KIND5 : 4 }
    def __init__(self):
        if Skill3.skill3 == None: Skill3.skill3 = load_image('hero/heroSkill/skill3.png')
        if Skill3.skill3Boom == None: Skill3.skill3Boom = load_image('hero/heroSkill/skill3boom.png')
        #마법은 주인공 기준으로 생성된다.
        self.x = hero.x+carpet.x
        self.y = hero.y+carpet.y
        self.frame = 0
        self.aniDelay = 0
        self.self_explosion_time = 180
        self.power = 0
        self.collision = False
        self.carpetX = carpet.x
        self.carpetY = carpet.y
        self.kind = random.randint(1, 36)
        if 0 < self.kind and self.kind < 16:
            self.kind = self.KIND1
            self.power = 50
        elif 15< self.kind and self.kind <26:
            self.kind = self.KIND2
            self.power = 100
        elif 25< self.kind and self.kind <31:
            self.kind = self.KIND3
            self.power = 150
        elif 30< self.kind and self.kind <36:
            self.kind = self.KIND4
            self.power = 200
        elif 35< self.kind and self.kind <37:
            self.kind = self.KIND5
            self.power = 350
        #마법 탄환 초기 생성 위치 초기화
        if hero.attackDirect=='UP': self.y += 30
        elif hero.attackDirect == 'DOWN': self.y -= 30
        elif hero.attackDirect == 'LEFT': self.x -= 30
        elif hero.attackDirect == 'RIGHT': self.x += 30
    def update(self):
        if self.collision == False :
            self.self_explosion_time -= 1
            if self.self_explosion_time < 0:
                self.collision = True

    def draw(self):
        if self.collision == False :
            self.skill3.clip_draw(self.skill3_kind[self.kind]*40,0, 40, 40, self.x-0.7*(carpet.x-self.carpetX), self.y-0.7*(carpet.y-self.carpetY))
        else :
            self.aniDelay+=1
            self.skill3Boom.clip_draw(60*self.frame, 0, 60, 60,self.x-0.7*(carpet.x-self.carpetX), self.y-0.7*(carpet.y-self.carpetY))
            if self.aniDelay == 10:
                self.frame = (self.frame+1)%8
                self.aniDelay = 0
                if self.frame == 0:
                    for i in range(-1, len(heroSkill3Box)-1):
                        if self == heroSkill3Box[i]:
                            del heroSkill3Box[i]
                            break

#양탄자 클래스 : 이동방향 플래그 변수에 종속적
#속성값 : 양탄자 위치
class Carpet:
    goToRight, goToLeft, goToUp, goToDown = False, False, False, False
    def __init__(self):
        self.x = 350
        self.y = 350
        self.carpet = load_image('hero/carpet.png')

    def update(self):
        if self.goToRight == True:
            if self.x+50 > 650 : self.x -= 2
            else: self.x += 2
        if self.goToLeft == True:
            if self.x-50 < 50 : self.x += 2
            else: self.x -= 2
        if self.goToUp == True:
            if self.y+50 > 650 : self.y -=2
            else: self.y += 2
        if self.goToDown == True:
            if self.y-50 < 50 : self.y +=2
            else: self.y -= 2
    def draw(self):
        self.carpet.draw(self.x, self.y)
    pass

#enemy2 클래스
class Enemy2:
    global hero
    global carpet
    global enemy2RazerBox
    enemy2 = None
    NORMAL, ENEMY2_PATTERN1, ENEMY2_PATTERN2, ENEMY2_PATTERN3  = 0, 1, 2, 3

    def enemy2_normal(self):        #enemy2의 평범한 움직임
        if self.move_count == 4:
            if self.frame == 0:     #self.aniDelay == 0 인 상태
                self.state = random.randint(3,3) #차후 추가되면 랜덤으로 패턴을 돌린다.
                self.move_flag = False
                self.move_count = 0
        else :
            if self.move_flag == False:
                self.move_delay+=1
                if self.move_delay == 100:
                    self.endX = carpet.x
                    self.endY = carpet.y
                    self.angle = angle(self.x-0.7*(carpet.x-350), self.y-0.7*(carpet.y-350), self.endX, self.endY)
                    self.move_flag = True
                    self.move_delay = 0
            elif self.move_flag == True:
                if (self.endX-15 < self.x-0.7*(self.endX-350) and self.x-0.7*(self.endX-350)< self.endX+15) \
                        and (self.endY-15 < self.y-0.7*(self.endY-350) and self.y-0.7*(self.endY-350)< self.endY+15) :
                    self.move_flag = False
                    self.move_count+=1
                else:
                    self.x += 2*math.cos(math.pi/180*self.angle)
                    self.y += 2*math.sin(math.pi/180*self.angle)

    def enemy2_pattern1(self):
        if self.move_count == 3:
            if self.frame == 0:     #self.aniDelay == 0 인 상태
                self.state = random.randint(3,3)#차후 추가되면 랜덤으로 패턴을 돌린다.
                self.move_flag = False
                self.move_count = 0
        else:
            if self.move_flag == False:    #초기 위치값 지정
                if self.attack_ready == False:
                    self.around_r= random.randint(180,200)
                    self.angle=angle(carpet.x, carpet.y, self.x-0.7*(carpet.x-350), self.y-0.7*(carpet.y-350))+random.randint(-90,90)
                    self.carpetX=carpet.x
                    self.carpetY=carpet.y
                    self.endX = self.carpetX+self.around_r*math.cos(math.pi/180*self.angle)
                    self.endY = self.carpetY+self.around_r*math.sin(math.pi/180*self.angle)
                    self.angle=angle( self.x-0.7*(self.carpetX-350), self.y-0.7*(self.carpetY-350),self.endX, self.endY)
                    self.move_flag = True
                elif self.attack_ready == True: #공격을 준비
                    if self.attack_flag == False:
                        if self.frame == 3: #공격 모션을 취하는 애니메이션 프레임 컷이 될 때까지 대기
                            self.attack_flag = True
                    elif self.attack_flag == True: #공격 시작
                        self.attack_flag = False
                        for i in range(-10,10):
                            self.razer_angle= angle(self.x-0.7*(carpet.x-350), self.y-0.7*(carpet.y-350), carpet.x, carpet.y)+i*18
                            enemy2RazerBox.append(Eenemy2Razer())
                        self.move_count+=1
            elif self.move_flag == True:    #이동한다.
                if (self.endX-20 < self.x-0.7*(self.carpetX-350) and self.x-0.7*(self.carpetX-350)< self.endX+20) \
                        and (self.endY-20 < self.y-0.7*(self.carpetY-350) and self.y-0.7*(self.carpetY-350)< self.endY+20) :
                    if self.frame == 0:  #프레임이 0이 될 때까지 대기
                        self.move_flag = False
                        self.attack_ready = True #멈췄다면 공격 준비 상태로 설정.
                else:
                    self.x += 4*math.cos(math.pi/180*self.angle)
                    self.y += 4*math.sin(math.pi/180*self.angle)

    def enemy2_pattern2(self):
        if self.move_count == 5:
            if self.frame == 0:     #self.aniDelay == 0 인 상태
                self.state = random.randint(3,3) #차후 추가되면 랜덤으로 패턴을 돌린다.
                self.move_flag = False
                self.move_count = 0
        else:
            if self.move_flag == False:    #초기 위치값 지정
                if self.attack_ready == False:
                    self.carpetX=carpet.x
                    self.carpetY=carpet.y
                    self.endX = 350-0.7*(self.carpetX-350)
                    self.endY = 350-0.7*(self.carpetY-350)
                    self.angle=angle( self.x-0.7*(self.carpetX-350), self.y-0.7*(self.carpetY-350),self.endX, self.endY)
                    self.move_flag = True
                elif self.attack_ready == True: #공격을 준비
                    if self.attack_flag == False:
                        if self.frame == 3: #공격 모션을 취하는 애니메이션 프레임 컷이 될 때까지 대기
                            self.attack_flag = True
                    elif self.attack_flag == True: #공격 시작
                        #self.around_r= 50*(random.randint(0,4))+150
                        self.around_r=distance(carpet.x, carpet.y, self.x-0.7*(carpet.x-350), self.y-0.7*(carpet.y-350))+random.randint(-3, 3)
                        for j in range(1,4):
                            for i in range(0,30):
                                self.skillX = self.x-0.7*(carpet.x-350)+(self.around_r+(j-2)*80)*math.cos(math.pi/180*i*360/30)
                                self.skillY = self.y-0.7*(carpet.y-350)+(self.around_r+(j-2)*80)*math.sin(math.pi/180*i*360/30)
                                enemy2BombBox.append(Bomb())
                        self.attack_flag = False
                        self.move_count+=1
            elif self.move_flag == True:    #이동한다.
                if (self.endX-20 < self.x-0.7*(self.carpetX-350) and self.x-0.7*(self.carpetX-350)< self.endX+20) \
                        and (self.endY-20 < self.y-0.7*(self.carpetY-350) and self.y-0.7*(self.carpetY-350)< self.endY+20) :
                    if self.frame == 0:  #프레임이 0이 될 때까지 대기
                        self.move_flag = False
                        self.attack_ready = True #멈췄다면 공격 준비 상태로 설정.
                else:
                    self.x += 4*math.cos(math.pi/180*self.angle)
                    self.y += 4*math.sin(math.pi/180*self.angle)

    def enemy2_pattern3(self):
        if self.move_count == 1:
            if self.frame == 0:     #self.aniDelay == 0 인 상태
                self.state = 2 #차후 추가되면 랜덤으로 패턴을 돌린다.
                self.move_flag = False
                self.move_count = 0
        else:
            if self.move_flag == False:    #초기 위치값 지정
                self.carpetX=carpet.x
                self.carpetY=carpet.y
                self.endX = 350-0.7*(self.carpetX-350)
                self.endY = 350-0.7*(self.carpetY-350)
                self.angle=angle( self.x-0.7*(self.carpetX-350), self.y-0.7*(self.carpetY-350),self.endX, self.endY)
                self.move_flag = True #가운데 위치로 간다.
            elif self.move_flag == True:    #이동한다.
                if (self.endX-20 < self.x-0.7*(self.carpetX-350) and self.x-0.7*(self.carpetX-350)< self.endX+20) \
                        and (self.endY-20 < self.y-0.7*(self.carpetY-350) and self.y-0.7*(self.carpetY-350)< self.endY+20) :
                    if self.spaning_ball == False:
                        for i in range(0, 4):
                            self.skillX = self.x+150*math.cos(math.pi/ 180*90*i)#-0.7*(carpet.x-350)
                            self.skillY = self.y+150*math.sin(math.pi/ 180*90*i)#-0.7*(carpet.y-350)
                            self.ballList.append(Ball())
                        self.spaning_ball = True
                    else:
                        if self.allBallDie == True:
                            self.spaning_ball = False
                            self.allBallDie = False
                            self.move_count+=1
                        else:
                            if 0== len(enemy2.ballList): enemy2.allBallDie=True
                else:
                    self.x += 2*math.cos(math.pi/180*self.angle)
                    self.y += 2*math.sin(math.pi/180*self.angle)

    enemy2_state = {
        NORMAL : enemy2_normal,
        ENEMY2_PATTERN1 : enemy2_pattern1,
        ENEMY2_PATTERN2 : enemy2_pattern2,
        ENEMY2_PATTERN3 : enemy2_pattern3
    }

    def __init__(self):
        self.x, self.y = 550.0, 350.0
        self.frame = 0
        self.move_count = 0 #패턴 총 행동 횟수
        self.move_flag = False
        self.move_delay = 0
        self.angle = 0.0
        self.carpetX=0.0
        self.carpetY=0.0
        self.endX = 0.0
        self.endY = 0.0
        self.around_r = 0
        self.state = self.NORMAL
        self.aniDelay = 0
        self.razer_angle = 0.0
        self.skillX = 0.0
        self.skillY = 0.0
        self.spaning_ball = False
        self.allBallDie = False
        self.ballList = []
        self.attack_ready = False
        self.attack_flag = False
        if Enemy2.enemy2 == None:
            Enemy2.enemy2 = load_image('enemy2/enemy2normalprototype2.png')

    def update(self):
        self.enemy2_state[self.state](self)

    def draw(self):
        self.aniDelay+=1
        if self.state == self.NORMAL :
            self.enemy2.clip_draw(self.frame*300, 350, 300,350, self.x-0.7*(carpet.x-350), self.y-0.7*(carpet.y-350))
        elif self.state != self.NORMAL :
            if self.move_flag == True:
                self.enemy2.clip_draw(self.frame*300, 350, 300,350, self.x-0.7*(carpet.x-350), self.y-0.7*(carpet.y-350))
            elif self.move_flag == False :
                if self.attack_ready == True: #적이 멈춰있는 상태며, 공격 준비 상태
                    if self.attack_flag == True: self.frame = 4
                self.enemy2.clip_draw(self.frame*300, 0, 300,350, self.x-0.7*(carpet.x-350), self.y-0.7*(carpet.y-350))
        if self.aniDelay == 8 :
                self.frame = (self.frame+1)%8
                if self.state != self.NORMAL and self.frame == 0:
                    self.attack_ready = False
                self.aniDelay=0
class Eenemy2Razer:
    global hero
    global carpet
    global enemy2
    global enemy2RazerBox

    razer = None

    def __init__(self):
        if Eenemy2Razer.razer == None:
            Eenemy2Razer.razer = load_image('enemy2/enemy2razer.png')
        self.x = enemy2.x-0.7*(carpet.x-350)
        self.y = enemy2.y-0.7*(carpet.y-350)
        self.angle = enemy2.razer_angle
        self.collision = False
        self.carpetX = carpet.x
        self.carpetY = carpet.y
        self.velocity = 3
        self.acceleration = 0
        self.slope = 0
        self.slope_flag = (-1+ 2*(enemy2.move_count % 2))
    def update(self):
        if self.collision == False:
            self.acceleration+=0.03
            self.slope+=1
            self.x += self.velocity*self.acceleration*math.cos(math.pi/180*(self.angle+self.slope_flag*self.slope))
            self.y += self.velocity*self.acceleration*math.sin(math.pi/180*(self.angle+self.slope_flag*self.slope))

    def draw(self):
        if self.collision == False : self.razer.clip_draw(0, 0, 30,30, self.x-0.7*(carpet.x-self.carpetX), self.y-0.7*(carpet.y-self.carpetY))
        else:
            for i in range(-1, len(enemy2RazerBox)-1):
                if self == enemy2RazerBox[i]:
                    del enemy2RazerBox[i]
                    break

class Bomb:
    global hero
    global carpet
    global enemy2
    global enemy2BombBox

    bomb = None
    boom = None

    def __init__(self):
        if Bomb.bomb == None: Bomb.bomb = load_image('enemy2/enemy2bomb.png')
        if Bomb.boom == None: Bomb.boom = load_image('enemy2/enemy2boom.png')
        self.x = enemy2.skillX
        self.y = enemy2.skillY
        self.carpetX = carpet.x
        self.carpetY = carpet.y
        self.boom_flag = False
        self.aniDelay = 0
        self.ding = 5
        self.frame = 0
    def update(self):
        pass

    def draw(self):
        self.aniDelay += 1
        if self.boom_flag == False : self.bomb.clip_draw(self.frame*50, 0, 50, 50, self.x-0.7*(carpet.x-self.carpetX), self.y-0.7*(carpet.y-self.carpetY))
        elif self.boom_flag == True : self.boom.clip_draw(self.frame*100, 0, 100,100, self.x-0.7*(carpet.x-self.carpetX), self.y-0.7*(carpet.y-self.carpetY))
        if self.aniDelay == self.ding :
            self.frame = (self.frame+1)%8
            if self.frame == 0:
                if self.boom_flag == False :
                    self.boom_flag = True
                    self.ding = 4
                    self.aniDelay=0
                    #충돌체크
                elif self.boom_flag == True :
                    for i in range(-1, len(enemy2BombBox)-1):
                        if self == enemy2BombBox[i]:
                            del enemy2BombBox[i]
                            break
            self.aniDelay = 0

class Ball:
    global hero
    global carpet
    global enemy2
    global ballRazerBox

    span = None
    ball = None
    boom = None

    NORMAL = 0

    def ball_normal(self):        #enemy2의 평범한 움직임
        if self.move_count == 4:
            if self.frame == 0:     #self.aniDelay == 0 인 상태
                self.state = self.NORMAL #차후 추가되면 랜덤으로 패턴을 돌린다.
                self.move_flag = False
                self.move_count = 0
        else :
            if self.move_flag == False:
                if self.attack_start == False:
                    self.move_delay+=1
                    if self.move_delay == 50:
                        self.carpetX=carpet.x
                        self.carpetY=carpet.y
                        self.course = random.randint(0, 2)
                        if self.course==0:
                            self.endX = carpet.x
                            self.endY = carpet.y
                            self.angle = angle(self.x-0.7*(carpet.x-350), self.y-0.7*(carpet.y-350), self.endX, self.endY)
                        elif self.course==1:
                            self.angle=angle(carpet.x, carpet.y, self.x-0.7*(carpet.x-350), self.y-0.7*(carpet.y-350))+random.randint(-90,90)
                            self.endX = self.carpetX+100*math.cos(math.pi/180*self.angle)
                            self.endY = self.carpetY+100*math.sin(math.pi/180*self.angle)
                            self.angle=angle( self.x-0.7*(self.carpetX-350), self.y-0.7*(self.carpetY-350),self.endX, self.endY)
                        elif self.course==2:
                            self.angle=angle(carpet.x, carpet.y, enemy2.x-0.7*(carpet.x-350), enemy2.y-0.7*(carpet.y-350))
                            self.around_r = random.randint(200, 300)
                            self.endX = enemy2.x-0.7*(self.carpetX-350)+self.around_r*math.cos(math.pi/180*self.angle)
                            self.endY = enemy2.y-0.7*(self.carpetY-350)+self.around_r*math.sin(math.pi/180*self.angle)
                            self.angle = angle( self.x-0.7*(self.carpetX-350), self.y-0.7*(self.carpetY-350),self.endX, self.endY)
                        self.move_flag = True
                        self.move_delay = 0
                else: #self.attack_start
                    self.attack_delay +=1
                    if self.attack_delay == self.attack_ding: #공격 입력
                        if self.attack_type == 0:
                            ballRazerBox.append(BallRazer(angle(self.x-0.7*(carpet.x-350), self.y-0.7*(carpet.y-350), carpet.x, carpet.y), self.x-0.7*(carpet.x-350),self.y-0.7*(carpet.y-350)))
                        if self.attack_type == 1:
                            for i in range(0, 20):
                             ballRazerBox.append(BallRazer(360/20*i, self.x-0.7*(carpet.x-350),self.y-0.7*(carpet.y-350)))
                        self.attack_count+=1
                        self.attack_delay = 0
                    if self.attack_count == 5:
                        self.attack_start = False
                        self.move_count+=1
                        self.attack_count=0
            elif self.move_flag == True:
                if (self.endX-20 < self.x-0.7*(self.carpetX-350) and self.x-0.7*(self.carpetX-350)< self.endX+20) \
                         and (self.endY-20 < self.y-0.7*(self.carpetY-350) and self.y-0.7*(self.carpetY-350)< self.endY+20):
                    self.move_flag = False
                    self.attack_start = True
                    self.attack_type = random.randint(0, 1);
                    self.attack_ding = 15
                else:
                    if self.ball_survive == True:
                        self.x += self.velocity*math.cos(math.pi/180*self.angle)
                        self.y += self.velocity*math.sin(math.pi/180*self.angle)
    ball_state = {
        NORMAL : ball_normal
    }

    def __init__(self):
        if Ball.span == None : Ball.span = load_image('enemy2/enemy2ballspan.png')
        if Ball.ball == None: Ball.ball = load_image('enemy2/enemy2ball.png')
        if Ball.boom == None: Ball.boom = load_image('enemy2/enemy2boom.png')
        self.x = enemy2.skillX
        self.y = enemy2.skillY
        self.carpetX = carpet.x
        self.carpetY = carpet.y
        self.ball_span = False
        self.ball_survive = False
        self.boom_flag = False
        self.move_count = 0
        self.move_flag = False
        self.move_delay = 0
        self.endX = 0
        self.endY = 0
        self.angle = 0.0
        self.course = 0
        self.state = self.NORMAL
        self.attack_start = False
        self.attack_type = 0
        self.attack_count = 0
        self.attack_delay = 0
        self.attack_ding = 0
        self.velocity = 3
        self.around_r = 0
        self.aniDelay = 0
        self.ding = 5
        self.frame = 0
        self.HP= 50
    def update(self):
        if self.HP <= 0: self.ball_survive = False
        if self.ball_survive == True : self.ball_state[self.state](self)

    def draw(self):
        self.aniDelay += 1
        if self.ball_span == False : self.span.clip_draw(self.frame*50, 0, 50,50, self.x-0.7*(carpet.x-350), self.y-0.7*(carpet.y-350))
        else:
            if self.ball_survive == True : self.ball.clip_draw(0, 0, 40,40, self.x-0.7*(carpet.x-350), self.y-0.7*(carpet.y-350))
            else: self.boom.clip_draw(self.frame*100, 0, 100,100, self.x-0.7*(carpet.x-350), self.y-0.7*(carpet.y-350))

        if self.aniDelay == 5 :
            if self.ball_survive != True: self.frame = (self.frame+1)%8
            if self.ball_span == False and self.frame == 0:
                self.ball_span = True
                self.ball_survive = True
            else:
                if self.ball_survive == False and self.frame == 0:
                    for i in range(-1, len(enemy2.ballList)-1):
                        if self == enemy2.ballList[i]:
                            del enemy2.ballList[i]
                            break

            self.aniDelay=0

class BallRazer:
    global hero
    global carpet
    global ballRazerBox

    razer = None

    def __init__(self, angle, x, y):
        if BallRazer.razer == None:
            BallRazer.razer = load_image('enemy2/ballrazer.png')
        self.x = x
        self.y = y
        self.angle = angle
        self.collision = False
        self.carpetX = carpet.x
        self.carpetY = carpet.y
        self.velocity = 3
        self.acceleration = 0
        self.slope = 0
    def update(self):
        if self.collision == False:
            self.acceleration+=0.01
            self.slope+=1
            self.x += self.velocity*self.acceleration*math.cos(math.pi/180*(self.angle))
            self.y += self.velocity*self.acceleration*math.sin(math.pi/180*(self.angle))

    def draw(self):
        if self.collision == False : self.razer.clip_draw(0, 0, 15,15, self.x-0.7*(carpet.x-self.carpetX), self.y-0.7*(carpet.y-self.carpetY))
        else:
            for i in range(-1, len(ballRazerBox)-1):
                if self == ballRazerBox[i]:
                    del ballRazerBox[i]
                    break
#인질 클래스
class Hostage:
    global carpet
    global hostageList

    king, queen, butler, knight, clergy, slave1, slave2 = None, None, None, None, None, None, None
    hostageDie = None
    KING, BUTLER, KNIGHT, CLERGY, SLAVE1, SLAVE2, QUEEN = 0, 1, 2, 3, 4, 5, 6
    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
    #왕과 왕비는 한 스테이지에 한 번밖에 등장하지 않는다.
    #스테이지가 바뀌면 아래 두 클래스 변수는 0으로 초기화된다.
    #supervise_hostage에서 관리한다.
    king_appearance, queen_appearance = 0, 0

    def __init__(self):
        if Hostage.king == None: Hostage.king = load_image('hostage/king.png')
        if Hostage.queen == None:Hostage.queen = load_image('hostage/queen.png')
        if Hostage.butler == None:Hostage.butler = load_image('hostage/butler.png')
        if Hostage.knight == None:Hostage.knight = load_image('hostage/knight.png')
        if Hostage.clergy == None:Hostage.clergy = load_image('hostage/clergy.png')
        if Hostage.slave1 == None:Hostage.slave1 = load_image('hostage/slave1.png')
        if Hostage.slave2 == None:Hostage.slave2 = load_image('hostage/slave2.png')
        if Hostage.hostageDie == None : Hostage.hostageDie = load_image('hostage/hostage_die.png')

        self.frame = 0
        self.aniDelay = 0
        self.x = 0
        self.y = 0
        self.guardMax=350
        self.guardMin=-350
        self.turnFlag=random.randint(0, 1)
        self.velocity = random.randint(1, 2)
        self.position = random.randint(0+Hostage.king_appearance,100-Hostage.queen_appearance)
        self.direct = random.randint(0,3)
        self.survive = True

        if self.direct == self.UP:
            self.y += 375
        elif self.direct == self.DOWN:
            self.y -= 375
        elif self.direct == self.LEFT:
            self.x -= 375
        elif self.direct == self.RIGHT:
            self.x += 375
        self.point = 0

        if -1 < self.position and self.position < 1:
            self.position = self.KING
            Hostage.king_appearance = 1
            self.point = 1500
        elif 0 < self.position and self.position < 11:
            self.position = self.BUTLER
            self.point = 50
        elif 10 < self.position and self.position < 17:
            self.position = self.KNIGHT
            self.point = 100
        elif 16 < self.position and self.position < 21:
            self.position = self.CLERGY
            self.point = 120
        elif 20 < self.position and self.position < 100:
            self.position = random.randint(self.SLAVE1, self.SLAVE2)
            self.point = 10
        elif 99 < self.position and self.position < 101:
            self.position = self.QUEEN
            Hostage.queen_appearance = 1
            self.point = 1000

        self.life = True
    def update(self):
        if self.survive == True:
            if self.direct == self.UP or self.direct == self.DOWN:
                if self.turnFlag == 1:
                    self.x += self.velocity
                    if self.x > self.guardMax:
                        self.x=self.guardMax
                        self.guardMin=random.randint(-350, self.x)
                        self.turnFlag = 0
                elif self.turnFlag == 0:
                    self.x -= self.velocity
                    if self.x < self.guardMin:
                        self.x=self.guardMin
                        self.guardMax=random.randint(self.x, 350)
                        self.turnFlag = 1

            elif self.direct  == self.LEFT or self.direct  == self.RIGHT:
                if self.turnFlag == 1:
                    self.y += self.velocity
                    if self.y > self.guardMax:
                        self.y=self.guardMax
                        self.guardMin=random.randint(-350, self.y)
                        self.turnFlag = 0
                elif self.turnFlag == 0:
                    self.y -= self.velocity
                    if self.y < self.guardMin:
                        self.y=self.guardMin
                        self.guardMax=random.randint(self.y, 350)
                        self.turnFlag = 1
        else : pass
    def draw(self):
        global hostage_num
        self.aniDelay +=1
        if self.survive == True:
            if self.position == self.KING:self.king.clip_draw(self.frame*40, 0, 40,40, 350+self.x-0.20*(carpet.x-350), 350+self.y-0.20*(carpet.y-350))
            elif self.position == self.QUEEN:self.queen.clip_draw(self.frame*40, 0, 40,40, 350+self.x-0.20*(carpet.x-350), 350+self.y-0.20*(carpet.y-350))
            elif self.position == self.CLERGY:self.clergy.clip_draw(self.frame*40, 0, 40,40, 350+self.x-0.20*(carpet.x-350), 350+self.y-0.20*(carpet.y-350))
            elif self.position == self.KNIGHT:self.knight.clip_draw(self.frame*40, 0, 40,40, 350+self.x-0.20*(carpet.x-350), 350+self.y-0.20*(carpet.y-350))
            elif self.position == self.BUTLER:self.butler.clip_draw(self.frame*40, 0, 40,40, 350+self.x-0.20*(carpet.x-350), 350+self.y-0.20*(carpet.y-350))
            elif self.position == self.SLAVE1:self.slave1.clip_draw(self.frame*40, 0, 40,40, 350+self.x-0.20*(carpet.x-350), 350+self.y-0.20*(carpet.y-350))
            elif self.position == self.SLAVE2:self.slave2.clip_draw(self.frame*40, 0, 40,40, 350+self.x-0.20*(carpet.x-350), 350+self.y-0.20*(carpet.y-350))

            if self.aniDelay == 30 :
                self.frame = (self.frame+1)%2
                self.aniDelay=0
        elif self.survive == False:
            self.hostageDie.clip_draw(self.frame*40, 0, 40,40, 350+self.x-0.20*(carpet.x-350), 350+self.y-0.20*(carpet.y-350))
            if self.aniDelay == 10:
                self.frame = (self.frame+1)%12
                self.aniDelay = 0
                if self.frame == 0:
                    for i in range(-1, len(hostageList)-1):
                        if self == hostageList[i]:
                            del hostageList[i]
                            hostage_num-=1
                            break

def distance(v1X,v1Y,  v2X, v2Y):
    return math.sqrt((v1X-v2X)*(v1X-v2X)+ (v1Y-v2Y)*(v1Y-v2Y))

#주인공의 스킬 속성 변화를 관리하는 함수
def supervise_bullet():
    global heroSkillBox
    global enemy2RazerBox
    global ballRazerBox
    global enemy2
    global carpet

    #supervise skill1
    for i in range(-1, len(heroSkill1Box)-1):
        if heroSkill1Box[i] in heroSkill1Box:
            if heroSkill1Box[i].direct == 'UP':
                if heroSkill1Box[i].y-0.7*(carpet.y-heroSkill1Box[i].carpetY) > 800-0.20*(carpet.y-350) : heroSkill1Box[i].collision = True
            elif heroSkill1Box[i].direct == 'DOWN':
                if heroSkill1Box[i].y-0.7*(carpet.y-heroSkill1Box[i].carpetY) < -100-0.20*(carpet.y-350) : heroSkill1Box[i].collision = True
            elif heroSkill1Box[i].direct == 'LEFT':
                if heroSkill1Box[i].x-0.7*(carpet.x-heroSkill1Box[i].carpetX) < -100-0.20*(carpet.x-350) : heroSkill1Box[i].collision = True
            elif heroSkill1Box[i].direct == 'RIGHT':
                if heroSkill1Box[i].x-0.7*(carpet.x-heroSkill1Box[i].carpetX) > 800-0.20*(carpet.x-350) : heroSkill1Box[i].collision = True
    # superbise_allSkill
    for i in range(-1, len(heroSkillBox)-1):
        for j in range(-1, len(heroSkillBox[i])-1):
            if heroSkillBox[i][j].collision == False:
                if ((enemy2.x-0.7*(carpet.x-350)-40 < heroSkillBox[i][j].x-0.7*(carpet.x-heroSkillBox[i][j].carpetX) and \
                    heroSkillBox[i][j].x-0.7*(carpet.x-heroSkillBox[i][j].carpetX) < enemy2.x-0.7*(carpet.x-350)+40 and \
                    enemy2.y-0.7*(carpet.y-350)-100 < heroSkillBox[i][j].y-0.7*(carpet.y-heroSkillBox[i][j].carpetY) and \
                    heroSkillBox[i][j].y-0.7*(carpet.y-heroSkillBox[i][j].carpetY) < enemy2.y-0.7*(carpet.y-350)+100)) or \
                        ((enemy2.x-0.7*(carpet.x-350)-75 < heroSkillBox[i][j].x-0.7*(carpet.x-heroSkillBox[i][j].carpetX) and \
                    heroSkillBox[i][j].x-0.7*(carpet.x-heroSkillBox[i][j].carpetX) < enemy2.x-0.7*(carpet.x-350)+75 and \
                    enemy2.y-0.7*(carpet.y-350)-40 < heroSkillBox[i][j].y-0.7*(carpet.y-heroSkillBox[i][j].carpetY) and \
                    heroSkillBox[i][j].y-0.7*(carpet.y-heroSkillBox[i][j].carpetY) < enemy2.y-0.7*(carpet.y-350)+40)) : heroSkillBox[i][j].collision = True
                for b in range(-1, len(enemy2.ballList)-1):
                    if enemy2.ballList[b].ball_survive == True:
                        if i == 0: #첫 번째 스킬이고
                            if 35 > distance(enemy2.ballList[b].x-0.7*(carpet.x-350), enemy2.ballList[b].y-0.7*(carpet.y-350), heroSkillBox[i][j].x-0.7*(carpet.x-heroSkillBox[i][j].carpetX),heroSkillBox[i][j].y-0.7*(carpet.y-heroSkillBox[i][j].carpetY)):
                                heroSkillBox[i][j].collision = True
                                enemy2.ballList[b].HP-=1
                        else:
                            if 40 > distance(enemy2.ballList[b].x-0.7*(carpet.x-350), enemy2.ballList[b].y-0.7*(carpet.y-350), heroSkillBox[i][j].x-0.7*(carpet.x-heroSkillBox[i][j].carpetX),heroSkillBox[i][j].y-0.7*(carpet.y-heroSkillBox[i][j].carpetY)):
                                heroSkillBox[i][j].collision = True
                                enemy2.ballList[b].HP-=heroSkillBox[i][j].power


    # enemy2 razer
    for i in range(-1, len(enemy2RazerBox)-1):
        if enemy2RazerBox[i] in enemy2RazerBox:
            if enemy2RazerBox[i].y-0.7*(carpet.y-enemy2RazerBox[i].carpetY) > 800-0.20*(carpet.y-350) or \
                enemy2RazerBox[i].y-0.7*(carpet.y-enemy2RazerBox[i].carpetY) < -100-0.20*(carpet.y-350) or \
                enemy2RazerBox[i].x-0.7*(carpet.x-enemy2RazerBox[i].carpetX) < -100-0.20*(carpet.x-350) or \
                enemy2RazerBox[i].x-0.7*(carpet.x-enemy2RazerBox[i].carpetX) > 800-0.20*(carpet.x-350) :
                enemy2RazerBox[i].collision = True
    for i in range(-1, len(enemy2RazerBox)-1):
        for j in range(-1, len(hostageList)-1):
            if 20 > distance(350+hostageList[j].x-0.20*(carpet.x-350), 350+hostageList[j].y-0.20*(carpet.y-350), enemy2RazerBox[i].x-0.7*(carpet.x-enemy2RazerBox[i].carpetX), enemy2RazerBox[i].y-0.7*(carpet.y-enemy2RazerBox[i].carpetY) ) and \
                hostageList[j].survive == True:
                hostageList[j].survive = False
                hostageList[j].frame = 0
                hostageList[j].aniDelay = 0
    # ball razer
    for i in range(-1, len(ballRazerBox)-1):
        if ballRazerBox[i] in ballRazerBox:
            if ballRazerBox[i].y-0.7*(carpet.y-ballRazerBox[i].carpetY) > 800-0.20*(carpet.y-350) or \
                ballRazerBox[i].y-0.7*(carpet.y-ballRazerBox[i].carpetY) < -100-0.20*(carpet.y-350) or \
                ballRazerBox[i].x-0.7*(carpet.x-ballRazerBox[i].carpetX) < -100-0.20*(carpet.x-350) or \
                ballRazerBox[i].x-0.7*(carpet.x-ballRazerBox[i].carpetX) > 800-0.20*(carpet.x-350) :
                ballRazerBox[i].collision = True




# 인질의 속성 변화를 관리하는 함수


def supervise_hostage():
    global hostageList
    global delay_create_hostage
    global carpet
    global hostage_num

    if hostage_num < 30:
        delay_create_hostage+=1
        if delay_create_hostage ==50:
            hostageList.append(Hostage())
            hostage_num+=1
            delay_create_hostage = 0

    for i in range(-1, len(hostageList)-1):
        if 80 > distance(350+hostageList[i].x-0.20*(carpet.x-350), 350+hostageList[i].y-0.20*(carpet.y-350), carpet.x, carpet.y ) and \
                hostageList[i].survive == True:
            del hostageList[i]
            hostage_num-=1
            break


def handle_events(): #플래그에 한 순간 영향받는 변수 처리
    global running
    global carpet
    global hero

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE: running = False
            # 마법 타입이 바뀔 수 있는 유일한 부분.l
            if event.key == SDLK_LSHIFT or event.key == SDLK_RSHIFT:
                hero.skill1Delay = 0
                hero.skill2Delay = 0
                if hero.skillType == 'SKILL1' : hero.skillType = 'SKILL2'
                elif hero.skillType == 'SKILL2' : hero.skillType = 'SKILL3'
                elif hero.skillType == 'SKILL3' : hero.skillType = 'SKILL1'
            if event.key == SDLK_d: carpet.goToRight = True
            if event.key == SDLK_a: carpet.goToLeft = True
            if event.key == SDLK_w: carpet.goToUp = True
            if event.key == SDLK_s: carpet.goToDown = True
            # 주인공의 공격 방향 설정 및 공격을 수행한다.
            if event.key == SDLK_i or event.key == SDLK_k or event.key ==SDLK_j or event.key == SDLK_l:
                if event.key == SDLK_i : hero.attackDirect = 'UP'
                if event.key == SDLK_k : hero.attackDirect = 'DOWN'
                if event.key == SDLK_j : hero.attackDirect = 'LEFT'
                if event.key == SDLK_l : hero.attackDirect = 'RIGHT'
                # hero.state는 공격 모션, 마법 탄환 생성에 영향을 준다.
                hero.state = 'ATTACK'
                hero.delay = 0
                hero.frame = 0

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_d: carpet.goToRight = False
            if event.key == SDLK_a: carpet.goToLeft = False
            if event.key == SDLK_w: carpet.goToUp = False
            if event.key == SDLK_s: carpet.goToDown = False
            if event.key == SDLK_i or event.key == SDLK_k or event.key ==SDLK_j or event.key == SDLK_l:
                hero.attackDirect = 'DEFAULT'
                hero.state = 'NORMAL'
                hero.skill1Delay = 0
                hero.attackAniFlag = 0
                hero.delay = 0
                hero.frame = 0
            pass
        #공격 키 간에 동기화가 필요해보인다.

#UI 관련 클래스
ui = None

#맵 관련 클래스
map = None

#주인공 관련 클래스
hero = None                       #주인공 인스턴스
heroSkillBox = []
heroSkill1Box = []                   #주인공 skill1 타입 마법 관리 리스트
heroSkill2Box = []                   #주인공 skill2 타입 마법 관리 리스트
heroSkill3Box = []                   #주인공 skill3 타입 마법 관리 리스트
heroSkillBox.append(heroSkill1Box)
heroSkillBox.append(heroSkill3Box)
#양탄자 관련 클래스
carpet = None

#enemy2 클래스
enemy2 = None
enemy2RazerBox = []
enemy2BombBox = []
ballRazerBox = []

#인질 리스트
hostageList=[]
delay_create_hostage = 0
hostage_num = 0

#running = True;

#리팩토링
def enter():
    global map
    global ui
    global hero
    global carpet
    global enemy2
    map = Map()
    ui = UI()
    hero = Hero()
    carpet = Carpet()
    enemy2 = Enemy2()


def exit():
    global map
    global ui
    global hero
    global carpet
    global enemy2
    del(map)
    del(ui)
    del(hero)
    del(carpet)
    del (enemy2)


def update():
    carpet.update()
    hero.update()
    enemy2.update()
    for ball in enemy2.ballList:
        ball.update()
    for skill1 in heroSkill1Box:
         skill1.update()
    for skill3 in heroSkill3Box:
         skill3.update()
    for razer in enemy2RazerBox:
        razer.update()
    for razer in ballRazerBox:
        razer.update()
    for hostage in hostageList:
        hostage.update()
    supervise_bullet()
    supervise_hostage()
    #delay(0.005)


def draw():
    clear_canvas()
    map.draw()
    carpet.draw()
    hero.draw()
    for hostage in hostageList:
        hostage.draw()
    enemy2.draw()
    for ball in enemy2.ballList:
        ball.draw()
    for skill1 in heroSkill1Box:
        skill1.draw()
    for skill2 in heroSkill2Box:
        skill2.draw()
    for skill3 in heroSkill3Box:
        skill3.draw()
    for razer in enemy2RazerBox:
        razer.draw()
    for razer in ballRazerBox:
        razer.draw()
    for bomb in enemy2BombBox:
        bomb.draw()

    #ui.draw()
    update_canvas()


