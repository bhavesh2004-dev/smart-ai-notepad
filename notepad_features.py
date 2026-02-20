import threading
from sympy import *
from sympy.parsing.sympy_parser import *
from tkinter.messagebox import showerror, showinfo
import numpy as np
import matplotlib.pyplot as plt
from sympy.abc import x, y
from sympy.utilities.lambdify import lambdify
import webbrowser
from api import Chat
import math
from tkinter import simpledialog, messagebox, filedialog, Toplevel, Button, Checkbutton, IntVar
import pandas as pd
import io
import re



def is_math_expression(s):
    """
    Validate if the string resembles a solvable mathematical expression.
    Allows variables, equations, functions.
    """
    # Only allow letters, digits, operators, parentheses, spaces, underscores, commas, and dots
    if not re.fullmatch(r"[A-Za-z0-9+\-*/^=().\s_,]+", s):
        return False

    # Reject plain words (no numbers, no parentheses, no operators)
    if re.fullmatch(r"[A-Za-z\s_]+", s):
        return False

    # If it's an equation, skip sympify validation — we'll parse later
    if "=" in s:
        return True

    # For single expressions (no '='), try parsing with sympy
    try:
        last_line = s.strip().split("\n")[-1]
        sympify(last_line)
        return True
    except SympifyError:
        return False




class NotepadFeatures:
    def _init_(self, text_area):
        self.text_area = text_area
        self.textArea = text_area

    # ------------------ Utility: Thread wrapper ------------------ #
    def run_in_thread(self, target, *args):
        t = threading.Thread(target=target, args=args, daemon=True)
        t.start()

    # ------------------ Solve Selection ------------------ #
    def solveSelection(self):
        self.run_in_thread(self._solveSelection_impl)

    def _solveSelection_impl(self):
        try:
            # Get the selected text
            selected_text = self.text_area.get("sel.first", "sel.last").strip()

            # ✅ Validate before solving
            if not is_math_expression(selected_text):
                self.text_area.after(
                    0,
                    lambda: showerror(
                        "Invalid Selection",
                        "Please select a valid expression or equation."
                    )
                )
                return

            # Support multi-line definitions
            lines = selected_text.split('\n')

            # Environment for math functions/variables
            env = {
                "sin": sin, "cos": cos, "tan": tan, "sqrt": sqrt,
                "exp": math.exp, "pi": pi, "ln": log,
                "log": lambda x, b=E: log(x, b),
                "log10": lambda x: log(x, 10), "log2": lambda x: log(x, 2),
            }
            transformations = standard_transformations + (implicit_multiplication_application,)

            # Assign variables from earlier lines
            for line in lines[:-1]:
                if '=' in line:
                    var, val = line.split('=')
                    env[var.strip()] = parse_expr(
                        val.strip(),
                        local_dict=env,
                        transformations=transformations
                    ).evalf()

            final_expr = lines[-1].strip()

            # Solve
            if '=' in final_expr:
                lhs, rhs = final_expr.split('=')
                lhs_expr = parse_expr(lhs.strip(), local_dict=env, transformations=transformations)
                rhs_expr = parse_expr(rhs.strip(), local_dict=env, transformations=transformations)
                expr = Eq(lhs_expr, rhs_expr)
                symbols_in_expr = list(expr.free_symbols)
                if not symbols_in_expr:
                    raise ValueError("No variable found to solve for.")
                result = solve(expr, symbols_in_expr)
            else:
                result = parse_expr(final_expr, local_dict=env, transformations=transformations).evalf()

            # Insert the result below the selection
            def insert_result():
                index = self.text_area.index("sel.last")
                self.text_area.insert(index, f"\n# {final_expr} = {result}")

            self.text_area.after(0, insert_result)

        except Exception as e:
            error_message = str(e)  # Fix for 'e' scope issue
            self.text_area.after(
                0,
                lambda msg=error_message: showerror(
                    "Solve Error",
                    f"Could not solve expression:\n{msg}"
                )
            )


   

   

    # ------------------ Chatbot ------------------ #
    def chatbotSelection(self):
        self.run_in_thread(self._chatbotSelection_impl)

    def _chatbotSelection_impl(self):
        try:
            selected = self.text_area.get("sel.first", "sel.last")
            result = Chat(selected)
            def insert_result():
                self.text_area.insert("insert", f"\nChatbot: {result}\n")
            self.text_area.after(0, insert_result)
        except Exception as e:
            self.text_area.after(0, lambda: showerror("Chatbot Error", f"Could not get chatbot response:\n{e}"))

    # ------------------ Google Search ------------------ #
    def googleSelection(self):
        try:
            selected = self.text_area.get("sel.first", "sel.last")
            webbrowser.open(f"https://www.google.com/search?q={selected}")
        except:
            self.text_area.after(0, lambda: showerror("Google Search", "Please select some text to search."))

    # ------------------ YouTube Search ------------------ #
    def youtubeSelection(self):
        try:
            selected = self.text_area.get("sel.first", "sel.last")
            webbrowser.open(f"https://www.youtube.com/results?search_query={selected}")
        except:
            self.text_area.after(0, lambda: showerror("YouTube Search", "Please select some text to search."))




 # ------------------ Plot Data Selection from CSV text ------------------ #
    def plot_data_selection(self, chart_type, selected_text):
        self.run_in_thread(self._plot_data_selection_impl, chart_type, selected_text)

    def _plot_data_selection_impl(self, chart_type, selected_text):
        try:
            df = pd.read_csv(io.StringIO(selected_text))
        except Exception as e:
            self.text_area.after(0, lambda: messagebox.showerror("Data Parsing Error", f"Unable to parse selected data:\n{e}"))
            return

        def ui_plot():
            try:
                plt.close('all')

                if chart_type == "bar":
                    df.plot(kind="bar")
                    plt.title("Bar Chart")

                elif chart_type == "pie":
                    if df.shape[1] < 2:
                        df.iloc[0].plot(kind="pie", autopct='%1.1f%%')
                    else:
                        df_ = df.set_index(df.columns[0])
                        df_.iloc[:, 0].plot(kind="pie", autopct='%1.1f%%')
                    plt.title("Pie Chart")

                elif chart_type == "scatter":
                    if df.shape[1] < 2:
                        messagebox.showerror("Scatter Plot Error", "Scatter plot requires at least two columns.")
                        return
                    df.plot(kind="scatter", x=df.columns[0], y=df.columns[1])
                    plt.title("Scatter Plot")

                elif chart_type == "heatmap":
                    try:
                        import seaborn as sns
                    except ImportError:
                        messagebox.showerror("Missing Dependency", "Seaborn is required for heatmap plots.\nInstall with: pip install seaborn")
                        return
                    plt.figure()
                    sns.heatmap(df, annot=True, cmap='viridis')
                    plt.title("Heatmap")

                elif chart_type == "line":
                    df.plot(kind="line")
                    plt.title("Line Graph")

                elif chart_type == "box":
                    df.plot(kind="box")
                    plt.title("Box Plot")

                else:
                    messagebox.showerror("Unknown Chart Type", f"Unknown chart type: {chart_type}")
                    return

                plt.xlabel("Index")
                plt.ylabel("Values")
                plt.tight_layout()
                plt.show()
                plt.close()
            except Exception as e:
                messagebox.showerror("Plotting Error", f"An error occurred during plotting:\n{e}")

        self.text_area.after(0, ui_plot)

    # ------------------ File Import ------------------ #
    def import_file_with_column_selection(self):
        self.run_in_thread(self._import_file_with_column_selection_impl)

    def _import_file_with_column_selection_impl(self):
        file_path = filedialog.askopenfilename(
            title="Select file to import",
            filetypes=[
                ("Excel Files", "*.xlsx *.xls"),
                ("CSV Files", "*.csv"),
                ("JSON Files", "*.json")
            ]
        )
        if not file_path:
            return

        try:
            if file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            elif file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.json'):
                df = pd.read_json(file_path)
            else:
                self.text_area.after(0, lambda: messagebox.showerror("Unsupported File", "The selected file format is not supported."))
                return
        except Exception as e:
            self.text_area.after(0, lambda: messagebox.showerror("Import Error", f"Could not read file:\n{e}"))
            return

        def show_column_selection():
            cols = df.columns.tolist()
            popup = Toplevel()
            popup.title("Select Columns to Import")
            popup.geometry("300x400")
            popup.grab_set()

            vars = []
            for col in cols:
                var = IntVar(value=1)
                chk = Checkbutton(popup, text=col, variable=var)
                chk.pack(anchor='w')
                vars.append((var, col))

            def on_import():
                chosen_cols = [col for (var, col) in vars if var.get() == 1]
                if not chosen_cols:
                    messagebox.showerror("Selection Error", "Please select at least one column.")
                    return
                popup.destroy()
                try:
                    filtered_df = df[chosen_cols]
                    data_str = filtered_df.to_csv(index=False)
                    self.textArea.delete("1.0", "end")
                    self.textArea.insert("1.0", data_str)
                except Exception as e:
                    messagebox.showerror("Import Error", f"Could not import selected columns:\n{e}")

            Button(popup, text="Import", command=on_import).pack(pady=10)
            Button(popup, text="Cancel", command=popup.destroy).pack()

        self.text_area.after(0, show_column_selection)









 # ------------------ Plot Selected Math Expression or Equation ------------------ #
    def plotSelection(self):
        self.run_in_thread(self._plotSelection_impl)

    def _plotSelection_impl(self):
        try:
            selected_text = self.text_area.get("sel.first", "sel.last").strip()
            if not selected_text:
                self.text_area.after(0, lambda: showerror("Plot Error", "Please select an equation or expression."))
                return

            selected_text = selected_text.replace("^", "**")
            env = {
                "sin": sin,
                "cos": cos,
                "tan": tan,
                "log": log,
                "sqrt": sqrt,
                "exp": math.exp,
                "pi": pi
            }

            transformations = standard_transformations + (implicit_multiplication_application,)

            if "=" in selected_text:
                lhs, rhs = selected_text.split("=")
                lhs_expr = parse_expr(lhs.strip(), local_dict=env, transformations=transformations)
                rhs_expr = parse_expr(rhs.strip(), local_dict=env, transformations=transformations)
                equation = Eq(lhs_expr, rhs_expr)

                x_vals = np.linspace(-10, 10, 400)
                y_vals = np.linspace(-10, 10, 400)
                X, Y = np.meshgrid(x_vals, y_vals)
                f_lambdified = lambdify((x, y), lhs_expr - rhs_expr, modules=["numpy"])
                try:
                    Z = f_lambdified(X, Y)
                except:
                    self.text_area.after(0, lambda: showerror("Plot Error", "Could not evaluate the equation over grid."))
                    return

                def ui_plot():
                    plt.figure(figsize=(6, 4))
                    plt.contour(X, Y, Z, levels=[0], colors="blue")
                    plt.title(f"Graph of: {selected_text}")
                    plt.xlabel("x")
                    plt.ylabel("y")
                    plt.grid(True)
                    plt.tight_layout()
                    plt.show()

                self.text_area.after(0, ui_plot)

            else:
                y_expr = parse_expr(selected_text, local_dict=env, transformations=transformations)
                f = lambdify(x, y_expr, modules=["numpy"])

                x_vals = np.linspace(-10, 10, 400)
                try:
                    y_vals = f(x_vals)
                except:
                    x_vals = np.linspace(0.1, 10, 400)
                    y_vals = f(x_vals)

                def ui_plot():
                    plt.figure(figsize=(6, 4))
                    plt.plot(x_vals, y_vals, label=f"y = {selected_text}")
                    plt.title(f"Graph of y = {selected_text}")
                    plt.xlabel("x")
                    plt.ylabel("y")
                    plt.grid(True)
                    plt.legend()
                    plt.tight_layout()
                    plt.show()

                self.text_area.after(0, ui_plot)

        except Exception as e:
            self.text_area.after(0, lambda: showerror("Plot Error", f"Could not plot expression:\n{e}"))