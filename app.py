from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        try:
            buy_price = float(request.form["buy_price"])
            sell_price = float(request.form["sell_price"])
            quantity = int(request.form["quantity"])

            # === 基本金額 ===
            buy_total = buy_price * quantity
            sell_total = sell_price * quantity

            # === 交易成本（台灣）===
            fee_rate = 0.001425   # 手續費 0.1425%
            tax_rate = 0.003      # 證交稅 0.3%

            buy_fee = buy_total * fee_rate
            sell_fee = sell_total * fee_rate
            sell_tax = sell_total * tax_rate

            # === 損益 ===
            profit = (sell_total - sell_fee - sell_tax) - (buy_total + buy_fee)

            result = {
                "profit": f"{profit:,.2f}",
                "buy_fee": f"{buy_fee:,.2f}",
                "sell_fee": f"{sell_fee:,.2f}",
                "sell_tax": f"{sell_tax:,.2f}"
            }

        except ValueError:
            result = {"error": "請輸入正確的數字格式"}

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
