# permite acessar diretórios relativos ao diretório do projeto.
import os

from flask import Flask
from flask import render_template
from flask import request

# importacao do SQLAlchemy do Flask
from flask_sqlalchemy import SQLAlchemy

# capturando o caminho do projeto
project_dir = os.path.dirname(os.path.abspath(__file__))
# configurando o arquivo do SQLite
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__)
# define o local de armazenamento do banco
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
# variavel para manipulação do banco de dados
db = SQLAlchemy(app)

class Book(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Title: {}>".format(self.title)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        # cria o objeto
        book = Book(title=request.form.get("title"))
        # insere no banco
        db.session.add(book)
        # efetiva a ação
        db.session.commit()
    #consultando todos os registros
    books = Book.query.all()
    #redirecionando e enviando dados para a tela
    return render_template("home.html", books=books)
  
if __name__ == "__main__":
    app.run(debug=True)
