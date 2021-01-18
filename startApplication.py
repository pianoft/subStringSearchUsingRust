import subprocess


def run(commands):
    subprocess.run([commands], shell=True)
    return


#run("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh")#Run these 2 commnads as you have not installed them.
#run('sudo apt install speech-dispatcher')




run('pip3 install pipenv;pip3 install bs4 flask flask_sqlalchemy sqlalchemy_imageattach numpy;cd application;python3 server.py')

run('pipenv shell')
