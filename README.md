### Hexlet tests and linter status:
[![Actions Status](https://github.com/AntonLysachev/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/AntonLysachev/python-project-83/actions)

Description: Page analyzer
             Check websites for SEO suitability for free
             https://hexlet-code-qxkq.onrender.com

Commands: 
        Install - `make install`,
        start guincorn - `make start`,
        start flask server - `make dev`,
        linter - `make lint`,
        run build.sh - `make build`

Environment variables: FLASK_APP=page_analyzer:app, SECRET_KEY=your private key, DATABASE_URL=url of your database, DEBUG_SWITCH=Enables/disables debug mode(True/Fals)