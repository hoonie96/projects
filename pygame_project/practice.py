lst = ["가", "나", "다"]

for lst_idx, lst_val in enumerate(lst):
    print(lst_idx, lst_val)

##################################################################################

balls = [1, 2, 3, 4]
weapons = [11, 22, 3, 44]

for ball_idx, ball_val in enumerate(balls):
    print("ball :", ball_val)
    for weapon_idx, weapon_val in enumerate(weapons):
        print("weapon :", weapon_val)
        if ball_val == weapon_val: # 충돌 체크
            print("공과 무기가 충돌")
            break
    else:
        continue
    print("바깥 for 문 break")
    break
    
    # if 조건:
    #     동작
    # else: 
    #     그 외의 동작