from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, \
    TextAreaField,FileField
from wtforms.validators import ValidationError, DataRequired, \
    Length
from app.models import User
from flask_wtf.file import FileAllowed


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    age = StringField('Age', validators=[DataRequired()])
    profile = FileField("Profile Picture", validators=[FileAllowed(['jpg', 'png', 'gif'], "Nur Bilder du linksversifter!")])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    post = TextAreaField('Sag irgendwas', validators=[DataRequired()])
    hashtags = StringField('Coole Hashtags(mit leertaste einen neuen Hashtag schreiben)')
    image = FileField("Postiere ein Bild")
    submit = SubmitField('Mit Brieftaube versenden')

class ComForm(FlaskForm):
    compost = TextAreaField('Lasse deine geistigen Ergüsse ab', validators=[DataRequired()])
    comimage = FileField("Bild hin stampfen")
    comsubmit = SubmitField('Mit einer Brieftaube verschicken')

