#!/usr/bin/env python

"""
https://acaird.github.io/2016/02/07/simple-python-gui

Transform_InqScribe_to_IOH.py

Python2 script to parse transcription XML output from InqScribe and translate
to the native <cues> structure required for the Islandora Oral Histories Solution Pack
(https://github.com/digitalutsc/islandora_solution_pack_oralhistories).

Basic GUI with command-line option lifted from https://acaird.github.io/2016/02/07/simple-python-gui
source.

"""

import os.path
import argparse
import tkFileDialog
from Tkinter import *


def get_output_filename(input_file_name):
  """ replace the suffix of the file with .rst """
  parts = os.path.split(input_file_name)
  return parts[0] + "/IOH_" + parts[1]

def gui():
  """make the GUI version of this command that is run if no options are
  provided on the command line"""

  def button_transform_callback():
    """ what to do when the "Transform" button is pressed """
    input_file = entry.get()
    
    if input_file.rsplit(".")[-1] != "xml":
      statusText.set("Filename must have a .xml extension!")
      message.configure(fg="red")
      return
    else:
      IOH_xml = xsl_transormation(input_file)
      if IOH_xml is None:
        statusText.set("Error transforming file `{}'.".format(input_file))
        message.configure(fg="red")
        return
 
      output_file_name = get_output_filename(input_file)
      
      ioh_file = open(output_file_name, "w")
      if ioh_file:
        ioh_file.write(str(IOH_xml))
        ioh_file.close()
        statusText.set("Output is in {}".format(output_file_name))
        message.configure(fg="dark green")
      else:
        statusText.set("File `{}' could not be opened for output.".format(output_file_name))
        message.configure(fg="red")

  def button_hms_callback():
    """ what to do when the "Convert hh:mm:ss..." button is pressed """

  def button_format_callback():
    """ what to do when the "Format" button is pressed """

  def button_browse_callback():
    """ What to do when the Browse button is pressed """
    filename = tkFileDialog.askopenfilename()
    entry.delete(0, END)
    entry.insert(0, filename)

  # Transform any XML with a XSLT
  # You can pass additional parameters for your stylesheet
  # Lifted from https://gist.github.com/revolunet/1154906

  def xsl_transormation(xmlfile, xslfile="./Transform_InqScribe_to_IOH.xsl", xmlstring=None, params={}):
    from lxml import etree
    import StringIO
  
    xsl = open(xslfile)
    if xsl:
      xslt = xsl.read()
    else:
      statusText.set("XSLT file `{}' could not be opened.".format(xslfile))
      message.configure(fg="red")
  
    xslt_tree = etree.XML(xslt)
    transform = etree.XSLT(xslt_tree)
  
    xml_contents = xmlstring
    if not xml_contents:
      if xmlfile:
        xml = open(xmlfile)
        if xml:
          xml_contents = xml.read()
        else:
          statusText.set("XML file `{}' could not be opened.".format(xmlfile))
          message.configure(fg="red")
      else:
        xml_contents = '<?xml version="1.0"?>\n<foo>A</foo>\n'
  
    f = StringIO.StringIO(xml_contents)
    doc = etree.parse(f)
    f.close()
    transform = etree.XSLT(xslt_tree)
    result = transform(doc, **params)
  
    return result
  
  # ------------------------------------------------

  root = Tk()
  frame = Frame(root)
  frame.pack()

  statusText = StringVar(root)
  statusText.set("Press Browse button or enter XML filename then press the Transform button.")

  label = Label(root, text="Transform InqScribe XML file:")
  label.pack(padx=10)
  entry = Entry(root, width=80)
  entry.pack(padx=10)
  separator = Frame(root, height=2, bd=1, relief=SUNKEN)
  separator.pack(fill=X, padx=10, pady=5)

  button_browse = Button(root, text="Browse", command=button_browse_callback)
  button_transform = Button(root, text="Transform", command=button_transform_callback)
  button_hms = Button(root, text="Convert hh:mm:ss to Seconds", command=button_hms_callback)
  button_format = Button(root, text="Format Speakers", command=button_format_callback)
  button_exit = Button(root, text="Exit", command=sys.exit)
  button_browse.pack()
  button_transform.pack()
  button_hms.pack()
  button_format.pack()
  button_exit.pack()

  separator = Frame(root, height=2, bd=1, relief=SUNKEN)
  separator.pack(fill=X, padx=10, pady=5)

  message = Label(root, textvariable=statusText)
  message.pack(padx=10, pady=5)

  mainloop()


def command_line(args):
  """ Run the command-line version
  if args.output is None:
    args.output = get_output_filename(args.input)

  table_contents = read_csv(args.input)

  if write_table(args.output, table_contents):
    print "rst table is in file `{}'".format(args.output)
  else:
    print "Writing file `{}' did not succeed.".format(args.output)
  """

def get_parser():
  """ The argument parser of the command-line version """
  parser = argparse.ArgumentParser(description=('convert csv to rst table'))

  parser.add_argument('--input', '-F',
                        help='name of the intput file')

  parser.add_argument('--output', '-O',
                        help=("name of the output file; " +
                              "defaults to <inputfilename>.rst"))
  return parser

# -----------------------------------------------------

if __name__ == "__main__":
  """ Run as a stand-alone script """

  parser = get_parser()       # Start the command-line argument parsing
  args = parser.parse_args()  # Read the command-line arguments

  if args.input:              # If there is an argument,
    command_line(args)      # run the command-line version
  else:
    gui()                   # otherwise run the GUI version