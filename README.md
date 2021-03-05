# Language Analytics - Spring 2021

This repository contains all of the assignments and code-along sessions of the Language Analytics course.

## Running my scripts

For running my scripts I'd recommend doing the following from your terminal (and remembering to use the new environment that it creates):

__MAC/LINUX/WORKER02__
```bash
git clone https://github.com/CDS-AU-DK/cds-language.git
cd cds-language
bash ./create_lang_venv.sh
```
__WINDOWS:__
```bash
git clone https://github.com/CDS-AU-DK/cds-language.git
cd cds-language
bash ./create_lang_venv_win.sh
```

## Repo structure and files

This repository has the following directory structure:

| Column | Description|
|--------|:-----------|
```data```| Contains the data used in both the scripts and the notebooks
```notebooks``` | Contains the notebooks (code along sessions)
```src``` | Contains the assignments
```utils``` | Utility functions written by [Ross](https://pure.au.dk/portal/en/persons/ross-deans-kristensenmclachlan(29ad140e-0785-4e07-bdc1-8af12f15856c).html) which are utilised in some of the scripts

Furthermore it contains the files:
- ```./create_lang_venv.sh``` -> A bash script which automatically generates a new virtual environment, and install all the packages contained within ```requirements.txt```
- ```requirements.txt``` -> A list of packages along with the versions that are certain to work
- ```README.md``` -> This very readme file

## Contact

Feel free to write me, Emil Jessen for any questions (also regarding the reviews). 
You can do so on [Slack](https://app.slack.com/client/T01908QBS9X/D01A1LFRDE0) or on [Facebook](https://www.facebook.com/emil.t.jessen/).
