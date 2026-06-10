from flask import Flask, render_template, request, jsonify
import uuid
import re

app = Flask(__name__)

# دالة بسيطة للتحقق من صيغة تاريخ الانتهاء MM/YY
def is_valid_expiry(expiry):
    pattern = r"^(0[1-9]|1[0-2])\/([0-9]{2})$"
    return bool(re.match(pattern, expiry))

@app.route('/')
def index():
    # عرض الصفحة الرئيسية ونظام الدفع
    return render_template('index.html')

@app.route('/process_payment', codecs=['POST'])
def process_payment():
    try:
        data = request.get_json()
        
        # استخراج البيانات القادمة من الواجهة الأمامية
        card_number = data.get('card_number', '').strip()
        expiry = data.get('expiry', '').strip()
        cvv = data.get('cvv', '').strip()
        amount = data.get('amount', '')

        # 1. التحقق من وجود جميع الحقول
        if not all([card_number, expiry, cvv, amount]):
            return jsonify({
                "success": False,
                "message": "برجاء ملء جميع الحقول المطلوبة بشكل صحيح."
            }), 400

        # 2. التحقق من رقم البطاقة (يجب أن يكون 16 رقماً بعد التنظيف في الـ JS)
        if not card_number.isdigit() or len(card_number) != 16:
            return jsonify({
                "success": False,
                "message": "رقم البطاقة غير صالح، يجب أن يتكون من 16 رقماً."
            }), 400

        # 3. التحقق من صيغة تاريخ الانتهاء (MM/YY)
        if not is_valid_expiry(expiry):
            return jsonify({
                "success": False,
                "message": "تاريخ الانتهاء غير صالح. الصيغة الصحيحة هي الشهر/السنة (MM/YY)."
            }), 400

        # 4. التحقق من الـ CVV (يجب أن يكون 3 أرقام)
        if not cvv.isdigit() or len(cvv) != 3:
            return jsonify({
                "success": False,
                "message": "رمز الأمان (CVV) غير صالح، يجب أن يتكون من 3 أرقام."
            }), 400

        # 5. التحقق من قيمة المبلغ
        try:
            amount_float = float(amount)
            if amount_float <= 0:
                raise ValueError
        except ValueError:
            return jsonify({
                "success": False,
                "message": "قيمة المبلغ يجب أن تكون أكبر من الصفر."
            }), 400

        # ---- محاكاة معالجة الدفع الناجحة ----
        # توليد رقم عملية فريد عشوائي لحفظ المعاملة
        transaction_id = str(uuid.uuid4().hex[:12]).upper()

        return jsonify({
            "success": True,
            "message": f"تمت عملية الدفع بنجاح بقيمة ${amount_float:.2f}",
            "transaction_id": f"PAY-{transaction_id}"
        }), 200

    except Exception as e:
        # التعامل مع أي أخطاء غير متوقعة في الخادم
        return jsonify({
            "success": False,
            "message": "حدث خطأ داخلي في الخادم أثناء معالجة العملية."
        }), 500

if __name__ == '__main__':
    # تشغيل التطبيق في وضع التطوير المحلي
    app.run(debug=True)
    
