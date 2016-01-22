#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2015
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import os
import gzip
import shutil
import numpy


def element_to_list(element):
    """ Set an element to an empty list.

    <unit>
        <input name="element" type="Any" description="an input element." />
        <output name="adaptedelement" type="List" content="Any" desc="the
            returned list containing the input element only."/>
    </unit>
    """
    adaptedelement = [element]
    return adaptedelement


def list_to_element(listobj, force=False):
    """ Get the singleton list element.

    <unit>
        <input name="listobj" type="List" content="Any" desc="an input
            singleton list."/>
        <input name="force" type="Bool" optional="True" desc="force conversion
            even if more then one element in the list" />
        <output name="element" type="Any" desc="the returned
            list single element."/>
    </unit>
    """
    # Check that we have a singleton list
    if len(listobj) != 1 and not force:
        raise ValueError("A list with '{0}' element(s) is not a singleton "
                         "list.".format(len(listobj)))

    element = listobj[0]
    return element


def normalize_array(filepath):
    """
        Get a numpy array from a file and normalize column by column

    <unit>
        <input name="filepath" type="File" desc="the input file containing 
            the numpy array"/>
        <output name="outfile" type="File" desc="the output file with normalized
            array"/>
    </unit>
    """
    # load input file
    array = numpy.loadtxt(filepath)
    array = (array - array.mean(axis=0)) / array.std(axis=0)
    outfile = filepath
    numpy.savetxt(outfile, array, fmt="%5.8f")

    return outfile


def ungzip_file(fname, prefix="u", output_directory=None):
    """ Copy and ungzip the input file.

    <unit>
        <input name="fname" type="File" desc="an input file to ungzip."/>
        <input name="prefix" type="String" desc="the prefix of the result
            file."/>
        <input name="output_directory" type="Directory" desc="the output
            directory where ungzip file is saved."/>
        <output name="ungzipfname" type="File" desc="the returned
            ungzip file."/>
    </unit>
    """
    # Check the input file exists on the file system
    if not os.path.isfile(fname):
        raise ValueError("'{0}' is not a valid filename.".format(fname))

    # Check that the outdir is valid
    if output_directory is not None:
        if not os.path.isdir(output_directory):
            raise ValueError(
                "'{0}' is not a valid directory.".format(output_directory))
    else:
        output_directory = os.path.dirname(fname)

    # Get the file descriptors
    base, extension = os.path.splitext(fname)
    basename = os.path.basename(base)

    # Ungzip only known extension
    if extension in [".gz"]:

        # Generate the output file name
        basename = prefix + basename
        ungzipfname = os.path.join(output_directory, basename)

        # Read the input gzip file
        with gzip.open(fname, "rb") as gzfobj:
            data = gzfobj.read()

        # Write the output ungzip file
        with open(ungzipfname, "wb") as openfile:
            openfile.write(data)

    # Default, unknown compression extension: the input file is returned
    else:
        ungzipfname = fname

    return ungzipfname


def gzip_file(fname, prefix="g", output_directory=None,
              remove_original_file=False):
    """ Copy and gzip the input file.

    <unit>
        <input name="fname" type="File" desc="an input file to gzip."/>
        <input name="prefix" type="String" desc="the prefix of the result
            file."/>
        <input name="output_directory" type="Directory" desc="the output
            directory where gzip file is saved."/>
        <input name="remove_original_file" type="Bool" desc="remove the original
            file" />
        <output name="gzipfname" type="File" desc="the returned
            gzip file."/>
    </unit>
    """
    # Check the input file exists on the file system
    if not os.path.isfile(fname):
        raise ValueError("'{0}' is not a valid filename.".format(fname))

    # Check that the outdir is valid
    if output_directory is not None:
        if not os.path.isdir(output_directory):
            raise ValueError(
                "'{0}' is not a valid directory.".format(output_directory))
    else:
        output_directory = os.path.dirname(fname)

    # Get the file descriptors
    base, extension = os.path.splitext(fname)
    # Gzip only non compressed file
    if extension not in [".gz"]:

        # Generate the output file name
        if prefix:
            basename = prefix + os.path.basename(base) + ".gz"
        else:
            basename = os.path.basename(base) + ".gz"
        gzipfname = os.path.join(output_directory, basename)

        # Write the output gzip file
        with open(fname, "rb") as openfile:
            with gzip.open(gzipfname, "w") as gzfobj:
                gzfobj.writelines(openfile)

        if remove_original_file:
            os.remove(fname)

    # Default, the input file is returned
    else:
        gzipfname = fname

    return gzipfname


def rename_file(input_filepath, output_filepath, overwrite=False):
    """ Rename a file (same loc)

    <unit>
        <input name="input_filepath" type="File" desc="an input file
            to rename."/>
        <input name="overwrite" type="Bool" desc="Overwrite of not
            if the file already exists (optional, default=False)"/>
        <input name="output_filepath" type="String" desc="the output
            filepath."/>
        <output name="output_file" type="File" desc="the renamed file."/>
    </unit>
    """

    if os.path.isfile(output_filepath):
        if overwrite:
            os.remove(output_filepath)
        else:
            raise Exception("Output file exist !")
    # get output folder
    shutil.move(input_filepath, output_filepath)

    output_file = output_filepath

    return output_file


def spm_tissue_probability_maps():
    """ SPM tissue probability maps.

    <unit>
        <output name="tpm_struct" type="List" content="Any" desc="a struct
            containing the spm tissue probability map descriptions."/>
    </unit>
    """
    # Try to import the resource
    try:
        from caps.toy_datasets import get_sample_data
    except:
        raise ImportError("Can't import 'caps'.")
    tmp_file = get_sample_data("tpm").all

    # Format the tpm for spm
    tissue1 = ((tmp_file, 1), 2, (True, True), (False, True))
    tissue2 = ((tmp_file, 2), 2, (True, True), (False, True))
    tissue3 = ((tmp_file, 3), 2, (True, False), (False, False))
    tissue4 = ((tmp_file, 4), 3, (False, False), (False, False))
    tissue5 = ((tmp_file, 5), 4, (False, False), (False, False))

    tpm_struct = [tissue1, tissue2, tissue3, tissue4, tissue5]
    return tpm_struct


def noprocess_switch(input_value):
    """
    Do nothing, returns the input value
    Used in switch

    <unit>
        <input name="input_value" type="Any" desc="a variable to let through"/>
        <output name="output_value" type="Any" desc="the input value"/>

    </unit>
    """

    output_value = input_value

    return output_value
