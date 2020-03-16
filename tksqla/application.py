from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tkinter import messagebox, ttk
from . import db
from . import gui
import tkinter as tk
import sys


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.title('TkSQLA')
        engine = create_engine('sqlite:///var/db.sqlite', echo=True)
        self.Session = sessionmaker(bind=engine)
        self.callbacks = {
            'filter_vehiclemodel_by_vehiclemake': self.filter_vehiclemodel_by_vehiclemake,
            'open_vehiclemake_form': self.open_vehiclemake_form,
            'open_vehiclemodel_form': self.open_vehiclemodel_form,
            'open_vehicletrim_form': self.open_vehicletrim_form,
            'on_save_vehiclemake_form': self.on_save_vehiclemake_form,
            'on_save_vehiclemodel_form': self.on_save_vehiclemodel_form,
            'on_save_vehicletrim_form': self.on_save_vehicletrim_form,
            'qry_vehiclemake': self.qry_vehiclemake
        }

        self.vehicletrim_btn = ttk.Button(self, text='Add Vehicle Trim',
                                          command=self.callbacks['open_vehicletrim_form'])
        self.vehicletrim_btn.pack()

        self.vehiclemake_form_window = None
        self.vehiclemodel_form_window = None
        self.vehicletrim_form_window = None
        self.vehiclemake_form = None
        self.vehiclemodel_form = None
        self.vehicletrim_form = None

    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            print('@contextmanager caught an error! {}'.format(e))
            session.rollback()
            raise
        finally:
            session.close()

    def open_vehiclemake_form(self, called_from=None, modal=False):
        self.vehiclemake_form_window = gui.widgets.Toplevel(self, called_from, modal)
        if modal is True:
            self.vehiclemake_form_window.grab_set()
        self.vehiclemake_form = gui.forms.VehicleMakeForm(
            self.vehiclemake_form_window,
            db.forms.VehicleMakeForm().fields,
            self.callbacks
        )
        self.vehiclemake_form.pack()
        self.vehiclemake_form_window.focus()

    def on_save_vehiclemake_form(self):
        previous_form = self.vehiclemake_form_window.called_from
        if self.vehiclemake_form.is_valid():
            data = self.vehiclemake_form.get()
            with self.session_scope() as session:
                new_record = db.forms.VehicleMakeForm().save(session, data)
            if previous_form is not None:
                previous_form.focus()
                previous_form.on_vehiclemake_saved(new_record)  # last saved value
            if self.vehiclemake_form_window.modal is True:
                self.vehiclemake_form_window.destroy()

    def open_vehiclemodel_form(self, called_from=None, modal=False):
        vehiclemake_id = None
        if callable(getattr(called_from, 'get_vehiclemake_id', None)):
            vehiclemake_id = called_from.get_vehiclemake_id()
        self.vehiclemodel_form_window = gui.widgets.Toplevel(self, called_from, modal)
        if modal is True:
            self.vehiclemodel_form_window.grab_set()
        with self.session_scope() as session:
            self.vehiclemodel_form = gui.forms.VehicleModelForm(
                self.vehiclemodel_form_window,
                db.forms.VehicleModelForm(session, vehiclemake_id=vehiclemake_id).fields,
                self.callbacks
            )
        self.vehiclemodel_form.pack()
        self.vehiclemodel_form_window.focus()

    def on_save_vehiclemodel_form(self):
        previous_form = self.vehiclemodel_form_window.called_from
        data = self.vehiclemodel_form.get()
        with self.session_scope() as session:
            new_record = db.forms.VehicleModelForm(session).save(session, data)
        if previous_form is not None:
            previous_form.focus()
            previous_form.on_vehiclemodel_saved(new_record)
        if self.vehiclemodel_form_window.modal is True:
            self.vehiclemodel_form_window.destroy()

    def open_vehicletrim_form(self):
        if self.vehicletrim_form_window is None or not self.vehicletrim_form_window.winfo_exists():
            self.vehicletrim_form_window = tk.Toplevel(self)
            with self.session_scope() as session:
                self.vehicletrim_form = gui.forms.VehicleTrimForm(
                    self.vehicletrim_form_window,
                    db.forms.VehicleTrimForm(session).fields,
                    self.callbacks
                )
            self.vehicletrim_form.pack()
        else:
            self.vehicletrim_form_window.lift(self)
        self.vehicletrim_form_window.focus()

    def on_save_vehicletrim_form(self):
        data = self.vehicletrim_form.get()
        try:
            with self.session_scope() as session:
                db.forms.VehicleTrimForm(session, data).save()
        except Exception as e:
            messagebox.showerror(title='Error',
                                 message='Problem while saving form',
                                 detail=str(e))
            self.vehicletrim_form.focus()
        else:
            self.vehicletrim_form.reset()

    def qry_vehiclemake(self):
        with self.session_scope() as session:
            return db.queries.qry_vehiclemake(session)

    def filter_vehiclemodel_by_vehiclemake(self, vehiclemake_id):
        with self.session_scope() as session:
            return db.queries.qry_filter_vehiclemodel(session, vehiclemake_id)