from flask import Flask,render_template,request
import pickle
import numpy as np

# Load pickled data
popular_df = pickle.load(open('C:\\Users\\sameer\\PycharmProjects\\book-recommender-system\\pythonProject1\\popular.pkl','rb'))
pt = pickle.load(open('C:\\Users\\sameer\\PycharmProjects\\book-recommender-system\\pythonProject1\\pt.pkl','rb'))
books = pickle.load(open('C:\\Users\\sameer\\PycharmProjects\\book-recommender-system\\pythonProject1\\books.pkl','rb'))
similarity_scores = pickle.load(open('C:\\Users\\sameer\\PycharmProjects\\book-recommender-system\\pythonProject1\\similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')

    # Check if the user_input exists in the DataFrame index
    if user_input in pt.index:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            data.append(item)

        print(data)
        return render_template('recommend.html', data=data)
    else:
        # Handle the case where the book is not found
        return render_template('recommend.html', data=[], message="Sorry, the book you entered was not found in our database. Please try another one.")

if __name__ == '__main__':
    app.run(debug=True)

# islo run karne k liye bus hume app.py wali file h usko run karwa dena h or terminal par jo link aayaga
# usko click kar denan h toh woh apne aap open ho jaygi
