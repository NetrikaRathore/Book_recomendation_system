from flask import Flask,render_template,request
import pickle
import numpy as np
fp1 = r'C:\Users\netri\Documents\Recomendation System (5th Sem)\popular.pkl'
fp2 = r'C:\Users\netri\Documents\Recomendation System (5th Sem)\pt.pkl'
fp3 = r'C:\Users\netri\Documents\Recomendation System (5th Sem)\books.pkl'
fp4 = r'C:\Users\netri\Documents\Recomendation System (5th Sem)\similarity_scores.pkl'
popular_df = pickle.load(open(fp1,'rb'))
pt  = pickle.load(open(fp2,'rb'))
books  = pickle.load(open(fp3,'rb'))
similarity_scores  = pickle.load(open(fp4,'rb'))
app = Flask(__name__)
@app.route('/')
def index():
 return render_template('index.html',
                        book_name = list(popular_df['Book-Title'].values),
                        author=list(popular_df['Book-Author'].values),
                        image=list(popular_df['Image-URL-M'].values),
                        votes=list(popular_df['num_ratings'].values),
                        ratings = list(popular_df['avg_ratings'].values)
                        )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')
@app.route('/recommend_books',methods = ['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]
    data = []
    for i in similar_items:
        # print(pt.index[i[0]])
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    print(data)
    return render_template('recommend.html',data = data)
if __name__ == '__main__':
 app.run(debug=True)