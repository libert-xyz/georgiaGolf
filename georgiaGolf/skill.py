import logging
import os
import random
from flask import Flask, render_template
from flask_ask import Ask, request, session, question, statement, audio


app = Flask(__name__)
ask = Ask(app, "/")

log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


golfcourse_logo = 'https://s3.amazonaws.com/golf-course-skill-production/new-optimized/golf+swing+logo+white+x+512.png'
golfcourse_img = 'https://s3.amazonaws.com/golf-course-skill-production/new-optimized/golf+swing+logo+white+x+512.png'

#oldendpoint: arn:aws:lambda:us-east-1:770591633881:function:golf-course-production-skill


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


@ask.intent('eventIntent')
def event():

    session.attributes['error'] = 1

    details = render_template('details')
    details_tts = render_template('details_tts')
    main_tmp_beep = render_template('main_voice_beep')


    #Repeat
    session.attributes['repeat']  = details
    session.attributes['repeat_tts'] = details_tts
    session.attributes['repeat_reprompt'] = main_tmp_beep

    return question(details) \
        .reprompt(main_tmp_beep) \
        .standard_card(title='Zendesk Relate',
        text=details_tts,
        large_image_url=voice_summit_img)


@ask.intent('AMAZON.YesIntent')
def yes_respond(numbers):

    if session.attributes.get('yesIntent') == 'facts':

        session.attributes['error'] = 1

        #Replace facts list
        facts = session.attributes['facts']
        if len(facts) > 0:
            random.shuffle(facts)
            factNumber = facts.pop()

            fact = render_template(factNumber)
            fact_tts = render_template(factNumber+'_tts')

            #No response re-prompt
            main_tmp_beep = render_template('main_voice_beep')

            #Repeat
            session.attributes['repeat']  = fact
            session.attributes['repeat_tts'] = fact_tts
            session.attributes['repeat_reprompt'] = main_tmp_beep

            return question(fact) \
                    .reprompt(main_tmp_beep) \
                    .standard_card(title='Zendesk Relate',
                    text=fact_tts,
                    large_image_url=voice_summit_img)
        else:

            return statement('')

    elif session.attributes.get('yesIntent') == 'speakers':

        session.attributes['error'] = 1

        #Replace speakers list
        facts = session.attributes['speakers']
        if len(facts) > 0:
            random.shuffle(facts)
            spk = facts.pop()

            fact = render_template(spk)
            fact_tts = render_template(spk+'_tts')

            #No response re-prompt
            main_tmp_beep = render_template('main_voice_beep')

            #Repeat
            session.attributes['repeat']  = fact
            session.attributes['repeat_tts'] = fact_tts
            session.attributes['repeat_reprompt'] = main_tmp_beep
            session.attributes['spk_img'] = speakers_dict[spk]

            return question(fact) \
                    .reprompt(main_tmp_beep) \
                    .standard_card(title='Zendesk Relate',
                    text=fact_tts,
                    large_image_url=speakers_dict[spk])
        else:

            return statement('')

    else:
        close_session_fn = render_template('close_session')
        return statement(close_session_fn)


@ask.intent('AMAZON.StopIntent')
def stop():

    stop_bye = render_template('stop_bye')
    stop_bye_tts = render_template('stop_bye_tts')


    return statement(stop_bye) \
        .standard_card(title='Zendesk Relate',
        text=stop_bye_tts,
        large_image_url=voice_summit_img)

@ask.intent('AMAZON.CancelIntent')
def cancel_fnc():

    stop_bye = render_template('stop_bye')
    stop_bye_tts = render_template('stop_bye_tts')
    return statement(stop_bye) \
        .standard_card(title='Zendesk Relate',
        text=stop_bye_tts,
        large_image_url=voice_summit_img)

@ask.intent('AMAZON.FallbackIntent')
def fallback():
    fallback = render_template('fallback')
    return question(fallback) \
        .standard_card(title='Golf Course',
        text=fallback,
        large_image_url=golfcourse_img)

@ask.intent('AMAZON.HelpIntent')
def help_fn():

    session.attributes['error'] = 1

    help_tmp = render_template('help')
    help_tmp_tts = render_template('help_tts')

    #Repeat
    session.attributes['repeat']  = help_tmp
    session.attributes['repeat_tts'] = help_tmp_tts
    session.attributes['repeat_reprompt'] = help_tmp

    return question(help_tmp) \
            .standard_card(title='Zendesk Relate',
            text=help_tmp_tts,
            large_image_url=voice_summit_img)




@ask.session_ended
def session_ended():

    close_session_fn = render_template('close_session')
    return statement(close_session_fn)
    #return statement('test')


if __name__ == '__main__':
    app.run(debug=True)
