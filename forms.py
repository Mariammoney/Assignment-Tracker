from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed

from wtforms import(
    StringField,
    PasswordField,
    DecimalField,
    TextAreaField,
    SubmitField,
    IntegerField,
    BooleanField,
    FileField
    
)

from wtforms.validators import(
    DataRequired,
    Email,
    EqualTo,
    Length,
    NumberRange,
    Optional
)





class SignUp(FlaskForm):
     name = StringField(
         "Name",
         validators=[
             DataRequired(),
         ]
     )
     
     
     email = StringField(
            "Email",
            validators=[
                DataRequired(),
            ]
         )
     
     password = PasswordField(
                " Password",
                validators=[
                 DataRequired(),
            ]
        )
     
     confirm_password = PasswordField(
            "confirm password",
                     validators=[
                      DataRequired(),
                      EqualTo("password", message="passwords must match")
                 ]
             )
     submit = SubmitField("Create Account")
     
    
class Login(FlaskForm):
      
     email = StringField(
                  "Email",
                  validators=[
                      DataRequired(),
                  ]
               )
           
     password = PasswordField(
                      " Password",
                      validators=[
                       DataRequired(),
                  ]
              )   
     
     submit = SubmitField("Login")
     
     
     
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class AssignmentForm(FlaskForm):

    title = StringField(
        "Assignment Title",
        validators=[
            DataRequired(),
            Length(max=200)
        ]
    )

    course = StringField(
        "Course",
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )

    description = TextAreaField(
        "Description"
    )

    due_date = DateField(
        "Due Date",
        validators=[
            DataRequired()
        ],
        
    )

    status = SelectField(
        "Status",
        choices=[
            ("Pending", "Pending"),
            ("Completed", "Completed")
        ],
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Add Assignment")