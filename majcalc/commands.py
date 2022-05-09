import random

import click
from majcalc import app
from majcalc import db
from faker import Faker

@app.cli.command()
@click.option("--drop", is_flag = True)
def init_db(drop):
    """Initiate the database. Run the command before run the app."""
    if drop:
        click.confirm("Drop ALL the database?", abort = True)
        db.drop_all()
        click.echo("Database dropped")
    db.create_all()
    click.echo("Database created")

@app.cli.command()
@click.option("-user", "-u", default = 50)
@click.option("-game", "-g", default = 100)
def forge_fake(user, game):
    """Generate fake users etc."""
    from majcalc.models import User, Game, Round, Result
    faker = Faker(locale = 'zh_CN')
    for i in range(user):
        new_user = User()
        new_user.username = faker.user_name()
        new_user.setPassword(faker.password())
        new_user.nickname = faker.name()
        db.session.add(new_user)
    db.session.commit()
    click.echo("Fake users generated")
    for i in range(game):
        new_game = Game()
        player_list = random.sample(range(1, user + 1), 4)
        point = 40000
        for player_id in player_list:
            new_game.players.append(User.query.get(player_id))
            new_result = Result()
            new_result.player_id = player_id
            new_result.player_nickname = User.query.get(player_id).nickname
            new_result.player_point = point
            point -= 10000
            new_game.results.append(new_result)
        db.session.add(new_game)
        for round_cnt in range(1, 9):
            new_round = Round()
            new_round.bonba = 0
            new_round.round = 1
            new_round.game_id = new_game.id
            db.session.add(new_round)
    db.session.commit()
    click.echo("Fake games generated")