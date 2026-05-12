# POLILIBRO Django App

Legacy Django project for the POLILIBRO digital book. This project was updated to run on Django 5.2 LTS while keeping CKEditor for the existing rich text content.

## Project Layout

```text
application/
  Book/                 # Django project root
    manage.py
    requirements.txt
    data.clean.json     # Clean fixture for fresh local restores
    data.json           # Old legacy fixture, includes Django metadata
    db.sqlite3          # Local SQLite database, ignored by git
    media/              # Uploaded files, ignored by git
  env/
    app_env/            # Local virtual environment
```

Run the commands below from the Django project folder:

```powershell
cd "C:\Users\kevin\Documents\POLILIBRO 2026\application\Book"
```

## Environment

You have to create or activate a virtual environment before running the app.

Create a local virtual environment from the `application/` folder:

```powershell
python -m venv .\env\app_env
.\env\app_env\Scripts\Activate.ps1
```

Activate an existing local virtual environment:

```powershell
.\env\app_env\Scripts\Activate.ps1
```

Deactivate it:

```powershell
deactivate
```

The virtual environment is outside the Django project folder:

```powershell
..\env\app_env\Scripts\python.exe --version
..\env\app_env\Scripts\python.exe -m django --version
```

The app reads environment variables from `.env` through `python-decouple`. This project already includes a local `.env` file with the required development values:

```text
SECRET_KEY=...
DEBUG=True
```

For normal local work from the `Book/` folder, you should not need to set `SECRET_KEY` manually because `python-decouple` reads `.env`.

If you ever run commands from a context where `.env` is not being picked up, you can temporarily set values in the current PowerShell session:

```powershell
$env:SECRET_KEY='dummy-local-secret'
$env:DEBUG='True'
```

Those `$env:...` values are only temporary for that shell session. Do not commit real production secrets.

## Install Or Refresh Dependencies

```powershell
..\env\app_env\Scripts\python.exe -m pip install -r requirements.txt
```

The project currently targets:

```text
Django==5.2.13
```

CKEditor is intentionally kept for now because the old book content uses CKEditor rich text fields. Django will show a warning that bundled CKEditor 4 is unsupported; this is expected and should be handled in a future editor migration.

The requirements are intentionally small for PythonAnywhere deployment. The old S3 stack was removed because this project currently uses local media files:

```text
boto3
botocore
django-storages
s3transfer
jmespath
```

## Run Locally

```powershell
..\env\app_env\Scripts\python.exe manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Admin:

```text
http://127.0.0.1:8000/polilibroescom/
```

The `/admin/` URL is a fake admin/honeypot-style route and should return not found.

## Fresh Local Database Restore

Use this when you want a clean SQLite database with the saved book content.

```powershell
Remove-Item .\db.sqlite3
..\env\app_env\Scripts\python.exe manage.py migrate
..\env\app_env\Scripts\python.exe manage.py loaddata .\data.clean.json
..\env\app_env\Scripts\python.exe manage.py runserver
```

If `db.sqlite3` does not exist, skip the `Remove-Item` line.

`data.clean.json` includes:

```text
auth.user: 1
home.book: 1
book.unit: 4
book.chapter: 12
book.section: 44
book.resource: 44
```

It intentionally excludes old Django-generated metadata:

```text
contenttypes.contenttype
auth.permission
admin.logentry
sessions.session
```

Django recreates modern `contenttypes` and permissions during `migrate`. Old admin log entries and old sessions are not needed for the app to run.

## Fixture Notes

Use `data.clean.json` for new database restores.

Avoid using `data.json` unless you specifically need the original legacy export. It includes old Django metadata and can fail on fresh databases with duplicate `contenttypes` errors.

The fixture stores database rows and file paths only. It does not contain the uploaded media files themselves. Keep the `media/` folder backed up separately if the project depends on uploaded PDFs, SVGs, or images.

## CKEditor Uploads And Media Files

The book HTML content is edited through Django admin using CKEditor fields. For example, `Section.content` is a `RichTextUploadingField`, so the admin editor can store formatted HTML in the database.

The public section template renders that saved HTML with:

```django
{{ section.content|safe }}
```

This project configures CKEditor uploads with:

```python
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
```

When using CKEditor's upload feature in the admin panel, you can select a local image from your computer. CKEditor uploads that image into the media folder using the current date:

```text
media/uploads/YYYY/MM/DD/
```

For example:

```text
media/uploads/2021/09/06/picture-1.png
```

Because `CKEDITOR_IMAGE_BACKEND = 'pillow'`, django-ckeditor also creates a thumbnail next to the original image:

```text
media/uploads/2021/09/06/picture-1_thumb.png
```

The saved HTML usually points to the original image:

```html
<img src="/media/uploads/2021/09/06/picture-1.png" alt="">
```

The `_thumb` file is mainly for the CKEditor image browser preview in the admin UI. If you manually type or paste an `<img>` tag in CKEditor's source/HTML mode, CKEditor saves that HTML, but it does not upload a file unless you use the upload feature.

## Export A New Clean Fixture

After editing book content in admin, create a new clean fixture:

```powershell
$env:PYTHONUTF8='1'
..\env\app_env\Scripts\python.exe manage.py dumpdata home book auth.user --indent 2 -o .\data.clean.json
```

`PYTHONUTF8=1` matters on Windows because some section content contains math symbols such as `⋯`.

And then push the new fixture to the GitHub repo. On PythonAnywhere, pull the latest code and load the updated fixture:

```bash
git pull
python manage.py migrate --settings=Book.settings.prod
python manage.py loaddata data.clean.json --settings=Book.settings.prod
```

Only delete `db.sqlite3` on PythonAnywhere if you intentionally want a full production database reset.

## PythonAnywhere Deployment Notes

Once you create a PythonAnywhere account, use this setup checklist.

1. Make sure the project is pushed to GitHub. This project currently uses:

```text
https://github.com/kgarmtz/PolilibroProject/tree/feature/2026
```

2. Open a new **Bash** console on PythonAnywhere.

3. Clone the repo and switch to the deployment branch:

```bash
git clone https://github.com/kgarmtz/PolilibroProject.git
cd PolilibroProject
git fetch --all
git checkout feature/2026
git pull
```

4. Create and activate a PythonAnywhere virtual environment:

```bash
mkvirtualenv app_env --python=/usr/bin/python3.13
```

After this, future Bash consoles can activate it with:

```bash
workon app_env
```

5. Install project dependencies:

```bash
pip install -r requirements.txt
```

6. In the PythonAnywhere dashboard, go to **Web** and select **Add a new web app**.

7. Use the custom domain:

```text
www.polilibrocalculo.com
```

8. Select **Manual configuration** and choose the same Python version used for the virtualenv.

9. In the Web tab **Virtualenv** section, use the full virtualenv path:

```text
/home/<your-pythonanywhere-username>/.virtualenvs/app_env
```

10. In the Web tab **Security** section, generate an auto-renewing Let's Encrypt certificate and enable **Force HTTPS**.

Important note: `media/` is ignored by git, so it must be uploaded separately. The easiest way is to upload a ZIP through the PythonAnywhere **Files** tab and unzip it in Bash:

```bash
unzip media.zip -d /home/<your-pythonanywhere-username>/PolilibroProject/
```

If your PythonAnywhere plan has SSH access, you can also upload media in bulk from your computer with `scp` or `rsync`.

This project includes a production settings file:

```text
Book/settings/prod.py
```

On PythonAnywhere, you can configure the web app to use the settings file for production

```text
DJANGO_SETTINGS_MODULE=Book.settings.prod
```

In the Code section, you can modify the wsgi.py file:

/var/www/www_polilibrocalculo_com_wsgi.py

```python
import os
import sys

path = '/home/kgarciam/PolilibroProject'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'Book.settings.prod'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Production environment values should look like `.env.example`:

```text
SECRET_KEY=replace-with-production-secret
DEBUG=False
ALLOWED_HOSTS=www.polilibrocalculo.com,polilibrocalculo.com
```

In production, create a server-only `.env` file in the project folder on PythonAnywhere. You can create or upload it through the **Files** tab. Do not place `.env` inside `static/`, `staticfiles/`, or `media/`.

Initial deployment flow:

```bash
workon app_env
python -m pip install -r requirements.txt
python manage.py migrate --settings=Book.settings.prod
python manage.py loaddata data.clean.json --settings=Book.settings.prod
python manage.py collectstatic --settings=Book.settings.prod --noinput
```

For routine code-only updates after the site already has a database, usually run:

```bash
workon app_env
git pull
python -m pip install -r requirements.txt
python manage.py migrate --settings=Book.settings.prod
python manage.py collectstatic --settings=Book.settings.prod --noinput
```

Only run `loaddata data.clean.json` again when you intentionally want to reload the fixture data.

Static files are collected into:

```text
staticfiles/
```

Uploaded media files live in:

```text
media/
```

Make sure PythonAnywhere is configured to serve:

```text
/static/ -> /home/<your-pythonanywhere-username>/PolilibroProject/staticfiles
/media/  -> /home/<your-pythonanywhere-username>/PolilibroProject/media
```

`staticfiles/` is generated using the `collectstatic` Django command.

Both `/static/` and `/media/` are set in the **Static files** section of the Web tab on PythonAnywhere.

For this small mostly-read-only project, SQLite is acceptable to start. If multiple people will edit content often, consider moving the production database to MySQL on PythonAnywhere.

## Health Checks

Run these after dependency or code changes:

```powershell
..\env\app_env\Scripts\python.exe manage.py check
..\env\app_env\Scripts\python.exe manage.py makemigrations --check --dry-run
..\env\app_env\Scripts\python.exe manage.py test
```

At the time of this update, there are no project tests yet, so `test` reports `0 tests`.

## Annual Maintenance Checklist

1. Update Django only within the 5.2 LTS line unless CKEditor has been migrated.
2. Refresh dependencies in the virtual environment.
3. Run `manage.py check`.
4. Run `makemigrations --check --dry-run`.
5. Start the server and verify the home page and `/polilibroescom/`.
6. If content changed, export a new `data.clean.json`.
7. Back up `data.clean.json` and the `media/` folder.
