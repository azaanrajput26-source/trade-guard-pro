from kivy.app import App
from kivy.lang import Builder
from datetime import datetime

trade_history = []

KV = """
ScrollView:
    BoxLayout:
        orientation: "vertical"
        padding: 18
        spacing: 12
        size_hint_y: None
        height: self.minimum_height

        canvas.before:
            Color:
                rgba: 0.03, 0.04, 0.08, 1
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: "TRADE GUARD PRO PLUS"
            font_size: 28
            bold: True
            color: 0, 1, 0.7, 1
            size_hint_y: None
            height: 60

        TextInput:
            id: market
            hint_text: "Market Name e.g. BTC / GOLD"
            font_size: 18
            multiline: False
            background_color: 0.15, 0.17, 0.22, 1
            foreground_color: 1, 1, 1, 1
            size_hint_y: None
            height: 55

        TextInput:
            id: price
            hint_text: "Current Price"
            font_size: 18
            multiline: False
            input_filter: "float"
            background_color: 0.15, 0.17, 0.22, 1
            foreground_color: 1, 1, 1, 1
            size_hint_y: None
            height: 55

        TextInput:
            id: ema50
            hint_text: "EMA 50"
            font_size: 18
            multiline: False
            input_filter: "float"
            background_color: 0.15, 0.17, 0.22, 1
            foreground_color: 1, 1, 1, 1
            size_hint_y: None
            height: 55

        TextInput:
            id: ema200
            hint_text: "EMA 200"
            font_size: 18
            multiline: False
            input_filter: "float"
            background_color: 0.15, 0.17, 0.22, 1
            foreground_color: 1, 1, 1, 1
            size_hint_y: None
            height: 55

        TextInput:
            id: rsi
            hint_text: "RSI"
            font_size: 18
            multiline: False
            input_filter: "float"
            background_color: 0.15, 0.17, 0.22, 1
            foreground_color: 1, 1, 1, 1
            size_hint_y: None
            height: 55

        TextInput:
            id: account
            hint_text: "Account Balance e.g. 100"
            font_size: 18
            multiline: False
            input_filter: "float"
            background_color: 0.15, 0.17, 0.22, 1
            foreground_color: 1, 1, 1, 1
            size_hint_y: None
            height: 55

        TextInput:
            id: risk
            hint_text: "Risk % e.g. 2"
            font_size: 18
            multiline: False
            input_filter: "float"
            background_color: 0.15, 0.17, 0.22, 1
            foreground_color: 1, 1, 1, 1
            size_hint_y: None
            height: 55

        Button:
            text: "ANALYZE TRADE"
            font_size: 22
            bold: True
            background_color: 0, 0.75, 0.45, 1
            size_hint_y: None
            height: 60
            on_press: app.analyze()

        Button:
            text: "SHOW HISTORY"
            font_size: 20
            bold: True
            background_color: 0.15, 0.35, 0.75, 1
            size_hint_y: None
            height: 55
            on_press: app.show_history()

        Button:
            text: "CLEAR"
            font_size: 20
            bold: True
            background_color: 0.35, 0.35, 0.35, 1
            size_hint_y: None
            height: 55
            on_press: app.clear()

        Label:
            id: result
            text: "Enter values and press Analyze"
            font_size: 18
            bold: True
            color: 1, 1, 1, 1
            size_hint_y: None
            height: 330
"""

class TradeGuardProPlus(App):
    def build(self):
        self.title = "Trade Guard Pro Plus"
        return Builder.load_string(KV)

    def analyze(self):
        try:
            market = self.root.ids.market.text or "Unknown"
            price = float(self.root.ids.price.text)
            ema50 = float(self.root.ids.ema50.text)
            ema200 = float(self.root.ids.ema200.text)
            rsi = float(self.root.ids.rsi.text)
            account = float(self.root.ids.account.text)
            risk_percent = float(self.root.ids.risk.text)

            risk_amount = account * (risk_percent / 100)

            signal = "NO TRADE"
            trend = "Market unclear"
            sl = "-"
            tp = "-"
            rr = "-"
            qty = "-"
            confidence = 40
            warning = "Wait for clearer setup."
            color = (1, 0.9, 0.1, 1)

            if price > ema50 and ema50 > ema200:
                trend = "Uptrend"
                confidence += 20
            elif price < ema50 and ema50 < ema200:
                trend = "Downtrend"
                confidence += 20

            if 45 <= rsi <= 55:
                confidence += 20
            elif 40 <= rsi <= 65:
                confidence += 10

            if price > ema50 and ema50 > ema200 and 40 <= rsi <= 60:
                signal = "BUY"
                sl = round(price * 0.98, 2)
                tp = round(price * 1.04, 2)
                risk_per_unit = price - sl
                reward_per_unit = tp - price
                rr = round(reward_per_unit / risk_per_unit, 2)
                qty = round(risk_amount / risk_per_unit, 4)
                confidence += 20
                warning = "Use small risk. Avoid revenge trading."
                color = (0, 1, 0.4, 1)

            elif price < ema50 and ema50 < ema200 and 40 <= rsi <= 65:
                signal = "SELL"
                sl = round(price * 1.02, 2)
                tp = round(price * 0.96, 2)
                risk_per_unit = sl - price
                reward_per_unit = price - tp
                rr = round(reward_per_unit / risk_per_unit, 2)
                qty = round(risk_amount / risk_per_unit, 4)
                confidence += 20
                warning = "Use stop loss. Do not overtrade."
                color = (1, 0.2, 0.2, 1)

            if confidence > 95:
                confidence = 95

            result = (
                f"Market: {market}\n"
                f"Signal: {signal}\n"
                f"Trend: {trend}\n"
                f"Confidence: {confidence}%\n"
                f"Entry Price: {price}\n"
                f"Stop Loss: {sl}\n"
                f"Take Profit: {tp}\n"
                f"Risk Amount: {round(risk_amount, 2)}\n"
                f"Position Size: {qty}\n"
                f"Risk/Reward: {rr}\n"
                f"Warning: {warning}"
            )

            self.root.ids.result.text = result
            self.root.ids.result.color = color

            trade_history.append(
                f"{datetime.now().strftime('%H:%M')} | {market} | {signal} | Price: {price} | SL: {sl} | TP: {tp}"
            )

        except:
            self.root.ids.result.text = "Enter all numbers correctly"
            self.root.ids.result.color = (1, 1, 1, 1)

    def show_history(self):
        if len(trade_history) == 0:
            self.root.ids.result.text = "No trade history yet."
            self.root.ids.result.color = (1, 1, 1, 1)
        else:
            self.root.ids.result.text = "\n".join(trade_history[-8:])
            self.root.ids.result.color = (1, 1, 1, 1)

    def clear(self):
        self.root.ids.market.text = ""
        self.root.ids.price.text = ""
        self.root.ids.ema50.text = ""
        self.root.ids.ema200.text = ""
        self.root.ids.rsi.text = ""
        self.root.ids.account.text = ""
        self.root.ids.risk.text = ""
        self.root.ids.result.text = "Enter values and press Analyze"
        self.root.ids.result.color = (1, 1, 1, 1)

TradeGuardProPlus().run()