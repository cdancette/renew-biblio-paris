# Renew books for bibliotheque de paris (bibliotheque.paris.fr)


### Renewal script
This script will renew all the books in the "A rendre bientôt" state.

To use this script, put a .env file in this folder with the following content

```bash
USERNAME=<username>
PASSWORD=<password>
```

You can put this script in the crontab, to run for example once a day

### Dashboard

To see a dashboard of your current books, start the web server with `flask run`.

<img width="875" alt="image" src="https://github.com/cdancette/renew-biblio-paris/assets/10550327/a10a5560-20bb-4eb1-8330-5aa6c1d019ac">
