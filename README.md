# Pladmed backend

Vagrant:

You can run everything through a virtual machine using vagrant with the following instructions:

- Install virtualbox and vagrant
- Run: vagrant up
- Run: vagrant ssh
- Go to the pladmed-backend folder (cd .. & cd .. & cd vagrant)
- Install dependencies using pipenv: pipenv install -r requirements.txt
- Access the venv created: pipenv shell
- You are ready to go, try testing using: make debug

Commands:

- Debug with 'make debug' (It tracks changes)
- Run with 'make start'
- Accessible at port 5000.