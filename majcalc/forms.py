from flask_wtf import FlaskForm
from wtforms.validators import *
from wtforms import *


class LoginForm(FlaskForm):
    username = StringField("用户名",
                           validators = [DataRequired("请输入用户名"),
                                                Length(6, 20, message = "用户名的长度应为6-20个字符"),
                                                Regexp("^\w+$", message = "用户名中只能含有数字，字母与下划线")])
    password = PasswordField("密码",
                             validators = [DataRequired("请输入密码"),
                                           Length(8, 20, message = "密码的长度应为8-20个字符"),
                                           Regexp("^\w+$", message = "密码中只能含有数字，字母与下划线")])
    remember = BooleanField("记住我")
    submit = SubmitField("登录")


class RegisterForm(FlaskForm):
    username = StringField("用户名",
                           validators = [DataRequired("请输入用户名"),
                                                Length(6, 20, message = "用户名的长度应为6-20个字符"),
                                                Regexp("^\w+$", message = "用户名中只能含有数字，字母与下划线")])
    password = PasswordField("密码",
                             validators = [DataRequired("请输入密码"),
                                                 Length(8, 20, message = "密码的长度应为8-20个字符"),
                                                 Regexp("^\w+$", message = "密码中只能含有数字，字母与下划线")])
    repPassword = PasswordField("重复密码",
                                validators = [DataRequired("请重复输入密码"),
                                              Length(1, 20),
                                              EqualTo("password", "两次输入的密码不一致")])
    nickname = StringField("昵称",
                           validators = [DataRequired("请输入昵称"),
                                         Length(1, 20, message = "昵称长度应在1-20个字符之间（一个汉字算两个字符）")])
    submit = SubmitField("注册")

    def is_char(self, ch):
        return "\u4e00" <= ch <= "\u9fff"

    def validate_nickname(form, field):
        nickname_data = field.data
        for ch in nickname_data:
            if not (form.is_char(ch) or ch.isalnum() or ch == '-'):
                raise ValidationError('昵称中只能包含汉字、数字、字母与下划线')
        from majcalc.models import User
        user = User.query.filter(User.nickname == field.data).first()
        if user:
            raise ValidationError('昵称已存在')


def get_all_nicknames():
    from majcalc.models import User
    q = User.query.with_entities(User.nickname).all()
    return [u.nickname for u in q]


class PlayerSelectForm(FlaskForm):
    player_east = StringField("东：", validators = [DataRequired("请指定一名玩家"), AnyOf(get_all_nicknames(), "东家昵称错误")])
    player_south = StringField("南：", validators = [DataRequired("请指定一名玩家"), AnyOf(get_all_nicknames(), "南家昵称错误")])
    player_west = StringField("西：", validators = [DataRequired("请指定一名玩家"), AnyOf(get_all_nicknames(), "西家昵称错误")])
    player_north = StringField("北：", validators = [DataRequired("请指定一名玩家"), AnyOf(get_all_nicknames(), "北家昵称错误")])
    bonba = IntegerField("本场：", validators = [Optional()],
                        render_kw = {
                            "placeholder": "100"
                        })
    uma = StringField("马点：",
                      render_kw = {
                          "placeholder": "30 10 -10 -30"
                      })
    submit = SubmitField("确认")

    def validate_uma(self, field):
        if field.data:
            umas = field.data.split(" ")
        else:
            umas = field.render_kw["placeholder"].split(" ")
        if len(umas) != 4:
            raise ValidationError("请以空格分隔，输入顺位码")
