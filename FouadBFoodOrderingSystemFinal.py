import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import sys

dishes_menu = [
    ["Couscous with Vegetables", 7.50],
    ["Chicken Tagine", 8.00],
    ["Lamb Tagine", 9.00],
    ["Harira Soup", 4.00],
    ["Pastilla (Chicken)", 6.50]
]

drinks_menu = [
    ["Moroccan Coffee", 2.50],
    ["Moroccan Mint Tea", 2.00],
    ["Mango Juice", 3.00],
    ["Fresh Orange Juice", 2.50],
    ["Hawai Tropical", 1.50]
]

desserts_menu = [
    ["Msemen with Honey", 2.50],
    ["Briwat (Pastry with Almonds)", 3.00],
    ["Chebakia (Sesame Pastry)", 2.80]
]

order = []
discount_code = "LOYALTY10"  
discount_percentage = 0.10  

def add_to_order(item, category):
    order.append(item)
    update_order_display()
    messagebox.showinfo("Added", f"Added {item[0]} to your order.")

def remove_from_order(item):
    order.remove(item)
    update_order_display()

def update_order_display():
    for widget in order_frame.winfo_children():
        widget.destroy()
    
    for item in order:
        label = tk.Label(order_frame, text=f"{item[0]} - £{item[1]:.2f}", font=("Arial", 12))
        label.pack()
        
        remove_button = tk.Button(order_frame, text="Remove", width=10, height=1, 
                                  command=lambda item=item: remove_from_order(item))
        remove_button.pack(pady=2)

def apply_loyalty_discount(total_cost):
    return total_cost * (1 - discount_percentage)

def generate_receipt_text():
    total_cost = 0
    receipt_text = (
        "-------------------------------\n"
        "        QuickBite Receipt\n"
        "-------------------------------\n\n"
        "Items Ordered:\n"
        "-------------------------------\n"
    )
    
    for item in order:
        receipt_text += f"{item[0]:<30} £{item[1]:>6.2f}\n"
        total_cost += item[1]
    
    total_cost_with_discount = total_cost
    receipt_text += (
        "-------------------------------\n"
        f"Total Cost:                   £{total_cost:>6.2f}\n"
    )
    
    if loyalty_discount_var.get() == 1:
        total_cost_with_discount = apply_loyalty_discount(total_cost)
        receipt_text += f"Discount (10%):               -£{(total_cost * discount_percentage):>6.2f}\n"
    
    receipt_text += (
        f"Total After Discount:         £{total_cost_with_discount:>6.2f}\n"
        "-------------------------------\n"
        "Thank you for your order!\n"
        "-------------------------------\n"
    )
    
    return receipt_text

def print_receipt():
    if not order:
        messagebox.showinfo("Your Order", "Your order is empty.")
        return
    
    receipt_text = generate_receipt_text()
    
    file_name = "receipt.txt"
    with open(file_name, "w") as f:
        f.write(receipt_text)
    
    messagebox.showinfo("Receipt Saved", f"Your receipt has been saved as {file_name}.")

def confirm_and_display_bill():
    if not order:
        messagebox.showinfo("Your Order", "Your order is empty.")
        return
    
    confirm = messagebox.askyesno("Confirm Order", "Do you want to confirm your order?")
    
    if confirm:
        receipt_text = generate_receipt_text()
        messagebox.showinfo("Final Bill", receipt_text)
        
        save_confirmation = messagebox.askyesno("Save Receipt", "Do you want to save the receipt as a file?")
        if save_confirmation:
            print_receipt()

        order.clear()
        update_order_display()
    else:
        messagebox.showinfo("Order Cancelled", "Your order was not confirmed.")

def create_buttons(menu, category):
    for index, item in enumerate(menu, start=1):
        button = tk.Button(menu_frame, text=f"{item[0]} - £{item[1]:.2f}", 
                           width=30, height=2, 
                           command=lambda item=item, category=category: add_to_order(item, category))
        button.pack(pady=5)

def show_menu(category):
    for widget in menu_frame.winfo_children():
        widget.destroy()  
    
    if category == "Dishes":
        create_buttons(dishes_menu, category)
    elif category == "Drinks":
        create_buttons(drinks_menu, category)
    elif category == "Desserts":
        create_buttons(desserts_menu, category)

def category_selection(category):
    show_menu(category)

def apply_discount_option():
    if loyalty_discount_var.get() == 1:
        messagebox.showinfo("Loyalty Discount", "A 10% loyalty discount has been applied.")
    else:
        messagebox.showinfo("Loyalty Discount", "No loyalty discount applied.")

def clear_order():
    global order
    order.clear()
    update_order_display()
    messagebox.showinfo("Order Cleared", "Your order has been cleared.")

root = tk.Tk()
root.title("Food Ordering System")

label = tk.Label(root, text="Welcome to QuickBite Food Ordering!", font=("Arial", 16))
label.pack(pady=10)

menu_buttons_frame = tk.Frame(root)
menu_buttons_frame.pack(pady=10)

dishes_button = tk.Button(menu_buttons_frame, text="Dishes", width=15, height=2, 
                          command=lambda: category_selection("Dishes"))
dishes_button.grid(row=0, column=0, padx=10)

drinks_button = tk.Button(menu_buttons_frame, text="Drinks", width=15, height=2, 
                          command=lambda: category_selection("Drinks"))
drinks_button.grid(row=0, column=1, padx=10)

desserts_button = tk.Button(menu_buttons_frame, text="Desserts", width=15, height=2, 
                            command=lambda: category_selection("Desserts"))
desserts_button.grid(row=0, column=2, padx=10)

menu_frame = tk.Frame(root)
menu_frame.pack(pady=10)

order_frame = tk.Frame(root)
order_frame.pack(pady=10)

loyalty_discount_var = tk.IntVar()
loyalty_check_button = tk.Checkbutton(root, text="Apply Loyalty Card (10% Discount)", 
                                      variable=loyalty_discount_var, command=apply_discount_option)
loyalty_check_button.pack(pady=10)

bill_button = tk.Button(root, text="Confirm and Display Bill", width=20, height=2, command=confirm_and_display_bill)
bill_button.pack(pady=10)

clear_button = tk.Button(root, text="Clear Order", width=20, height=2, command=clear_order)
clear_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", width=20, height=2, command=root.quit)
exit_button.pack(pady=10)

root.mainloop()
