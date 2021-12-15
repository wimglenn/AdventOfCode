from setuptools import setup

setup(
    name="aoc-jpaulson",
    version="0.1",
    url="https://github.com/jonathanpaulson/AdventOfCode",
    py_modules=["aoc_jpaulson"],
    entry_points={"adventofcode.user": ["jpaulson = aoc_jpaulson:plugin"]},
)
