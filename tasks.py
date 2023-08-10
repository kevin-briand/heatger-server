from invoke import task


@task
def run(c):
    c.run("python app.py")


@task
def tests(c):
    c.run("pytest")


@task
def coverage(c):
    c.run("coverage run -m pytest")
    c.run("coverage html")


@task
def lint(c):
    c.run("pylint src/ || pylint-exit $?")
