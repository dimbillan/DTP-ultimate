from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, SelectField
from wtforms.validators import Length, DataRequired, EqualTo, ValidationError, Email

from dtp.models import Student

class RegisterForm(FlaskForm):
    email = EmailField(
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "E-Posta"}
    )

    first_name = StringField(
        validators=[DataRequired(), Length(min=3, max=64)],
        render_kw={"placeholder": "Ad"}
    )

    last_name = StringField(
        validators=[DataRequired(), Length(min=3, max=64)],
        render_kw={"placeholder": "Soyad"}
    )

    student_number = StringField(
        validators=[DataRequired(), Length(min=3, max=64)],
        render_kw={"placeholder": "Öğrenci Numarası"}
    )

    university = SelectField(
        choices=[],  # Backend tarafından doldurulacak
        validators=[DataRequired()]
    )

    faculty = SelectField(
        choices=[],  # Backend tarafından doldurulacak
        validators=[DataRequired()]
    )

    department = SelectField(
        choices=[],  # Backend tarafından doldurulacak
        validators=[DataRequired()]
    )

    class_year = SelectField(
        choices=[],  # Backend tarafından doldurulacak
        validators=[DataRequired()]
    )

    password = PasswordField(
        validators=[DataRequired(), Length(min=6, max=64)],
        render_kw={"placeholder": "Şifre"}
    )

    confirm_password = PasswordField(
        validators=[DataRequired(), EqualTo('password', message="Şifreler eşleşmiyor!")],
        render_kw={"placeholder": "Şifreyi Tekrar Yaz"}
    )

    submit = SubmitField('Kayıt Ol')

    def validate_email(self, email):
        student = Student.query.filter_by(email=email.data).first()
        if student:
            raise ValidationError('Bu e-posta ile daha önce kayıt olunmuş. Lütfen başka bir e-posta seçin.')

class LoginForm(FlaskForm):
    email = EmailField(validators=[
                           DataRequired(), Email() ], render_kw={"placeholder": "E-Posta"})

    password = PasswordField(validators=[
                             DataRequired(), Length(min=6, max=64)], render_kw={"placeholder": "Şifre"})

    submit = SubmitField('Giriş Yap')