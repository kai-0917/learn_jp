from flask import Flask, render_template, request, redirect, url_for
import random, os

dir_path = "/Users/subin/Desktop/me/Japanese/website/data/verbs"

data = []
cnt = 0
on_test = False
mode = 0
miss_num = 0
current = False

###########################################
def init_para():
    global data, cnt, on_test, mode, current, miss_num
    data = []
    cnt = 0
    on_test = False
    mode = 0
    current = False
    miss_num = 0
    

def count_files():
    return len(os.listdir(dir_path))

def import_data(file_num_list):
    global data
    init_para()
    for i in file_num_list:
        with open("data/verbs/verb" + i + ".txt", "r") as f:
            for line in f.readlines():
                a = line.split()
                data.append([a.pop(0), a.pop(0), a.pop(0), a.pop(0), " ".join(a)])
    random.shuffle(data)
###########################################

def get_file_list():
    print("get_file_list running")
    print(len(request.form.getlist('file_cb')))
    return redirect("/select_file")


app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('select_file'))

@app.route('/select_file', methods=['GET', 'POST'])
def select_file():
    init_para()
    file_num = count_files()
    return render_template("select_file.html", file_num=file_num)

@app.route('/random_test', methods=['GET', 'POST'])
def random_test():
    global data, cnt, on_test, mode, current, miss_num
    if not on_test:
        cnt = 0
        file_list = request.form.getlist('file_cb')
        if len(file_list) == 0:
            return redirect(url_for("select_file"))
        import_data(file_list)
    if not on_test:
        on_test = True
        pair = data[cnt]
        return render_template("random_test.html", KR=data[cnt][2], hint=data[cnt][0] + "[" + data[cnt][1] + "]")
    user_input = request.form.get("user_input")
    print(user_input)
    pair = data[cnt]
    print(pair)
    if mode == 0:
        if user_input == pair[0] or user_input == pair[1]:
            mode = 1
            return render_template("random_test.html", KR=pair[4], hint=data[cnt][3])
        current = True
        return render_template("random_test.html", KR=pair[2], hint=pair[0] + "[" + pair[1] + "]")
    if user_input == pair[3]:
        if current == True:
            miss_num += 1
            current = False 
        cnt += 1
        if cnt == 20:
            return redirect(url_for("show_result"))
        mode = 0
        pair = data[cnt]
        return render_template("random_test.html", KR=pair[2], hint=pair[0] + "[" + pair[1] + "]")
    current = True
    return render_template("random_test.html", KR=pair[4], hint=data[cnt][3])

@app.route("/show_result")
def show_result():
    global miss_num
    return render_template("result.html", hit_rate= (20 - miss_num) * 5)
    

if __name__ == '__main__':
    app.run(debug=True)