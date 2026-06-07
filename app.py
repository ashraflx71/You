from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# الصفحة الرئيسية
@app.route('/')
def home():
    return render_template('index.html')

# معالجة عملية الدفع
@app.route('/process_payment', methods=['POST'])
def process_payment():
    data = request.get_json()
    
    # محاكاة معالجة الدفع
    card_number = data.get('card_number')
    amount = data.get('amount')
    
    # تحقق بسيط (في الحقيقة ستتصل بـ Stripe أو PayPal API)
    if card_number and amount:
        return jsonify({
            'success': True,
            'message': f'تم استلام مبلغ {amount}$ بنجاح',
            'transaction_id': 'TXN_' + os.urandom(4).hex()
        })
    else:
        return jsonify({
            'success': False,
            'message': 'بيانات الدفع غير مكتملة'
        }), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
