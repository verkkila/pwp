# Meetings notes

## Meeting 1.
* **DATE:** 15.02.2019
* **ASSISTANTS:** Mika Oja
* **GRADE:** *To be filled by course staff*

### Minutes
The text explaining our main concepts and relations was rather dense and lacked a diagram. Our API use cases were mostly listing human interfaces. We should focus more on machine clients to make things easier for the future.

### Action points
* Make diagram for concepts
* Create API uses cases that are more related to machine clients rather than human interfaces


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Meeting 2.
* **DATE:** 28.02.2019
* **ASSISTANTS:** Ivan Sanchez
* **GRADE:** *To be filled by course staff*

### Minutes
The readme file in this repository should contain instructions for setting up and running the program.
As well as containing all the prerequisite libraries and dependencies.
We should examine whether to have a one-to-many or many-to-many relationship between events/items and routines.
Documentation should explain the difference between events and items and in general should explain the different
models in the database.
RoutineItem and RoutineEvent could be removed from models and replaced by a simple table.
Foreign key tests should be implemented.

### Action points
* Documentation
  1. For the program
  2. For the models in the database

* Re-examine the database models
* Foreign key tests


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Meeting 3.
* **DATE:** 29.03.2019
* **ASSISTANTS:** Ivan Sanchez
* **GRADE:** *To be filled by course staff*

### Minutes
We have too many resources (10), so we will remove RepeatSchedules and RepeatSchedule to simplify.
Entry relation (all-schedules) should be marked into the diagram.
Allow moving between events, items and tasks instead of having to move through schedules.
Update the REST conformance section to include examples of each case.
Resource state diagram should be updated to include all the link relations and the previously mentioned relations between events, items and tasks. In addition, names should be double-checked to match the documentation.
Apiary document is lacking profiles which should be added and contain the documentation of each data member. Profiles should be included in HTTP responses too.
Error responses should include error messages.
Add namespaces to link relations.
*Summary of what was discussed during the meeting*

### Action points
* Update documentation
	- Add and update relations
	- Profiles
	- Error responses
	- Namespaces

### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Meeting 4.
* **DATE:** 25.04.2019
* **ASSISTANTS:** Mika Oja
* **GRADE:** *To be filled by course staff*

### Minutes
The readme file is still missing content. Using PUT instead of PATCH should be considered with items/events/tasks (PATCH is loosely documented, client likely autofills missing fields with PUT).
Using url_for instead of regexp allows for more features.
Schedules must have names.
Deleting can be done straight from the query, put cascades correctly on foreign keys.
Document tests, especially put, patch and post.
Add coverage


### Action points
-Readme
-DB foreign keys
-Test documentation & coverage
*List here the actions points discussed with assistants*


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Midterm meeting
* **DATE:**
* **ASSISTANTS:**
* **GRADE:** *To be filled by course staff*

### Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*


## Final meeting
* **DATE:** 16.05.2019
* **ASSISTANTS:** Ivan Sanchez
* **GRADE:** *To be filled by course staff*

### Minutes
Test coverage for the project was low (65%). Some of the client features didn't work, specifically adding events, items and tasks to schedules.

### Action points
To improve grade:
-Increase test coverage
-Fix broken functionality


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

