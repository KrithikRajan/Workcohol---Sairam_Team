import openai
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
openai.api_key = os.getenv('OPENAI_API_KEY')
class BlogForm(FlaskForm):
    topic = StringField('Script Topic', validators=[DataRequired()])
    keyword = StringField('Keyword for SEO', validators=[DataRequired()])
    tone = StringField('Tone (e.g., formal, informal)', validators=[DataRequired()])
    length = StringField('Length (Word count)', validators=[DataRequired()])
    submit = SubmitField('Generate Script')

def generate_blog_content(topic, keyword, tone="informal", length=800):
    prompt = f"Generate a {length}-word content about {topic} with the keyword '{keyword}' in an {tone} tone. Make sure the content is complete, well-structured, and does not leave incomplete sentences."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000,
        temperature=0.7
    )
    
    blog_content = response['choices'][0]['message']['content'].strip()
    return blog_content

@app.route('/', methods=['GET', 'POST'])
def index():
    form = BlogForm()
    blog_content = None
    if form.validate_on_submit():
        topic = form.topic.data
        keyword = form.keyword.data
        tone = form.tone.data
        length = int(form.length.data)
        blog_content = generate_blog_content(topic, keyword, tone, length)

    return render_template('index.html', form=form, blog_content=blog_content)

if __name__ == '__main__':
    app.run(debug=True)