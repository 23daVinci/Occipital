
import os
from flask import Flask, render_template, url_for, request, redirect, flash
from flask import Markup
from flask_wtf import FlaskForm
from wtforms import SelectField, TextField, IntegerField, SubmitField
from wtforms.validators import DataRequired

########################################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a354f614d02a1cbf66a3d69528ab2b26'

class UserForm(FlaskForm):
    productName = TextField('Product Name', validators=[DataRequired()])
    breed = TextField('Product Breed', validators=[DataRequired()])
    freshness = IntegerField('Enter no. of days after produce', validators=[DataRequired()])
    temp = IntegerField('Enter the storage temp. in degree celcius', validators=[DataRequired()])
    submit = SubmitField('Next')

class VidForm(FlaskForm):
    save = SubmitField('Save Video')

@app.route("/", methods=['POST', 'GET'])
def form():

    form = UserForm()
    productName = False
    breed = False
    freshness = False
    temp = False

    if form.validate_on_submit():
        productName = form.productName.data
        breed = form.breed.data
        freshness = form.freshness.data
        temp = form.temp.data
        return redirect(url_for('screen'))

    return render_template('form.html', form=form)

@app.route("/screen", methods=['POST', 'GET'])
def screen():
    saveForm = VidForm()
    if saveForm.validate_on_submit():
        from camera import CameraInput
        import cv2
        import numpy as np 
        import cvHelper
        import time
        from uuid import uuid4

        name = str(uuid4()).split("-")[-1]

        fourcc = cv2.VideoWriter_fourcc(*'XVID')



        cv2.namedWindow('wnd', cv2.WINDOW_NORMAL)
        cv2.resizeWindow("wnd", 1080, 720)
        
        cam = CameraInput(mode="cam")

        frame = cam.read()[1]
        (h,w,_) = frame.shape
        out = cv2.VideoWriter('output_'+name+'.avi', fourcc, 30.0, (w,h))



        while (True):
            ret, frame = cam.read()

            a = time.time()

            if not ret:
                out.release()
                cv2.destroyAllWindows()
                break

                b = time.time()
                print("FPS:", 1/(b-a), end="\r")

                cv2.imshow("wnd",frame)
                k=cv2.waitKey (1) & 0xFF
                out.write(frame)

                if k==ord ("q"):
                    out.release ()
                    cv2.destroyAllWindows ()
                    break
    return render_template('screen.html')

if __name__ == "__main__":
    app.run(debug=True)
