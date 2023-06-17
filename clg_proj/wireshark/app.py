from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
#store the pcapng file in files folder

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file found"

    file = request.files['file']
    if file.filename == '':
        return "No file selected"

    if file and file.filename.endswith('.pcapng'):
        file.save('files/hello.pcapng')
        return "File uploaded successfully"

    return "Invalid file format"
#retrievs the csv file from files folder and sends it to index.html
@app.route('/details', methods=['GET','POST'])
def display_details():
    os.system("echo CURRENT WORKING DIRECTORY")

    # gets a choice from the user on filtering parameters
    usr_choice = 1
    usr_choice = request.form.get("choice")
    print("User choive ", usr_choice)
    # gets the value of the current choice
    usr_val = request.form.get("ipaddr")

    # writing the index within the csv file
    line = "Srno., Date, Time, IP source, IP destination, Protocol, Packet length"

    # os.system("tshark -r files/hello.pcapng > files/traffic.csv")
    os.system("tshark -r files/hello.pcapng -T fields -E separator=, -e frame.number -e frame.time -e ip.src -e ip.dst -e ip.proto -e frame.len > files/traffic.csv")
    with open('files/traffic.csv', 'r') as file:
        df = file.read()
    print(df)
    with open('files/traffic.csv', 'w') as file:
        file.write(line + '\n' + df)
    df = pd.read_csv('files/traffic.csv', sep=',')
    print(usr_choice)
    # using the "all" filter
    if usr_choice == 1 or None:
        html_table = df.to_html(index=False)
        print(type(html_table))
        print(html_table)
    elif usr_choice == 2:
        # filtered_df = df[df['ip.proto'] == 'tcp']
        print(df[1])
    else:
        html_table = df.to_html(index=False)
        print(type(html_table))
        print(html_table)
    return html_table

if __name__ == '__main__':
    app.run()
