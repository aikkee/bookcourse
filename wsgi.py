import os
import json
import datetime
import flask_excel as excel
import flask_sqlalchemy 

from flask import Flask, render_template, redirect, session, url_for, request, make_response, send_from_directory, abort, flash
from sqlalchemy import and_
from datetime import date, timedelta
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, HiddenField, validators
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config.from_pyfile('bookings.cfg')
db = SQLAlchemy(application)
excel.init_excel(application)

# -- Forms --
class BookingForm(FlaskForm):
    #location = SelectField('location')
    location = HiddenField('location')
    date_time = SelectField('date_time')
    hardcopy = BooleanField('hardcopy')
    rtype = HiddenField('rtype')
    booking_ref = HiddenField('booking_ref')
    expire_on = HiddenField('expire_on')

# -- Models --
class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rtype = db.Column(db.String(10)) # Resource Type
    location = db.Column(db.String(10))
    description = db.Column(db.String(20))
    capacity = db.Column(db.Integer)
    available = db.Column(db.Integer)

    def __repr__(self):
        return '<Resource %r, %r, %r, %r, %r>' % (self.rtype, self.location, self.description, \
            self.capacity, self.available)

class Reference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resource_type = db.Column(db.String(10), unique=True) # Resources that this reference can book
    booking_ref = db.Column(db.String(10), unique=True) # reference made to the person who make a booking
    expire_on = db.Column(db.DateTime)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'))
    hardcopy = db.Column(db.String(1))
    update_on = db.Column(db.DateTime)

    def __repr__(self):
        return '<Reference %r, %r>' % (self.booking_ref, self.expire_on)


# -- Views --
@application.route('/')
@application.route('/index')
def index():
    return render_template('index.html')


@application.route('/init')
def init():
    try:
        ref = request.args.get('ref').upper()
        mod = request.args.get('mod')
        course = request.args.get('course')
        hardcopy = request.args.get('hardcopy')
        course_id, course_desc = course.split(":")
        isnew = request.args.get('isnew')
        rtype = get_rtype(ref)
        # print(f'ref:{ref}, course:{course}, isnew:{isnew}, rtype:{rtype}')
        # also use this as the indicator for where the request comes from
        if (isnew is None or isnew==''):
            isnew='yes'

        if (isValidReference(ref+"**"+course_id, rtype) == False):
            return redirect(url_for('index'))

        if (ref is None or ref == ''):
            return redirect(url_for('index'))
    except:
        return redirect(url_for('index'))

    # TODO: Improve the query later by combining the 2 statements
    reference = Reference.query.filter(Reference.booking_ref==ref+"**"+course_id).first()
    booked_resource = Resource.query.filter(Resource.id==reference.resource_id).first()
    # Need to also handle cases where user use the same link to amend booking
    # When initiated from user through the sms link, isnew will be 'yes'
    # When initiated from change_booking page, isnew will be 'no'
    if (isnew=='yes' and booked_resource!=None):
        m = {'location':booked_resource.location, \
              'date_time':booked_resource.description}
        b = [{'ref':ref, 'course':course, 'rtype':rtype, 'hardcopy':reference.hardcopy, 'isnew':'no', 'label':'Yes'}]
        return render_template('change_booking.html', message=m, buttons=b)

    # obtain the resource slots from database
    # available_resource = Resource.query.filter(Resource.available>0)
    bookingForm = BookingForm()
    # bookingForm.date_time.choices = [('', 'Choose Date & Time')] + [ (t.id, t.description) for t in available_resource]
    # bookingForm.date_time.choices = [('', 'Choose Date & Time')]

    # obtain locations of available slots
    resources = Resource.query.filter(and_(Resource.location==course, Resource.available>0, Resource.rtype==rtype)).all()
    

    #locations = list(set([(r.location) for r in resources if show_for_booking(r, str(reference.expire_on), rtype)]))
    #bookingForm.location.choices = [('', 'Choose Course')] + [
    #    (l, l) for l in locations]
    course_run = [(r.id, r.description) for r in resources if show_for_booking(r, str(reference.expire_on), rtype)]
    bookingForm.date_time.choices = [('', 'Choose Course')] + course_run
    
    bookingForm.booking_ref.data = ref + "**" + course_id
    bookingForm.location.data = course
    bookingForm.rtype.data = rtype
    bookingForm.hardcopy.data = hardcopy
    if (reference != None):
        bookingForm.expire_on.data = reference.expire_on
    return render_template('book_htmb_form.html', form=bookingForm, isnew='yes')

def get_rtype(email):
    agency = email.split("@")[1].split(".")[0].upper()
    if (agency in ['SPF','SCDF','SPS','PRIS','CNB','ICA','HTA','MHA']):
        return 'MHA'
    elif (agency == 'VITAL' or agency == 'MOE'):
        return agency
    else:
        return 'PSD'


@application.route('/save', methods=['POST'])
def save():

    if (request.form.get('date_time')==""):
        flash('Please select a course run')
        return redirect(redirect_url())

    b_ref = request.form.get('booking_ref')
    r_id = request.form.get('date_time', type=int)
    hardcopy = request.form.get('hardcopy')

    # Release booking slot, retrieve booking_ref record 
    reference = Reference.query.filter(Reference.booking_ref==b_ref).first()
    if (reference is None):
        # error, should not happen, request the user to start from the SMS booking link again
        flash("An error occurred when processing your booking, please try again again.")
        return render_template('error.html')

    if (reference.resource_id is not None):
        booked_resource = Resource.query.filter(Resource.id==reference.resource_id).first()
        if (booked_resource is not None):
            booked_resource.available = booked_resource.available + 1 
            application.logger.info('Return slot for Resource ID: %r' % booked_resource.id)
            db.session.commit()

    resource = Resource.query.filter(Resource.id==r_id).first()
    if (resource.available == 0):
        # Fully booked, cannot accept anymore
        m = {'location':resource.location, \
             'date_time':resource.description}
        b = [{'ref':b_ref, 'label':'OK'}]
        return render_template('fully_booked.html', message=m, buttons=b)
    else:
        # update new booking
        reference.resource_id = r_id
        reference.update_on = datetime.datetime.now()
        reference.hardcopy = hardcopy
            
        resource.available = resource.available - 1 

        application.logger.info('Draw down from Resource ID: %s for Reference ID: %s' % (r_id, reference.id))

        db.session.commit()
        #flash('Thank you for your registration.  Your training for <b>%s</b> on <b>%s</b> is confirmed.' %
        #      (resource.location, resource.description))

        m = {'location':resource.location, \
              'date_time':resource.description}
        b = [{'label':'OK'}]
        # l = {'url': get_gcal_url(resource.location, resource.description)}
        # return render_template('acknowledge.html', message=m, gcal_link=l)
        return render_template('acknowledge.html', message=m, buttons=b)

"""
def get_gcal_url(location, dt_str):
    try:
        start_dt = datetime.datetime.strptime(dt_str, '%d %b %Y - %I.%M%p')
    except ValueError:
        start_dt = datetime.datetime.strptime(dt_str, '%d %b %Y - %I%p')
    end_dt = start_dt + timedelta(hours=2)
    start_dt_str = start_dt.strftime("%Y%m%dT%H%M00")
    end_dt_str = end_dt.strftime("%Y%m%dT%H%M00")
    t = "http://www.google.com/calendar/event?action=TEMPLATE&" \
        "dates="+ start_dt_str +"/" + end_dt_str + "&ctz=Asia/Singapore&" \
        "text=HRP%20Training&location=TBC&" \
        "details=Pre%20course%20admin%20instruction%20to%20be%20added."
    return t 
"""

def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)

# Function to filter out and handle expiry date
# rtype determines the type of resources to be retreived, hence it should not be None
def show_for_booking(resource, exp, rtype, location=None):
    # handle reference expiry date

    exp_date = date( int(exp[:4]), int(exp[5:7]), int(exp[8:10]) )
    earliest_date = exp_date + datetime.timedelta(days=3)
    # change resource description to date object
    resource_date = datetime.datetime.strptime(resource.description[:11], '%d %b %Y').date()
    if (location == None):
        return resource.available > 0 and resource.rtype == rtype and resource_date > earliest_date
    else:
        return resource.location == location and resource.rtype == rtype and resource.available > 0 and resource_date > earliest_date
         

@application.route("/coursesfor/<email>/", methods=["GET", "POST"])
def get_courses(email):
    email = request.args['ref']
    mod = request.args['mod']
    search = "{}%{}%".format(email,mod)
    search.upper()
    # Get the courses eligible for the email registered
    refs = Reference.query.filter(Reference.booking_ref.like(search)).all()
    course_codes = []
    rtype = get_rtype(email)
    for r in refs:
        course_codes.append(r.booking_ref.split("**")[1])

    data = [
            (code+":"+get_course_description(code), get_course_description(code)) for code in course_codes 
    ]
    print(json.dumps(data))
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

def get_course_description(code):
    course = {
        "ATT-GEN102":"Re-Employment",
        "ATT-GEN104":"Part-Time Employment",
        "ATT-MHA106M":"Enlistment Process for HRMG",
        "DVP-MHA102":"Training Admin-Nomination & Course",
        "PAY-GEN101":"Pre-Payroll - Allowance & Deduction Processing and Payroll Retro Adjuster"
    }
    return course[code]

def isValidReference(booking_ref, rtype):
    bRef = Reference.query.filter(and_(Reference.booking_ref==booking_ref,
                                       Reference.resource_type==rtype,
                                       Reference.expire_on>datetime.datetime.now())).first()
    if (bRef != None):
        return True
    else:
        flash('You are unable to register for this course. Please contact HRP training admin <email>.')
        return False

@application.route('/admin/check_slots')
def check_slots():
    return render_template('show_slots.html', slots=Resource.query.all())

@application.route("/admin/add_case", methods=['GET', 'POST'])
def add_case():
    # handle submission
    if request.method == 'POST':
        rtype = request.form.get('rtype')
        ref = request.form.get('ref')
        expiry = request.form.get('expiry')
        r = create_new_reference(rtype, ref, expiry)
        flash('%s activated. Expires on %s.' \
                % (r.booking_ref, r.expire_on.strftime('%d-%b-%Y')))
        return render_template('add_case.html')

    return render_template('add_case.html')

def create_new_reference(rtype, ref, expiry):
    r = Reference()
    r.resource_type = rtype
    r.booking_ref = ref 
    expiry_str = expiry + " 16:00:00" #handle timezone of server - 8 hrs behind us
    r.expire_on = datetime.datetime.strptime(expiry_str, "%Y-%m-%d %H:%M:%S")
    db.session.add(r)
    db.session.commit()
    return r

@application.route("/admin/import_case", methods=['GET', 'POST'])
def import_case():
    if (request.method == 'POST'):
        def ref_init_func(row):
            r = Reference()
            r.resource_type = row['RESOURCE_TYPE']
            r.booking_ref = row['BOOKING_REF']
            r.expire_on = datetime.datetime.strptime(str(row['EXPIRE_ON']) + " 16:00:00", "%Y-%m-%d %H:%M:%S")
            return r
        request.save_to_database(field_name='file', session=db.session, \
                                      table=Reference, \
                                      initializer=(ref_init_func))
        flash('HRP Course Registration cases created.')
        return render_template('admin_acknowledge.html')
    return render_template('import.html', title='Import HRP Training Registration Cases')

@application.route("/admin/import_slot", methods=['GET', 'POST'])
def import_slot():
    if (request.method == 'POST'):
        def resource_init_func(row):
            r = Resource()
            r.rtype = row['TYPE']
            r.location = row['LOCATION']
            r.description = row['DESCRIPTION']
            r.capacity = row['CAPACITY']
            r.available = row['CAPACITY']
            return r
        request.save_to_database(field_name='file', session=db.session, \
                                      table=Resource, \
                                      initializer=(resource_init_func))
        flash('HRP Training timeslots created.')
        return render_template('admin_acknowledge.html')
    return render_template('import.html', title='Import HRP Training Timeslot')

'''
@application.route("/admin/export_booking", methods=['GET'])
def doexport():

    col = ['resource_type', 'booking_ref','description', 'update_on', 'location']
    qs = Reference.query.join(Resource, Reference.resource_id == Resource.id).add_columns( \
            Reference.resource_type, Reference.booking_ref, Resource.description, \
            Reference.update_on, Resource.location).filter( \
                Reference.resource_id != None)
    return excel.make_response_from_query_sets(qs, col, "csv")
'''

@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#----------test codes----------------------
@application.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)

@application.route("/test")
def test():
    user_agent = request.headers.get('User-Agent')
    return "<p>It's Alive!<br/>Your browser is %s</p>" % user_agent

#----------main codes----------------------
if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8080)
