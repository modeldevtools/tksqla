from tkinter import ttk
import tkinter as tk
from . import widgets as w


class VehicleMakeForm(tk.Frame):
    def __init__(self, parent, fields, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.callbacks = callbacks
        self.inputs = {}
        self.inputs['name'] = w.FormField(self, fields['name']['label'], ttk.Entry, fields['name']['required'])
        self.save_btn = ttk.Button(self, text='Save', command=self.callbacks['on_save_vehiclemake_form'])
        # Layout
        self.inputs['name'].grid(column=0, row=1)
        self.save_btn.grid(column=0, row=2)

    def is_valid(self):
        valid = True
        for key, widget in self.inputs.items():
            if not widget.is_valid():
                valid = False
        return valid

    def get(self):
        data = {'name': self.inputs['name'].get()}
        return data


class VehicleModelForm(tk.Frame):
    def __init__(self, parent, fields, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.callbacks = callbacks
        self.inputs = {}
        # Labels
        self.vmake_label = ttk.Label(self, text=fields['vehiclemake']['label'])
        self.name_label = ttk.Label(self, text=fields['name']['label'])
        # Inputs
        self.vehiclemake_lookups = fields['vehiclemake']['values']
        self.inputs['vehiclemake'] = ttk.Combobox(self, values=['', *sorted(self.vehiclemake_lookups)])
        if fields['vehiclemake']['disabled']:
            self.inputs['vehiclemake'].state(['disabled'])
        if 'initial' in fields['vehiclemake']:
            self.inputs['vehiclemake'].set(fields['vehiclemake']['initial'])
        self.name_var = tk.StringVar()
        self.inputs['name'] = ttk.Entry(self, textvariable=self.name_var)
        self.save_btn = ttk.Button(self, text='Save', command=self.callbacks['on_save_vehiclemodel_form'])
        # Layout
        self.vmake_label.grid(column=0, row=0)
        self.inputs['vehiclemake'].grid(column=0, row=1)
        self.name_label.grid(column=1, row=0)
        self.inputs['name'].grid(column=1, row=1)
        self.save_btn.grid(column=1, row=2)

    def get(self):
        vehiclemake = self.inputs['vehiclemake'].get()
        vehiclemake_id = self.vehiclemake_lookups[vehiclemake]
        name = self.inputs['name'].get()
        data = {'vehiclemake_id': vehiclemake_id, 'name': name}
        return data


class VehicleTrimForm(tk.Frame):
    def __init__(self, parent, fields, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.callbacks = callbacks
        self.inputs = {}
        # Labels
        self.vehiclemake_label = ttk.Label(self, text=fields['vehiclemake']['label'])
        self.vehiclemodel_label = ttk.Label(self, text=fields['vehiclemodel']['label'])
        self.vehicletrim_name_label = ttk.Label(self, text=fields['name']['label'])
        # Lookups and inputs
        self.vehiclemake_lookups = fields['vehiclemake']['values']
        self.inputs['vehiclemake'] = ttk.Combobox(self, values=['', *sorted(self.vehiclemake_lookups)])
        self.inputs['vehiclemake'].bind('<<ComboboxSelected>>', self.on_vehiclemake_selected)
        self.vehiclemodel_lookups = fields['vehiclemodel']['values']
        self.inputs['vehiclemodel'] = ttk.Combobox(self, values=['', *sorted(self.vehiclemodel_lookups)])
        self.inputs['vehiclemodel'].bind('<<ComboboxSelected>>', self.on_vehiclemodel_selected)
        self.vehicletrim_name_var = tk.StringVar()
        self.inputs['name'] = ttk.Entry(self, textvariable=self.vehicletrim_name_var)
        # Buttons to open new forms
        self.vehiclemake_form_btn = ttk.Button(
            self, text='Add VehicleMake',
            command=lambda: self.callbacks['open_vehiclemake_form'](called_from=self, modal=True)
        )
        self.vehiclemodel_form_btn = ttk.Button(
            self, text='Add VehicleModel',
            command=lambda: self.callbacks['open_vehiclemodel_form'](called_from=self, modal=True)
        )
        # A save button
        self.save_btn = ttk.Button(self, text='Save',
                                   command=self.callbacks['on_save_vehicletrim_form'])
        # Default states
        self.inputs['vehiclemodel'].state(['disabled'])
        self.vehiclemodel_form_btn.state(['disabled'])
        self.inputs['name'].state(['disabled'])
        # Layout
        self.vehiclemake_label.grid(column=0, row=0)
        self.vehiclemodel_label.grid(column=1, row=0)
        self.vehicletrim_name_label.grid(column=2, row=0)
        self.inputs['vehiclemake'].grid(column=0, row=1)
        self.inputs['vehiclemodel'].grid(column=1, row=1)
        self.inputs['name'].grid(column=2, row=1)
        self.vehiclemake_form_btn.grid(column=0, row=2)
        self.vehiclemodel_form_btn.grid(column=1, row=2)
        self.save_btn.grid(column=2, row=3)

    def get(self):
        vehiclemodel = self.inputs['vehiclemodel'].get()
        vehiclemodel_id = self.vehiclemodel_lookups[vehiclemodel]
        name = self.inputs['name'].get()
        data = {'vehiclemodel_id': vehiclemodel_id, 'name': name}
        return data

    def get_vehiclemake_id(self):
        vehiclemake = self.inputs['vehiclemake'].get()
        vehiclemake_id = self.vehiclemake_lookups[vehiclemake]
        return vehiclemake_id

    def reset(self):
        self.inputs['vehiclemake'].set('')
        self.inputs['vehiclemodel'].set('')
        self.vehicletrim_name_var.set('')

    def on_vehiclemake_saved(self, new_record):
        self.vehiclemake_lookups = self.callbacks['qry_vehiclemake']()
        new_values = ['', *sorted(self.vehiclemake_lookups)]
        idx = new_values.index(new_record['name'])
        self.inputs['vehiclemake'].configure(values=new_values)
        self.inputs['vehiclemake'].current(idx)
        self.inputs['vehiclemake'].event_generate('<<ComboboxSelected>>')

    def on_vehiclemodel_saved(self, new_record):
        vehiclemake = self.inputs['vehiclemake'].get()
        vehiclemake_id = self.vehiclemake_lookups[vehiclemake]
        self.vehiclemodel_lookups = self.callbacks['filter_vehiclemodel_by_vehiclemake'](vehiclemake_id)
        new_values = ['', *sorted(self.vehiclemodel_lookups)]
        idx = new_values.index(new_record['name'])
        self.inputs['vehiclemodel'].configure(values=new_values)
        self.inputs['vehiclemodel'].current(idx)
        self.inputs['vehiclemodel'].event_generate('<<ComboboxSelected>>')

    def on_vehiclemake_selected(self, event):
        selected_value = self.inputs['vehiclemake'].get()
        if selected_value == '':
            self.inputs['vehiclemodel'].state(['disabled'])
            self.vehiclemodel_form_btn.state(['disabled'])
            self.inputs['name'].state(['disabled'])
        else:
            vehiclemake_id = self.vehiclemake_lookups[selected_value]
            self.vehiclemodel_lookups = self.callbacks['filter_vehiclemodel_by_vehiclemake'](vehiclemake_id)
            self.inputs['vehiclemodel'].configure(values=['', *sorted(self.vehiclemodel_lookups)])
            self.inputs['vehiclemodel'].state(['!disabled'])
            self.vehiclemodel_form_btn.state(['!disabled'])
            self.inputs['name'].state(['disabled'])
        self.inputs['vehiclemodel'].set('')
        self.vehicletrim_name_var.set('')

    def on_vehiclemodel_selected(self, event):
        selected_value = self.inputs['vehiclemodel'].get()
        if selected_value == '':
            self.inputs['name'].state(['disabled'])
        else:
            self.inputs['name'].state(['!disabled'])