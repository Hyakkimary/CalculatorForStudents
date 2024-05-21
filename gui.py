import tkinter as tk
from tkinter import ttk
from calculations import calculate_ratings


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Rating System")
        self.root.geometry("800x600")  # Initial window size

        self.students = []
        self.num_students = tk.IntVar()
        self.num_subjects = tk.IntVar()
        self.subject_names = []

        self.create_initial_entries()

    def create_initial_entries(self):
        tk.Label(self.root, text="Кількість студентів").grid(row=0, column=0, sticky='w')
        tk.Entry(self.root, textvariable=self.num_students).grid(row=0, column=1, sticky='ew')

        tk.Label(self.root, text="Кількість дисциплін").grid(row=1, column=0, sticky='w')
        tk.Entry(self.root, textvariable=self.num_subjects).grid(row=1, column=1, sticky='ew')

        tk.Button(self.root, text="Далі", command=self.create_subject_entries).grid(row=2, column=0, columnspan=2,
                                                                                    sticky='ew')

        self.root.grid_columnconfigure(1, weight=1)

    def create_subject_entries(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.subject_entries = []
        for i in range(self.num_subjects.get()):
            tk.Label(self.root, text=f"Назва дисципліни {i + 1}").grid(row=i, column=0, sticky='w')
            entry = tk.Entry(self.root)
            entry.grid(row=i, column=1, sticky='ew')
            self.subject_entries.append(entry)

        tk.Button(self.root, text="Далі", command=self.create_student_table).grid(row=self.num_subjects.get(), column=0,
                                                                                  columnspan=2, sticky='ew')

        self.root.grid_columnconfigure(1, weight=1)

    def create_student_table(self):
        self.subject_names = [entry.get() for entry in self.subject_entries]
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")

        canvas = tk.Canvas(frame)
        canvas.grid(row=0, column=0, sticky="nsew")

        v_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        v_scrollbar.grid(row=0, column=1, sticky="ns")

        h_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        table_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=table_frame, anchor="nw")

        # Configuring columns to expand with the window
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        for j in range(self.num_subjects.get() + 2):
            table_frame.grid_columnconfigure(j, weight=1)

        # Creating header
        tk.Label(table_frame, text="ПІБ").grid(row=0, column=0, sticky='ew')
        for j, subject in enumerate(self.subject_names):
            tk.Label(table_frame, text=subject).grid(row=0, column=j + 1, sticky='ew')
        tk.Label(table_frame, text="Додаткові бали").grid(row=0, column=len(self.subject_names) + 1, sticky='ew')

        self.student_entries = []
        for i in range(self.num_students.get()):
            row = []
            name_entry = tk.Entry(table_frame)
            name_entry.grid(row=i + 1, column=0, sticky='ew')
            row.append(name_entry)

            for j in range(self.num_subjects.get()):
                score_entry = tk.Entry(table_frame)
                score_entry.grid(row=i + 1, column=j + 1, sticky='ew')
                row.append(score_entry)

            extra_points_entry = tk.Entry(table_frame)
            extra_points_entry.grid(row=i + 1, column=self.num_subjects.get() + 1, sticky='ew')
            row.append(extra_points_entry)

            self.student_entries.append(row)

        tk.Button(self.root, text="Обчислити рейтинги", command=self.calculate_ratings).grid(row=2, column=0,
                                                                                             columnspan=2, sticky='ew')

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def calculate_ratings(self):
        self.students = []  # Clear previous student data
        for row in self.student_entries:
            name = row[0].get()
            scores = [float(entry.get()) for entry in row[1:-1] if entry.get()]
            extra_points = float(row[-1].get() if row[-1].get() else 0)

            student = {"name": name, "scores": scores, "extra_points": extra_points}
            self.students.append(student)

        results = calculate_ratings(self.students)

        result_window = tk.Toplevel(self.root)
        result_window.title("Результати")
        tk.Label(result_window, text=results).pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
