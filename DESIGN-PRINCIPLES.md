# Design Principles

These are meant to guide development and approval of new code.

Note that these design principles are not followed consistently throughout any repository, for one of several reasons:
1. The principles were formulated, in whole or in part, after the development of the repository, and the repository should be gradually modified to meet them.
2. The files are organized in a way which is ultimately better than the design principles, and the design principles should be modified to account for that. 

## File Nomenclature

- Files containing only functions should be given a verb relating to their purpose(`write.py`, `convert.py`) 
- Files containing a class should either be named:
    - `core.py` , if the class is central to the logic of the directory (e.g. `pydantic_to_marshmallow/generator/core.py`)
    - A short, logical name, if the class is a helper class to other logic (e.g., `scheduled_tasks/manager.py`)
- Files should generally be at most two but preferably one word. If multiple words are used, that normally indicates they are diferentiating themselves from other similar files in the same directory, and they should be organized into a subdirectory that contains the shared component of their name (usually the suffix), with the files named solely on what differentiates them.
- `helper.py` files are permitted, but discouraged due to their vagueness. 

## Class Nomenclature

- Non-model classes should be given an agent noun (`writer.py`)
- Model classes should either be in a `models`, `containers`, `dtos`, or other folder that clearly indicates its purpose, or in a standalone file that does the same (e.g., `dto.py`)

## File Composition

- Files should generally contain only one *kind* of thing, whether that is constants files (`constants.py`), enums (`enums.py`), and so on. 
- Classes should exist as separate files from any other logic. Only in rare situations (such as unavoidable coupling) should two or more classes exist in the same file.

## Static Methods

- Static methods might be less preferable to functions. A method, even a static one, implies relation between other elements in the class, whereas a function does not, and hence can be simpler to think about. 
- Instead of having a static method, a helper file containing relevant functions should be present in the same directory as the class.

## File Organization

- Files should be organized *by higher order function* and *recursively*
    - *By higher order function* in that files which support particular concepts should congregate in the same region (e.g., all files supporting a specific endpoint should be in the same directory as that endpoint). This is meant to make it easier to find files relevant to a specific domain.
        - By contrast, files should *not* be primarily organized simply according to the kind of file they are. Single-type directories should not have more than zero or one levels of subdirectories.
            - To give an example: The DS directory currently has a `middleware/schema-and-dto` directory, with many subdirectories depending on the endpoints involved. Instead of this, each endpoint should have a `schemas` and `dtos` directory, which relevant files should be placed in, and no lower.
        - Files should be located as close as possible to other files which use them
    - *Recursively* in that different directories should follow the same pattern -- the same nomenclature for particular files (e.g. `middleware.py`, `schema.py`, and so on). 
- The proper organization for subdirectories relative to other files is that the files within the subdirectory should either:
    - Provide logic for files within the supporting directory
    - Express a variation of the logic of the supporting directory
- Where a file is used across multiple conceptual domains, a `shared` directory should be made which includes those components shared between them, and located as close to those domains as possible.

## Specific File Types/Names

- `constants.py`: Denotes all constants used for the domain
- `mappings`: Denotes dictionary mappings (and occasionally any helper functions) used for that domain.
- `enums.py` : Denotes all enums used for the domain
- `types_.py`: Denotes specific types used for the domain. Denoted with an underscore to avoid conflict with vanilla python files.
- `exceptions.py`: Denotes custom exceptions for the domain.
- `mixins.py`: Denotes mixin classes for the domain.
- `base.py`: Denotes a base class used for the domain.

## Specific Directory Names/Types

- `models`: Outside of `db`, denotes containers or Pydantic Models used by the domain. Inside `db`, denotes SQLAlchemy models
- `helpers` or `_helpers`: Denotes helper files
- `implementations`: Where multiple sub-variants of a domain are implemented, they should be contained within an `implementations` directory where they can be further subdivided.
- `templates`: Denote templates or patterns used by other components in the domain.
- `src` : Denotes all programmatic logic for the repository and is accessible from root.
- `tests` : Denotes all tests for the repository and is accessible from root.
- `alembic` : Denotes all alembic versions and helper logic and is accessible from root


## The `db` directory

- The `db` directory should be accessible from the root of the `src` directory (not the root of the whole repository)
- It should contain logic specific to interfacing with the database, including:
    - SQLAlchemy models (in a `models` directory)
    - Connection configuration
    - Helper logic for low-level database interactions.
- It should contain a `client` directory, which must contain a `DatabaseClient` class which all queries against the database (read or write) must utilize. 
    - The `DatabaseClient` class should be either contained within a file named `core.py`, or `sync_.py` and `async_.py`, if two clients exists for synchronous and asynchronous logic, respectively.


## Test Organization

- Tests should be located in a separate root-level `tests` directory 
    - This is to ensure they 
        - Are easily accessible
        - Do not get picked up by packaging logic
        - Integrate well with pytest `conftest.py` files
- Where possible, the organization of tests should imitate the organization of the files they're testing. i.e., `a/b` should have tests also arranged in an `a/b` directory structure
- There should be *one file per test.*
- Tests should be organized such that the directory name indicates either the higher-level concept the tests are for, e.g. `data-requests/`, or the function the tests are for, e.g. `data-requests/get/`.
- Test file names should indicate what scenario the logic is being tested under, e.g. `test_happy_path.py`, `test_unauthorized.py`
- Fixtures in a `conftest.py` should be positioned at the lowest level possible to still be used by all relevant tests.
- Constants, helper files, and other supporting logic should be located in files (like `constants.py`) or subdirectories (like `helpers/`) that are in the same directory as the logic being tested.

## What should be tested?

- Logic which *absolutely* should be tested is logic which:
    - The user interacts with (such as endpoints)
    - Has a high number of moving parts that are likely to change
    - Interacts with third party APIs
    - Impacts the database
    - Just *looks* like something that could break easily
- Candidates where testing is less important
    - Logging logic
    - Minor logic that is rarely modified 
    - Middleware functionality that is decently complex but already tested with reasonable thoroughness in integration tests (e.g., passthrough functions)
- Candidates where testing often can (and sometimes should) be avoided:
    - Functions where the logic is likely to be used in other functions that will comprehensively test the logic in their workflow anyway 
    - Testing expensive and convoluted third party logic directly.  
        - For example, GitHub OAuth often requires a GitHub account, a browser, and multiple request redirects, and hence is quite cumbersome to set up testing infrastructure for. It is better to test the logic *up to the point that requests are sent or received from GitHub,* leveraging mocks where possible, than to test that GitHub's logic itself performs as expected -- we should expect that it does.  


## READMEs

- A directory-level README (as distinguished from a root-level README) should only be as verbose as is necessary to summarize the contents of the directory. Summaries of subdirectories and their contents should be contained in separate READMEs within those subdirectories. 
    - This is partly to reduce the risk of documentation going out of date, due to a README describing too much of a directory which has had its subordinate contents changed over time.
- Directory-level READMEs are most important for directories which convey unique, domain-specific information (e.g., `db`) and are less important (or not necessary at all) for generic directories whose purpose is repeated throughout the repository and where the name alone often describes the purpose (e.g., `dtos`, `schemas`) 

## Required Root Directory Files

- `pyproject.toml`
- `uv.lock`
- `README.md`
- `.gitignore`

## Common (but not required) Root Directory Files

- `ENV.md`: Provides a description of environment variables used by the application
- `Dockerfile`: Used for spinning up a local version of the application.

## Nested logic

- Functions should contain only one or at most two levels of nesting (e.g., for loops, if conditionals, secondary functions or classes as in constructors).
- If more than this exist, then one of several things should be done:
    - The logic should be extracted to a separate function or class
    - In the case of some if conditionals, exit early using guard clauses 

## Type Hinting

- Type hints are necessary for all but the most trivial of functions (and often recommended even then).

## Inheritance

- Where classes inherit from other classes, there should generally only be one level of inheritence (i.e. not a class inheriting from a class inheriting from a class inheriting from a class). Two may be merited, but should be used with caution. Every extra level of inheritance reduces the comprehensibility of the overall logic. 
- Inheritance is most appropriate when designating an abstract base class which mandates the presence of certain functions or properties. 
- Where inheritance goes beyond that, it should be replaced with dependency injection or some other reworking of the class logic. 

## Redundant Logic and Generalization

- Generally speaking, redundancy should be avoided in code. Code is more often unnecessarily duplicated than it is unnecessarily generalized.
- That being said, redundancy is acceptable if generalization adds too much complexity. Where the line should be drawn is an art and not a science, but good candidates for redundant logic is where:
    - Generalization requires an excessive level of abstraction or function/class jumping
    - Generalization requires passing functions as arguments to other functions (which tends to be harder to parse at a glance)
    - The "redundant" entities share logic now but have potential to be developed separately in the future (i.e., two endpoints which have overlapping output or input formats), and generalization would likely hamper that in the future.
    - Generalization requires a one-off if-conditional that is used only once by one variant of the function.
        - Even this situation aside, using if-conditionals to aid in generalization should be approached with caution.
    - There is only one duplicate, and the duplicate is relatively simple (i.e., one or two lines).

## Docstrings

- Docstrings are often useful, but sometimes add clutter that can be avoided with good design of other components.
- Before adding docstring, consider if the amount of docstring can be reduced (or eliminated) by
    - Making the function, class name, or argument names informative
    - Adding type hints
- Add docstrings where the logic is unavoidably complex in a manner that cannot be inferred from declaration nomenclature and type hints alone. Candidates for this include:
    - If the code has considerable side effects or calls other logic which may include considerable side effects
    - If the function is a decorator or other logic that is unavoidably unintuitive or unclear.

#### Example

Here is an example where a docstring is useful.:

```python
    def validate_and_add_user(self, validation_token: str) -> str:
        """Validate pending user, add as full user, and return user email."""
```

In this case, the type hint does not convey what is being returned, and changing the function name `validate_and_add_user_and_return_email` is awkward. A docstring is helpful here.  

# Comments

- In many cases, a descriptive comment for a section of logic can (and often should) be replaced by extracting that logic to a function (or functions) and giving the function(s) a name similar to what the comment stated. 

## Decorators

- Decorators are powerful but often confusing elements of python, and should be used with caution.
- Docstrings are especially necessary with decorators, as type hints and function names are often insufficient to convey behavior.

## Dictionaries

- Dictionaries should only be used for those purposes where a dictionary is necessary (for example, where rapid lookups of a variable number of values is needed), and not as a tool of convenience for storing data.
    - To that end, dictionaries should not be used for the transfer of named key-value pairs between scopes, where its composition is harder to see. Where this is done, a data model class should be used in its place. 

## Wide vs. Tall Code

- When in doubt, code should be tall versus wide. It is easier to scroll up or down than it is to scroll left or right or adjust a view window.
- One or at most two elements of logic should be on a single line (i.e., instead of `a += b + c` do `a += b` and `a += c` on separate lines).
- If there are more than two parameters in a function definition or class inheritance, they should be on separate lines. Ideally, each has its own line.

## Preferred Modules

- `pydantic` to data model storage
- `FastAPI` for API development
- `environs` for Environment variable management
- `sqlalchemy` for ORM logic
- `alembic` for supporting database migrations using `sqlalchemy` logic
- `polars` (not `pandas`) for DataFrame management
    - Polars is faster and offers more clear design than `pandas`
- `pytest` for testing
- `ruff` for linting
- `basedpyright` for static type checking
    - `basedpyright` is `pyright` with several enhancements, and is commonly used.
- `uv` for package management

# Database 

- Generally speaking, use of list columns are discouraged. These are considerably more difficult to search on than a linked-list format, and can introduce unexpected bugs owing to their non-scalar format. 
    - If a column accepts a list entry, it should not allow null values. To represent a lack of values or an empty default, an empty list can be used. This is to avoid confusion and potential bugs from having two different ways of representing "nothing". 

## Triggers

- Triggers should generally be avoided in favor of application code.
    - This is because triggers are more difficult to see and validate with tests or debug.
- Where triggers cannot be avoid, document more aggressively.

## Table Nomenclature

- Tables should be in plural form, except in the case of 
    - Link tables, whose nomenclature is described below.
    - Tables which have a primary dependence on another table, whose nomenclature is described below.
- Tables should be created in `snake_case` form
- Tables which have a primary dependence on one other table should have that table (singular) as a prefix. 
    - For example, if `breed` is an attribute dependent solely on `dogs`, the table should be named `dog_breeds` 

## Common Table Columns

The following columns should be present in all tables unless there is a compelling reason not to have them:

- `id`
- `created_at`
- `updated_at`

## Link Tables

- Link tables should have an `id` column that is separate from the foreign keys.
    - Often, this column is not used, but consistency is preferred over eliminating redundancy. 
- Link tables should have a `link_` prefix, and the table names should be singular or plural depending on the relationship. e.g.:
    - one-to-one: `link_apple_orange`
    - one-to-many: `link_apple_oranges`
    - many-to-many: `link_apples_oranges`
- Link tables should have unique constraints reflective of the particular relationship:
    - one-to-one: separate unique constraints on each foreign key column
    - one-to-many: unique constraint on the `one` column
    - many-to-many: single unique constraint encompassing *both* columns

# SQLAlchemy

- 

