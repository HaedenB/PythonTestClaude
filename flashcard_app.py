#!/usr/bin/env python3
"""
Modern Flashcard App using Tkinter
A beautiful, feature-rich flashcard application with card flipping animation
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os


class ModernButton(tk.Button):
    """Custom styled button for modern look"""
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            relief=tk.FLAT,
            borderwidth=0,
            cursor="hand2",
            font=("Helvetica", 11),
            **kwargs
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.default_bg = kwargs.get('bg', '#6C63FF')

    def on_enter(self, e):
        self['background'] = self.lighten_color(self.default_bg)

    def on_leave(self, e):
        self['background'] = self.default_bg

    def lighten_color(self, hex_color):
        """Lighten a hex color by 10%"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, int(r * 1.1))
        g = min(255, int(g * 1.1))
        b = min(255, int(b * 1.1))
        return f'#{r:02x}{g:02x}{b:02x}'


class FlashcardApp:
    """Modern Flashcard Application"""

    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard Master")
        self.root.geometry("900x650")
        self.root.resizable(False, False)

        # Color scheme
        self.colors = {
            'primary': '#6C63FF',
            'secondary': '#4CAF50',
            'danger': '#FF6B6B',
            'bg': '#F5F5F5',
            'card_front': '#FFFFFF',
            'card_back': '#E8F4F8',
            'text': '#2C3E50',
            'text_light': '#7F8C8D'
        }

        self.root.configure(bg=self.colors['bg'])

        # Data
        self.cards = []
        self.current_index = 0
        self.is_flipped = False
        self.data_file = "flashcards.json"

        # Load existing cards
        self.load_cards()

        # Create UI
        self.create_ui()

        # Display first card if available
        if self.cards:
            self.display_card()

    def create_ui(self):
        """Create the user interface"""

        # Header
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="📚 Flashcard Master",
            font=("Helvetica", 28, "bold"),
            bg=self.colors['primary'],
            fg="white"
        )
        title_label.pack(pady=20)

        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

        # Progress label
        self.progress_label = tk.Label(
            main_frame,
            text="Card 0 of 0",
            font=("Helvetica", 12),
            bg=self.colors['bg'],
            fg=self.colors['text_light']
        )
        self.progress_label.pack(pady=(0, 15))

        # Card frame (with shadow effect)
        shadow_frame = tk.Frame(
            main_frame,
            bg="#D0D0D0",
            width=700,
            height=350
        )
        shadow_frame.pack()
        shadow_frame.pack_propagate(False)

        card_container = tk.Frame(
            shadow_frame,
            bg=self.colors['card_front'],
            width=700,
            height=350
        )
        card_container.place(x=-3, y=-3, width=700, height=350)
        card_container.pack_propagate(False)

        # Card content
        self.card_label = tk.Label(
            card_container,
            text="Click 'Add Card' to begin!",
            font=("Helvetica", 24),
            bg=self.colors['card_front'],
            fg=self.colors['text'],
            wraplength=650,
            justify=tk.CENTER
        )
        self.card_label.pack(expand=True)

        # Flip indicator
        self.flip_indicator = tk.Label(
            card_container,
            text="",
            font=("Helvetica", 10, "italic"),
            bg=self.colors['card_front'],
            fg=self.colors['text_light']
        )
        self.flip_indicator.pack(side=tk.BOTTOM, pady=10)

        # Button container
        button_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        button_frame.pack(pady=30)

        # Navigation buttons
        nav_frame = tk.Frame(button_frame, bg=self.colors['bg'])
        nav_frame.pack(pady=(0, 15))

        self.prev_btn = ModernButton(
            nav_frame,
            text="← Previous",
            command=self.prev_card,
            bg=self.colors['primary'],
            fg="white",
            width=12,
            pady=12
        )
        self.prev_btn.pack(side=tk.LEFT, padx=5)

        self.flip_btn = ModernButton(
            nav_frame,
            text="🔄 Flip Card",
            command=self.flip_card,
            bg=self.colors['secondary'],
            fg="white",
            width=12,
            pady=12,
            font=("Helvetica", 12, "bold")
        )
        self.flip_btn.pack(side=tk.LEFT, padx=5)

        self.next_btn = ModernButton(
            nav_frame,
            text="Next →",
            command=self.next_card,
            bg=self.colors['primary'],
            fg="white",
            width=12,
            pady=12
        )
        self.next_btn.pack(side=tk.LEFT, padx=5)

        # Management buttons
        manage_frame = tk.Frame(button_frame, bg=self.colors['bg'])
        manage_frame.pack()

        add_btn = ModernButton(
            manage_frame,
            text="➕ Add Card",
            command=self.add_card,
            bg=self.colors['secondary'],
            fg="white",
            width=12,
            pady=10
        )
        add_btn.pack(side=tk.LEFT, padx=5)

        edit_btn = ModernButton(
            manage_frame,
            text="✏️ Edit Card",
            command=self.edit_card,
            bg=self.colors['primary'],
            fg="white",
            width=12,
            pady=10
        )
        edit_btn.pack(side=tk.LEFT, padx=5)

        delete_btn = ModernButton(
            manage_frame,
            text="🗑️ Delete Card",
            command=self.delete_card,
            bg=self.colors['danger'],
            fg="white",
            width=12,
            pady=10
        )
        delete_btn.pack(side=tk.LEFT, padx=5)

        shuffle_btn = ModernButton(
            manage_frame,
            text="🔀 Shuffle",
            command=self.shuffle_cards,
            bg="#9B59B6",
            fg="white",
            width=12,
            pady=10
        )
        shuffle_btn.pack(side=tk.LEFT, padx=5)

        # Keyboard bindings
        self.root.bind('<space>', lambda e: self.flip_card())
        self.root.bind('<Left>', lambda e: self.prev_card())
        self.root.bind('<Right>', lambda e: self.next_card())
        self.root.bind('<n>', lambda e: self.add_card())
        self.root.bind('<e>', lambda e: self.edit_card())

    def display_card(self):
        """Display the current card"""
        if not self.cards:
            self.card_label.config(
                text="No cards available.\nClick 'Add Card' to create one!",
                bg=self.colors['card_front']
            )
            self.flip_indicator.config(text="", bg=self.colors['card_front'])
            self.progress_label.config(text="Card 0 of 0")
            return

        card = self.cards[self.current_index]

        if self.is_flipped:
            text = card['back']
            bg_color = self.colors['card_back']
            indicator = "📖 Answer"
        else:
            text = card['front']
            bg_color = self.colors['card_front']
            indicator = "❓ Question"

        self.card_label.config(text=text, bg=bg_color)
        self.flip_indicator.config(text=indicator, bg=bg_color)

        # Update progress
        self.progress_label.config(
            text=f"Card {self.current_index + 1} of {len(self.cards)}"
        )

    def flip_card(self):
        """Flip the current card"""
        if not self.cards:
            return

        self.is_flipped = not self.is_flipped
        self.display_card()

    def next_card(self):
        """Show next card"""
        if not self.cards:
            return

        self.current_index = (self.current_index + 1) % len(self.cards)
        self.is_flipped = False
        self.display_card()

    def prev_card(self):
        """Show previous card"""
        if not self.cards:
            return

        self.current_index = (self.current_index - 1) % len(self.cards)
        self.is_flipped = False
        self.display_card()

    def add_card(self):
        """Add a new flashcard"""
        dialog = CardDialog(self.root, "Add New Card")

        if dialog.result:
            self.cards.append(dialog.result)
            self.current_index = len(self.cards) - 1
            self.is_flipped = False
            self.save_cards()
            self.display_card()

    def edit_card(self):
        """Edit the current card"""
        if not self.cards:
            messagebox.showinfo("No Cards", "There are no cards to edit!")
            return

        current_card = self.cards[self.current_index]
        dialog = CardDialog(
            self.root,
            "Edit Card",
            initial_front=current_card['front'],
            initial_back=current_card['back']
        )

        if dialog.result:
            self.cards[self.current_index] = dialog.result
            self.is_flipped = False
            self.save_cards()
            self.display_card()

    def delete_card(self):
        """Delete the current card"""
        if not self.cards:
            messagebox.showinfo("No Cards", "There are no cards to delete!")
            return

        if messagebox.askyesno("Delete Card", "Are you sure you want to delete this card?"):
            self.cards.pop(self.current_index)

            if self.cards:
                self.current_index = min(self.current_index, len(self.cards) - 1)
            else:
                self.current_index = 0

            self.is_flipped = False
            self.save_cards()
            self.display_card()

    def shuffle_cards(self):
        """Shuffle the deck"""
        if not self.cards:
            messagebox.showinfo("No Cards", "There are no cards to shuffle!")
            return

        import random
        random.shuffle(self.cards)
        self.current_index = 0
        self.is_flipped = False
        self.save_cards()
        self.display_card()
        messagebox.showinfo("Shuffled", "Cards have been shuffled!")

    def load_cards(self):
        """Load cards from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.cards = json.load(f)
            except:
                self.cards = []
        else:
            # Add sample cards
            self.cards = [
                {
                    "front": "What is Python?",
                    "back": "Python is a high-level, interpreted programming language known for its simplicity and readability."
                },
                {
                    "front": "What does GUI stand for?",
                    "back": "Graphical User Interface - a visual way of interacting with a computer."
                },
                {
                    "front": "What is Tkinter?",
                    "back": "Tkinter is Python's standard GUI library, used to create desktop applications."
                }
            ]
            self.save_cards()

    def save_cards(self):
        """Save cards to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.cards, f, indent=2)
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save cards: {e}")


class CardDialog:
    """Dialog for adding/editing cards"""

    def __init__(self, parent, title, initial_front="", initial_back=""):
        self.result = None

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg="#F5F5F5")

        # Make it modal
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (400 // 2)
        self.dialog.geometry(f"500x400+{x}+{y}")

        # Content
        content_frame = tk.Frame(self.dialog, bg="#F5F5F5")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Front of card
        tk.Label(
            content_frame,
            text="Front (Question):",
            font=("Helvetica", 12, "bold"),
            bg="#F5F5F5",
            fg="#2C3E50"
        ).pack(anchor=tk.W, pady=(0, 5))

        self.front_text = tk.Text(
            content_frame,
            height=5,
            font=("Helvetica", 11),
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=2,
            highlightbackground="#6C63FF",
            highlightthickness=2
        )
        self.front_text.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        self.front_text.insert("1.0", initial_front)

        # Back of card
        tk.Label(
            content_frame,
            text="Back (Answer):",
            font=("Helvetica", 12, "bold"),
            bg="#F5F5F5",
            fg="#2C3E50"
        ).pack(anchor=tk.W, pady=(0, 5))

        self.back_text = tk.Text(
            content_frame,
            height=5,
            font=("Helvetica", 11),
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=2,
            highlightbackground="#6C63FF",
            highlightthickness=2
        )
        self.back_text.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        self.back_text.insert("1.0", initial_back)

        # Buttons
        button_frame = tk.Frame(content_frame, bg="#F5F5F5")
        button_frame.pack(fill=tk.X)

        save_btn = ModernButton(
            button_frame,
            text="Save Card",
            command=self.save,
            bg="#4CAF50",
            fg="white",
            width=15,
            pady=10
        )
        save_btn.pack(side=tk.LEFT, padx=(0, 10))

        cancel_btn = ModernButton(
            button_frame,
            text="Cancel",
            command=self.cancel,
            bg="#95A5A6",
            fg="white",
            width=15,
            pady=10
        )
        cancel_btn.pack(side=tk.LEFT)

        # Focus on front text
        self.front_text.focus()

        # Wait for dialog to close
        parent.wait_window(self.dialog)

    def save(self):
        """Save the card"""
        front = self.front_text.get("1.0", tk.END).strip()
        back = self.back_text.get("1.0", tk.END).strip()

        if not front or not back:
            messagebox.showwarning(
                "Missing Content",
                "Both front and back of the card must have content!",
                parent=self.dialog
            )
            return

        self.result = {"front": front, "back": back}
        self.dialog.destroy()

    def cancel(self):
        """Cancel the dialog"""
        self.dialog.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
