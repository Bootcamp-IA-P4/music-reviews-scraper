run-back:
	python -m app.main

run-front:
	cd frontend && . ~/.nvm/nvm.sh && nvm use && npm run dev

dev:
	python -m app.main &
	cd frontend && . ~/.nvm/nvm.sh && nvm use && npm run dev

install-back:
	pip install -r requirements.txt

install-front:
	cd frontend && . ~/.nvm/nvm.sh && nvm use && npm install

test-db:
	python -m scripts.test_db
