from flask import Flask, render_template, request
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

app = Flask(__name__, static_url_path='/static')

data = pd.read_excel('unemployment_cleaned.xlsx')  

# Bağımsız değişkenleri ve bağımlı değişkeni belirle
X = data[['Inflation, consumer prices (annual %)', 'Inflation, GDP deflator (annual %)', 
          'Real interest rate (%)', 'Deposit interest rate (%)', 'Lending interest rate (%)']]
y = data['Unemployment, total (% of total labor force) (national estimate)']

# Rastgele Orman regresör modelini tanımla ve eğit
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
rf_regressor.fit(X, y)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Kullanıcı girişlerini al
        inflation_consumer_prices = float(request.form['inflation_consumer_prices'])
        inflation_gdp_deflator = float(request.form['inflation_gdp_deflator'])
        real_interest_rate = float(request.form['real_interest_rate'])
        deposit_interest_rate = float(request.form['deposit_interest_rate'])
        lending_interest_rate = float(request.form['lending_interest_rate'])
        
        # Kullanıcı girişlerini bir veri çerçevesine dönüştür
        user_input = pd.DataFrame({
            'Inflation, consumer prices (annual %)': [inflation_consumer_prices],
            'Inflation, GDP deflator (annual %)': [inflation_gdp_deflator],
            'Real interest rate (%)': [real_interest_rate],
            'Deposit interest rate (%)': [deposit_interest_rate],
            'Lending interest rate (%)': [lending_interest_rate]
        })

        # Tahmin yap
        predicted_unemployment = rf_regressor.predict(user_input)
        

        return render_template('result.html', predicted_unemployment=predicted_unemployment[0])

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
