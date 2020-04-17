import asyncio 
import pathlib as pl
import logging
import time 
import tempfile



async def writeFile( header_name: str, wdir: pl.Path ):
    content = f'''#include "{header_name}"

int main(){{

    return 0;
}}
'''

    fname = pl.Path( "main_" + header_name.replace(".h", ".cxx") )
    main_path = wdir / fname
    with main_path.open("w") as fid:
        fid.write( content )
    
    return str(fname)

async def compile(c_opt: dict, file: str, wdir:pl.Path):
    cmd = f"{c_opt['CXX']} {c_opt['CXXFLAGS']} {c_opt['LDFLAGS']} -c {file}"
    proc = await asyncio.create_subprocess_shell( cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, cwd=str(wdir) )
    _, err = await proc.communicate()
    logging.debug(err.decode())
    if proc.returncode != 0:
        return False
    else:
        return True 


async def test_header( queue: asyncio.Queue, results: asyncio.Queue, c_opt: dict, wdir: pl.Path):
    while True:
        header = await queue.get()
        fname  = await writeFile(header, wdir)
        status = await compile(c_opt, fname, wdir)
    
        queue.task_done()
        if status: 
            logging.info(f"{header} test compilation succeed")
        else:
            logging.error(f"{header} test compilation failed")
            results.put_nowait( header )


async def test_self_contained_header(compiler_opt: dict, header_regex: str, header_dir: str, n_worker: int):
    started_at = time.monotonic()
    include_path = pl.Path(header_dir)
    ## Create temporary directory 
    #tmp_dir = tempfile.TemporaryDirectory(suffix="sanitizer")
    tmp_dir = "/tmp/test"
    # Create a queue that we will use to store our "workload".
    queue = asyncio.Queue()
    ## List all header file to test .
    for x in include_path.glob(header_regex):
        queue.put_nowait( str(x.relative_to(include_path)) )

    n_header = queue.qsize()
    results = asyncio.Queue()
    # Create three worker tasks to process the queue concurrently.
    tasks = []
    for _ in range(n_worker):
        task = asyncio.create_task(test_header(queue, results, compiler_opt, tmp_dir))
        tasks.append(task)
        
    # Wait until the queue is fully processed.
    await queue.join()
    # Cancel our worker tasks.
    for task in tasks:
        task.cancel()

    time_execution = time.monotonic() - started_at


    logging.info("====== RESULTS =====")
    logging.info(f"Execution time : {time_execution}")
    logging.info(f"Number of tested header : {n_header}")
    logging.info(f"   * {n_header - results.qsize()} succeed")
    logging.info(f"   * {results.qsize()} failed")