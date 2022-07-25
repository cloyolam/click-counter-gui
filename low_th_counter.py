import argparse
import pickle
import random
import tkinter as tk


def count_characters(name, th, metric):
    count_dict[name][th][metric] += 1


def add_character():
    global n_col, button_label_list, count_dict
    new_label = input("Enter a new label: ")
    metrics = ['TP', 'FN', 'FP']
    if new_label not in count_dict:
        count_dict[new_label] = {}
    column_elems = []
    character_color = "#" + ("%06x" % random.randint(0, 16777215))
    column_elems.append(tk.Label(frame, text=new_label, bg=character_color))
    th_color = "#" + ("%06x" % 10000000)
    for th in ["0.50", "0.30", "0.15"]:
        if new_label not in count_dict:
            count_dict[new_label][th] = {m: 0 for m in metrics}
        column_elems.append(tk.Label(frame, text=th, bg=th_color))
        for ix, metric in enumerate(['TP', 'FN', 'FP']):
            column_elems.append(tk.Button(frame, text=metric,
                                          command=lambda x=[new_label, th, metric]: count_characters(x[0], x[1], x[2])))
        button_label_list.append(column_elems)
    column_elems.append(tk.Button(frame, text="All TP", bg=character_color,
                                  command=lambda x=new_label: all_true_positives(new_label)))
    column_elems.append(tk.Button(frame, text="All FN", bg=character_color,
                                  command=lambda x=new_label: all_false_negatives(new_label)))
    for ix, elem in enumerate(column_elems):
        button_label_list[-1][ix].grid(row=ix, column=n_col, sticky='nsew')
    n_col += 1


def increase_frame_number():
    global frame_number, count_dict
    frame_number += 1
    tk.Label(root, text=f"Frame: {frame_number}", bg="PeachPuff").grid(row=1, column=2, columnspan=1, sticky='nsew')
    print(f"Frame: {frame_number}")
    for name in count_dict:
        print(f"{name}:")
        for th in count_dict[name]:
            print(f"  threshold = {th}")
            print(f"   {count_dict[name][th]}")


def save_dict():
    global count_dict, frame_number
    output_fn = input("Enter output name: ")
    with open(f'{output_fn}_frame-{str(frame_number).zfill(6)}.pkl', 'wb') as f:
        pickle.dump(count_dict, f)


def print_dict():
    global count_dict
    for name in count_dict:
        print(f"{name}:")
        for th in count_dict[name]:
            print(f"  threshold = {th}")
            print(f"   {count_dict[name][th]}")


def all_true_positives(character):
    global count_dict
    for th in count_dict[character]:
        count_dict[character][th]['TP'] += 1


def all_false_negatives(character):
    global count_dict
    for th in count_dict[character]:
        count_dict[character][th]['FN'] += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GUI for characters metrics")
    parser.add_argument("-d", "--load_dict", default=None, help="Load a .pkl dictionary")
    args = parser.parse_args()

    root = tk.Tk()
    n_col = 0
    if args.load_dict is not None:
        frame_number = int(args.load_dict[-10:-4])
        with open(args.load_dict, 'rb') as f:
            count_dict = pickle.load(f)
    else:
        frame_number = 0
        count_dict = {}
    button_label_list = []
    root.title("Characters count")
    root.rowconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)

    frame = tk.Frame(root)
    frame.rowconfigure(1, weight=1)
    frame.grid(row=0, column=3, sticky='nsew', rowspan=3)

    tk.Button(root, text="Add new character", command=add_character).grid(row=0, column=0, sticky='nsew')
    # tk.Button(root, text="Quit!", command=root.quit).grid(row=0, column=1, sticky='nsew')
    tk.Button(root, text="Save dictionary", command=save_dict).grid(row=0, column=2, sticky='nsew')
    tk.Button(root, text="Increase fn", command=increase_frame_number).grid(row=1, column=0, sticky='nsew')

    root.mainloop()
