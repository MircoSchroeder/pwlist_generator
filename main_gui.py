import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading # Optional: For better UI responsiveness in future, but keeping synchronous per requirements
from generator_logic import PasswordGeneratorLogic

class PasswordGeneratorApp:
    """
    Main GUI Class for the Password List Generator.
    Handles user interaction and delegates logic to PasswordGeneratorLogic.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Password List Generator")
        self.root.geometry("700x850")
        
        self.logic = PasswordGeneratorLogic()
        
        # --- Initialize Variables ---
        self.num_lists = tk.IntVar(value=2)
        self.min_length = tk.IntVar()
        self.max_length = tk.IntVar()
        self.order = tk.StringVar()
        self.insert_option = tk.BooleanVar()
        self.insert_chars_type = tk.StringVar()
        self.num_insertions = tk.IntVar(value=1)
        self.generate_all = tk.BooleanVar(value=True)
        self.specific_num = tk.IntVar()
        self.output_file = tk.StringVar()
        
        self.progress = None
        
        self.create_widgets()
    
    def create_widgets(self):
        """Constructs the GUI elements."""
        # Main Layout with Scrollbar
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(main_frame)
        canvas.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Mousewheel binding
        canvas.bind_all("<MouseWheel>", lambda event: self._on_mousewheel(event, canvas))
        canvas.bind_all("<Button-4>", lambda event: self._on_mousewheel(event, canvas))
        canvas.bind_all("<Button-5>", lambda event: self._on_mousewheel(event, canvas))
        
        inner_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="center")
        
        # --- Section 0: Output File ---
        frame0 = ttk.LabelFrame(inner_frame, text="0. Select Output File")
        frame0.pack(padx=10, pady=10, fill="x")
        
        output_frame = ttk.Frame(frame0)
        output_frame.pack(pady=5, padx=5, fill="x")
        
        ttk.Label(output_frame, text="Target File:").pack(side="left", padx=5)
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_file)
        self.output_entry.pack(side="left", padx=5, fill="x", expand=True)
        browse_btn = ttk.Button(output_frame, text="Browse", command=self.browse_output_file)
        browse_btn.pack(side="left", padx=5)
        
        # --- Section 1: Number of Lists ---
        frame1 = ttk.LabelFrame(inner_frame, text="1. Select Number of Lists")
        frame1.pack(padx=10, pady=10, fill="x")
        
        btn_frame = ttk.Frame(frame1)
        btn_frame.pack(pady=5)
        
        up_btn = ttk.Button(btn_frame, text="▲", width=3, command=self.increase_num_lists)
        up_btn.grid(row=0, column=0, padx=5)
        
        self.num_label = ttk.Label(btn_frame, textvariable=self.num_lists, width=5, anchor="center")
        self.num_label.grid(row=0, column=1)
        
        down_btn = ttk.Button(btn_frame, text="▼", width=3, command=self.decrease_num_lists)
        down_btn.grid(row=0, column=2, padx=5)
        
        # --- Section 2: Load Lists ---
        frame2 = ttk.LabelFrame(inner_frame, text="2. Load Lists")
        frame2.pack(padx=10, pady=10, fill="x")
        
        ttk.Button(frame2, text="Load Word List", command=self.load_words).pack(pady=5, fill="x")
        ttk.Button(frame2, text="Load Number List", command=self.load_numbers).pack(pady=5, fill="x")
        ttk.Button(frame2, text="Load Symbol List", command=self.load_symbols).pack(pady=5, fill="x")
        
        self.loaded_labels = ttk.Label(frame2, text="Loaded Lists: 0")
        self.loaded_labels.pack(pady=5)
        
        # --- Section 3: Password Lengths ---
        frame3 = ttk.LabelFrame(inner_frame, text="3. Set Password Lengths")
        frame3.pack(padx=10, pady=10, fill="x")
        
        ttk.Label(frame3, text="Minimum Length:").pack(pady=5, anchor="w", padx=5)
        ttk.Entry(frame3, textvariable=self.min_length).pack(pady=5, padx=5, fill="x")
        
        ttk.Label(frame3, text="Maximum Length:").pack(pady=5, anchor="w", padx=5)
        ttk.Entry(frame3, textvariable=self.max_length).pack(pady=5, padx=5, fill="x")
        
        # --- Section 4: Element Order ---
        frame4 = ttk.LabelFrame(inner_frame, text="4. Define Element Order")
        frame4.pack(padx=10, pady=10, fill="x")
        
        ttk.Label(frame4, text="Enter order (e.g. word, number, symbol):").pack(pady=5, anchor="w", padx=5)
        ttk.Entry(frame4, textvariable=self.order).pack(pady=5, padx=5, fill="x")
        ttk.Label(frame4, text="Use 'word', 'number', and 'symbol', separated by commas or spaces.").pack(pady=2, anchor="w", padx=5)
        
        # --- Section 5: Insertion Option ---
        frame5 = ttk.LabelFrame(inner_frame, text="5. Option: Inject Characters into Words")
        frame5.pack(padx=10, pady=10, fill="x")
        
        ttk.Checkbutton(frame5, text="Inject characters into words", variable=self.insert_option, command=self.toggle_insert_options).pack(pady=5, anchor="w", padx=5)
        
        insert_frame = ttk.Frame(frame5)
        insert_frame.pack(pady=5, padx=5, fill="x")
        
        ttk.Label(insert_frame, text="Characters to inject:").grid(row=0, column=0, sticky="w")
        self.insert_combo = ttk.Combobox(insert_frame, textvariable=self.insert_chars_type, 
                                         values=["Numbers", "Special Characters", "Both"], state="disabled")
        self.insert_combo.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        
        ttk.Label(insert_frame, text="Insertions per word:").grid(row=1, column=0, sticky="w")
        self.insert_spin = ttk.Spinbox(insert_frame, from_=1, to=10, textvariable=self.num_insertions, state="disabled")
        self.insert_spin.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        
        insert_frame.columnconfigure(1, weight=1)
        
        # --- Section 6: Generation Settings ---
        frame6 = ttk.LabelFrame(inner_frame, text="6. Generation Settings")
        frame6.pack(padx=10, pady=10, fill="x")
        
        gen_opts_frame = ttk.Frame(frame6)
        gen_opts_frame.pack(pady=5, padx=5, fill="x")
        
        ttk.Radiobutton(gen_opts_frame, text="Generate all possible combinations", variable=self.generate_all, value=True, command=self.toggle_generate_options).pack(anchor="w", pady=2, padx=5)
        ttk.Radiobutton(gen_opts_frame, text="Generate specific number of passwords", variable=self.generate_all, value=False, command=self.toggle_generate_options).pack(anchor="w", pady=2, padx=5)
        
        specific_frame = ttk.Frame(frame6)
        specific_frame.pack(pady=5, padx=5, fill="x")
        
        ttk.Label(specific_frame, text="Count:").pack(side="left", padx=5)
        self.specific_entry = ttk.Entry(specific_frame, textvariable=self.specific_num, state="disabled")
        self.specific_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # --- Section 7: Generate & Save ---
        frame7 = ttk.LabelFrame(inner_frame, text="7. Generate and Save")
        frame7.pack(padx=10, pady=10, fill="x")
        
        ttk.Button(frame7, text="Generate Password List", command=self.generate_passwords).pack(pady=10)
        
        self.progress = ttk.Progressbar(frame7, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)
    
    # --- Event Handlers & Helpers ---
    
    def _on_mousewheel(self, event, canvas):
        if event.num == 5 or event.delta == -120:
            canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta == 120:
            canvas.yview_scroll(-1, "units")
    
    def increase_num_lists(self):
        current = self.num_lists.get()
        self.num_lists.set(current + 1)
    
    def decrease_num_lists(self):
        current = self.num_lists.get()
        limit = 1 if self.insert_option.get() else 2
        if current > limit:
            self.num_lists.set(current - 1)
    
    def load_words(self):
        self._load_generic(self.logic.words, "Word List")
        # Need to re-set logic lists because reference might change if reassigned
        self.logic.words = self._load_file_helper("Word List")
        self.update_loaded_labels()

    def load_numbers(self):
        self.logic.numbers = self._load_file_helper("Number List")
        self.update_loaded_labels()

    def load_symbols(self):
        self.logic.symbols = self._load_file_helper("Symbol List")
        self.update_loaded_labels()
        
    def _load_generic(self, target_list, title):
        # Placeholder, actual logic in _load_file_helper to handle assignment cleanly
        pass

    def _load_file_helper(self, title):
        file_path = filedialog.askopenfilename(title=f"Select {title}", filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                return self.logic.load_list_from_file(file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Error loading file:\n{e}")
        return []

    def update_loaded_labels(self):
        required = 1 if self.insert_option.get() else 2
        count = self.logic.get_list_counts()
        self.loaded_labels.config(text=f"Loaded Lists: {count} (minimum {required} required)")
    
    def toggle_insert_options(self):
        if self.insert_option.get():
            self.insert_combo.config(state="readonly")
            self.insert_spin.config(state="normal")
        else:
            self.insert_combo.set('')
            self.insert_combo.config(state="disabled")
            self.insert_spin.config(state="disabled")
        self.update_loaded_labels()
    
    def browse_output_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt")],
                                                 title="Select Output File")
        if file_path:
            self.output_file.set(file_path)
    
    def toggle_generate_options(self):
        if self.generate_all.get():
            self.specific_entry.config(state="disabled")
            self.specific_num.set('')
        else:
            self.specific_entry.config(state="normal")
    
    def generate_passwords(self):
        self.progress['value'] = 0
        
        # --- Validation ---
        output_path = self.output_file.get()
        if not output_path:
            messagebox.showerror("Error", "Please select an output file.")
            return
        
        min_required = 1 if self.insert_option.get() else 2
        if self.logic.get_list_counts() < min_required:
            messagebox.showerror("Error", f"Please load at least {min_required} lists.")
            return
        
        order_input = self.order.get().lower().replace(',', ' ').split()
        valid_elements = {'word', 'number', 'symbol'}
        
        # Simple mapping for user friendliness (handling German habits or typos if needed, 
        # but strictly we expect English now based on UI prompts)
        clean_order = []
        for item in order_input:
            if item in valid_elements:
                clean_order.append(item)
        
        if not clean_order:
            messagebox.showerror("Error", "Please enter a valid order (e.g., 'word number symbol').")
            return
            
        min_len = self.min_length.get() if self.min_length.get() else None
        max_len = self.max_length.get() if self.max_length.get() else None
        
        if min_len and max_len and min_len > max_len:
            messagebox.showerror("Error", "Minimum length cannot be greater than maximum length.")
            return
            
        insert_option = self.insert_option.get()
        insert_chars_list = []
        if insert_option:
            choice = self.insert_chars_type.get()
            insert_chars_list = self.logic.get_insertion_characters(choice)
            if not insert_chars_list:
                messagebox.showerror("Error", "Please select valid characters for injection.")
                return

        num_insertions = self.num_insertions.get()

        # --- Generation Process ---
        generated_passwords = set()
        
        try:
            if self.generate_all.get():
                # ALL COMBINATIONS
                total_combos = self.logic.calculate_total_combinations(clean_order)
                self.progress['maximum'] = total_combos
                
                iterator = self.logic.get_combinations_iterator(clean_order)
                
                for i, combo in enumerate(iterator, start=1):
                    password = ''.join(combo)
                    
                    # Special Logic: If insertion is active, the original code essentially 
                    # regenerated the specific components to inject chars.
                    if insert_option and 'word' in clean_order:
                        password = self.logic.construct_password_with_injection(clean_order, insert_chars_list, num_insertions)
                    
                    pwd_len = len(password)
                    if ((min_len is None or pwd_len >= min_len) and 
                        (max_len is None or pwd_len <= max_len)):
                        generated_passwords.add(password)
                    
                    if i % 1000 == 0 or i == total_combos:
                        self.progress['value'] = i
                        self.root.update_idletasks()

            else:
                # RANDOM SAMPLING
                specific_num = self.specific_num.get()
                if specific_num < 1:
                    messagebox.showerror("Error", "Please enter a valid quantity.")
                    return
                
                max_attempts = specific_num * 10
                self.progress['maximum'] = max_attempts
                attempts = 0
                
                while len(generated_passwords) < specific_num and attempts < max_attempts:
                    pwd = self.logic.generate_random_password(
                        clean_order, insert_option, insert_chars_list, num_insertions,
                        min_len if min_len else 0, max_len if max_len else float('inf')
                    )
                    
                    if pwd:
                        generated_passwords.add(pwd)
                    
                    attempts += 1
                    self.progress['value'] = attempts
                    if attempts % 100 == 0:
                        self.root.update_idletasks()
                
                if len(generated_passwords) < specific_num:
                    messagebox.showwarning("Warning", "Max attempts reached. Some passwords may not have been generated.")

            # --- Saving ---
            with open(output_path, 'w', encoding='utf-8') as f:
                for pwd in generated_passwords:
                    f.write(pwd + '\n')
            
            messagebox.showinfo("Success", f"{len(generated_passwords)} passwords saved to '{output_path}'.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during generation:\n{e}")

def main():
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
