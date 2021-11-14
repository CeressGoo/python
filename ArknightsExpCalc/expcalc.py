def expcalc():
    l4 = int(input('Level 4 gold books:'))
    l3 = int(input('Level 3 yellow books:'))
    l2 = int(input('Level 2 blue books:'))
    l1 = int(input('Level 1 green books:'))

    exp_sum = 2000 * l4 + 1000 * l3 + 400 * l2 + 200 * l1

    l4_ratio = format(200000 * l4 / exp_sum, '.2f')
    l3_ratio = format(100000 * l3 / exp_sum, '.2f')
    l2_ratio = format(40000 * l2 / exp_sum, '.2f')
    l1_ratio = format(20000 * l1 / exp_sum, '.2f')

    print('*'*50)
    print(f'Total exp: {exp_sum}')
    print(f'gold: {2000 * l4} ({l4_ratio}%)')
    print(f'yellow: {1000 * l3} ({l3_ratio}%)')
    print(f'blue: {400 * l2} ({l2_ratio}%)')
    print(f'green: {200 * l1} ({l1_ratio}%)')
    print('*'*50)

def main():
    loopctrl = True
    while loopctrl:
        expcalc()
        loopctrl = input('Recalculate?[y/n]').upper() == 'Y'

if __name__ == '__main__':
    main()
