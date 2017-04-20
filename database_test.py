"""
Screwing around with databases, go to terminal and type in: sqlite3 database.db < schema.sql
before running this code otherwise it won't work
also for some reason the email is getting cut off
type in terminal: sqlite3
then type in: .help
then type in: .open database.db
then type in: .read database.db
to see what has been inserted
"""

import sqlite3 as sql
import sys
import bcrypt   # INCLUDE INSTALL DEPENDENCY
salt = '$2b$12$oipF.pNP9t4uEUUTEExH8.'  # Global salt used to hash passwords and comparisons
salt = salt.encode('utf-8')


# Drinks Data --------------->

def update_drink(drink):
    """
    This function takes a drink and decrements the amount of drink based off the type
    """
    con = sql.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM drinks_data')
    data = cur.fetchall()
    amount = 0
    for category in data:
        if category[0] == drink:
            active_drink = category[0]
            amount = category[1]
            if active_drink == 'coke' or 'sprite' or 'tonic' or 'orange' or 'ginger':
                amount = amount - 4
            elif active_drink == 'vodka' or 'rum' or 'gin' or 'tequila':
                amount = amount - 1
    cur.execute('UPDATE drinks_data SET amount=? WHERE drink=?', (amount, drink))
    con.commit()
    con.close()


def get_drink_count(drink):
    """
    This function takes a drink and returns the amount of that drink that is left
    """
    con = sql.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM drinks_data')
    data = cur.fetchall()
    for choice in data:
        if choice[0] == drink:
            return choice[1]

# --------------------------->


def sync_user(username, barcode):
    """
    This function takes a username and barcode readin from a reader
    and syncs the corresponding user account with the barcode.
    """
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute('SELECT * FROM account_holder')
    data = cur.fetchall()
    for person in data:
        if person[2] == username:
            person_barcode = barcode
    cur.execute('UPDATE account_holder SET barcode=? WHERE username=?', (person_barcode, username))
    con.commit()
    con.close()


def insert_user(email, username, phone, password):
    """
    This function creates a new username with attributes:
    -email
    -username
    -phone number
    -password
    based off of the information gathered from the sign up sheet
    """
    con = sql.connect("database.db")
    cur = con.cursor()
    password = password.encode('utf-8')
    password = bcrypt.hashpw(password, salt)
    cur.execute("INSERT INTO account_holder (email,username,phone,password,drinks,barcode) VALUES (?,?,?,?,?,?)", (email, username, phone, password, 0,''))
    con.commit()
    con.close()


def increase_drink_count(barcode):
    """
    This function increases the drinks count for a user based off their
    linked barcode identity
    """
    con = sql.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM account_holder')
    data = cur.fetchall()
    drinks = 0
    for category in data:
        if category[6] == barcode:
            drinks = category[5] + 1
    cur.execute('UPDATE account_holder SET drinks=? WHERE barcode=?', (drinks, barcode))
    con.commit()
    con.close()


def return_data():
    """
    Returns all the data in the account_holder table
    """
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM account_holder")
    row = cur.fetchall()
    print(row)
    con.close()


def update_info(username, password):
    """
    This function updates a username with a new password and sets them in the database
    """
    con = sql.connect('database.db')
    cur = con.cursor()
    password = password.encode('utf-8')
    password = bcrypt.hashpw(password, salt)
    cur.execute('UPDATE account_holder SET password=? WHERE username=?', (password, username))
    con.commit()
    con.close()


def return_user(username):
    """
    This function takes a username and returns all the information about them including:
    -id
    -email
    -username
    -phone
    -password
    -number of drinks
    -barcode identifier
    -height
    -weight
    -age
    -gender
    """
    con = sql.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM account_holder')
    data = cur.fetchall()
    for person in data:
        if person[2] == username:
            return(person)
    con.commit()
    con.close()
    return None


def chec_password(username, password):
    """
    This function takes a username and the entered password and checks to see if
    the password is correct. It does this by using the global salt and hashing
    the given password and checking to see if this hashed phrase is the same
    as what is in the database.
    """
    con = sql.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM account_holder')
    data = cur.fetchall()
    state = False   # Match state, by default false
    for person in data:
        if person[2] == username:
            real_password = person[4]   # Hashed password for asociated match person
    password = password.encode('utf-8')     # Encode given password
    comp_password = bcrypt.hashpw(password, salt)
    print(comp_password)
    print(real_password)
    if real_password == comp_password:      # Compare given password and what the db says
        state = True
    con.commit()
    con.close()

    print(state)
    return state


if __name__ == '__main__':
    return_data()
    increase_drink_count('hello')
    update_drink('coke')
    sync_user('pseger1', '12123132')
    print(get_drink_count(input('Drink: ')))
    # return_user(input('Username: '))
