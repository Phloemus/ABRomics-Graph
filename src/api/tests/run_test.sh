# Run the tests associated with the API 
#
 
## Activate the test environment 
. ../.venv/bin/activate

## change the python path so the sources can be imported properly
export PYTHONPATH="../src"

## Perform all the tests
python -m unittest discover -v

## Deactivate the virtual environment
deactivate
