import logging
import os
import random
from flask import Flask, render_template
from flask_ask import Ask, request, session, question, statement, audio
from mapper import map
from dynamoDB import write_user, check_phone


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



# GOLF_COURSES = ['river-pines-golf',
#                 'brown-mill',
#                 'northcrest-golf-range',
#                 'cobblestone-golf-club',
#                 'bears-best-atlanta',
#                 'alfred-tup-holmes',
#                 'charlie-yates-golf',
#                 'fox-creek-golf-club',
#                 'ansley-golf-club',
#                 'golf-tech-driving-range',
#                 'marietta-golf-center-driving-range']

# GOLF_COURSES_DICT = {
#
#             'river-pines-golf' : 'https://s3.amazonaws.com/golf-course-skill-production/new-optimized/river-pines-golf.png',
#             'brown-mill' : 'https://s3.amazonaws.com/golf-course-skill-production/new-optimized/browns-mill.png',
#             'northcrest-golf-range' : 'https://s3.amazonaws.com/golf-course-skill-production/new-optimized/north-cherokee-town-and-country.png',
#             'cobblestone-golf-club' : 'https://s3.amazonaws.com/golf-course-skill-production/new-optimized/cobblestone-golf-club.png',
#             'bears-best-atlanta' : 'https://s3.amazonaws.com/golf-course-skill-production/new-optimized/bears-best-atlanta.png',
#             'alfred-tup-holmes' : 'https://s3.amazonaws.com/golf-course-skill-production/new-optimized/alfred-tup-holmes.png',
#             'charlie-yates-golf': 'https://s3.amazonaws.com/golf-course-skill-production/new-optimized/charlie-yates-golf.png',
#             'fox-creek-golf-club': 'https://s3.amazonaws.com/golf-course-skill-production/new-optimized/fox-creek-golf-club.png',
#             'ansley-golf-club' : 'https://s3.amazonaws.com/golf-course-skill-production/new-optimized/ansley-golf-club.png',
#             'golf-tech-driving-range' : 'https://s3.amazonaws.com/golf-course-skill-production/new-optimized/golf-tech-driving-range.png',
#             'marietta-golf-center-driving-range' : 'https://s3.amazonaws.com/golf-course-skill-production/new-optimized/marietta-golf-center-driving-range.png'
#             }

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
    session.attributes['featured'] = featured

    random.shuffle(featured)
    ft = session.attributes['featured'].pop()
    ft_tts = 'Golf Course'

    featured_courses = render_template(ft)

    return question(featured_courses) \
            .reprompt(featured_courses) \
            .standard_card(title='Golf Georgia',
            text=ft_tts,
            large_image_url=featured_dict[ft])


@ask.intent('DrivingRangesAtlantaIntent')
def drvingRange():

    session.attributes['drivingrange'] = True

    driving_range = render_template('drivingrange')

    return question(driving_range) \
        .standard_card(title='Golf Georgia',
        text='Driving Ranges',
        large_image_url=golfcourse_img)


@ask.intent('SelectGolfCourseOnlyIntent')
def selectGolfCourse(golfCourseName):

    #return ft_{number} or None
    cName = map(golfCourseName)
    print '++++++' + golfCourseName + '+++++++'
    print '######' + cName + '#######'

    if cName != None:
        golf_course = render_template(cName)
        return question(golf_course) \
            .standard_card(title='Golf Georgia',
            text='Driving Ranges',
            large_image_url=featured_dict[cName])

    else:
        return statement('whot?')


@ask.intent('AMAZON.YesIntent')
def yes_func():

    #check if phone in DB
    if session.attributes.get('yes') == 'featured':

        if check_phone(str(session.user.userId)) == False:

            session.attributes['yes'] = 'phone_ask'
            return question('Great!, tell me your phone number') \
                    .standard_card(title='Golf Georgia',
                    text='Great!,  tell me your phone number',
                    large_image_url=golfcourse_img)

        #phone in DB, send message
        else:
            send_text = render_template('send_text')
            return question(send_text) \
                    .standard_card(title='Golf Georgia',
                    text=send_text,
                    large_image_url=golfcourse_img)

    #Phone OK send text to phone and write phone to DB
    elif session.attributes.get('yes') == 'phone_confirm':
        session.attributes['yes'] = ''

        #Write to DynamoDB
        writeU = write_user(str(session.user.userId),session.attributes.get('phone_number'))

        #TWILIO SEND
        send_text = render_template('send_text')
        return question(send_text) \
                .standard_card(title='Golf Georgia',
                text=send_text,
                large_image_url=golfcourse_img)
    else:
        return question('Would you like to hear today featured golf course or ask a question about a golf course or driving range?') \
                .standard_card(title='Golf Georgia',
                text=send_text,
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
    else:
        return statement('Thanks for using Golf Georgia. Bye') \
            .standard_card(title='Golf Georgia',
            text='Thanks for using Golf Georgia. Bye',
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

    return statement(help_tmp) \
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
