import tkinter as tk
import match_scraping as ms
import image_composing as ic

def fill_options():
    my_list.delete(0, tk.END)
    for (i, opt) in enumerate(current_options):
        my_list.insert(tk.END, opt)
        if opt in selected_options:
            my_list.itemconfig(i, {'bg': 'lightblue'})

def update_entry(e):
    my_entry.delete(0, tk.END)
    active_option = my_list.get(tk.ANCHOR)
    my_entry.insert(0, active_option)

    if active_option not in selected_options:
        selected_options.append(active_option)
    else:
        selected_options.remove(active_option)

    fill_options()


def update_options(e):
    global current_options

    typed_text = my_entry.get()
    t_size = len(typed_text)
    current_options = [opt for opt in options if (typed_text.upper() == opt[0:t_size].upper())]

    fill_options()

options = ms.all_teams

if __name__ == "__main__":
    current_options = options.copy()
    selected_options = options.copy()

    root = tk.Tk()
    root.title("Match Retriever V0.9")
    root.iconbitmap('logos/field.ico')
    root.geometry("500x400")

    # Creating a label
    my_label = tk.Label(root, text="Search for a team", font=("Helvetica", 14))
    my_label.pack()

    # Creating our entry box
    my_entry = tk.Entry(root, font=("Helvetica", 20))
    my_entry.pack()

    # Creating our listbox
    my_list = tk.Listbox(root, width=60)
    my_list.pack(pady=40)

    # Adding the options
    fill_options()

    # Quando se clica num item da lista, 
    my_list.bind("<<ListboxSelect>>", update_entry)
    my_entry.bind("<KeyRelease>", update_options)

    generateImage = tk.Button(root, text="Generate an image", bg="lightblue", fg="black",
                              command=lambda: ic.get_image(selected_options))
    generateImage.pack()

    root.mainloop()
