from flask import Flask, render_template, request
import mysql.connector
connector=mysql.connector.connect(host="localhost",user="root",password="gajendra",database="chatbot")
cursor=connector.cursor()


from twilio.rest import Client
import random
import numpy as np
import model_recommandation as sugg
import news 
import you_tube_recommandation as you_tube
from newsapi import NewsApiClient

# Replace these values with your actual Twilio credentials
TWILIO_ACCOUNT_SID = 'AC5127904a59e6533d154fbf2dfcd596e4'
TWILIO_AUTH_TOKEN = '899f8caf028f66a93ba95f1e64c0893f'
TWILIO_PHONE_NUMBER = '+16599009903'

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


# Replace these values with your actual database credentials
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'gajendra',
    'database': 'chatbot',
}

app = Flask(__name__)
def execute_query(query, params=None, fetchone=False):
    with mysql.connector.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            if fetchone:
                result = cursor.fetchone()
                return result[0] if result else None
            else:
                result = cursor.fetchall()
                return result if result else None




@app.route('/')
def index():
    return render_template('signup.html')

@app.route('/index.html')
def login():
    return render_template('index.html')

@app.route('/marks.html')
def marks():
    return render_template('marks.html')




@app.route('/login', methods=['POST'])
def login_new():
    email = request.form['signupEmail']
    userpassword = request.form['loginPassword']

    query = "SELECT password FROM unique_employees WHERE emp_email = %s"
    password = execute_query(query, (email,), fetchone=True)
    
    query = "SELECT emp_name FROM unique_employees WHERE emp_email = %s"
    emp_name = execute_query(query, (email,), fetchone=True)
    
    unique_list=get_all_emails()
    
    if email not in unique_list:
        return render_template('signup.html', error="This email is Not Registered please Signup First")
    else:
        if password is not None:
            if password == userpassword:
                emp_hobby = execute_query("SELECT emp_hobby FROM unique_employees WHERE emp_email = %s", (email,), fetchone=False)[0][0]
                # print("this is emp_hobby",emp_hobby)
                result=sugg.recommend(emp_hobby)
                newss=news.news()
                return render_template('home_page.html', username=emp_name,result=(result,newss) )
            else:
                return render_template('index.html', error="Invalid password")

        return render_template('index.html', error="User not found")











otp=str(np.random.randint(1,9,4))[:]

@app.route('/signup', methods=['POST'])
def signup():
    
   
    # Handle signup logic here
    # You can access form data using request.form['fieldname']
    username = request.form['signupUsername']
    email = request.form['signupEmail']
    password = request.form['signupPassword']
    mobile_number = request.form['mobilenumber']
    Hobby = request.form['hobby']
    age=request.form['age']
    
    unique_list=get_all_emails()
    
    
    if email in unique_list:
            return render_template('signup.html', error="This email is already Registered please use other emails")
    else:
            
        # Use parameterized query to prevent SQL injection
        query="insert into unique_employees(emp_name,emp_email,password,mobile_number,emp_hobby,emp_age) values('{}','{}','{}','{}','{}','{}'   )".format(username,email,password,mobile_number,Hobby,age)
        
        cursor.execute(query)
        query="commit"
        cursor.execute(query)
        
        
        message = client.messages.create(
                        to="+91"+"{}".format(mobile_number),
                        from_=TWILIO_PHONE_NUMBER   ,  # Your Twilio phone number
                        body='hello my name is gajendra and otp is {}{}{}{}'.format(otp[1],otp[3],otp[5],otp[7]))

        # After handling signup logic, you can redirect or render a new template
        return render_template('otp_verification.html', username=username)





@app.route('/verify_otp',methods=['POST'])
def verify_otp():
    user_otp=request.form['otp']
    
    user_email=request.form["userEMAIL"]
    
    emp_hobby = execute_query("SELECT emp_hobby FROM unique_employees WHERE emp_email = %s", (user_email,), fetchone=False)[0][0]
    
    print("this is emp_hobby",emp_hobby)
    result=sugg.recommend(emp_hobby)
    newss=news.news()
    
    
    if str('{}{}{}{}'.format(otp[1],otp[3],otp[5],otp[7])) == user_otp:
        return render_template('home_page.html',result = (result,newss))
        
    else:
        return render_template('otp_verification.html',error="Invalid otp")

@app.route('/result', methods=['POST'])
def result_output():
    subject = request.form['subject']
    query = request.form['textareaMessage']
    user_email = request.form["userEMAIL"]
    # print(user_email)
    
    emp_id = execute_query("SELECT emp_id FROM unique_employees WHERE emp_email = %s", (user_email,), fetchone=False)
    # print("this is your emp_id",emp_id)
    if not emp_id:
        return render_template('home_page.html',result=(None,None), error="Employee ID not found.")
    
    emp_id = emp_id[0][0]  # Extracting emp_id from the result

    # print("this is emp_id", emp_id)
    
    marks = execute_query("SELECT emp_marks FROM user_marks_details WHERE emp_id = %s", (emp_id,), fetchone=False)
    if not marks or marks[0] in [None,0]:
        return render_template('home_page.html',result=(None,None), error="Please enter the Student marks.")

    marks = marks[0]
    # print("this is marks", marks[0])
    
     
    cursor.execute("INSERT INTO user_history(emp_id, emp_email, emp_subject, emp_query) VALUES (%s, %s, %s, %s)", (emp_id, user_email, subject, query))
    cursor.execute("COMMIT")
    
    performance = get_performance_category(marks[0])
    # performance="Beginner"
    if subject == "Language" or subject == "language":
        prompt = f"User: I provided you English language text input -> {query}\n"
        prompt += f"User: Provide appropriate corrections to improve language skills\n"
        prompt += f"User: also , write the correct form of input text final output look like 'INPUT TEXT ->       \n CORRECTED TEXT ->   '\n  CORRECTED WORD  \n"   
        prompt += f" return  the output in html code"
        prompt += "Chatbot:"
        
        answer=cg.TextGenerator(prompt)
        # print(answer)
        return render_template('result.html', result_html=answer    )
    elif subject  == "Health" or subject ==  "health":
        prompt = f"User: I have a Question  in English for  Related to health and Question is  -> {query}\n"
        prompt += "User: Please provide me Guidance for  enhance the health .\n"
        prompt += "User: The final output should look like:\n"
        prompt += "'HEALTH GUIDANCE'\n"
        prompt += f" return  the output in html code"
        prompt += "Chatbot: "
        answer=cg.TextGenerator(prompt)
        # print(answer)
        return render_template('result.html', result_html=answer    )
        
        
    else:
        answer = get_answer(subject, query, performance)
        ans = speech_answer(query)

        result_html = f"{answer}"
        return render_template('result.html', result_html=answer)




@app.route('/marks', methods=['POST'])
def marks_update():
    user_email = request.form['signupEmail']
    marks = request.form['marks']
    unique_list=get_all_emails()
    if user_email not in unique_list:
            return render_template('marks.html', error="This email is Not Registered please Registered emails")
    emp_id = execute_query("SELECT emp_id FROM unique_employees WHERE emp_email = %s", (user_email,), fetchone=False)
    emp_id = emp_id[0][0]  # Extracting emp_id from the result
    query = "INSERT INTO user_marks_details(emp_id,emp_marks) VALUES ('{}', '{}')".format(emp_id,marks)
    cursor.execute(query)
    query = "COMMIT"
    cursor.execute(query)
    return render_template('marks.html', error="Marks update Successfully")






@app.route('/suggestion_hobby/', methods=['POST'])
def Suggest():
    user_email = request.form["user"]
    # Assuming you have a function to get user's hobby from the database
    # Replace the below line with your database query
    emp_hobby = "hobby"  # Execute your database query to get user's hobby
    
    # Assuming you have a function to get search results from YouTube API
    result = you_tube.main(emp_hobby)
    
    if result.empty:
        has_results = False
    else:
        has_results = True
    
    return render_template('sugg.html', result=result, has_results=has_results)






@app.route("/alexa", methods=["POST"])
def alexa_output():
    user_email = request.form["userEMAIL"]
    question = request.form["alexa_input"]
    # print("use Ques")
    subject="Alexa"
    # print("this is my email",user_email)
    # print(question)

    emp_id = execute_query("SELECT emp_id FROM unique_employees WHERE emp_email = %s", (user_email,), fetchone=False)[0][0]
    # print(emp_id)
    marks = execute_query("SELECT emp_marks FROM user_marks_details WHERE emp_id = %s", (emp_id,), fetchone=False)
    if not marks or marks[0] in [None,0]:
        return render_template('home_page.html',result=(None,None), error="Please enter the Student marks.")
    
    marks = marks[0]
    # print(marks)
    performance = get_performance_category(marks[0])
    
    last_study_topic = execute_query("SELECT Last_key FROM student WHERE Student_id = %s", (emp_id,), fetchone=False)[0][0]
    last_study_topic_name= execute_query("SELECT topic FROM python_syllabus WHERE key_value = %s", (last_study_topic,), fetchone=False)[0][0]
    print("this is my last updatation",last_study_topic,last_study_topic_name)
    

    cursor.execute("INSERT INTO user_history(emp_id, emp_email, emp_subject, emp_query) VALUES (%s, %s, %s, %s)", (emp_id, user_email, subject, question))
    cursor.execute("COMMIT")
    
    prompt = f"User: I'm interested in learning more about Python.\n"
    prompt += f"User: My topic is: {last_study_topic_name}.\n"
    prompt += f"User: write the short answer in html code\n"
    prompt += "Chatbot:"
    # print(prompt)    
    answer=cg.TextGenerator(prompt)
    # subject=None
    # answer = get_answer(subject, question, performance)
    # ans = speech_answer(query)
    result_html = f" Your next Topic is {last_study_topic_name}"
    result_html = f"{answer}"
    
    cursor.execute("UPDATE student SET Last_key = Last_key + 1 WHERE Student_id = %s", (emp_id,))
    connector.commit()
    return render_template('result.html', result_html=result_html)

    
    
@app.route('/result_page_suggestion', methods=['POST'])
def result_page_suggestion():
    user_email = request.form.get("userEMAIL") 
    old_question = request.form.get("old_question")  

    if not user_email or not old_question:
        return render_template('home_page.html', result=(None, None), error="Invalid user email or old question.")

    emp_id_result = execute_query("SELECT emp_id FROM unique_employees WHERE emp_email = %s", (user_email,), fetchone=False)
    
    if emp_id_result is None or not emp_id_result:
        return render_template('home_page.html', result=(None, None), error="No employee found with the provided email.")
    
    emp_id = emp_id_result[0][0]  # Access the first result and first column

    marks_result = execute_query("SELECT emp_marks FROM user_marks_details WHERE emp_id = %s", (emp_id,), fetchone=False)
    
    if marks_result is None or not marks_result:
        return render_template('home_page.html', result=(None, None), error="No marks found for the employee.")
    
    marks = marks_result[0][0]  # Access the first result and first column

    # Assuming `get_performance_category()` and other functions are defined correctly
    performance = get_performance_category(marks)
    subject = "Suggestion based"

    # Assuming `cursor` is defined and connected to the database correctly
    cursor.execute("INSERT INTO user_history(emp_id, emp_email, emp_subject, emp_query) VALUES (%s, %s, %s, %s)", (emp_id, user_email, subject, old_question))
    cursor.execute("COMMIT")

    prompt = f"User: I'm currently studying the topic: {old_question}.\n"
    prompt += f"User: Can you suggest me more recent study topics?\n"
    prompt += f"User: Please provide the short  response in HTML format.\n"
    prompt += "Chatbot:"

    answer = cg.TextGenerator(prompt)
    result_html = f" Your next Topic is "
    result_html = f"{answer}"

    return render_template('result.html', result_html=result_html)


@app.route('/resultalexa', methods=['POST'])
def result_page_alexa():
    user_email = request.form["userEMAIL"]
    question = request.form["alexa_input"]
    subject="alexa"
    emp_id = execute_query("SELECT emp_id FROM unique_employees WHERE emp_email = %s", (user_email,), fetchone=False)[0][0]
    # print(emp_id)
    marks = execute_query("SELECT emp_marks FROM user_marks_details WHERE emp_id = %s", (emp_id,), fetchone=False)
    if not marks or marks[0] in [None, 0]:
        return render_template('home_page.html', result=(None, None), error="Please enter the Student marks.")

    
    marks = marks[0]
    performance = get_performance_category(marks[0])
    
    cursor.execute("INSERT INTO user_history(emp_id, emp_email, emp_subject, emp_query) VALUES (%s, %s, %s, %s)", (emp_id, user_email, subject, question))
    cursor.execute("COMMIT")
    
    prompt = f"User: I have a question.\n"
    prompt += f"User: {question}\n"
    prompt += f"User: My understanding level is {performance} .write the short answer in html code\n"
    prompt += "Chatbot:"
    
    answer=cg.TextGenerator(prompt)
    return render_template("result.html",result_html=answer)


    
    
    
    
    


import content_generator as cg

def generate_prompt(subject, question , performace):
    prompt = f"User: In the subject of {subject}, I have a question.\n"
    prompt += f"User: {question}\n"
    prompt += f"User: My understanding level is {performace} .write the short answer in html code\n"
    prompt += "Chatbot:"
    return prompt

def speech_answer(question):
    ans = cg.TextGenerator(f"User: write small answer for the question -> {question}. Chatbot:")
    return ans


def get_answer(subject,question,performace):
    full_prompt = generate_prompt(subject, question, performace)
    text = cg.TextGenerator(full_prompt)
    return text

def get_performance_category(total_marks):
    if total_marks is None:
        return "No data available"
    elif total_marks < 45:
        return "Beginner"
    elif 45 <= total_marks <= 70:
        return "Intermediate"
    else:
        return "Advanced"
    
def get_all_emails():
    all_mails = execute_query("SELECT emp_email FROM unique_employees", fetchone=False)
    unique_list=[]
    for i in all_mails:
        unique_list.append(i[0])
    return unique_list

if __name__ == '__main__':
    app.run(debug=True)
