import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from main import PlanetApp
import sys
import io


class PlanetAppGUI:
    """GUI version of the Planet Information System using Tkinter."""

    def __init__(self, planet_app):
        """Initialize the GUI with a reference to the planet app."""
        self.planet_app = planet_app
        self.root = tk.Tk()
        self.root.title("Solar System Information System")
        self.root.geometry("700x500")
        self.root.minsize(600, 400)

        self.create_widgets()

    def create_widgets(self):
        """Create and arrange GUI widgets."""
        # Frame for the entire layout
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title label
        title_label = tk.Label(
            main_frame,
            text="Solar System Information Program",
            font=("Arial", 16, "bold"),
        )
        title_label.pack(pady=(0, 10))

        # Instructions label
        instructions = """
        Ask questions about planets in our solar system.
        
        Examples:
        - Tell me everything about Saturn
        - How massive is Neptune?
        - Is Pluto in the list of planets?
        - How many moons does Earth have?
        """
        instructions_label = tk.Label(
            main_frame, text=instructions, justify=tk.LEFT, anchor="w"
        )
        instructions_label.pack(fill=tk.X, pady=(0, 10))

        # Query input field
        input_frame = tk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))

        query_label = tk.Label(input_frame, text="Your question:")
        query_label.pack(side=tk.LEFT, padx=(0, 5))

        self.query_entry = tk.Entry(input_frame)
        self.query_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.query_entry.bind("<Return>", self.on_submit)

        submit_button = tk.Button(input_frame, text="Ask", command=self.on_submit)
        submit_button.pack(side=tk.LEFT, padx=(5, 0))

        # Response display area
        response_frame = tk.LabelFrame(main_frame, text="Response")
        response_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.response_text = scrolledtext.ScrolledText(
            response_frame, wrap=tk.WORD, font=("Courier", 10)
        )
        self.response_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.response_text.config(state=tk.DISABLED)

        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X)

        clear_button = tk.Button(
            button_frame, text="Clear", command=self.clear_response
        )
        clear_button.pack(side=tk.LEFT)

        planet_list_button = tk.Button(
            button_frame,
            text="List All Planets",
            command=lambda: self.process_special_query("List all planets"),
        )
        planet_list_button.pack(side=tk.LEFT, padx=(10, 0))

        exit_button = tk.Button(button_frame, text="Exit", command=self.root.destroy)
        exit_button.pack(side=tk.RIGHT)

        # Set focus to the entry field
        self.query_entry.focus_set()

    def on_submit(self, event=None):
        """Handle submission of a query."""
        query = self.query_entry.get().strip()

        if not query:
            messagebox.showwarning("Empty Query", "Please enter a question.")
            return

        # Process the query and display the response
        self.process_query(query)

        # Clear the entry field
        self.query_entry.delete(0, tk.END)

    def process_query(self, query):
        """Process a query and display the result."""
        # Get the response from the query processor
        response = self.planet_app.query_processor.process_query(query)

        # Display the query and response
        self.update_response_text(f"Q: {query}\n\n{response}\n\n{'-' * 50}\n\n")

    def process_special_query(self, query):
        """Process a special query triggered by a button."""
        self.query_entry.delete(0, tk.END)
        self.query_entry.insert(0, query)
        self.process_query(query)

    def update_response_text(self, text):
        """Update the response text area with new text."""
        self.response_text.config(state=tk.NORMAL)
        self.response_text.insert(tk.END, text)
        self.response_text.see(tk.END)  # Scroll to the end
        self.response_text.config(state=tk.DISABLED)

    def clear_response(self):
        """Clear the response text area."""
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete(1.0, tk.END)
        self.response_text.config(state=tk.DISABLED)

    def run(self):
        """Run the GUI application."""
        self.root.mainloop()


# This code should be added to main.py or in a separate file
def run_gui(app):
    """Run the GUI version of the application."""
    gui = PlanetAppGUI(app)
    gui.run()


# If you want to add this to the PlanetApp class in main.py, add this method:
def gui_interface(self):
    """Run the GUI interface."""
    gui = PlanetAppGUI(self)
    gui.run()


# Modified main block for main.py to support command line arguments for GUI
if __name__ == "__main__":
    import sys

    app = PlanetApp()
    app.load_data()

    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1].lower() == "--gui":
        # Run GUI interface
        try:
            gui = PlanetAppGUI(app)
            gui.run()
        except ImportError:
            print("GUI extension not found. Running text interface instead.")
            app.text_interface()
    else:
        # Run text interface
        app.text_interface()
