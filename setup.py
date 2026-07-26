"""Setuptools wheel-tag hook for the bundled Windows .NET runtime."""

from setuptools import setup
from setuptools.command.bdist_wheel import bdist_wheel


class WindowsWheel(bdist_wheel):
    """Mark the universal Python code as dependent on Windows runtime files."""

    def finalize_options(self) -> None:
        super().finalize_options()
        self.root_is_pure = False

    def get_tag(self) -> tuple[str, str, str]:
        return "py3", "none", "win_amd64"


setup(cmdclass={"bdist_wheel": WindowsWheel})
