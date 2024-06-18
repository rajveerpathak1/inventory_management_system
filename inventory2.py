import tkinter as tk
from tkinter import messagebox, filedialog
import csv
import os
import speech_recognition as sr
import pyttsx3

class Item:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Inventory Management System")
        self.master.configure(background="#D2B48C")  # Greenish background

        self.inventory = []
        self.current_file = None

        self.engine = pyttsx3.init()

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        self.master.geometry("600x500")
        center_frame = tk.Frame(self.master, bg="#808080")
        center_frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=20)

        # Menu bar
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)

        # Product Name
        self.label_name = tk.Label(center_frame, text="Product Name:", font=("Arial", 12, "bold"))
        self.label_name.pack(pady=5)
        self.entry_name = tk.Entry(center_frame, font=("Arial", 12))
        self.entry_name.pack(pady=5)

        # Quantity
        self.label_quantity = tk.Label(center_frame, text="Quantity (Kg):", font=("Arial", 12, "bold"))
        self.label_quantity.pack(pady=5)
        self.entry_quantity = tk.Entry(center_frame, font=("Arial", 12))
        self.entry_quantity.pack(pady=5)

        # Price
        self.label_price = tk.Label(center_frame, text="Price (per Kg):", font=("Arial", 12, "bold"))
        self.label_price.pack(pady=5)
        self.entry_price = tk.Entry(center_frame, font=("Arial", 12))
        self.entry_price.pack(pady=5)

        # Buttons
        button_frame = tk.Frame(center_frame, bg="")
        button_frame.pack(pady=10)
        self.button_add = tk.Button(button_frame, text="Add", command=self.add, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.button_add.pack(side=tk.LEFT, padx=5)
        self.button_update = tk.Button(button_frame, text="Update", command=self.update, bg="#008CBA", fg="white", font=("Arial", 12, "bold"))
        self.button_update.pack(side=tk.LEFT, padx=5)
        self.button_delete = tk.Button(button_frame, text="Delete", command=self.delete, bg="#f44336", fg="white", font=("Arial", 12, "bold"))
        self.button_delete.pack(side=tk.LEFT, padx=5)
        self.button_voice = tk.Button(button_frame, text="Voice Command", command=self.voice_command, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.button_voice.pack(side=tk.LEFT, padx=5)

        # Inventory List
        self.label_list = tk.Label(center_frame, text="Inventory List:", font=("Arial", 12, "bold"))
        self.label_list.pack(pady=10)
        self.listbox = tk.Listbox(center_frame, height=10, width=70, font=("Arial", 12))
        self.listbox.pack(padx=5, pady=5)
        self.listbox.bind("<<ListboxSelect>>", self.select)

        # Search
        search_frame = tk.Frame(center_frame, bg="#34A85A")
        search_frame.pack(pady=5)
        self.label_search = tk.Label(search_frame, text="Search:", font=("Arial", 12, "bold"))
        self.label_search.pack(side=tk.LEFT)
        self.entry_search = tk.Entry(search_frame, font=("Arial", 12))
        self.entry_search.pack(side=tk.LEFT, padx=5)
        self.button_search = tk.Button(search_frame, text="Search", command=self.search, bg="#2196F3", fg="white", font=("Arial", 12, "bold"))
        self.button_search.pack(side=tk.LEFT, padx=5)

        # Sort
        sort_frame = tk.Frame(center_frame,bg="")
        sort_frame.pack(pady=5)
        self.button_sort_name = tk.Button(sort_frame, text="Sort by Name", command=lambda: self.sort_inventory("name"), bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.button_sort_name.pack(side=tk.LEFT, padx=5)
        self.button_sort_quantity = tk.Button(sort_frame, text="Sort by Quantity", command=lambda: self.sort_inventory("quantity"), bg="#008CBA", fg="white", font=("Arial", 12, "bold"))
        self.button_sort_quantity.pack(side=tk.LEFT, padx=5)
        self.button_sort_price = tk.Button(sort_frame, text="Sort by Price", command=lambda: self.sort_inventory("price"), bg="#f44336", fg="white", font=("Arial", 12, "bold"))
        self.button_sort_price.pack(side=tk.LEFT, padx=5)

        # Export CSV
        self.button_export = tk.Button(center_frame, text="Export CSV", command=self.export_csv, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.button_export.pack(pady=10)

    def populate_listbox(self, items=None):
        self.listbox.delete(0, tk.END)
        items = items or self.inventory
        for item in items:
            self.listbox.insert(tk.END, f"{item.name} - Qty: {item.quantity}, Price: Rs {item.price:.2f}")

    def add(self):
        name = self.entry_name.get().strip()
        quantity = self.entry_quantity.get().strip()
        price = self.entry_price.get().strip()

        if not name or not quantity or not price:
            messagebox.showerror("Error", "All fields must be filled.")
            return

        try:
            quantity = int(quantity)
            price = float(price)
            if quantity <= 0 or price <= 0:
                raise ValueError("Quantity and price must be positive")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        item = Item(name, quantity, price)
        self.inventory.append(item)

        self.populate_listbox()

        self.entry_name.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)

        messagebox.showinfo("Success", "Item added successfully.")

    def update(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "No item selected for update.")
            return

        index = selection[0]
        name = self.entry_name.get().strip()
        quantity = self.entry_quantity.get().strip()
        price = self.entry_price.get().strip()

        if not name or not quantity or not price:
            messagebox.showerror("Error", "All fields must be filled.")
            return

        try:
            quantity = int(quantity)
            price = float(price)
            if quantity <= 0 or price <= 0:
                raise ValueError("Quantity and price must be positive")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        self.inventory[index].name = name
        self.inventory[index].quantity = quantity
        self.inventory[index].price = price

        self.populate_listbox()

    def delete(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "No item selected for deletion.")
            return

        index = selection[0]
        del self.inventory[index]

        self.populate_listbox()

    def select(self, event):
        selection = self.listbox.curselection()
        if selection:
           index = selection[0]
        item = self.inventory[index]
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(tk.END, item.name)
        self.entry_quantity.delete(0, tk.END)
        self.entry_quantity.insert(tk.END, item.quantity)
        self.entry_price.delete(0, tk.END)
        self.entry_price.insert(tk.END, item.price)

    def new_file(self):
        if messagebox.askyesno("Save", "Do you want to save the current inventory before creating a new one?"):
            self.save_file()
        self.inventory = []
        self.current_file = None
        self.populate_listbox()

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.current_file = file_path
            self.inventory = []
            try:
                with open(file_path, "r") as file:
                    reader = csv.reader(file)
                    next(reader)
                    for row in reader:
                        name, quantity, price = row
                        item = Item(name, int(quantity), float(price))
                        self.inventory.append(item)
                self.populate_listbox()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurredwhile loading the file: {str(e)}")

    def save_file(self):
        if self.current_file:
            self.save_to_file(self.current_file)
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.current_file = file_path
            self.save_to_file(file_path)

    def save_to_file(self, file_path):
        try:
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Product Name", "Quantity", "Price"])
                for item in self.inventory:
                    writer.writerow([item.name, item.quantity, item.price])
            messagebox.showinfo("Save Successful", f"Inventory saved to {file_path} successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file: {str(e)}")

    def sort_inventory(self, key):
        if key not in ["name", "quantity", "price"]:
            messagebox.showerror("Error", "Invalid sort key.")
            return
        self.inventory.sort(key=lambda x: getattr(x, key))
        self.populate_listbox()

    def search(self):
        query = self.entry_search.get().strip().lower()
        if not query:
            messagebox.showerror("Error", "Search field cannot be blank.")
            return
        results = [item for item in self.inventory if query in item.name.lower()]
        self.populate_listbox(results)

    def export_csv(self):
        if not self.inventory:
            messagebox.showerror("Error", "Inventory is empty, nothing to export.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                with open(file_path, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Product Name", "Quantity", "Price"])
                    for item in self.inventory:
                        writer.writerow([item.name, item.quantity, item.price])
                messagebox.showinfo("Export Successful", f"Inventory exported to {file_path} successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while exporting the file: {str(e)}")

    def voice_command(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)
            try:
                command = r.recognize_google(audio, language="en-IN")
                print("You said:", command)
                # Process the command here
                if command == "add item":
                    self.add()
                elif command == "update item":
                    self.update()
                elif command == "delete item":
                    self.delete()
                elif command == "search":
                    self.search()
                elif command == "sort by name":
                    self.sort_inventory("name")
                elif command == "sort by quantity":
                    self.sort_inventory("quantity")
                elif command == "sort by price":
                    self.sort_inventory("price")
                elif command == "export csv":
                    self.export_csv()
                else:
                    messagebox.showerror("Error", "Invalid voice command.")
            except sr.UnknownValueError:
                print("Speech recognition could not understand your audio")
            except sr.RequestError as e:
                print("Could not request results from speech recognition service; {0}".format(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()