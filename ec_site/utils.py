def calculate_shipping_fee(total_amount):
    # 送料計算のロジックをここに実装します。
        if total_amount >= 10000:
            return 0
        else:
            return 500