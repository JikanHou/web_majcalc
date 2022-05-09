import os.path
import uuid

from majcalc import app, db
from flask import render_template, redirect, url_for, flash, abort, request, make_response
from flask_login import login_required, current_user, login_user, logout_user
from majcalc.forms import LoginForm, RegisterForm, PlayerSelectForm
from majcalc.models import User
from urllib import parse
import click


def is_safe_link(url):
    local_parse = parse.urlparse(request.host_url)
    target_url = parse.urljoin(request.host_url, url)
    target_parse = parse.urlparse(target_url)
    return target_parse.scheme in ("http", "https") and target_parse.netloc == local_parse.netloc


def redirect_back(default = '/', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if target and is_safe_link(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


@app.route("/")
def index():
    from majcalc.models import User, Game, Round, game_player_ass_table as g_p
    from sqlalchemy import func, desc, text
    res = db.session.query(g_p.c.userID, func.count(g_p.c.gameID).label("game_cnt")).group_by(g_p.c.userID).order_by(text("-game_cnt")).limit(5).all()
    most_game_players = []
    for rec in res:
        most_game_players.append(User.query.get(rec[0]))
    return render_template("index.html", most_game_players = most_game_players)


@app.route("/statistics")
def statistics():
    return render_template("statistics.html")


@app.route("/help")
def help():
    return render_template("help.html")


@app.route("/login", methods = ["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    else:
        loginForm = LoginForm()
        if loginForm.validate_on_submit():
            username = loginForm.username.data
            password = loginForm.password.data
            user = User.query.filter(User.username == username).first()
            if not user:
                flash("不存在的账号")
                return render_template("login.html", form = loginForm)
            elif not user.validatePassword(password):
                flash("用户名或密码不正确")
                return render_template("login.html", form = loginForm)
            else:
                login_user(user)
                flash("登录成功")
                return redirect_back()
        else:
            return render_template("login.html", form = loginForm)


@app.route("/register", methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("您已成功登录")
        return redirect_back()
    form = RegisterForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data.lower()
        user.setPassword(form.password.data)
        user.nickname = form.nickname.data
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("index"))
    else:
        return render_template("register.html", form = form)


@app.route("/personalInfo/<id>")
def personalInfo(id):
    user = User.query.get(id)
    if user is None:
        flash("该玩家不存在")
        abort(404)
    if current_user.is_authenticated and user.id == current_user.id:
        game_list = user.games[::-1]
    else:
        game_list = user.games[::-1][:10]
    #click.echo(user.games)
    return render_template("personalInfo.html", user = user, game_list = game_list)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("登出成功")
    return redirect(url_for("index"))


@app.route("/newGame", methods = ["POST", "GET"])
@login_required
def newGame():
    playerSelectForm = PlayerSelectForm()
    if playerSelectForm.validate_on_submit():
        nicknames = [playerSelectForm.player_east.data,  playerSelectForm.player_south.data, playerSelectForm.player_west.data, playerSelectForm.player_north.data]
        order = "东南西北"
        for i in range(4):
            if nicknames[i] in nicknames[i + 1:]:
                flash("%s家昵称重复" % order[i])
                return render_template("newGame_collectInfo.html", form = playerSelectForm)
        player_east = User.query.filter(User.nickname == playerSelectForm.player_east.data).first()
        player_south = User.query.filter(User.nickname == playerSelectForm.player_south.data).first()
        player_west = User.query.filter(User.nickname == playerSelectForm.player_west.data).first()
        player_north = User.query.filter(User.nickname == playerSelectForm.player_north.data).first()
        return render_template("newGame_gameDetails.html", player_e = player_east, player_s = player_south, player_w = player_west, player_n = player_north)
    else:
        return render_template("newGame_collectInfo.html", form = playerSelectForm)


@app.route("/avatar_upload", methods = ['POST'])
@login_required
def avatar_upload():
    save_img = ["jpg", "jpeg", "png", "gif"]
    avatar = request.files['avatar']
    avatar.filename = avatar.filename.lower()
    if '.' not in avatar.filename or avatar.filename.split('.')[-1] not in save_img:
        return make_response("文件类型不合法，头像仅支持jpg，jpeg，png，gif格式", 403)
    pic_name = ''.join(str(uuid.uuid4()).split('-')) + '.' + avatar.filename.split('.')[-1]
    path = os.path.join(app.root_path, 'static', 'avatars', pic_name)
    avatar.save(path)
    if current_user.avatar != "defaultAvatar.png":
        try:
            os.remove(os.path.join(app.root_path, 'static', 'avatars', current_user.avatar))
        except:
            pass
    User.query.get(current_user.id).avatar = pic_name
    db.session.commit()
    return "success"


@app.route("/game_details/<id>")
def game_details(id):
    from majcalc.models import Game
    game = Game.query.get(id)
    if game:
        return render_template("gameDetails.html", game = game)
    else:
        abort(404)

@app.route("/game_result_upload", methods = ["POST"])
@login_required
def game_result_upload():
    from majcalc.models import User, Game, Round, Result
    import json
    player_list = json.loads(request.form["player_list"])
    game_result = json.loads(request.form["game_result"])
    game = Game()
    game.uploader_id = current_user.id
    for player in player_list:
        game.players.append(User.query.filter(User.nickname == player).first())
    for result in game_result:
        round = Round()
        round.game_id = game.id
        round.round, round.bonba = map(int, result["id"].split("."))
        round.result = " ".join(map(str, result["round_result"]))
        round.result += " " + str(result["kyoutaku"])
        round.reason = result["reason"]
        db.session.add(round)
    db.session.add(game)
    round_result = game_result[-1]["round_result"]
    rank = [0, 1, 2, 3]
    for i in range(3):
        for j in range(3):
            if round_result[rank[j]] < round_result[rank[j + 1]]:
                rank[j], rank[j + 1] = rank[j + 1], rank[j]
    for r in rank:
        result = Result()
        result.player_id = User.query.filter(User.nickname == player_list[r]).first().id
        result.player_nickname = player_list[r]
        result.player_point = round_result[r]
        game.results.append(result)
        db.session.add(result)
    db.session.commit()


    return f"gameDetails/{game.id}"


@app.route("/gameDetails/<id>")
def gameDetails(id):
    from majcalc.models import Game, Round
    return f"{id}局细节"


@app.errorhandler(404)
def page_not_found(err):
    return render_template("errorHandler/404.html", message = err)


@app.errorhandler(405)
def method_not_allowed(err):
    return render_template("errorHandler/405.html", message = err)