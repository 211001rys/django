# views.py
import re
import uuid

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date

from .models import Employee, Shiiregyosha, Medicine, Treatment
from .models import Tabyouin
from .models import Patient


def login_view(request):
    if request.method == 'POST':
        empid = request.POST['empid']
        emppasswd = request.POST['emppasswd']
        try:
            employee = Employee.objects.get(empid=empid)
            if employee.emprole == 1:

                if emppasswd == employee.emppasswd:
                    request.session['employee_id'] = employee.empid
                    request.session['employee_role'] = employee.emprole
                    return render(request, 'E100/E100.html')

            if employee.emprole == 2:
                if check_password(emppasswd, employee.emppasswd):
                    request.session['employee_id'] = employee.empid
                    request.session['employee_role'] = employee.emprole
                    return render(request, 'E100/E103.html')

            if employee.emprole == 3:
                 if check_password(emppasswd, employee.emppasswd):
                    request.session['employee_id'] = employee.empid
                    request.session['employee_role'] = employee.emprole
                    return render(request, 'E100/E104.html')

            if emppasswd == employee.emppasswd:
                request.session['employee_id'] = employee.empid
                if employee.emprole == 1:
                    return render(request, 'E100/E100.html')
                elif employee.emprole == 2:
                    return render(request, 'E100/E103.html')
                elif employee.emprole == 3:
                    return render(request, 'E100/E104.html')
                else:
                    return render(request, 'E100/E100.html')

                    return render(request, 'L101.html', {'error': 'Unknown role'})
            else:
                return render(request, 'L101.html', {'error': 'Invalid password'})
        except Employee.DoesNotExist:
            return render(request, 'L101.html', {'error': 'Employee not found'})
    return render(request, 'L101.html')

def logout_view(request):
    logout(request)
    return render(request, 'L101.html')


def home1(request):
    return render(request, 'E100/E101.html')


# 従業員登録
def employee_register(request):
    if request.method == 'POST':
        empid = request.POST.get('empid')
        empfname = request.POST.get('empfname')
        emplname = request.POST.get('emplname')
        emppasswd = request.POST.get('emppasswd')
        confirm_password = request.POST.get('confirm_password')
        emprole = request.POST.get('emprole')

        # エラーチェック
        errors = []
        if not empid or not empfname or not emplname or not emppasswd or not confirm_password or not emprole:
            errors.append("All fields are required.")
        if emppasswd != confirm_password:
            errors.append("Passwords do not match.")
        if Employee.objects.filter(empid=empid).exists():
            errors.append("User ID already exists.")

        if errors:
            return render(request, 'E100/E101.html', {'errors': errors})

        # セッションにデータを保存して確認画面へ
        request.session['employee_form_data'] = {
            'empid': empid,
            'empfname': empfname,
            'emplname': emplname,
            'emppasswd': emppasswd,
            'emprole': emprole,
        }
        return redirect('employee_confirm')

    return render(request, 'E100/E101.html')

def employee_confirm(request):
    form_data = request.session.get('employee_form_data')
    if not form_data:
        return redirect('employee_register')

    if request.method == 'POST':
        emprole=form_data['emprole']
        emppasswd = form_data['emppasswd']
        if emprole == '1':
            hashed_password = emppasswd
        else:
            hashed_password = make_password(emppasswd)
        # 登録処理
        Employee.objects.create(
            empid=form_data['empid'],
            empfname=form_data['empfname'],
            emplname=form_data['emplname'],
            emppasswd=hashed_password,
            emprole=form_data['emprole'],
        )
        messages.success(request, 'Employee registered successfully!')
        return redirect('employee_register_complete')

    return render(request, 'E100/employee_confirm.html', {'form_data': form_data})

# 従業員登録完了ビュー
def employee_register_complete(request):
    return render(request, 'E100/Completion.html')

def employee_search_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        try:
            employee = Employee.objects.get(empid=user_id)
            return redirect('employee_update_view', empid=employee.empid)
        except Employee.DoesNotExist:
            messages.error(request, '従業員が見つかりません。')
            return redirect('employee_search_view')
    return render(request, 'E100/E102.html')


def employee_update_view(request, empid):
    employee = get_object_or_404(Employee, empid=empid)
    if request.method == 'POST':
        empfname = request.POST.get('empfname')
        emplname = request.POST.get('emplname')
        errors = []

        if not empfname and not emplname:
            errors.append('姓または名のいずれかを入力してください。')

        if errors:
            return render(request, 'E100/E108.html', {'errors': errors, 'employee': employee})

        if empfname:
            employee.empfname = empfname
        if emplname:
            employee.emplname = emplname
        employee.save()
        messages.success(request, '従業員情報を更新しました。')
        return redirect('employee_search_view')
    return render(request, 'E100/E108.html', {'employee': employee})


def employee_update_search(request):
    if request.method == 'POST':
        empid = request.POST.get('empid')
        errors = []

        if not empid:
            errors.append('ユーザーIDは必須です。')
        else:
            try:
                employee = Employee.objects.get(empid=empid)
                return render(request, 'E100/E106.html', {'employee': employee})
            except Employee.DoesNotExist:
                errors.append('従業員が見つかりませんでした。')


def supplier_list_view(request):
    suppliers = Shiiregyosha.objects.all()
    return render(request, 'S100/S102.html', {'suppliers': suppliers})


def success(request):
    return None


def convert_to_number(value):
    # 全角数字を半角に変換
    value = value.translate(str.maketrans('０１２３４５６７８９', '0123456789'))
    # 全角カンマを半角カンマに変換
    value = value.replace('，', ',')
    # 半角カンマを削除
    value = value.replace(',', '')
    # 全角および半角の\や￥を削除
    value = value.replace('￥', '').replace('\\', '')

    try:
        return float(value)
    except ValueError:
        return None

def search_hospitals_by_capital(request):
    hospitals = []
    if request.method == 'POST':
        capital_input = request.POST.get('capital', '')

        # エラーチェック
        if not capital_input:
            errors = ['資本金の入力は必須です。.']
            return render(request, 'H100/H104.html', {'errors': errors})

        # 資本金の値を変換
        capital = convert_to_number(capital_input)
        if capital is None:
            errors = ['資本金は有効な数値である必要があります。']
            return render(request, 'H100/H104.html', {'errors': errors})

        if capital < 0:
            errors = ['資本金は0以上でなければなりません。']
            return render(request, 'H100/H104.html', {'errors': errors})


        # DBから資本金が入力された値以上の病院を検索
        hospitals = Tabyouin.objects.filter(tabyouinshihonkin__gte=capital)

        if not hospitals:
            message = '入力された金額以上の資本金を持つ病院は見つかりませんでした。'
            return render(request, 'H100/H104.html', {'message': message})

    return render(request, 'H100/H104.html', {'hospitals': hospitals})


def edit_hospital(request, tabyouinid):
    hospital = get_object_or_404(Tabyouin, tabyouinid=tabyouinid)

    if request.method == 'POST':
        new_phone = request.POST.get('phone_number')

        # 電話番号のフォーマットを確認
        phone_pattern = re.compile(r'^\(?\d{2,4}\)?-?\d{2,4}-?\d{3,4}$')
        if not phone_pattern.match(new_phone) or len(new_phone) > 14:
            messages.error(request, '有効な電話番号を入力してください。')
            return render(request, 'H100/confirm_hospital.html', {'tabyouin': hospital})

        if request.POST.get('action') == 'confirm':
            # 確認画面を表示
            return render(request, 'H100/confirm_hospital.html', {'new_phone': new_phone})

        elif request.POST.get('action') == 'update':
            # 電話番号を更新
            hospital.tabyouintel = new_phone
            hospital.save()
            messages.success(request, '電話番号が正常に更新されました。')
            return redirect('hospital_list')

    return render(request, 'H100/confirm_hospital.html', {'tabyouin': hospital})

def hospital_list(request):
    hospitals = Tabyouin.objects.all()
    return render(request, 'H100/hospital_list.html', {'hospitals': hospitals})




# ここから受付

#ホーム画面に移動
def home2(request):
    return render(request, 'E100/E104.html')

# 患者登録
def patient_register(request):
    if request.method == 'POST':
        patid = request.POST.get('patid')
        patfname = request.POST.get('patfname')
        patlname = request.POST.get('patlname')
        hokenmei = request.POST.get('hokenmei')
        hokenexp = request.POST.get('hokenexp')

        # エラーチェック
        errors = []
        if not patid:
            errors.append('患者IDは必須です。')
        if not patfname:
            errors.append('患者名は必須です。')
        if not patlname:
            errors.append('患者姓は必須です。')
        if not hokenmei:
            errors.append('保険証記号番号は必須です。')
        if not hokenexp:
            errors.append('有効期限は必須です。')
        else:
            try:
                hokenexp_date = parse_date(hokenexp)
                if not hokenexp_date:
                    raise ValueError
            except ValueError:
                errors.append('有効な有効期限を入力してください。')

        # 保険証記号番号の長さをチェックし、10桁でなければエラーを返す
        if hokenmei and (not hokenmei.isdigit() or len(hokenmei) != 10):
            errors.append('保険証記号番号は10桁の数字で入力してください。')

        if errors:
            return render(request, 'P100/P101.html', {'errors': errors})

        # 確認画面表示
        if 'confirm' in request.POST:
            return render(request, 'P100/P101_confirm.html', {
                'patid': patid,
                'patfname': patfname,
                'patlname': patlname,
                'hokenmei': hokenmei,
                'hokenexp': hokenexp,
            })

        # 登録処理
        if 'register' in request.POST:
            Patient.objects.create(
                patid=patid,
                patfname=patfname,
                patlname=patlname,
                hokenmei=hokenmei,
                hokenexp=hokenexp
            )
            messages.success(request, '患者が正常に登録されました。')
            return redirect('patient_register_success')

    return render(request, 'P100/P101.html')

def patient_register_success(request):
    return render(request, 'P100/P101_success.html')


#従業員パスワード変更
def password_change_view(request):
    employee_role = request.session.get('employee_role')
    employee_id = request.session.get('employee_id')

    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not password1 or not password2:
            messages.error(request, "パスワードを入力してください。")
        elif password1 != password2:
            messages.error(request, "パスワードが一致しません。")
        else:
            employee = get_object_or_404(Employee, pk=employee_id)
            employee.emppasswd = make_password(password1)
            employee.save()
            messages.success(request, "パスワードが変更されました。")
            return redirect('password_change_success')

    return render(request, 'E100/password_change.html')

def password_change_success_view(request):
    return render(request, 'E100/password_change_success.html')


# 患者検索
def patient_search_view(request):
    patients = None
    if request.method == 'POST':
        search_name = request.POST.get('search_name')
        if search_name:
            patients = Patient.objects.filter(patfname__icontains=search_name) | Patient.objects.filter(patlname__icontains=search_name)
            if not patients:
                messages.error(request, '該当する患者が見つかりませんでした。')
        else:
            messages.error(request, '検索名を入力してください。')
    return render(request, 'P100/P103.html', {'patients': patients})

# 患者保険証変更


def patient_insurance_edit(request):
    if request.method == 'POST':
        mode = request.POST.get('mode')

        if mode == 'search':
            patid = request.POST.get('patid')
            try:
                patient = Patient.objects.get(patid=patid)
                return render(request, 'P100/P102.html', {'patient': patient})
            except Patient.DoesNotExist:
                messages.error(request, '患者が見つかりません。')
                return redirect('patient_insurance_edit')

        elif mode == 'modify':
            patid = request.POST.get('patid')
            patient = get_object_or_404(Patient, patid=patid)
            new_patfname = request.POST.get('patfname', patient.patfname)
            new_patlname = request.POST.get('patlname', patient.patlname)
            new_hokenmei = request.POST.get('hokenmei', patient.hokenmei)
            new_hokenexp = request.POST.get('hokenexp', patient.hokenexp)

            # 保険証記号番号の長さをチェックし、10桁でなければエラーを返す
            if new_hokenmei and (not new_hokenmei.isdigit() or len(new_hokenmei) != 10):
                messages.error(request, '保険証記号番号は10桁の数字で入力してください。')
                return render(request, 'P100/P102.html', {'patient': patient})

            # その他の入力チェック
            errors = []
            if new_hokenmei and not new_hokenexp:
                errors.append('保険証記号番号が変わるときは有効期限も変わっていなければなりません。')
            elif new_hokenexp:
                try:
                    new_hokenexp_date = parse_date(new_hokenexp)
                    if not new_hokenexp_date:
                        raise ValueError

                    if new_hokenexp_date < patient.hokenexp:
                        errors.append('有効期限は現在の期限より後の日付である必要があります。')
                    elif new_hokenexp_date == patient.hokenexp:
                        errors.append('有効期限を現在の期限と同一日付には変更できません。')

                except ValueError:
                    errors.append('有効な有効期限を入力してください。')

            if errors:
                return render(request, 'P100/P102.html', {
                    'patient': patient,
                    'errors': errors
                })

            if request.POST.get('action') == 'confirm':
                # 確認画面を表示
                return render(request, 'P100/confirm_patient_insurance.html', {
                    'patient': patient,
                    'new_patfname': new_patfname,
                    'new_patlname': new_patlname,
                    'new_hokenmei': new_hokenmei,
                    'new_hokenexp': new_hokenexp
                })

            elif request.POST.get('action') == 'update':
                # 保険証情報を更新
                patient.patfname = new_patfname
                patient.patlname = new_patlname
                patient.hokenmei = new_hokenmei
                patient.hokenexp = new_hokenexp
                patient.save()
                messages.success(request, '変更完了')
                return redirect('patient_insurance_edit')

    return render(request, 'P100/P102.html')



def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'P100/patient_list.html', {'patients': patients})


# 医師
def doctor_home(request):
    return render(request, 'E100/E103.html')

# 患者検索

def patient_search_view2(request):
    patients = None
    if request.method == 'POST':
        search_fname = request.POST.get('search_fname')
        search_lname = request.POST.get('search_lname')
        if search_fname or search_lname:
            patients = Patient.objects.filter(
                patfname__icontains=search_fname,
                patlname__icontains=search_lname
            )
            if not patients:
                messages.error(request, '該当する患者が見つかりませんでした。')
        else:
            messages.error(request, '検索名を入力してください。')
    return render(request, 'D100/doctor_patient_search.html', {'patients': patients})

def medication_order_view(request, patid):
    patient = get_object_or_404(Patient, patid=patid)
    medicines = Medicine.objects.all()
    cart = request.session.get('cart', [])

    if request.method == 'POST':
        medicine_id = request.POST.get('medicine_id')
        dosage = request.POST.get('dosage')

        if not dosage.isdigit():
            messages.error(request, '数量は正の整数で入力してください。')
        else:
            cart.append({'medicine_id': medicine_id, 'dosage': dosage})
            request.session['cart'] = cart
            return redirect('medication_order_view', patid=patid)

    return render(request, 'D100/medicine_order.html', {
        'patient': patient,
        'medicines': medicines,
        'cart': cart
    })

def medication_confirm_view(request, patid):
    patient = get_object_or_404(Patient, patid=patid)
    cart = request.session.get('cart', [])

    if request.method == 'POST':
        if 'submit' in request.POST:
            for item in cart:
                Treatment.objects.create(
                    treatmentid=str(uuid.uuid4())[:8],
                    quantity=int(item['dosage']),
                    treatmentdata='投薬指示',
                    medicine=Medicine.objects.get(medicineid=item['medicine_id']),
                    patient=patient
                )
            request.session['cart'] = []
            messages.success(request, '処置が正常に登録されました。')
            return redirect('medication_order_view', patid=patient.patid)

        if 'delete' in request.POST:
            medicine_id = request.POST.get('medicine_id')
            cart = [item for item in cart if item['medicine_id'] != medicine_id]
            request.session['cart'] = cart
            messages.success(request, '処置が正常に削除されました。')
            return redirect('medication_order_view', patid=patient.patid)

        if 'back' in request.POST:
            return redirect('medication_order_view', patid=patient.patid)

    return render(request, 'D100/medicine_confirm.html', {
        'patient': patient,
        'cart': cart
    })


def search_patient_by_id(request):
    patients = None
    if request.method == 'POST':
        pat_id = request.POST.get('pat_id')
        if pat_id:
            try:
                patient = Patient.objects.get(patid=pat_id)
                return render(request, 'D100/medicine_order.html', {'patient': patient})
            except Patient.DoesNotExist:
                messages.error(request, '該当する患者が見つかりませんでした。')
        else:
            messages.error(request, '患者IDを入力してください。')
    return render(request, 'D100/D104.html', {'patients': patients})




def search_patient_by_id2(request):
    if request.method == 'POST':
        pat_id = request.POST.get('pat_id')
        if pat_id:
            try:
                patient = Patient.objects.get(patid=pat_id)
                treatments = Treatment.objects.filter(patient=patient)
                if treatments.exists():
                    return render(request, 'D100/D102.html', {'patient': patient, 'treatments': treatments})
                else:
                    messages.error(request, '該当患者に過去の処置履歴がありません。')
            except Patient.DoesNotExist:
                messages.error(request, '該当する患者が見つかりませんでした。')
        else:
            messages.error(request, '患者IDを入力してください。')
    return render(request, 'D100/D103.html')

