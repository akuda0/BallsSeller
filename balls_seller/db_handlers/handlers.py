import sqlite3
import os
import sys
sys.path.append("../")
from third_party.ops import gen_picture_path


def get_id_and_nicknames_from_DB():
    connection = sqlite3.Connection(os.path.join('db', 'balls_seller.sqlite'))
    cursor = connection.cursor()
    cursor.execute("SELECT nickname, id FROM Customers")
    list_of_id_and_nicks = cursor.fetchall()
    return list_of_id_and_nicks


def get_ordered_shaped_balls_from_DB(nickname: int):
    connection = sqlite3.Connection(os.path.join('db', 'balls_seller.sqlite'))
    cursor = connection.cursor()
    cursor.execute(f"SELECT "
                   f"Shaped_Balls.type, Shaped_Balls.subtype, Shaped_Balls.picture, Orders.amount, Shaped_Balls.price "
                   f"FROM "
                   f"Shaped_Balls, Orders "
                   f"WHERE "
                   f"Orders.nickname=={nickname} and Orders.type=='shaped' and Shaped_Balls.id == Orders.ball ")
    ordered_common_balls = cursor.fetchall()
    connection.close()
    return ordered_common_balls


def get_ordered_common_balls_from_DB(nickname: int):
    connection = sqlite3.Connection(os.path.join('db', 'balls_seller.sqlite'))
    cursor = connection.cursor()
    cursor.execute(f"SELECT "
                   f"Common_Balls.type, Common_Balls.material, Common_Balls.color, Common_Balls.picture, Orders.amount, Common_Balls.price "
                   f"FROM "
                   f"Common_Balls, Orders "
                   f"WHERE "
                   f"Orders.nickname=={nickname} and Orders.type=='common' and Common_Balls.id == Orders.ball ")
    ordered_common_balls = cursor.fetchall()
    connection.close()
    return ordered_common_balls


def get_own_shaped_balls_from_DB(nickname: int):
    connection = sqlite3.Connection(os.path.join('db', 'balls_seller.sqlite'))
    cursor = connection.cursor()
    cursor.execute(f"SELECT Orders.amount FROM Orders WHERE Orders.nickname=={nickname} and Orders.type=='Blow up'")
    ordered_common_balls = cursor.fetchall()
    connection.close()
    return ordered_common_balls

def get_common_colors_from_DB():
    connection = sqlite3.Connection(os.path.join('db', 'balls_seller.sqlite'))
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT color FROM Common_Balls ORDER BY color ASC")
    common_colors = cursor.fetchall()
    connection.close()
    common_colors = [x[0] for x in common_colors]
    return common_colors


def get_common_color_price_amount_DB(common_ball_type=None, common_ball_material=None):
    connection = sqlite3.Connection(os.path.join('db', 'balls_seller.sqlite'))
    cursor = connection.cursor()
    cursor.execute(f"SELECT DISTINCT color, price, amount FROM Common_Balls "
                   f"where type == '{common_ball_type}' AND material == '{common_ball_material}' ORDER BY color ASC")
    common_colors_price_amount = cursor.fetchall()
    connection.close()
    return common_colors_price_amount


def get_common_types_from_DB():
    connection = sqlite3.Connection(os.path.join('db', 'balls_seller.sqlite'))
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT type FROM Common_Balls ORDER BY color ASC")
    common_types = [tuple_element[0] for tuple_element in cursor.fetchall()]
    connection.close()
    return common_types


def get_shaped_types_from_DB():
    connection = sqlite3.Connection(os.path.join('db', 'balls_seller.sqlite'))
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT type FROM Shaped_Balls")
    common_types = [tuple_element[0] for tuple_element in cursor.fetchall()]
    connection.close()
    return common_types


def get_shaped_subtypes_from_DB(shaped_ball_type=None):
    connection = sqlite3.Connection(os.path.join('db', 'balls_seller.sqlite'))
    cursor = connection.cursor()
    if shaped_ball_type is None:
        return []
    else:
        cursor.execute(f"SELECT DISTINCT subtype FROM Shaped_Balls "
                       f"where type == '{shaped_ball_type}'")
        shaped_ball_subtypes = [tuple_element[0] for tuple_element in cursor.fetchall()]
        connection.close()
        return shaped_ball_subtypes


def get_shaped_pictures_from_DB(shaped_ball_type=None, shaped_ball_subtype=None):
    connection = sqlite3.Connection(os.path.join('db', 'balls_seller.sqlite'))
    cursor = connection.cursor()
    if shaped_ball_type is None and shaped_ball_subtype is None:
        return [], []
    else:
        # TODO: сделать в таблице отдельные строки для каждой картинки
        cursor.execute(f"SELECT picture FROM Shaped_Balls "
                       f"where type == '{shaped_ball_type}' and subtype == '{shaped_ball_subtype}' ORDER BY picture ASC")
        pictures_paths = [tuple_element[0] for tuple_element in cursor.fetchall()]
        pictures_names = pictures_paths.copy()
        for i in range(len(pictures_paths)):
            pictures_paths[i] = gen_picture_path(pictures_paths[i], balloon_type="shaped")
        connection.close()
        return pictures_paths, pictures_names


def get_common_pictures_from_DB(common_ball_type=None, common_ball_material=None, common_ball_color=None):
    connection = sqlite3.Connection(os.path.join('db', 'balls_seller.sqlite'))
    cursor = connection.cursor()
    if common_ball_type is None and common_ball_material is None and common_ball_color is None:
        return [], []
    else:
        # TODO: сделать в таблице отдельные строки для каждой картинки
        cursor.execute(f"SELECT picture FROM Common_Balls "
                       f"where type == '{common_ball_type}' "
                       f"and material == '{common_ball_material}'"
                       f"and color == '{common_ball_color}'ORDER BY picture ASC")
        pictures_paths = [tuple_element[0] for tuple_element in cursor.fetchall()]
        pictures_names = pictures_paths.copy()
        for i in range(len(pictures_paths)):
            pictures_paths[i] = gen_picture_path(pictures_paths[i], balloon_type="common")
        connection.close()
        return pictures_paths, pictures_names


def get_common_materials_from_DB(common_ball_type=None):
    connection = sqlite3.Connection(os.path.join('db', 'balls_seller.sqlite'))
    cursor = connection.cursor()
    if common_ball_type is None:
        return []
    else:
        cursor.execute(f"SELECT DISTINCT material FROM Common_Balls "
                       f"where type == '{common_ball_type}' ORDER BY material ASC")
        common_types = [tuple_element[0] for tuple_element in cursor.fetchall()]
        connection.close()
        return common_types


def get_amount_of_common_balls(type: str, material: str, color: str, picture: str):
    connection = sqlite3.Connection(os.path.join('db', 'balls_seller.sqlite'))
    cursor = connection.cursor()
    cursor.execute(f"SELECT amount FROM Common_Balls where type == '{type}' "
                   f"AND color == '{color}' "
                   f"AND material == '{material}'"
                   f"AND picture == '{picture}'")
    amount = cursor.fetchone()[0]
    connection.close()
    return amount


def get_amount_of_shaped_balls(type: str, subtype: str, picture_name: str):
    connection = sqlite3.Connection(os.path.join('db', 'balls_seller.sqlite'))
    cursor = connection.cursor()
    cursor.execute(f"SELECT amount FROM Shaped_Balls where type == '{type}' "
                   f"AND subtype == '{subtype}' "
                   f"AND picture == '{picture_name}'")
    amount = cursor.fetchone()[0]
    connection.close()
    return amount


# def add_note(note):
#     connection = sqlite3.Connection(os.path.join('db', 'balls_seller.sqlite'))
#     cursor = connection.cursor()
#     cursor.execute(f"INSERT INTO Orderd (notes) VALUES ('{note}')")
#     connection.commit()
#     connection.close()

def complete_common_order(type: str, material: str, color: str, picture: str,  amount: int, curr_amount: int, nickname: str, note: str):
    connection = sqlite3.Connection(os.path.join('db', 'balls_seller.sqlite'))
    cursor = connection.cursor()
    if amount == curr_amount:
        cursor.execute(f"UPDATE Common_Balls set amount = {0} where type == '{type}' "
                       f"AND color == '{color}'"
                       f"AND material == '{material}' "
                       f"AND picture == '{picture}'")
    else:
        new_amount = curr_amount - amount
        cursor.execute(f"UPDATE Common_Balls set amount = {new_amount} where type == '{type}' "
                       f"AND color == '{color}'"
                       f"AND material == '{material}'"
                       f"AND picture == '{picture}'")
    cursor.execute(f"INSERT INTO Customers (nickname) VALUES ('{nickname}')")
    connection.commit()
    cursor.execute(f"SELECT Common_Balls.id, Customers.id from Common_Balls, Customers "
                   f"where Common_Balls.type = '{type}'"
                   f"AND Common_Balls.color = '{color}'"
                   f"AND Common_Balls.material = '{material}'"
                   f"AND Common_Balls.picture == '{picture}'"
                   f"AND Customers.nickname = '{nickname}'")
    id_ball, id_customer = cursor.fetchone()
    cursor.execute(
        f"SELECT amount FROM Orders where ball='{id_ball}' AND type='common' AND nickname='{id_customer}' AND notes='{note}' AND status='not paid'")
    orders_before_amount = cursor.fetchone()
    if orders_before_amount is None:
        cursor.execute(f"INSERT INTO Orders (ball, type, amount, nickname, notes)"
                       f" VALUES ({id_ball}, \"common\", {amount}, {id_customer}, \"{note}\")")
    else:
        cursor.execute(
            f"UPDATE Orders SET amount={amount + orders_before_amount[0]} where "
            f"ball='{id_ball}' "
            f"AND type='common' "
            f"AND nickname='{id_customer}' "
            f"AND notes='{note}'")
    connection.commit()
    connection.close()


def complete_shaped_order(type: str, subtype: str, picture_name: str, amount: int, curr_amount: int, nickname: str, note: str):
    connection = sqlite3.Connection(os.path.join('db', 'balls_seller.sqlite'))
    cursor = connection.cursor()
    if amount == curr_amount:
        cursor.execute(f"UPDATE Shaped_Balls set amount = {0} where type == '{type}' "
                       f"AND subtype == '{subtype}'"
                       f"AND picture == '{picture_name}'")
        connection.commit()
    else:
        new_amount = curr_amount - amount
        cursor.execute(f"UPDATE Shaped_Balls set amount = {new_amount} where type == '{type}' "
                       f"AND subtype == '{subtype}'"
                       f"AND picture == '{picture_name}'")
        connection.commit()
    cursor.execute(f"INSERT INTO Customers (nickname) VALUES ('{nickname}')")
    connection.commit()
    cursor.execute(f"SELECT Shaped_Balls.id, Customers.id from Shaped_Balls, Customers "
                   f"where Shaped_Balls.type = '{type}'"
                   f"AND Shaped_Balls.subtype = '{subtype}'"
                   f"AND Shaped_Balls.picture = '{picture_name}'"
                   f"AND Customers.nickname = '{nickname}'")
    id_ball, id_customer = cursor.fetchone()
    cursor.execute(
        f"SELECT amount FROM Orders where ball='{id_ball}' AND type='shaped' AND nickname='{id_customer}' AND notes='{note}' AND status='not paid'")
    orders_before_amount = cursor.fetchone()
    if orders_before_amount is None:
        cursor.execute(f"INSERT INTO Orders (ball, type, amount, nickname, notes)"
                       f" VALUES ({id_ball}, \"shaped\", {amount}, {id_customer}, \"{note}\")")
    else:
        cursor.execute(
            f"UPDATE Orders SET amount={amount + orders_before_amount[0]} where "
            f"ball='{id_ball}' "
            f"AND type='shaped' "
            f"AND nickname='{id_customer}' "
            f"AND notes='{note}'")
    connection.commit()
    connection.close()


def complete_blowing_order(amount: int, nickname: str, note: str):
    connection = sqlite3.Connection(os.path.join('db', 'balls_seller.sqlite'))
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO Customers (nickname) VALUES ('{nickname}')")
    connection.commit()
    cursor.execute(f"SELECT id from Customers WHERE nickname = '{nickname}'")
    id_customer = cursor.fetchone()[0]
    cursor.execute(
        f"SELECT amount FROM Orders where nickname='{id_customer}' AND type='Blow up' AND status='not paid' AND notes='{note}'")
    orders_before_amount = cursor.fetchone()
    if orders_before_amount is None:
        cursor.execute(f"INSERT INTO Orders (amount, nickname, notes) VALUES ({amount}, {id_customer}, '{note}')")
    else:
        cursor.execute(
            f"UPDATE Orders SET amount={amount + orders_before_amount[0]} where "
            f"type='Blow up' "
            f"AND nickname='{id_customer}' "
            f"AND notes='{note}'")
    connection.commit()
    connection.close()