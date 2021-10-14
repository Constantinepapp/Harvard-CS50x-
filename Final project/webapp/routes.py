from flask import render_template, url_for, flash, redirect,abort,request,session
from flask_login import login_user,current_user,logout_user,login_required
import pygal
import pandas as pd
import csv
import numpy as np
from pygal.style import Style
import math
import datetime 
import requests
import time
from datetime import date
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.resources import CDN

from webapp import app,db,bcrypt
from webapp.forms import RegistrationForm,LoginForm,Running_Index,AccountForm,Import_file_csv,Personalized_program
from webapp.models import User,Post

from webapp import functions





@app.route("/home/<username>",methods=["GET","POST"])
@login_required
def home(username):
    user=User.query.filter_by(username=username).first()
    if user != current_user:
        abort(403)
    form = Running_Index()
    Rundex=0
    if form.validate_on_submit():
        HRmax=current_user.max_hr
        up=form.elevation_up.data
        down=form.elevation_down.data
        t=form.Duration.data
        distance=form.Distance.data
        HR=form.Heart_rate.data
        date=form.Date.data
        x=HR/HRmax*1.45-0.30
        d=distance+6*up-4*down
        RI0=213.9/t *(d/1000)**1.06 +3.5
        Rundex=RI0/x
        Rundex=round(Rundex,1)

        resting_heart_rate=current_user.resting_hr
        maximum_heart_rate=current_user.max_hr
        lactate_threshold_heart_rate=current_user.lactate_th
        
        #calculate trimp and tss
        hrr=(HR-resting_heart_rate)/(maximum_heart_rate-resting_heart_rate)
        trimp=0

        for i in range(0,int(t)):
            trimp=trimp +1*hrr*0.64*math.exp(1.92*hrr)

        hr_lthr=(lactate_threshold_heart_rate-resting_heart_rate)/(maximum_heart_rate-resting_heart_rate)
        hour_lthr=60*hr_lthr*0.64*math.exp(1.92*hr_lthr)
        tss=(trimp/hour_lthr)*100

        post=Post(date=form.Date.data,distance=form.Distance.data,duration=form.Duration.data,Heart_rate=form.Heart_rate.data,up=form.elevation_up.data,down=form.elevation_down.data,running_index=Rundex,tss=tss,trimp=trimp,athlete=current_user)
        db.session.add(post)
        db.session.commit()
            

        
        
        return render_template("home.html",form=form,Rundex=Rundex)
    return render_template('home.html',form=form,Rundex=Rundex)

@app.route("/register",methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home',username=current_user.username))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hashed_password,resting_hr=60,max_hr=200,lactate_th=180)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created {form.username.data}!','success')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/',methods=["GET","POST"])
@app.route("/login",methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home',username=current_user.username))
    form= LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=True)
            return redirect(url_for('home',username=current_user.username))
        else:
            flash(f"log in unsuccesful","danger")
    return render_template('login.html',form=form)


@app.route("/analytics/<username>" ,methods=["GET","POST"])
@login_required
def analytics(username):
    user=User.query.filter_by(username=username).first()
    if user != current_user:
        abort(403)

    date_list=Post.query.with_entities(Post.date).filter_by(athlete=current_user).order_by(Post.date.asc())
    Rundex_list=Post.query.with_entities(Post.running_index).filter_by(athlete=current_user).order_by(Post.date.asc())
    

    #this lines make a list out of list of turples
    date_list=[value for (value,) in date_list]
    Rundex_list=[value for (value,) in Rundex_list]

    #check if user has entered at least 3 activities to avoid out of index error
    if len(Rundex_list)<3:
        flash('Please enter at least 3 activities',"info")
        return redirect(url_for('home',username=current_user.username))

    #give Rundex_median 2 starting values so i dont get an error 
    Rundex_median=[Rundex_list[0],Rundex_list[1]]
    for i in  range(2,len(Rundex_list)):
        median=(Rundex_list[i-2]+Rundex_list[i-1]+Rundex_list[i])/3
        median=round(median,1)
        Rundex_median.append(median)

    your_running_fitness=Rundex_median[-1]


    custom_style = Style(
    background='transparent',
    plot_background='transparent',
    foreground='#FFFFFF',
    foreground_strong='#53A0E8',
    foreground_subtle='#343A40',
    opacity='.6',
    opacity_hover='.9',
    transition='400ms ease-in',
    colors=('#F1D901', '#E8537A', '#E95355', '#E87653', '#E89B53'))


    line_chart = pygal.Line(show_legend=False,width=1400,height=400,fill=False, interpolate='cubic', style=custom_style)
    line_chart.title = 'Running Fitness'
    line_chart.x_labels = date_list
    line_chart.add('Median', Rundex_median)
    line_chart.add('Raw', Rundex_list,stroke=False)
    
    line_chart.render()
    graph_data = line_chart.render_data_uri()

    table=Post.query.all()
    
    return render_template('analytics.html',graph_data=graph_data,table=table,your_running_fitness=your_running_fitness)


@app.route("/weeklymileage/<username>",methods=["GET","POST"])
@login_required
def weeklymileage(username):
    user=User.query.filter_by(username=username).first()
    if user != current_user:
        abort(403)
    
    date_list=[]
    distance_list=[]
    data_raw=Post.query.filter_by(athlete=current_user)
    # for loop to make the date list have a date format not string
    for item in data_raw:
        dat=datetime.datetime.strptime(item.date,'%Y-%m-%d')
        date_list.append(dat)
        distance_list.append(item.distance)

    #check if user has entered at least 3 activities to avoid out of index error
    if len(date_list)<3:
        flash('Please enter at least 3 activities',"info")
        return redirect(url_for('home',username=current_user.username))
        
    #created pandas dataframe from the two lists

    df = pd.DataFrame(
        {'Date': date_list,
        'Distance': distance_list,
        'week':''
        })

    #created a series of first day of the week so one entry for each week and the sum of distance for each week

    df = df.set_index('Date')
    series=df.resample('w').Distance.sum()

    # tranformed the series to a dataframe again and named the two columns as "Date" and "Sum"

    week_sum=pd.DataFrame({'Date':series.index, 'Sum':series.values})

    Average_per_week=0
    i=0
    for item in week_sum['Sum']:
        Average_per_week=Average_per_week+item/1000
        i=i+1
    
    Average_per_week=round(Average_per_week/len(week_sum['Sum']),2)



    custom_style = Style(
    background='transparent',
    plot_background='transparent',
    foreground='#FFFFFF',
    foreground_strong='#53A0E8',
    foreground_subtle='#343A40',
    opacity='.6',
    opacity_hover='.9',
    transition='400ms ease-in',
    colors=('#3294E8', '#FFFFFF', '#E95355', '#E87653', '#E89B53'))
    
    line_chart = pygal.StackedBar(show_legend=False,width=1400,height=400,fill=False, interpolate='cubic', style=custom_style)
    line_chart.title = 'Weekly mileage'
    line_chart.x_labels = week_sum['Date']
    line_chart.add('Median', week_sum['Sum']/1000)
    
    
    line_chart.render()
    trainingload_graph = line_chart.render_data_uri()
            
    return render_template('weeklymileage.html',trainingload_graph=trainingload_graph,Average_per_week=Average_per_week)


@app.route("/heartmonitor/<username>",methods=["GET","POST"])
@login_required
def heartmonitor(username):
    user=User.query.filter_by(username=username).first()
    if user != current_user:
        abort(403)
    return render_template('heartmonitor.html')

@app.route("/training_history/<username>",methods=["GET","POST"])
@login_required
def training_history(username):
    user=User.query.filter_by(username=username).first()
    if user != current_user:
        abort(403)
    table=Post.query.filter_by(athlete=current_user).order_by(Post.date.desc())
    return render_template('training_history.html',table=table)

@app.route("/training_zones/<username>",methods=["GET","POST"])
@login_required
def training_zones(username):
    user=User.query.filter_by(username=username).first()
    if user != current_user:
        abort(403)
    Running_fitness_list=Post.query.with_entities(Post.running_index).filter_by(athlete=current_user)

    Running_fitness_list=[value for (value,) in Running_fitness_list]

    #check if user has entered at least 3 activities to avoid out of index error
    if len(Running_fitness_list)<3:
        flash('Please enter at least 3 activities',"info")
        return redirect(url_for('home',username=current_user.username))

    

    Running_fitness=(Running_fitness_list[-1]+Running_fitness_list[-2]+Running_fitness_list[-3])/3
    Running_fitness=round(Running_fitness,1)

    Running_fitness_int=int(Running_fitness)
        
    #Aerobic_speed=(Running_fitness-10.48523539)/3.53842601
    Aerobic_speed_theory=(Running_fitness-5.668)/3.82
    Tempo_speed_theory=(Running_fitness-2.84)/3.75
    
    
    
    Tempo_speed_theory=round(Tempo_speed_theory,2)
    #Aerobic_speed=round(Aerobic_speed,2)
    Aerobic_speed_theory=round(Aerobic_speed_theory,2)

    #Tempo_speed=(Running_fitness-11.84)/3.13
    #Tempo_speed=round(Tempo_speed,2)


    rest=current_user.resting_hr
    max=current_user.max_hr
    reserve=max-rest

    aer1=int(rest+reserve*0.6)
    aer2=int(rest+reserve*0.7)
    aer3=int(rest+(reserve*0.7)+1)
    aer4=int(rest+reserve*0.8)
    thre1=int(rest+(reserve*0.8)+1)
    thre2=int(rest+reserve*0.9)
    max1=int(rest+(reserve*0.9)+1)

    Aerobic_speed_table=[]
    Running_fitness_table=[]
    for i in range (20,100):
        Running_fitness_table.append(i)

    for index in Running_fitness_table:
        Aerobic_speed_table.append(round((index-10.48523539)/3.53842601,2))

    return render_template('training_zones.html',Tempo_speed_theory=Tempo_speed_theory,Aerobic_speed_theory=Aerobic_speed_theory,Running_fitness_int=Running_fitness_int,Running_fitness_table=Running_fitness_table,Aerobic_speed_table=Aerobic_speed_table,rest=rest,aer1=aer1,aer2=aer2,aer3=aer3,aer4=aer4,thre1=thre1,thre2=thre2,max1=max1,max=max,Running_fitness=Running_fitness)


@app.route("/training_load/<username>",methods=["GET","POST"])
@login_required
def training_load(username):
    user=User.query.filter_by(username=username).first()

    if user !=current_user:
        abort(403)

    date_list=[]
    tss_list=[]
    data_raw=Post.query.filter_by(athlete=current_user)

    


    for item in data_raw:
        dat=datetime.datetime.strptime(item.date,'%Y-%m-%d')
        date_list.append(dat)
        tss_list.append(item.tss)

    #check if user has entered at least 3 activities to avoid out of index error
    if len(date_list)<3:
        flash('Please enter at least 3 activities',"info")
        return redirect(url_for('home',username=current_user.username))
    
    today_day=date.today()
    date_list.append(today_day)
    tss_list.append(0.00)
    

    df = pd.DataFrame(
        {'Date': date_list,
        'tss': tss_list,
        })


    df = df.set_index('Date')
    series=df.resample('d').tss.sum()

    
    frame=pd.DataFrame({'Date':series.index, 'tss':series.values})

    frame['fitness']=0.00
    frame['fatigue']=0.00
    frame['form']=0.00
    for i in range(1,len(frame)):
        frame['fitness'][i]=frame['fitness'][i-1]+(frame['tss'][i]-frame['fitness'][i-1])*(1-math.exp(-1/42))
        frame['fatigue'][i]=frame['fatigue'][i-1]+(frame['tss'][i]-frame['fatigue'][i-1])*(1-math.exp(-1/7))
        frame['form'][i]=frame['fitness'][i-1]-frame['fatigue'][i-1]

    custom_style = Style(
    background='#1a1e24',
    plot_background='#1a1e24',
    foreground='#FFFFFF',
    foreground_strong='#53A0E8',
    foreground_subtle='#343A40',
    opacity='.6',
    opacity_hover='.9',
    transition='400ms ease-in',
    colors=('#20d3e3', '#d9e320', '#E95355', '#E87653', '#E89B53'))

    line_chart = pygal.Line(show_dots=False,show_legend=False,width=1400,height=600,fill=False, interpolate='cubic', style=custom_style)
    line_chart.title = 'Training Load'
    line_chart.x_labels = frame['Date']
    line_chart.add('fitness', frame['fitness'])
    line_chart.add('fatigue', frame['fatigue'])
    line_chart.add('form', frame['form'])
    

    fatigue_current=round(frame['fatigue'].iloc[-1],2)
    fitness_current=round(frame['fitness'].iloc[-1],2)
    form_current=round(frame['form'].iloc[-1],2)
    
    #line_chart.render_in_browser()
    
    session['form_current'] = form_current

    f=figure(x_axis_type="datetime",height=500,width=1370,sizing_mode='scale_width')
    f.line(frame['Date'],frame['fitness'])
    f.line(frame['Date'],frame['fatigue'],color='yellow')
    f.line(frame['Date'],frame['form'],color='orange')

    f.background_fill_color = "#000000"
    f.border_fill_color = "#000000"
    f.background_fill_alpha= 0.0
    f.border_fill_alpha = 0.0

    f.axis.axis_line_color = "white"
    f.grid.grid_line_color = "#343A40"
    f.xaxis.fixed_location = 0
    
    #output_file("line.html")
    #show(f)
    script1,div1=components(f)

    cdn_js=CDN.js_files
    cdn_css=CDN.css_files
    


    
    return render_template('training_load.html',fatigue_current=fatigue_current,fitness_current=fitness_current,form_current=form_current,script1=script1,div1=div1,cdn_js=cdn_js,cdn_css=cdn_css)


@app.route("/logout",methods=["GET","POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route("/account/<username>",methods=["GET","POST"])
@login_required
def account(username):
    
    user=User.query.filter_by(username=username).first()
    if user != current_user:
        abort(403)

    form=AccountForm()
    if form.validate_on_submit():
        current_user.username=form.username.data
        current_user.email=form.email.data
        current_user.resting_hr=form.resting_heart.data
        current_user.max_hr=form.maximum_heart.data
        current_user.lactate_th=form.lactate_heart.data
        db.session.commit()
        flash('Your Account has been updated','info')
        return redirect(url_for("home",username=current_user.username))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
        form.resting_heart.data=current_user.resting_hr
        form.maximum_heart.data=current_user.max_hr
        form.lactate_heart.data=current_user.lactate_th
        
        
    return render_template('account.html',user=user,form=form)

@app.route("/delete/<username>/<activity_id>",methods=["GET","POST"])
@login_required
def delete_activity(username,activity_id):
    user=User.query.filter_by(username=username).first()
    post=Post.query.get_or_404(activity_id)
    if user != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Activity deleted',"info")
    return redirect(url_for('training_history',username=current_user.username))


@app.route("/analysis/<username>",methods=["GET","POST"])
@login_required
def analysis(username):
    user=User.query.filter_by(username=username).first()
    if user != current_user:
        abort(403)

    Running_fitness_list=Post.query.with_entities(Post.running_index).filter_by(athlete=current_user)

    Running_fitness_list=[value for (value,) in Running_fitness_list]

    #check if user has entered at least 3 activities to avoid out of index error
    if len(Running_fitness_list)<3:
        flash('Please enter at least 3 activities',"info")
        return redirect(url_for('home',username=current_user.username))

    

    Running_fitness=(Running_fitness_list[-1]+Running_fitness_list[-2]+Running_fitness_list[-3])/3
    Running_fitness=round(Running_fitness,1)
    
    VO2max=(Running_fitness*1.1175)-11.2879
    VO2max=round(VO2max,1)
    return render_template('analysis.html',VO2max=VO2max,Running_fitness=Running_fitness)
    
@app.route("/import_csv/<username>",methods=["GET","POST"])
@login_required
def import_csv(username):
    user=User.query.filter_by(username=username).first()
    if user != current_user:
        abort(403)
    
    
    if request.method == 'POST':
        datafile = pd.read_csv(request.files.get('file'))

        # in order to itterate dataframe rows and not get turple error i mush split data to index,activity
        for index,activity in datafile.iterrows():
            date=activity['dater']
            distance=activity['distance']
            t=activity['duration']
            HR=activity['Heart_rate']
            up=activity['up']
            down=activity['down']
            Rundex=activity['Running_index']


            
            

            resting_heart_rate=current_user.resting_hr
            maximum_heart_rate=current_user.max_hr
            lactate_threshold_heart_rate=current_user.lactate_th
            
            hrr=(HR-resting_heart_rate)/(maximum_heart_rate-resting_heart_rate)
            trimp=0

            for i in range(0,int(t)):
                trimp=trimp +1*hrr*0.64*math.exp(1.92*hrr)

            hr_lthr=(lactate_threshold_heart_rate-resting_heart_rate)/(maximum_heart_rate-resting_heart_rate)
            hour_lthr=60*hr_lthr*0.64*math.exp(1.92*hr_lthr)
            tss=(trimp/hour_lthr)*100
         

            post=Post(date=date,distance=distance,duration=t,Heart_rate=HR,up=up,down=down,running_index=Rundex,tss=tss,trimp=trimp,athlete=current_user)
            db.session.add(post)
            db.session.commit()
    return render_template('import_csv.html')


@app.route("/overview/<username>",methods=["GET","POST"])
@login_required
def overview(username):
    user=User.query.filter_by(username=username).first()
    if user != current_user:
        abort(403)

    Rundex_list=Post.query.with_entities(Post.running_index).filter_by(athlete=current_user).order_by(Post.date.asc())
    Rundex_median=functions.current_running_index(Rundex_list)
    your_running_fitness=Rundex_median[-1]

   


    form_current = session.get('form_current', None)
    message=functions.form_checker(form_current)

    VO2max=(your_running_fitness*1.1175)-11.2879
    VO2max=round(VO2max,1)
    estimate_5km=functions.estimated_times(5000,30,VO2max)   
    estimate_10km=functions.estimated_times(10000,70,VO2max)  
    estimate_21km=functions.estimated_times(21000,140,VO2max)  
    estimate_42km=functions.estimated_times(42000,280,VO2max)  

    
    
    return render_template("overview.html",your_running_fitness=your_running_fitness,form_current=form_current,message=message,VO2max=VO2max,estimate_5km=estimate_5km,estimate_10km=estimate_10km,estimate_21km=estimate_21km,estimate_42km=estimate_42km)



