"""Probably a better way to do this but...

I wanted a way to loop through the different python versions w/ pytest.
I also didn't care to set up envs.
Loops through the different python versions
and runs subprocess for each pytest.
Outputs data to `results` folder.
"""

import subprocess
import sys
import os
import tomllib
from datetime import datetime

with open("pyproject.toml", "rb") as f:
    pyproject = tomllib.load(f)

depend = " ".join(pyproject["project"]["dependencies"]) + " pytest"
format_depend = " ".join(pyproject["tool"]["curtis_janky_solution"]["dependencies"])

now = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
base_path = f"results\\{now}\\"
os.makedirs(base_path, exist_ok=True)


versions = [
    "python3.12",
    "python3.11",
    "python3.10",
    "python3.9",
    "python3.8",
]


def run_through_pytest(python_version: str):
    """Test pipeline for specific python versions.

    Resets python environment
    and installs what is needed from the `pyproject.toml` file.
    If on python3.12 runs formatting checks.
    Runs pytest regardless.
    Outputs results into terminal and
    writes to log files in results directory.
    """
    file = open(f"{base_path}{python_version.replace('.', '_')}.log", "wb")

    packages = (
        depend + " " + format_depend if python_version == "python3.12" else depend
    )

    cmd_setup = [
        f"{python_version} -m pip freeze > requirements.txt",
        f"{python_version} -m pip uninstall -r requirements.txt -y",
        f"{python_version} -m pip install {packages} --trusted-host files.pythonhosted.org",
    ]

    cmd_format = [f"{python_version} -m black .", f"{python_version} -m flake8"]

    cmd_test = [f"{python_version} -m pytest"]

    cmds = (
        cmd_setup + cmd_format + cmd_test
        if python_version == "python3.12"
        else cmd_setup + cmd_test
    )

    for cmd in cmds:
        run = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
        )

        for line in iter(run.stdout.readline, ""):
            if run.poll() is None:
                sys.stdout.write(line.decode("utf-8"))
                file.write(line)
            else:
                break

    try:
        os.remove("requirements.txt")
    except FileNotFoundError:
        print("Unable to remove requirements file...")

    file.close()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in versions:
        run_through_pytest(sys.argv[1])
    else:
        for version in versions:
            run_through_pytest(version)
