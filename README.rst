MCBrowse 0.1.0-dev.1 - Metacells Browsing
=========================================

.. image:: https://readthedocs.org/projects/mcbrowse?version=latest
    :target: https://mcbrowse.readthedocs.io/en/latest/
    :alt: Documentation Status

Context
-------

The ``mcbrowse`` package provides utilities for browsing the content of metacells data stored in a `daf
<https://pypi.org/project/daf>`_ repository, typically created by using the `metacells
<https://pypi.org/project/metacells>`_ package.

These utilities are meant to be used in two main ways:

* Directly using `plotly <https://pypi.org/project/plotly>`_, either inside `jupyter notebooks <https://jupyter.org>`_,
  inside `dash applications <https://dash.plotly.com>`_, or in standalone HTML files; or

* From inside an `R <https://www.r-project.org>`_ environment, using `reticulate
  <https://cran.r-project.org/package=reticulate>`_ and (**TODO**) the matching `mcbrowser
  <https://cran.r-project.org/package=mcbrowser>`_ packages (note the ``r`` at the end).

The utilities provided here allow generating figures in distinct steps: (1) extracting the `tidy data
<https://en.wikipedia.org/wiki/Tidy_data>`_ data needed for a specific figure from the overall metacells ``daf``
repository, (2) specifying parameters to control the figure appearance in a veneer object and (3) generating a
``plotly`` figure. The matching R package provides utilities that take the same data and veneer objects (accessed via
``reticulate``) and produce a `ggplot <https://cran.r-project.org/package=ggplot2>`_ figure.

One can use this in a pure script form, manually specifying all the parameters, or one can use the provided jupyter
notebook `ipywidgets <https://github.com/jupyter-widgets/ipywidgets>`_ to use a friendly UI to control the parameters.

See the `documentation <https://mcbrowse.readthedocs.io/en/latest/?badge=latest>`_ for the full API details.

Usage
-----

Simple usage in Python:

.. code-block:: python

    import daf
    import mcbrowse

    # Open some metacells data repository.
    data = daf.DafReader(...)

    # Extract the data for a gene-gene figure.
    figure_data = mcbrowse.GeneGeneData(...)

    # Control what the figure will look like.
    figure_veneer = mcbrowse.GeneGeneVeneer(...)

    # Obtain a plotly figure.
    figure = GeneGeneFigure(figure_data, figure_veneer)

    figure.show()

And equivalent usage in R:

.. code-block:: R

    require(reticulate)
    require(mcbrowser)
    require(ggplot2)

    daf <- reticulate::import("daf")
    mcbrowse <- reticulate$import("mcbrowse")

    # Open some metacells data repository.
    data <- daf$DafReader(...)

    # Extract the data for a gene-gene figure.
    figure_data <- mcbrowse$GeneGeneFilter(...).collect()

    # Control what the figure will look like.
    figure_veneer <- mcbrowse$GeneGeneVeneer(...)

    # Obtain a ggplot figure.
    figure = figure_veneer.plot(figure_data)

    print(figure)


Installation
------------

In short: ``pip install mcbrowse``. Note that ``mcbrowse`` requires many "heavy" dependencies, most notably ``daf``
which in turn requires ``numpy``, ``pandas``, ``scipy`` and ``anndata``, all of which ``pip`` should automatically
install for you. If you are running inside a ``conda`` environment, you might prefer to use it to first install these
dependencies, instead of having ``pip`` install them from ``PyPI``.

License (MIT)
-------------

Copyright © 2022 Weizmann Institute of Science

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
