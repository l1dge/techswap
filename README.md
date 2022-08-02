<!--
@TODO Update the Readme with a full description of how the project works 
-->

# techswap
Repo for the techswap project
## New features
Added Django-truncate to clean the db before running dbload
- python manage.py truncate --apps auth swapshop (WARNING this will blat your database)

Added dbload command
- python manage.py dbload -h (Still needs work on error checking)