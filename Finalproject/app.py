from flask import Flask,render_template,request,redirect,session,url_for,flash
import sqlite3
# import pandas as pd
import csv
import numpy as np
import pickle
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
from sklearn.ensemble import RandomForestClassifier
from flask import Flask, request, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
 #valence Aware Dictionary for Sentiment Reasoning
import nltk
from string import punctuation
import re
from nltk.corpus import stopwords

nltk.download('stopwords')

set(stopwords.words('english'))
app = Flask(__name__)
app.secret_key = "590"

# --------------------------------indexpage---------------------------
@app.route('/')
def index():
      return render_template('index.html')

# --------------------------------registerpage---------------------------
@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == "POST":
# sqlite
        connection = sqlite3.connect("app_data.db")
        cursor = connection.cursor()

#Html form
        name=request.form['name']
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        confirmpassword=request.form['confirmpassword']
        data=[name,username,email,password,confirmpassword]
        #print(name,username,email,password,confirmpassword)

#login authentications

        query1="SELECT username FROM registerdata WHERE username='"+username+"'"
        cursor.execute(query1)
        results = cursor.fetchall()
        if len(results) != 0:
            # return "user already exists"
             flash("user already exists",'warning')
        else:

#register data insert

            query="INSERT INTO registerdata(name,username,email,password,confirmpassword) VALUES (?,?,?,?,?)"
            cursor.execute(query,data)
            connection.commit()
            # flash("register success",'info')
            return redirect('/login')
    return render_template('register.html')

# --------------------------------loginpage---------------------------
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
# sqlite
        connection = sqlite3.connect("app_data.db")
        cursor = connection.cursor()

#Html form
        username=request.form['namelogin']
        password=request.form['passwordlogin']

       # print(username,password)
#query
        query = "SELECT username,password FROM registerdata where username='"+username+"' and password='"+password+"'"
        cursor.execute(query)

        results = cursor.fetchall()
#validation
        if len(results) == 0:
            #  flash("userid and password is incorrect",'warning')
            return "userid and password is incorrect"
        else:
             session['user'] = username
             return redirect(url_for("home"))
    else:
        if "user" in session:
            return redirect(url_for("home"))
        return render_template('login.html')
 # --------------------------------adminlogin---------------------------
@app.route('/admin',methods=['GET','POST'])
def admin():
    if request.method == "POST":
# sqlite
        # connection = sqlite3.connect("app_data.db")
        # cursor = connection.cursor()

#Html form
        username=request.form['namelogin']
        password=request.form['passwordlogin']
      
        if(username=="admin" and password=="admin123"):
                return redirect("/adminhome")
        else:
            return "userid and password is incorrect"
    # else:
    return render_template('admin.html')

# --------------------------------homepage---------------------------
@app.route('/home',methods=['POST','GET'])
def home():
    if request.method == "POST":
# sqlite
        connection = sqlite3.connect("app_data.db")
        cursor = connection.cursor()
#Html form
        stop_words = stopwords.words('english')
    
        #convert to lowercase
        text1 = request.form['messagetext'].lower()
    
        text_final = ''.join(c for c in text1 if not c.isdigit())
    
    #remove punctuations
    #text3 = ''.join(c for c in text2 if c not in punctuation)
        
    #remove stopwords    
        processed_doc1 = ' '.join([word for word in text_final.split() if word not in stop_words])

        sa = SentimentIntensityAnalyzer()
        dd = sa.polarity_scores(text=processed_doc1)
        compound = round((1 + dd['compound'])/2, 2)
#Html form
        if compound *100 >50:
            comment=request.form['messagetext']
            productname=request.form['product']
            Sentiment="Positive"
            data=[productname,comment,Sentiment]
 #register data insert

            query="INSERT INTO comment(ProductName,ProductComment,Sentiment) VALUES (?,?,?)"
            cursor.execute(query,data)
            connection.commit()
        elif compound*100 <50:
            comment=request.form['messagetext']
            productname=request.form['product']
            Sentiment="Negative"
            data=[productname,comment,Sentiment]
 #register data insert

            query="INSERT INTO comment(ProductName,ProductComment,Sentiment) VALUES (?,?,?)"
            cursor.execute(query,data)
            connection.commit()
        else:
            Sentiment=flash("Give valid review",'info')        
    if 'user' in session:
        user = session['user']
            # flash("register success",'info')
            #return redirect('/login')
        return render_template('home.html')
    else:
      return redirect(url_for("login"))

@app.route('/address',methods=['POST','GET'])
def address():
    if request.method == "POST":
# sqlite
        connection = sqlite3.connect("app_data.db")
        cursor = connection.cursor()
#Html form
        Name=request.form['name']
        Address=request.form['address']
        Pincode=request.form['pincode']
        value=[Name,Address,Pincode]
 #register data insert
        query="INSERT INTO useraddress(Name,Address,pincode) VALUES (?,?,?)"
        cursor.execute(query,value)
        connection.commit()
    return render_template('home.html')

@app.route('/form', methods=['POST', 'GET'])
def my_form_post():
    if request.method == "POST":
         # sqlite
        connection = sqlite3.connect("app_data.db")
        cursor = connection.cursor()
        stop_words = stopwords.words('english')
    
        #convert to lowercase
        text1 = request.form['text1'].lower()
    
        text_final = ''.join(c for c in text1 if not c.isdigit())
    
    #remove punctuations
    #text3 = ''.join(c for c in text2 if c not in punctuation)
        
    #remove stopwords    
        processed_doc1 = ' '.join([word for word in text_final.split() if word not in stop_words])

        sa = SentimentIntensityAnalyzer()
        dd = sa.polarity_scores(text=processed_doc1)
        compound = round((1 + dd['compound'])/2, 2)
#Html form
        if compound *100 >50:
            Review=request.form['text1']
            Sentiment="Positive"
            data=[Review,Sentiment]
            query="INSERT INTO reviews(review,sentiment) VALUES (?,?)"
            cursor.execute(query,data)
            connection.commit()
        elif compound*100 <50:
            Review=request.form['text1']
            Sentiment="Negative"
            data=[Review,Sentiment]
            query="INSERT INTO reviews(review,sentiment) VALUES (?,?)"
            cursor.execute(query,data)
            connection.commit()
        else:
            Sentiment=flash("Give valid review",'info')
        
        
        return render_template('form.html', final=compound, text1=text_final,text2=dd['pos'],text5=dd['neg'],text4=compound,text3=dd['neu'])
    return render_template('form.html')
# --------------------------------adminhome---------------------------
@app.route('/adminhome', methods=['GET', 'POST'])
def adminhome():
    if request.method == 'GET':
        return render_template('adminhome.html')
    elif request.method == 'POST':
        results = []
        
        user_csv = request.form.get('user_csv').split('\n')
        reader = csv.DictReader(user_csv)
        
        for row in reader:
            results.append(dict(row))

        fieldnames = [key for key in results[0].keys()]

        return render_template('table.html', results=results, fieldnames=fieldnames, len=len)


    return render_template('adminhome.html')


@app.route('/graph', methods=['GET', 'POST'])
def graph():
    if request.method == "POST":
    #    comment=request.form['user_csv']
       img = mpimg.imread('newplot.png')
       imgplot = plt.imshow(img)
       plt.show()
    #    return redirect(url_for('output'))
    #    return render_template('form.html')
    return render_template('form.html')

# --------------------------------logoutpage---------------------------
@app.route('/logout')
def logout():
    session.pop("user",None)
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)