from tkinter import *
from pymongo import MongoClient
from tkinter import ttk
from tkinter import messagebox

# connect to MongoDB
client = MongoClient()

# select database and collection
db = client['GestionDepartement']
collection = db['CRUDOperations']

# create GUI window
root = Tk()
root.title("CRUD operations with MongoDB")
root.configure(bg='#f8f9fa')

# define functions for CRUD operations
def create():
    input_values = [name_entry.get(), manager_entry.get(),
                      budget_entry.get(), nbrEmployees_entry.get(),
                      location_entry.get(),phoneNumber_entry.get()]
    empty_inputs = [i for i, val in enumerate(input_values) if not val]
    if empty_inputs:
        message_label.configure(text="Erreur, remplissez tout les champs!" , fg='red')
    else:
          # create a new document and insert into collection
          new_document = {"name": name_entry.get(), 
                          "manager": manager_entry.get(),
                            "budget": budget_entry.get(),
                            "nbrEmployees": nbrEmployees_entry.get(),
                            "location":location_entry.get(),
                            "phoneNumber":phoneNumber_entry.get()}
          collection.insert_one(new_document)
          # clear the entry fields
          name_entry.delete(0, END)
          manager_entry.delete(0, END)
          budget_entry.delete(0, END)
          nbrEmployees_entry.delete(0, END)
          location_entry.delete(0, END)
          phoneNumber_entry.delete(0, END)
          message_label.configure(text="Created succusfully!" , fg='green')

  


def read():
    # read documents from collection and display in the text area
    # tree.delete('1', END) # clear previous text
    tree.delete(*tree.get_children())
    for document in collection.find():
        tree.insert("",END, values=(document['name'],
                            document['manager'],
                            document['budget'], document['nbrEmployees'],
                            document['location'] , document['phoneNumber']))
    message_label.configure(text="")
        

def update():
    # update a document in the collection based on name
    collection.update_one({"name": name_entry.get()}, {"$set": {"manager": manager_entry.get(),
                           "budget": budget_entry.get() , "nbrEmployees": nbrEmployees_entry.get(),
                           "location":location_entry.get(), "phoneNumber":phoneNumber_entry.get()}})
    # clear the entry fields
    name_entry.delete(0, END)
    manager_entry.delete(0, END)
    budget_entry.delete(0, END)
    nbrEmployees_entry.delete(0, END)
    location_entry.delete(0, END)
    phoneNumber_entry.delete(0, END)
    message_label.configure(text="Updated succesfully!", fg='green')

def delete():
    result = messagebox.askyesnocancel("Confirmation", "Are you sure you want to delete this apartment?")
    if result == True:
        # delete a document from the collection based on name
      collection.delete_one({"name": name_entry.get()})
      # clear the entry field
      name_entry.delete(0, END)
      manager_entry.delete(0, END)
      budget_entry.delete(0, END)
      nbrEmployees_entry.delete(0, END)
      location_entry.delete(0, END)
      phoneNumber_entry.delete(0, END)
      message_label.configure(text="Deleted succufully!")
    else:
        # do nothing if the user clicks "Cancel"
        pass
    


# create entry fields for data input
name_label = Label(root, text="Nom de departement :", bg='#f8f9fa')
name_label.grid(row=0, column=0)
name_entry = Entry(root,bg='#f1faee')
name_entry.grid(row=0, column=1, padx=10, pady=20)

manager_label = Label(root, text="Nom de manager :", bg='#f8f9fa')
manager_label.grid(row=1, column=0)
manager_entry = Entry(root,bg='#f1faee')
manager_entry.grid(row=1, column=1, padx=10, pady=20)

budget_label = Label(root, text="Budget :", bg='#f8f9fa')
budget_label.grid(row=2, column=0)
budget_entry = Entry(root,bg='#f1faee')
budget_entry.grid(row=2, column=1, padx=10, pady=20)

nbrEmployees_label = Label(root, text="Le nombre d'employés :", bg='#f8f9fa')
nbrEmployees_label.grid(row=3, column=0)
nbrEmployees_entry = Entry(root,bg='#f1faee')
nbrEmployees_entry.grid(row=3, column=1, padx=10, pady=20)

location_label = Label(root, text="Localisation :", bg='#f8f9fa')
location_label.grid(row=4, column=0)
location_entry = Entry(root,bg='#f1faee')
location_entry.grid(row=4, column=1, padx=10, pady=20)

phoneNumber_label = Label(root, text="Numéro de téléphone :", bg='#f8f9fa')
phoneNumber_label.grid(row=5, column=0)
phoneNumber_entry = Entry(root,bg='#f1faee')
phoneNumber_entry.grid(row=5, column=1, padx=10, pady=20)

message_label = Label(root,text="", font=(17), bg='#f8f9fa', pady='20')
message_label.grid(row=7, column=0)

# create buttons for CRUD operations
create_button = Button(root, text="Create", command=create,padx=40,cursor="hand2",relief=RIDGE, bg="#9bded2")
create_button.grid(row=6, column=0)

read_button = Button(root, text="Read", command=read,padx=40,cursor="hand2",relief=RIDGE, bg='#146198',fg="white")
read_button.grid(row=6, column=1)

update_button = Button(root, text="Update", command=update,padx=40,cursor="hand2",relief=RIDGE, bg='#6a4b8a',fg="white")
update_button.grid(row=6, column=2)

delete_button = Button(root, text="Delete", command=delete,padx=45,cursor="hand2",relief=RIDGE , bg='#b62d65',fg="white")
delete_button.grid(row=6, column=3)

# create text area for displaying results
result_label = Label(root, text="Results:",padx=10, pady=20, bg='#f8f9fa')
result_label.grid(row=8, column=0)


columns = ("Nom de departement", "nom de manager", "budget", "Le nombre d'employés", "localisation", "numero de telephone")

tree = ttk.Treeview(root, columns=columns, show='headings')

# define headings
tree.heading('Nom de departement', text='Nom de departement')
tree.heading('nom de manager', text='Nom de manager')
tree.heading('budget', text='budget')
tree.heading("Le nombre d'employés", text='nombre demployee')
tree.heading('localisation', text='localisation')
tree.heading('numero de telephone', text='Numero de telephone')



def item_selected(event):
    item = tree.selection()[0]
    item_text = tree.item(item, 'values')
    name_entry.delete(0, END)
    name_entry.insert(END, item_text[0])

    manager_entry.delete(0, END)
    manager_entry.insert(END, item_text[1])

    budget_entry.delete(0, END)
    budget_entry.insert(END, item_text[2])

    nbrEmployees_entry.delete(0, END)
    nbrEmployees_entry.insert(END, item_text[3])

    location_entry.delete(0, END)
    location_entry.insert(END, item_text[4])

    phoneNumber_entry.delete(0, END)
    phoneNumber_entry.insert(END, item_text[5])
        


tree.bind('<<TreeviewSelect>>', item_selected)

tree.grid(row=10, column=0, sticky='nsew',columnspan=4)
# run the GUI
root.mainloop()
