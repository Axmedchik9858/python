from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.utils import redirect

app = Flask(__name__)#bioz ishlamoqchi bogan fyl nomini yozamiz buning uchun  __name__ funksiyasini ishlatamiz
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db' #ishlamoqchi bolgan baza dannixni nomini yozamiza
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)


class Article(db.Model):#bu yerda tepadagi db dan nasl olamiza
    id = db.Column(db.Integer, primary_key=True)#sonlar uchun polya yaratdim
    title  =  db.Column(db.Integer, nullable=False)#100 ta simvol sigadigan polya yaratdim
    intro = db.Column(db.String(300), nullable=False)#300 ta sozli polya yaratdim
    text = db.Column(db.Text, nullable=False)#ilmiy ish uchun polyada text ni ishlatamiz sababi ilmiy ish juda katta bolishi mumkin text bu uchun eng yaxshi tanlov
    date = db.Column(db.DateTime, default=datetime.utcnow)#ilmiy ishni qoygan vaqti 


    def __repr__(self):
        return '<Article %r>' % self.id#qachonki biz bu yerda ilmiy ish obyektni chaqirsak u biln birga id siniyam olamiza  


@app.route('/')#url adressni kuzatish uchun ishlatiladi
@app.route('/home')
def index():#bosh betni kuzatish uchun indeks htmlni yani topish uchun shu funksiyani ishlatamiza
    return render_template("index.html")


@app.route('/about')#url adressni kuzatish uchun ishlatiladi
def about():#about betni kuzatish uchun indeks htmlni yani topish uchun shu funksiyani ishlatamiza
    return render_template("about.html")


@app.route('/posts')#url adressni kuzatish uchun ishlatiladi
def posts():#posts betni kuzatish uchun indeks htmlni yani topish uchun shu funksiyani ishlatamiza
    articles = Article.query.order_by(Article.date.desc()).all()#bu yerda Article dan boshlab kelgan barcha malumotlar articles ga  ozlashtiriladi bu yerda order_by(Article..date)qaysi maydon boyicha sortirovka qilishni aytadi hozir bizda vaqt boyicha sortirovkalanadi desc() bu funksiya orqali biz kelgan habarlarni birinchi oringa yangilarni qoshadi eskilari pastga tushib ketaveradi
    return render_template("posts.html", articles=articles)#bu yerda articles ni oziga oxshagan qimatga ozlashtirimiz va shu orqali shablon ustida ish bajaramiza !diqqat hech qachan boshqa qiymatga ozlashtirilmaydi bolmasa chalkashlik yuz berishi mumkin


@app.route('/posts/<int:id>')#url adressni id boyicha oberadi va id beradi
def post_detail(id):#post_detail betni kuzatish uchun indeks htmlni yani topish uchun shu funksiyani ishlatamiza
    article = Article.query.get(id)#bu yerda Article class dagi id ni chaqiradi va article ga ozlashtiradi
    return render_template("post_detail.html", article=article)#bu yerda articles ni oziga oxshagan qimatga ozlashtirimiz va shu orqali shablon ustida ish bajaramiza !diqqat hech qachan boshqa qiymatga ozlashtirilmaydi bolmasa chalkashlik yuz berishi mumkin    


@app.route('/posts/<int:id>/del')#url adressni id boyicha oberadi va id beradi va uni ochiradi
def post_delete(id):#post_delete bu funksiya orqali keraksiy xabarlarni ochiramiza
    article = Article.query.get_or_404(id)#bu yerda ham huddi get id ga oxshaydi faqat ozgina farqi gar id topilmasa 404 hato beriladi
    #trayexept bu bazadanni bilan ishlash uchun eng kerakli komanda
    try:
        db.session.delete(article)#bu yerda articldagi xabarlarni ochirish metodi delete ni ishlatamiz
        db.session.commit()
        return redirect('/posts')#redrict qayta adreslaydi
    except:
        return "xabarni ochirishda hatolik yuz berdi"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])#get bu shu sahifaga otishimiza post bolsa shu sahifadan habar yuborishimiza
def post_update(id):
    article = Article.query.get(id)#bu yerda obyektga articlega ozlashtirilgan qiymatlar kiritiladi
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']


        try:
            db.session.commit()#articl obyektiga ozlashtirilgan yangi  qiymatlar  commit orqali yangilanadi
            return redirect('/posts')
        except:
            return "qoshishda hatolik yuz berdi"
    else:
        return render_template("post_update.html", article=article)

   
@app.route('/create-article', methods=['POST', 'GET'])
def create_articel():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']


        article = Article(title = title, intro = intro, text = text)


        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "qoshishda hatolik yuz berdi"
    else:
        return render_template("create-article.html")

# @app.route('/user/<string:name>/<int:id>')#url adressni kuzatish uchun ishlatiladi #va name va id poliyani parametrini bilish uchun uni turini yozamiz string, int
# def user(name, id):#user betni kuzatish uchun indeks htmlni yani topish uchun shu funksiyani ishlatamiza
#     return "User page: " + name + "-" + str(id)#bu yerda int tipini string tipiga ozgartirdim


if __name__=="__main__":
    app.run(debug=True)
    #debag True qilamiz bunga sabab hamma hatolar ekranda chiqadi








