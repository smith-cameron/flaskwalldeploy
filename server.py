from wallApp import app
from wallApp.controllers import main, loginReg, posts


if __name__=="__main__":
    app.run(debug=False)