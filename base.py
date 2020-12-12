from tkinter import Tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox


class Phonebook:

    def __init__(self, master):

        # Window Management
        master.title('Phonebook')
        master.state('zoomed')
        master.resizable(False, False)

        # Frame Management
        header_frame = ttk.Frame(master)
        header_frame.pack()

        body_frame = ttk.Frame(master)
        body_frame.pack()

        self.show_records = ttk.Frame(body_frame)
        self.show_records.grid(column=0, row=0, pady=20, padx=150)

        self.add_record = ttk.Frame(body_frame)
        self.add_record.grid(column=1, row=0, pady=20, padx=150)

        # Widgets Management
        ttk.Label(self.show_records, text="Search", font="Calibri 12 bold").grid(
            row=0, column=0, pady=3, columnspan=3)
        self.search = ttk.Entry(self.show_records, font="Calibri 11", width=50)
        self.search.grid(row=1, column=0, pady=3, padx=3, columnspan=3)
        self.search_button = ttk.Button(
            self.show_records, text='Search Contact', width=15, command=self.record_dashboard)
        self.search_button.grid(row=3, column=0, columnspan=3, pady=30)

        header = ttk.Label(
            header_frame, text="Phonebook")
        header.grid(row=0, column=0, pady=3)
        header.config(background='#228B22', foreground="#e7e6e6",
                      width=1920, font=('Calibri', 24, 'bold'))

        ttk.Label(self.add_record, text="Name", font="Calibri 12 bold").grid(
            row=0, column=0, pady=3)
        self.name = ttk.Entry(self.add_record, font="Calibri 11 ")
        self.name.grid(row=1, column=0, pady=3, padx=3)

        ttk.Label(self.add_record, text="Phone", font="Calibri 12 bold").grid(
            row=0, column=1, pady=3)
        self.phone = ttk.Entry(self.add_record, font="Calibri 11 ")
        self.phone.grid(row=1, column=1, pady=3, padx=3)

        self.add_record_button = ttk.Button(
            self.add_record, text='Add Contact', width=15, command=self.add_record_action)
        self.add_record_button.grid(row=3, column=0, columnspan=3, pady=10)

    def add_record_action(self):
        database = mysql.connector.connect(
            host="localhost", user="root", password="", database="phonebook")
        cursor = database.cursor()

        sql = "INSERT INTO `records` (`Name`, `Phone`) VALUES (%s, %s)"
        value = (self.name.get(), self.phone.get())
        cursor.execute(sql, value)
        database.commit()

        messagebox.showinfo(title="Confirmation",
                            message='Contact has been added')
    
        
    def delete_record_action(self):
        database = mysql.connector.connect(
            host="localhost", user="root", password="", database="phonebook")
        cursor = database.cursor()

        sql = "DELETE FROM records WHERE Name = %s"
        value = (self.search.get(),)
        cursor.execute(sql, value)
        database.commit()

        messagebox.showinfo(title="Confirmation",
                            message='Contact has been deleted')

    def record_dashboard(self):
        database = mysql.connector.connect(
            host="localhost", user="root", password="", database="phonebook")
        cursor = database.cursor()

        sql = "SELECT * FROM `records` WHERE `Name` = %s"
        value = (self.search.get(), )
        cursor.execute(sql, value)
        result = cursor.fetchall()

        if (len(result) != 0):
            ttk.Label(self.show_records, text="Name",
                      font="Calibri 12 bold").grid(row=4, column=0)
            ttk.Label(self.show_records, text="Phone",
                      font="Calibri 12 bold").grid(row=4, column=1)
            ttk.Label(self.show_records, text="Action",
                      font="Calibri 12 bold").grid(row=4, column=2)

            for i in range(len(result)):
                for j in range(3):
                    if (j != 2):
                        self.td = ttk.Entry(
                            self.show_records, font="Calibri 11")
                        self.td.grid(row=i+5, column=j, pady=10)
                        self.td.insert(0, result[i][j+1])
                        self.td.state(['readonly'])
                    else:
                        self.delete_contact_button = ttk.Button(
                            self.show_records, text='Delete', command=self.delete_record_action)
                        self.delete_contact_button.grid(
                            row=i+5, column=j, padx=10, pady=5)

        else:
            ttk.Label(self.show_records, text="No Match Found",
                      font="Calibri 12 bold").grid(row=5, column=0, columnspan=3)


def main():
    master = Tk()
    Phonebook(master)
    master.mainloop()


if __name__ == "__main__":
    main()
