# Run the tests associated with the API 
#
 
## Activate the test environment 
. ../.venv/bin/activate

## change the python path so the sources can be imported properly
export PYTHONPATH="../src"

## Perform all the tests
## the -s flag allows to perform print() in the tests... because when this flag is not indicated it doesn't work..
pytest -s 

## Deactivate the virtual environment
deactivate
