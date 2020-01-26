import cython_fast_api
import asyncio
from pyinstrument import Profiler

if __name__ == "__main__":
    profiler = Profiler()
    profiler.start()
    asyncio.run(cython_fast_api.main())
    profiler.stop()
    print(profiler.output_text(unicode=True, color=True))
