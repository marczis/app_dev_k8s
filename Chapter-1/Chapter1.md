# Chapter 1, Developing a simple REST service
In this chapter you will make a small python code to handle REST API requests, with the famous Flask python module.

## Setup your environment
 - If you don't have it yet, install pipenv tool.

### Create a new python environment
```bash
pipenv install
```

The output shall look something like this:

![alt](./.static/pipenv_create.png)

Enter into the new environment with:

```
pipenv shell

Launching subshell in virtual environment…
 . /home/marczis/.local/share/virtualenvs/python-gJL2SuBN/bin/activate
```

Note: The easiest way to confirm which environment you are "in" is to use: 
```
which python
/home/marczis/.local/share/virtualenvs/python-gJL2SuBN/bin/python
```

### Install python packages
Now we will install the python packages we need for our application

```bash
pipenv install flask
```

The output shall be something like this:

![](.static/pipenv_flask.png)

I like to have the "ipython" tool around, so add it as a development package - which means this won't be added to the release version. If you are not familiar with ipython this is a good time to check it out. It is an enhanced python shell - helps a lot to try out things on the fly.

```bash
pipenv install ipython -dev
```

Output:

![](.static/pipenv_ipython.png)

