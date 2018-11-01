import logging
import os
import random
from flask import Flask, render_template
from flask_ask import Ask, request, session, question, statement, audio
from mapper import map, map_info, map_img
from dynamoDB import write_user, check_phone
from send_sms import send_message
from datetime import date

app = Flask(__name__)
ask = Ask(app, "/")

log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


golfcourse_logo = 'https://s3.amazonaws.com/golf-course-skill-production/new-optimized/golf+swing+logo+white+x+512.png'
golfcourse_img = 'https://s3.amazonaws.com/golf-course-skill-production/new-optimized/golf+swing+logo+white+x+512.png'

#oldendpoint: arn:aws:lambda:us-east-1:770591633881:function:golf-course-production-skill

#newEndpoint: https://cx4hqadrlb.execute-api.us-east-1.amazonaws.com/dev

featured = ['ft_1','ft_2','ft_3','ft_4','ft_5','ft_5','ft_6','ft_7','ft_8','ft_9','ft_10','ft_11']

featured_dict = {
                'ft_1': 'https://s3.amazonaws.com/golf-course-skill-production/new-optimized/alfred-tup-holmes.png',
                'ft_2': 'https://s3.amazonaws.com/golf-course-skill-production/new-optimized/ansley-golf-club.png',
                'ft_3': 'https://s3.amazonaws.com/golf-course-skill-production/new-optimized/bears-best-atlanta.png',
                'ft_4' : 'https://s3.amazonaws.com/golf-course-skill-production/new-optimized/browns-mill.png',
                'ft_5' : 'https://s3.amazonaws.com/golf-course-skill-production/new-optimized/charlie-yates-golf.png',
                'ft_6': 'https://s3.amazonaws.com/golf-course-skill-production/new-optimized/cobblestone-golf-club.png',
                'ft_7': 'https://s3.amazonaws.com/golf-course-skill-production/new-optimized/fox-creek-golf-club.png',
                'ft_8' : 'https://s3.amazonaws.com/golf-course-skill-production/new-optimized/golf-tech-driving-range.png',
                'ft_9' : 'https://s3.amazonaws.com/golf-course-skill-production/new-optimized/marietta-golf-center-driving-range.png',
                'ft_10' : 'https://s3.amazonaws.com/golf-course-skill-production/new-optimized/north-cherokee-town-and-country.png',
                'ft_11' : 'https://s3.amazonaws.com/golf-course-skill-production/new-optimized/river-pines-golf.png'
                }


@ask.launch
def launch():

    session.attributes['error'] = 1

    welcome_q = render_template('welcome')

    return question(welcome_q) \
        .reprompt(welcome_q) \
        .standard_card(title='Golf Georgia',
        text=welcome_q,
        large_image_url=golfcourse_img)


@ask.intent('FeaturedGolfCourseIntent')
def featuredGolfCourse():


    session.attributes['yes'] = 'featured'

    #List of Courses
    #session.attributes['featured'] = featured

    #random.shuffle(featured)
    #ft = featured.pop()

    today = date.today().weekday() + 1

    ft = 'ft_' + str(today)

    #GOLF_INFO
    session.attributes['info'] = map_info(ft)

    ft_tts = 'Featured'

    featured_courses = render_template(ft)

    return question(featured_courses) \
            .reprompt(featured_courses) \
            .standard_card(title='Golf Georgia',
            text=ft_tts,
            large_image_url=featured_dict[ft])




@ask.intent('TellMeAboutGolfCourseIntent')
def askGolfCourse():

    ask_golf = render_template('ask_golf')

    return question(ask_golf) \
            .standard_card(title='Golf Georgia',
            text='About Golf Course',
            large_image_url=golfcourse_img)



@ask.intent('TellMeAboutAugustaCourseIntent')
def augusta_func():

    ask_augusta = render_template('ask_augusta')

    return question(ask_augusta) \
            .standard_card(title='Golf Georgia',
            text='Augusta Course',
            large_image_url=golfcourse_img)


@ask.intent('TellMeAboutAtlantaCourseIntent')
def atlanta_func():

    ask_atlanta = render_template('ask_atlanta')

    return question(ask_atlanta) \
            .standard_card(title='Golf Georgia',
            text='Atlanta Course',
            large_image_url=golfcourse_img)


@ask.intent('DrivingRangesAtlantaIntent')
def drvingRange():

    session.attributes['drivingrange'] = True

    driving_range = render_template('drivingrange')

    return question(driving_range) \
        .standard_card(title='Golf Georgia',
        text='Driving Ranges',
        large_image_url=golfcourse_img)


@ask.intent('SelectGolfCourseOnlyIntent')
def selectGolfCourseOnly(golfCourseName):


    session.attributes['yes'] = 'featured'

    #return {number} or None
    cName = map(golfCourseName.lower())
    print '++++++' + golfCourseName + '+++++++'
    print str(cName)

    #GOLF_INFO
    session.attributes['info'] = map_info('ft_'+str(cName))

    if cName != None:

        golf_info = 'g_'+str(cName)
        golf_course = render_template(golf_info)
        return question(golf_course) \
            .standard_card(title='Golf Georgia',
            text=golf_course,
            large_image_url=map_img(cName))

    else:
        return statement('whot?')



@ask.intent('SelectGolfCourseIntent')
def selectGolfCourse(golfCourseName):

    session.attributes['yes'] = 'featured'

    #return ft_{number} or None
    cName = map(golfCourseName.lower())
    print '++++++' + golfCourseName + '+++++++'
    print str(cName)

    #GOLF_INFO
    session.attributes['info'] = map_info('ft_'+str(cName))

    if cName != None:
        golf_course = render_template('g_'+str(cName))
        return question(golf_course) \
            .standard_card(title='Golf Georgia',
            text=golfCourseName.capitalize(),
            large_image_url=map_img(cName))

    else:
        return statement('whot?')


@ask.intent('AMAZON.YesIntent')
def yes_func():

    #check if phone in DB
    if session.attributes.get('yes') == 'featured':

        phone_n = check_phone(str(session.user.userId))
        #session.attributes['featured']

        if phone_n == False:

            session.attributes['yes'] = 'phone_ask'
            return question('Great!, tell me your phone number') \
                    .standard_card(title='Golf Georgia',
                    text='Great!,  tell me your phone number',
                    large_image_url=golfcourse_img)

        #phone in DB, send message
        #TWILIO SEND
        else:
            send_text = render_template('send_text')
            send_message(phone_n,session.attributes.get('info'))

            #For NO close session
            session.attributes['yes'] = 'another_golf'
            return question(send_text) \
                    .standard_card(title='Golf Georgia',
                    text=send_text,
                    large_image_url=golfcourse_img)

    #Phone OK send text to phone and write phone to DB
    elif session.attributes.get('yes') == 'phone_confirm':

        session.attributes['yes'] = 'another_golf'
        #Write to DynamoDB
        writeU = write_user(str(session.user.userId),session.attributes.get('phone_number'))

        #TWILIO SEND
        send_text = render_template('send_text')
        send_message('+1'+ str(session.attributes['phone_number']),session.attributes.get('info'))

        return question(send_text) \
                .standard_card(title='Golf Georgia',
                text=send_text,
                large_image_url=golfcourse_img)


    elif session.attributes.get('yes') == 'another_golf':
        ask_golf = render_template('ask_golf')
        return question(ask_golf) \
                .standard_card(title='Golf Georgia',
                text='About Golf Course',
                large_image_url=golfcourse_img)

    else:
        return question('Would you like to hear today featured golf course or ask a question about a golf course or driving range?') \
                .standard_card(title='Golf Georgia',
                text='Would you like to hear today featured golf course or ask a question about a golf course or driving range?',
                large_image_url=golfcourse_img)

@ask.intent('PhoneNumberIntent')
def phone(phoneNumber):
    if session.attributes.get('yes') == 'phone_ask':

        session.attributes['yes'] = 'phone_confirm'
        session.attributes['phone_number'] = phoneNumber

        phone_confirm = render_template('phone_confirm',phone=phoneNumber)
        return question(phone_confirm) \
                .standard_card(title='Golf Georgia',
                text=phone_confirm,
                large_image_url=golfcourse_img)


@ask.intent('AMAZON.NoIntent')
def no_func():

    #Phone incorrect, ask one more time
    if session.attributes.get('yes') == 'phone_confirm':
        session.attributes['yes'] = 'phone_ask'
        phone_incorrect = render_template('phone_incorrect')

        return question(phone_incorrect) \
                .standard_card(title='Golf Georgia',
                text=phone_incorrect,
                large_image_url=golfcourse_img)

    #NO response twice close session
    elif session.attributes.get('yes') == 'another_golf':
        return statement('Thanks for using Golf Georgia. Bye') \
            .standard_card(title='Golf Georgia',
            text='Thanks for using Golf Georgia. Bye',
            large_image_url=golfcourse_img)

    else:

        no_response = render_template('no_response')
        session.attributes['yes'] = 'another_golf'
        return question(no_response) \
            .standard_card(title='Golf Georgia',
            text=no_response,
            large_image_url=golfcourse_img)


@ask.intent('AMAZON.StopIntent')
def stop():
    return statement('Thanks for using Golf Georgia. Bye') \
        .standard_card(title='Golf Georgia',
        text='Thanks for using Golf Georgia. Bye',
        large_image_url=golfcourse_img)

@ask.intent('AMAZON.CancelIntent')
def cancel_fnc():

    return statement('Thanks for using Golf Georgia. Bye') \
        .standard_card(title='Golf Georgia',
        text='Thanks for using Golf Georgia. Bye',
        large_image_url=golfcourse_img)

@ask.intent('AMAZON.FallbackIntent')
def fallback():
    fallback = render_template('fallback')
    return question(fallback) \
        .standard_card(title='Golf Course',
        text=fallback,
        large_image_url=golfcourse_img)

@ask.intent('AMAZON.HelpIntent')
def help_fn():

    help_tmp = render_template('help')

    return question(help_tmp) \
            .standard_card(title='Golf Course',
            text=help_tmp,
            large_image_url=golfcourse_img)

# @ask.session_ended
# def session_ended():
#
#     close_session_fn = render_template('close_session')
#     return statement(close_session_fn)
#     #return statement('test')


if __name__ == '__main__':
    app.run(debug=True)
