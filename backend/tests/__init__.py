'''
Before you dive into writing tests, you’ll want to first make a couple of decisions:
1 - What do you want to test?
2 - Are you writing a unit test or an integration test?

Then the structure of a test should loosely follow this workflow:
1 - Create your inputs
2 - Execute the code being tested, capturing the output
3 - Compare the output with an expected result


Best practices
1 - If it can break, it should be tested. This includes models, views, forms, templates, validators, and so forth.
2 - Each test should generally only test one function.
3 - Keep it simple. You do not want to have to write tests on top of other tests.
4 - Run tests whenever code is PULLed or PUSHed from the repo and in the staging environment before PUSHing to production.
5 - When upgrading to a newer version of Django:
    - upgrade locally,
    - run your test suite,
    - fix bugs,
    - PUSH to the repo and staging, and then
    - test again in staging before shipping the code.


When your project grows and you want to better organise your tests, you can put them into a separate directory. If you go down this route, make sure you do these four things:

- Name the directory tests
- Add a file called __init__.py into the tests folder and all of its sub-folders. The file can be empty, it just needs to exist.
- Begin each file name with test_ . This is so Django knows where to look for tests.
- Also, it’s important that all tests are prefixed with test_ . Django will ignore methods which don’t follow this convention.
- Remove the original tests.py from the app’s directory.


TO RUN PYTEST
commands:
pytest (execute all tests)
pytest --durations=5(execute all tests and display the 5 slowest tests in time)
pytest directory_name (execute all tests inside a folder)
pytest backend/tests/unit/test_views.py::test_true (execute a specific function)

USEFUL RESOURCES:
- fixtures (useful to provide data for tests)
- Skip decorator: @pytest.mark.skip(reason=None)
- Use os.environ.setdefault('PYTHONOPTIMIZE', '2') to run on production mode (this will ignore any assert and docstring that exists inside code)
'''