from dataclasses import dataclass
import os
import asyncio
import random
import statistics

from faker import Faker
from pyinstrument import Profiler

from process_ml_batch import process_ml_batch

fake = Faker()


@dataclass
class NameFacts:
    name: str
    unknown: bool
    gender: str = "N/A"
    meaning: str = "N/A"
    popularity: int = 0
    age_stats: dict = None


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
    gender = await get_gender(name)
    meaning = await get_meaning(name)
    popularity = await get_popularity(name)
    process_ml_batch(name)
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
    return [random.randint(1, 100) for _ in range(10000)]


def get_age_stats(name):
    ages = get_ages(name)
    return {
        "mean": statistics.mean(ages),
        "median": statistics.median(ages),
        "most_common": statistics.mode(ages),
        "oldest": max(ages),
    }


async def main():
    profiler = Profiler()
    profiler.start()
    names = [await get_name_facts("Anis") for _ in range(50)]
    profiler.stop()
    print(profiler.output_text(unicode=True, color=True))
    return names


if __name__ == "__main__":
    asyncio.run(main())
