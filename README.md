# PWP SPRING 2019
# WORKOUT TRACKER / DIARY API
# Group information
* Student 1. Mauri Miettinen mauri.miettinen@gmail.com
* Student 2. Tuomas Koivuaho tuomas.koivuaho@gmail.com
* Student 3. Valtteri Erkkilä valtteri.erkkila@gmail.com

# Diary API

Diary API is general logging tool for your everyday tasks. It's simple and efficient to use due to small number of input fields. 


## To run application

At top level

* First

        pip install -r requirements.txt
        export FLASK_APP=diary
        flask init-db

* optional

        cd db
        python populate
        cd ..

* Then

        flask run


## Tests

* To run 

    cd to tests or in top level run

        pytest

