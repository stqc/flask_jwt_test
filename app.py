from backend import app,db,jwt
from backend.models import users
from flask import request, jsonify
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required,current_user,set_access_cookies,unset_jwt_cookies

@app.route('/signup',methods=['POST'])
def index():
    if request.method =='POST':
        try:            
            username = request.form['username']
            password = request.form['password']
            new_user = users(uname=username,pword=password)
            db.session.add(new_user)
            db.session.commit()
            return {"status":"success"}
        
        except Exception as e:
            print(e)
            return {'status':'Failed'}

@app.route('/login',methods=['POST'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        usr = users.query.filter_by(username=username).first()
        if usr.password == password:
            access_token = create_access_token(identity = username) #get access for a username with create_access_token(identity = username)
            response = jsonify({'login_status':'success'})
            set_access_cookies(response,access_token)#sends x-csrf-token in the cookie visible by js and hides the JWT, when using this the JWT is encoded with a double submit token to prevenet CSRF attacks
            return response
        else:
            return {'login_status':'wrong password or username'}

@app.route('/logout', methods=['POST'])
def logout():
    response = jsonify({"status":"successful"})
    unset_jwt_cookies(response)
    return response

@app.route('/allusers',methods=["GET"])
@jwt_required() #jwt protects from calls without a jwt token
def show_all():
    if request.method=='GET':
        user=users.query.all()
        user_dict = {}
        for u in user:
            user_dict[u.id]=u.username
        return user_dict

@app.route('/showprofile/<user_name>',methods=['GET'])
@jwt_required()
def show_profile(user_name):
    if request.method == 'GET':
        requester = get_jwt_identity() #automatically get username accessing this endpoint
        use = users.query.filter_by(username=user_name).all()
        output ={'requester':requester}
        for i in use:
            output[i.id] = i.username
        return output

#loads up the user that is trying to access the jwt protected route
@jwt.user_lookup_loader
def user_lookup_callback(jwt_header,jwt_data):
    #print(jwt_header)
    #print(jwt_data) contains JWT Data , the sub key contains the username belonging to this username
    identity = jwt_data["sub"]
    return users.query.filter_by(username=identity).first()

#route to load up user that is currently accessing the protected route
@app.route('/showself', methods=['GET'])
@jwt_required()
def show_self_info():
    return {'current_user':current_user.username}

if __name__ == "__main__":
    app.run(debug=True)