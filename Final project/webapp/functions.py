import math 
import datetime
# average running index of last 3 activities create a list with all these values

def current_running_index(Rundex_list):

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
    #return a list of averages of running index
    return Rundex_median


# check if current_form is at a specific level and give back feedback about athletes training

def form_checker(form):
    try:

        if form<-30:
            message="Your fatigue levels are dangerously high for your current fitness, take some rest days,press the help button"
        elif form<-20:
            message="Well done your training is optimal but you are pushing a little too hard. You should take some rest days"
        elif form<-15:
            message="Your Workout load is optimal"
        elif form<-10:
            message="Your Workout levels are optimal, you can maybe push a little more if you think your body can handle it"
        elif form<-5:
            message="Your Workout levels are in a good level to see physiological changes and fitness gains,However you are not in the optimal spot,keep on"
        elif form<0 :
            message="Your Training program is starting to work,keep on"
        elif form==0:
            message="Start Training!"
        else:
            message="You are not training hard lately, if you are tapering off for a race this is the optimal spot for the last prerace days,if not go run!"
    except:
        message="Please visit first the training load page to load your stats"
    return(message)

#estimates running race times for 5k,10k,21k,42k based on vo2max and running index value
def estimated_times(d,time,vo2max):
    percent_max = 0.8 + 0.1894393 * math.exp(-0.012778 * time) + 0.2989558 * math.exp(-0.1932605 * time)
    VP=vo2max*percent_max
    a=0.000104
    b=0.182258
    gamma=-4.6-VP
    velocity=(-b+(b**2 -4*a*gamma)**0.5)/(2*a)
    percent_max = 0.8 + 0.1894393 * math.exp(-0.012778 * time) + 0.2989558 * math.exp(-0.1932605 * time)
    #velocity in meters per min
    estimated=d/velocity

    
    estimated=str(datetime.timedelta(minutes=estimated)).rsplit('.', 1)[0]
    

    return(estimated)

