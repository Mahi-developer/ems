# EMS
_EMS is an Event Management System, which allows organizers to post and manage events and also allows customers to register for specific events_

## Installation Steps
_Follow the below instructions to setup the ems application in your local_

### Prerequisites
#### Docker / Docker Compose Installation
* Install docker desktop / docker based on your system OS and architecture.
  * Docker Desktop Installation (Windows) - https://docs.docker.com/desktop/setup/install/windows-install/
  * Docker Installation (choose your platform) - https://docs.docker.com/engine/install/
  * Docker Compose Installation - https://docs.docker.com/compose/install/

#### Setup WSL (only for windows)
* Setup wsl2 version in your Windows machine, by following the steps mentioned.
  * wsl2 Installation & Setup - https://learn.microsoft.com/en-us/windows/wsl/install

#### Install Postman
* Install Postman to trigger and verify ems APIs.
  * Download postman here - https://www.postman.com/downloads/

#### Git Installation
* Install GIT in your local, if required or download the source code from GIT
  * Download GIT - https://git-scm.com/downloads

#### Clone Project
* Ignore this step if you are downloading source code directly from GIT.
* Repo link - https://github.com/Mahi-developer/ems#
```bash
git clone https://github.com/Mahi-developer/ems.git
cd ems
# make sure branch is in master and up to date
git checkout master
git pull origin master
```

#### Launch EMS
* Ensue docker & compose is up and running.
```bash
docker ps -a
docker-compose -f docker-compose.yml ps -a
```
* Build EMS application
```bash
docker-compose -f docker-compose.yml build --no-cache
```
* Start the postgres & app containers and verify its up and running
```bash
docker-compose -f docker-compose.yml up -d
# check application status
docker-compose -f docker-compose.yml ps -a 
```

#### Create EMS User and DB.
* Login to postgresql, Refer user, password and host in env
```bash
docker-compose -f docker-compose.yml exec db bash
psql -U <username> -h <host_name> -d <db_name>
# default as per current env
psql -U ems_user -h db -d ems 
```
* Create user & db, if not created already by running queries from database.sql
* exit the bash with (exit) command

#### Apply initial migrations
* apply initial migrations with the following alembic command
```bash
docker-compose -f docker-compose.yml exec app bash
# migration command
alembic upgrade head
```

#### Test application with the postman collection included.
* Included the postman collection (ems.postman_collection.json).
* Import the collection in the postman app and try to create events and register attendees.

#### EMS routes (localhost).
* Ping - http://localhost:8000/events/ping/
* Create / fetch Events - http://localhost:8000/events/
* Register Attendee - http://localhost:8000/events/{event_id}/register/
* View Attendees of an event - http://localhost:8000/events/{event_id}/attendees/

#### Detailed API Specs (Swagger Docs)
* Look out the detailed API specs in the swagger documentation
  * Swagger UI - http://localhost:8000/docs

#### To generate migration file.
* Any changes in db structure, generate migration files with alembic
  (not required as initial migrations are already done)
* Follow upgrade command mentioned above to reflect the changes in db
```bash
docker-compose -f docker-compose.yml exec app bash alembic revision --autogenerate -m "<custom message>"
```
------
### Hooray! You've Made it 😅