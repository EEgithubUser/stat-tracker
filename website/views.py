from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
from flask_login import login_required, current_user
from .models import Note, Stat, StatSnapshot, User
from . import db
from datetime import datetime
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # these need to "initialized" from the start otherwise 404 error b/c it doesn't exist
    user = User.query.get_or_404(current_user.id)
    stat = Stat.query.get_or_404(current_user.id) # MASSSSSIVVVVVEEEE!

    if request.method == 'POST':

        if request.form['stats'] == '1':
            stat.pts += 1
            db.session.add(user)
            db.session.commit()
            flash('+1 POINT', category = 'success')            
        elif request.form['stats'] == '2':
            stat.pts += 2
            db.session.add(user)
            db.session.commit()
            flash('+2 POINT', category = 'success')
        elif request.form['stats'] == '3':
            stat.pts += 3
            db.session.add(user)
            db.session.commit()
            flash('+3 POINT', category = 'success')
        elif request.form['stats'] == 'tos':
            stat.tos += 1
            db.session.add(user)
            db.session.commit()
            flash('+1 TURNOVER', category = 'success')
        elif request.form['stats'] == 'temp':
            try:
                # these need to be entered, otherwise an error will be thrown
                min_start = int(request.form.get('min_start'))
                min_end = int(request.form.get('min_end'))
                if min_start < 0:
                    flash('Minutes less than 0', category = 'error')
                elif min_end > 40:
                    flash('Minutes greater than 40', category = 'error')
                elif min_end > min_start:
                    flash('End time cannot be greater than start time', category = 'error')
                else:
                    stat.mins = stat.mins + (min_start - min_end)
                    db.session.add(user)
                    db.session.commit()
                    flash('MINUTES ADDED', category = 'success')
            except ValueError:
                flash('Please enter your starting and ending minutes before clicking the minutes button.', category='error')
        elif request.form['stats'] == 'mins':
            try:
                # these need to be entered, otherwise an error will be thrown
                min_start = int(request.form.get('min_start'))
                min_end = int(request.form.get('min_end'))
                if min_start < 0:
                    flash('Minutes less than 0', category = 'error')
                elif min_end > 40:
                    flash('Minutes greater than 40', category = 'error')
                elif min_end > min_start:
                    flash('End time cannot be greater than start time', category = 'error')
                else:
                    stat.mins = stat.mins + (min_start - min_end)
                    db.session.add(user)
                    db.session.commit()
                    flash('MINUTES ADDED', category = 'success')
            except ValueError:
                flash('Please enter your starting and ending minutes before clicking the minutes button.', category='error')
        elif request.form['stats'] == 'confirm_popup_save':
            date = request.form.get('game_date')
            team1 = request.form.get('team1')
            team2 = request.form.get('team2')
            video = request.form.get('video')

            datetime_obj = datetime.strptime(date, '%Y-%m-%d')
            game_date = datetime_obj.strftime("%m/%d/%Y")

            note = "Pts: {pts}, Rbs: {rbs}, Asts: {asts}, Stls: {stls}, Tos: {tos}, Blks: {blks}, Mins: {mins}".format(pts = stat.pts, rbs = stat.rbs, asts = stat.asts, stls = stat.stls, tos = stat.tos, blks = stat.blks, mins = stat.mins,)
            snapshot = StatSnapshot(statline=note,
                                    pts_snapshot=stat.pts, 
                                    rbs_snapshot=stat.rbs, 
                                    asts_snapshot=stat.asts, 
                                    stls_snapshot=stat.stls, 
                                    tos_snapshot=stat.tos, 
                                    blks_snapshot=stat.blks, 
                                    mins_snapshot=stat.mins, 
                                    game_date=game_date, 
                                    team1=team1, 
                                    team2=team2, 
                                    video=video, 
                                    user_id=current_user.id)
            db.session.add(snapshot)
            db.session.commit()
            flash('SAVED SUCCESSFULLY!', category = 'success')
            redirect(url_for('views.statbook'))
            return render_template("statbook.html", user=current_user)
        elif request.form['stats'] == 'rbs':
            stat.rbs += 1
            db.session.add(user)
            db.session.commit()
            flash('+1 REBOUND', category = 'success')
        elif request.form['stats'] == 'asts':
            stat.asts += 1
            db.session.add(user)
            db.session.commit()
            flash('+1 ASSIST', category = 'success')
        elif request.form['stats'] == 'stls':
            stat.stls += 1
            db.session.add(user)
            db.session.commit()
            flash('+1 STEAL', category = 'success')
        elif request.form['stats'] == 'blks':
            stat.blks += 1
            db.session.add(user)
            db.session.commit()
            flash('+1 BLOCK', category = 'success')
        elif request.form['stats'] == 'reset':
            stat.pts = 0
            stat.rbs = 0
            stat.asts = 0
            stat.stls = 0
            stat.tos = 0
            stat.blks = 0
            stat.mins = 0
            db.session.add(user)
            db.session.commit()
            flash('Stats Reset', category = 'success')
        else:
            pass
    
    # pass in "stat" to our template, stat queries the Stat object under the current user id
    # stat now has "access" to all of the attributes in the Stats Model
    return render_template("home.html", stat = Stat.query.get_or_404(current_user.id), user=current_user,)


@views.route('/statbook', methods=['GET', 'POST'])
@login_required
def statbook():
        # note = request.form.get('note')#Gets the note from the HTML 

        # if len(note) < 1:
        #     flash('Note is too short!', category='error') 
        # else:
        #     new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
        #     db.session.add(new_note) #adding the note to the database 
        #     db.session.commit()
        #     flash('Note added!', category='success')

    return render_template('statbook.html', user=current_user,)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/delete-statsnapshot', methods=['POST'])
def delete_statsnapshot():
    statsnapshot = json.loads(request.data)
    statsnapshotId = statsnapshot['statsnapshotId']
    statsnapshot = StatSnapshot.query.get(statsnapshotId)
    if statsnapshot:
        if statsnapshot.user_id == current_user.id:
            db.session.delete(statsnapshot)
            db.session.commit()
            flash('Deleted!', category='success')

    return jsonify({})
