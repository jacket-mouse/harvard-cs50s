from logic import *

hair = Symbol("有毛发")
milk = Symbol("有奶")
feather = Symbol("有羽毛")
can_fly = Symbol("会飞")
lay_egg = Symbol("会下蛋")
eat_meat = Symbol("吃肉")
canine_tooth = Symbol("有犬齿")
claw = Symbol("有爪")
look_ahead = Symbol("眼盯前方")
feet = Symbol("有蹄")
rumination = Symbol("反刍")
tawny = Symbol("黄褐色")
dot = Symbol("有暗斑点")
black_stripes = Symbol("有黑色条纹")
long_neck = Symbol("长脖子")
long_leg = Symbol("长腿")
can_swim = Symbol("会游泳")
black_white = Symbol("黑白二色")
mammals = Symbol("哺乳类")
birds = Symbol("鸟类")
carnivorous = Symbol("食肉类")
hoofs = Symbol("蹄类")
leopard = Symbol("金钱豹")
tiger = Symbol("老虎")
giraffe = Symbol("长颈鹿")
zebra = Symbol("斑马")
ostrich = Symbol("鸵鸟")
penguin = Symbol("企鹅")
albatross = Symbol("信天翁")

symbols = [hair, milk, feather, can_fly, 
               lay_egg, eat_meat, canine_tooth, 
               claw, look_ahead, feet, rumination, 
               tawny, dot, black_stripes, long_neck, 
               long_leg, can_swim, black_white, mammals,
               birds, carnivorous, hoofs]
animals = [mammals, birds, carnivorous, hoofs, leopard, tiger, giraffe, zebra, ostrich, penguin, albatross]

knowledge = And(
    Implication(hair, mammals),
    Implication(milk, mammals),
    Implication(feather, birds),
    Implication(And(can_fly, lay_egg), birds),
    Implication(eat_meat, carnivorous),
    Implication(And(canine_tooth, claw, look_ahead), carnivorous),
    Implication(And(mammals, feet), hoofs),
    Implication(And(mammals, rumination), hoofs),
    Implication(And(mammals, carnivorous, tawny, dot), leopard),
    Implication(And(mammals, carnivorous, tawny, black_stripes), tiger),
    Implication(And(hoofs, long_neck, long_leg, dot), giraffe),
    Implication(And(hoofs, black_stripes), zebra),
    Implication(And(birds, long_neck, long_leg, Not(can_fly), black_white), ostrich),
    Implication(And(birds, can_swim, Not(can_fly), black_white), penguin),
    Implication(And(birds, can_fly), albatross)
)

def main():
    print(Implication(And(birds, can_fly), albatross).symbols())
    print("输入对应条件前的数字：")
    print("##############################################")
    for idx, symbol in enumerate(symbols, 1):
        if idx % 4 == 0: print()
        print(str(idx)+"."+str(symbol), end=" ")
    print()
    print("##############################################")
    print("###########当输入数字0时，程序结束############")
    select = []
    length = 0
    while(True):
        select.append(int(input("请输入：")) - 1)
        if select[length] == -1: break
        length += 1
    
    print("前提条件为：")
    for idx in range(len(symbols)):
        if idx in select:
            print(symbols[idx], end=" ")
            knowledge.add(symbols[idx])
        else:
            if symbols[idx] in animals:
                continue
            knowledge.add(Not(symbols[idx]))
    print()

    print("推理过程如下：")
    for animal in animals:
        print(f"    {animal}")
        if model_check(knowledge, animal):
             print(f"    {animal}") 

if __name__ == "__main__":
    main()