import modal
import subprocess
import shlex
app = modal.App("test-unav")

image = (modal.Image.debian_slim(python_version="3.8")
    .run_commands(
        "apt-get update",
        "apt-get install -y pkg-config libhdf5-dev gcc libgl1-mesa-glx libglib2.0-0",
        "pip install --upgrade pip",
    )
    .pip_install_from_requirements("requirements.txt"))



@app.function(
    image=image,
)
def main():
    subprocess.run(
        ["cd","src"],
        ["python", "server.py"],
       
    )
    
@app.local_entrypoint()
def run():
    main.remote()
    
    import shlex
import subprocess
from pathlib import Path

import modal

# ## Define container dependencies
#
# The `app.py` script imports three third-party packages, so we include these in the example's
# image definition.

image = modal.Image.debian_slim(python_version="3.11").pip_install(
    "streamlit~=1.35.0", "numpy~=1.26.4", "pandas~=2.2.2"
)

app = modal.App(name="example-modal-streamlit", image=image)

# ## Mounting the `app.py` script
#
# We can just mount the `app.py` script inside the container at a pre-defined path using a Modal
# [`Mount`](https://modal.com/docs/guide/local-data#mounting-directories).

streamlit_script_local_path = Path(__file__).parent / "app.py"
streamlit_script_remote_path = Path("/root/app.py")

if not streamlit_script_local_path.exists():
    raise RuntimeError(
        "app.py not found! Place the script with your streamlit app in the same directory."
    )

streamlit_script_mount = modal.Mount.from_local_file(
    streamlit_script_local_path,
    streamlit_script_remote_path,
)

# ## Spawning the Streamlit server
#
# Inside the container, we will run the Streamlit server in a background subprocess using
# `subprocess.Popen`. We also expose port 8000 using the `@web_server` decorator.


@app.function(
    allow_concurrent_inputs=100,
    mounts=[streamlit_script_mount],
)
@modal.web_server(8000)
def run():
    target = shlex.quote(str(streamlit_script_remote_path))
    cmd = f"streamlit run {target} --server.port 8000 --server.enableCORS=false --server.enableXsrfProtection=false"
    subprocess.Popen(cmd, shell=True)