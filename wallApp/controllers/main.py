from wallApp import app
from flask import Flask
from flask import Flask, render_template, request, redirect, session, flash
from wallApp.models.user import User
from wallApp.models.post import Post
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from datetime import datetime
dateFormat = "%m/%d/%Y %-I:%M %p"

@app.route('/landing')
def landingDashboard():
    if 'userId' in session:
        data = {
            "i" : session['userId']
            }
        return render_template(
            'landing.html', 
            users = User.getAllButOne(data), 
            user = User.findById(data), 
            recievedPosts = Post.findRecievedByUserId(data), 
            followers = User.getFollowers(data),
            dtf = dateFormat, 
        )
    return redirect('/')

@app.route('/follow/<int:followed>')
def follow(followed):
    if 'userId' in session:
        User.follow({"i" : session['userId'],"z" : followed})
        return redirect('/landing')
    return redirect('/')

@app.route('/unfollow/<int:toUnFollow>')
def unFollow(toUnFollow):
    if 'userId' in session:
        data = {      
                "z" : toUnFollow
            }
        User.unfollow(data)
        return redirect('/landing')
    return redirect('/')

@app.route('/user/edit')
def editUser():
    if 'userId' in session:
        data = {
            "i" : session['userId']
            }
        return render_template(
            'editUser.html', 
            user = User.findById(data) )
    return redirect('/')

@app.route('/user/edit', methods=['POST'])
def editUserPOST():
    sessionUserId= session['userId']
    email = request.form['email']
    if 'userId' in session:
        if email != User.findById({"i" : sessionUserId}).email:
            if not User.uniqueEmail({ "e" : email}):
                return redirect('/user/edit')
        if User.validateUser(request.form) :
            data = {
                "fn" : request.form['firstName'].capitalize(),
                "ln" : request.form['lastName'].capitalize(),
                "e" : email,
                "i" : sessionUserId
            }
            User.findById({"i" : sessionUserId}).updateUser(data)
            return redirect('/user/edit')
        return redirect('/user/edit')
    return redirect('/')
