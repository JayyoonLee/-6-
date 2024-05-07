def calculate_total_cost(items):
    total_cost = 0
    for item in items:
        total_cost += item['price'] * item['quantity']
    return total_cost

def main():
    items = []
    while True:
        food_name = input("음식 이름을 입력하세요 (종료하려면 'q' 입력): ")
        if food_name.lower() == 'q':
            break
        price = float(input("음식 가격을 입력하세요: "))
        quantity = int(input("음식 수량을 입력하세요: "))
        items.append({'name': food_name, 'price': price, 'quantity': quantity})

    total_cost = calculate_total_cost(items)
    print("\n푸드코스트 정산 내역:")
    for item in items:
        print(f"{item['name']}: {item['quantity']}개 - {item['price']}원")
    print(f"\n총 비용: {total_cost}원")

if __name__ == "__main__":
    main()
