# Jira automation

## 1. Yêu cầu: 

- Tạo group trên jira và thêm các user vào group đó, 

## 2. Câu lệnh mẫu:

~~~bash
python3 autojira.py -U johnwick -P 123456@ --u johndue alex --g GROUP1 --f myfile --d [TN]
~~~

## 3. Các tham số truyền vào:

- username: bắt buộc.
- password: bắt buộc.
- user: tên một hoặc nhiều user để add vào group.
- group: tên nhóm muốn tạo. Ví dụ: [MAAHT2304APP].
- division: tên scheme_permission. Ví dụ: [tên division][MAAHT2304APP].
- file: tên file để đọc quyền và group phân quyền.

## 4. Quick note:

- Phải nhập vào username và password.
- Grant permission cần có file excel và tên division kèm theo.
- Sửa file trong git repo khi muốn thay đổi group phân quyền.

## 5.Quick run:
### Step 1: git clone https://github.com/miasnguyenx/JIra-automation
### Step 2: pip install -r requirements.txt

### Step 3: chạy file theo câu lệnh mẫu
