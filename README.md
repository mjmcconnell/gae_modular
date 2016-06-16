# GAE Modular app

## Introduction
***

The purpose of this app, is to test out an approach of creating an app, where each section is modularised
much like the standard approach that the Django framework adopts.
The idea being, that each module is isolated, and interactions between modules, should be limited (with
the except of the core module).

The standard modules with be setup with the following structure:

    app/
        module/
            __init__.py
            modal.py
            form.py
            templates.py
            apis.py
            tests/

All interactions between modules should be exposed via functions in the `__init__.py` file, so that there
is a signle point of exposure.


Where possible, all module classes should extend from their assoicated base class, located in the `core` module.
These core classes provide basic functionality and helper methods, but their main purpose is to ensure a
struture to each module, enforcing similarity between the modules, and their functionality.
