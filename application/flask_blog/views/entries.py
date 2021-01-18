from flask import request, redirect, url_for, render_template, flash, session, Blueprint
from flask_blog import app
from flask_blog import db
from flask_blog.models.entries import Entry
from flask_blog.views.views import login_required
from sqlalchemy.sql.expression import func
from bs4 import BeautifulSoup
import requests
import bs4

import subprocess


def runBashCommand(commands):
    subprocess.run([commands], shell=True)
    return


@app.route('/')
@login_required
def show_entries():
    global state
    entries = Entry.query.order_by(Entry.id.desc()).all()
    flash("現在表示されてる記事の数:"+str(len(entries))+"個")
    return render_template('entries/index.html', entries=entries)


setOfFileNames = set()


@app.route('/entries/stringSearch', methods=['POST', 'GET'])
@login_required
def stringSearch():
    global setOfFileNames
    entries = Entry.query.order_by(Entry.id.desc()).all()
    specifiedDesiredStrings = request.form['stringSearch'].split('、')

    runBashCommand('rm -rfv result.txt')

    runBashCommand('cd ./rustLab/src;cargo run '+specifiedDesiredStrings[0])

    fr = open("result.txt", "r")

    found_names_of_files = fr.readlines()

    fr.close()

    newArticlesWhichWillBeListedInPage = set()

    for found_name_of_file in found_names_of_files:

        found_name_of_file = found_name_of_file[:len(found_name_of_file)-1]

        fr = open("rawTextsOfFiles/"+found_name_of_file, "r")

        content_of_file = fr.read()
        fr.close()

        x1 = content_of_file.find('<title>')+7
        x2 = content_of_file.find('</title>')-10
        title_of_article = content_of_file[x1:x2]
        newArticlesWhichWillBeListedInPage.add(
            (found_name_of_file, title_of_article))

    for article in newArticlesWhichWillBeListedInPage:
        # print("http://pathtimeblog.com/archives/" +
        #       article[0][0:len(article[0])-4]+".html")

        entry = Entry(
            title="http://pathtimeblog.com/archives/" +
            article[0][0:len(article[0])-4]+".html",
            text=article[1],
        )
        db.session.add(entry)
        db.session.commit()
    return redirect(url_for('show_entries'))


@app.route('/entries/deleteAllArticles', methods=['POST', 'GET'])
@login_required
def deleteAllArticles():
    entries = Entry.query.order_by(Entry.id.desc()).all()
    for entry in entries:
        db.session.delete(entry)
        db.session.commit()
    return redirect(url_for('show_entries'))
