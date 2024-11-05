from setup import app
from setup.models.table import Conexao

if __name__ == "__main__":
    Conexao()
    app.run(debug=True)