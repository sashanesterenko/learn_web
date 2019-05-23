from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from webapp.news.models import News

class CommentForm(FlaskForm):
	news_id = HiddenField('News ID', validators=[DataRequired()])
	comment_text = StringField('Comment text', validators=[DataRequired()], render_kw={"class": "form-control"})
	submit = SubmitField('Send!', render_kw={"class": "btn btn-primary"})

	def validate_news_id(self, news_id):
		if not News.query.get(news_id.data):
			raise ValidationError('No news with this id')