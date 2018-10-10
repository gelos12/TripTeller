import datetime, time

ad = datetime
bd = datetime


print("시작 날짜(연/월/일) --> ")

year = int(input())
month = int(input())
date = int(input())

print(year, month ,date)

d1 = datetime.date(year, month, date) #입력날짜
d2 = datetime.date.today() #현재날짜 

if(d2 < d1): #입력 날짜가 현재 날짜보다 클 경우
    ad = d2 - d1
    print("입력하신 날짜보다 현재날짜가 {0} 일이 지났습니다.".format(ad))
    
elif(d1 < d2): #입력 날짜가 현재날짜보다 작을 경우
    bd = d1 - d2
    print("입력하신 날짜보다 현재날짜가 {0} 일 전입니다.".format(bd))
else:
    print("입력하신 날짜와 현재 날짜가 같습니다.")
    