from dataclasses import dataclass
import os
import asyncio
from functools import lru_cache


from faker import Faker
from pyinstrument import Profiler
from redis import Redis
from rq import Queue
import numpy

from process_ml_batch import process_ml_batch

fake = Faker()

q = Queue(connection=Redis())

@dataclass
class NameFacts:
    name: str
    unknown: bool
    gender: str = "N/A"
    meaning: str = "N/A"
    popularity: int = 0
    age_stats: dict = None


@lru_cache(maxsize=None)
def get_known_names() -> [str]:
    path = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__), "first_names.all.txt")
    )
    with open(path, encoding="utf-8") as f:
        return [l.strip() for l in f.readlines()]


# noinspection PyUnusedLocal
async def get_gender(name):
    await asyncio.sleep(0.01)
    return "boy"


# noinspection PyUnusedLocal
async def get_meaning(name):
    await asyncio.sleep(0.01)
    return fake.paragraph(nb_sentences=3, variable_nb_sentences=True)


# noinspection PyUnusedLocal
async def get_popularity(name):
    await asyncio.sleep(0.01)
    return 100


async def get_name_facts(name):
    name = name.lower()
    known_names = get_known_names()
    if name not in known_names:
        return NameFacts(name=name, unknown=True)
    gender, meaning, popularity = await asyncio.gather(
        get_gender(name),
        get_meaning(name),
        get_popularity(name),
    )
    q.enqueue(process_ml_batch, name)
    return NameFacts(
        name=name,
        unknown=False,
        gender=gender,
        meaning=meaning,
        popularity=popularity,
        age_stats=get_age_stats(name),
    )


# noinspection PyUnusedLocal
def get_ages(name):
    return numpy.random.randint(100, size=100)


def get_age_stats(name):
    ages = numpy.array(get_ages(name))
    return {
        "mean": numpy.mean(ages),
        "median": numpy.median(ages),
        "most_common": numpy.bincount(ages).argmax(),
        "oldest": numpy.max(ages),
    }


async def main():
    names = [await get_name_facts("Anis") for _ in range(50)]
    print(names)
