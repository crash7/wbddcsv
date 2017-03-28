# -*- coding: utf-8 -*-
import os
import re
import csv
from wb import *
import grt
import mforms as gui

ModuleInfo = DefineModule(name="Workbench Data Dictionary", author="Christian Musa", version="0.1")
@ModuleInfo.plugin("cm.plugin.createDD_csv", 
	caption="Generate CSV Data Dictionary", 
	input=[wbinputs.currentCatalog()], 
	pluginMenu="Catalog"
)
@ModuleInfo.export(grt.INT, grt.classes.db_Catalog)

def createDD_csv(catalog):
	schema = catalog.defaultSchema
	tables = sorted(schema.tables, key=lambda table: table.name)
	csvlines = []

	# Header
	csvlines.append(" ; ; ;TITULO; ; ; ; ; ; ")

	# Columns
	csvlines.append("Tabla;Nombre;Tipo de campo;Tipo de dato;Longitud;PK;FK;Referencia;UNIQUE;Nulo;Descripción")

	for table in tables:
		#csvlines.append("%s;%s;Tabla; ; ; ; ; ; ;%s" % (table.name, table.name, str(table.comment).strip()))
		# FK's
		fkslist = {}
		for fk in table.foreignKeys:
			fkslist[fk.columns[0].name] = fk.referencedTable.name

		for column in table.columns:
			row = []
			# Data type
			rx = re.compile('([a-zA-Z]+)\(([0-9,]+)\)')
			datatype = column.formattedType
			rxs = rx.search(datatype)
			datatypelength = ""
			if rxs != None and len(rxs.groups()) == 2:
				datatype = rxs.group(1)
				datatypelength = rxs.group(2)

			row.append(column.name)
			row.append(table.name)
			row.append("Atributo")
			row.append(datatype)
			row.append(datatypelength)
			row.append("PK" if table.isPrimaryKeyColumn(column) else "")
			row.append("FK" if fkslist.has_key(column.name) else "")
			row.append(fkslist[column.name] if fkslist.has_key(column.name) else "")
			row.append('')
			row.append("No" if column.isNotNull == 1 else "Si")
			row.append(str(column.comment).strip())

			csvlines.append(";".join(row))


	# Ask file
	dialog = gui.FileChooser(gui.SaveFile)
	dialog.set_title("Save CSV data dictionary")
	dialog.set_directory(os.path.dirname(grt.root.wb.docPath))
	response = dialog.run_modal()
	filepath = dialog.get_path()

	if response:
		try:
			csvfile = open(filepath, "w")
		except IOError:
			gui.Utilities.show_error("Error saving the file",
				"Could not open " + filepath, "Ok", "", "")
		
		else:
			csvfile.writelines("%s\n" % l for l in csvlines)
			csvfile.close()

			gui.Utilities.show_message(schema.name + "'s DD",
				"DD was succesfully generated",
				"Ok", "", "")

	return 0


def buildHeader():
	return ""

def buildColumns():
	return ""
