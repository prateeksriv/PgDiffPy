# PgDiffPy

[![Build Status](https://travis-ci.org/Dancer3809/PgDiffPy.png)](https://travis-ci.org/Dancer3809/PgDiffPy)

## Purpose

PgDiffPy is a command-line tool for comparing two PostgreSQL database schema dumps and generating a SQL script to update the old schema to match the new one. It is based on the original apgdiff tool but rewritten in Python.

This tool is useful for database administrators and developers who need to manage and version-control their database schemas. It simplifies the process of deploying schema changes from a development environment to a production environment.

## Installation

You can install PgDiffPy directly from the source repository using `pip`. It is recommended to do this within a Python virtual environment to avoid conflicts with system-wide packages.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Dancer3809/PgDiffPy.git
    cd PgDiffPy
    ```

2.  **Install the package:**
    ```bash
    pip install .
    ```

This will install the `pgdiff` command-line tool and its dependencies. If you are using a virtual environment, the command will be available directly in your shell.

### Alternative: Installing for the Current User

If you prefer not to use a virtual environment, you can install the package for your user account:

```bash
pip install --user .
```

This installs the package in your user's local directory (e.g., `~/.local`). To run the `pgdiff` command directly, you may need to add the local bin directory (e.g., `~/.local/bin`) to your shell's `PATH`.

## Usage

Once installed, you can use the `pgdiff` command-line tool to compare two database dumps:

```bash
pgdiff [options] <old_dump.sql> <new_dump.sql>
```

### Arguments

*   `old_dump.sql`: The path to the SQL file containing the old database schema.
*   `new_dump.sql`: The path to the SQL file containing the new database schema.

### Options

*   `--add-transaction`: Adds `START TRANSACTION` and `COMMIT TRANSACTION` to the generated diff file.
*   `--add-defaults`: Adds `DEFAULT ...` in case a new column has a `NOT NULL` constraint but no default value.
*   `--ignore-start-with`: Ignores `START WITH` modifications on `SEQUENCE`s.
*   `--ignore-function-whitespace`: Ignores multiple spaces and new lines when comparing function content.

### Example

```bash
pgdiff original_schema.sql new_schema.sql > migration_script.sql
```

This will generate a `migration_script.sql` file that you can run on the original database to apply the schema changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
