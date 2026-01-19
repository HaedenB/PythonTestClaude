#!/usr/bin/env python3
"""
Modern Flashcard App using Tkinter
A beautiful, feature-rich flashcard application with modern web-inspired design
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os


class GradientFrame(tk.Canvas):
    """Frame with gradient background"""
    def __init__(self, parent, color1, color2, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.color1 = color1
        self.color2 = color2
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        """Draw gradient on canvas"""
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        limit = height

        # Parse colors
        r1, g1, b1 = self._hex_to_rgb(self.color1)
        r2, g2, b2 = self._hex_to_rgb(self.color2)

        # Draw gradient lines
        for i in range(limit):
            nr = int(r1 + (r2 - r1) * i / limit)
            ng = int(g1 + (g2 - g1) * i / limit)
            nb = int(b1 + (b2 - b1) * i / limit)
            color = f'#{nr:02x}{ng:02x}{nb:02x}'
            self.create_line(0, i, width, i, tags=("gradient",), fill=color)

    def _hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


class ModernButton(tk.Canvas):
    """Modern button with rounded corners and hover effects"""
    def __init__(self, parent, text, command, bg_color, fg_color="white",
                 width=140, height=45, **kwargs):
        super().__init__(parent, width=width, height=height,
                        bg=parent.cget('bg'), highlightthickness=0, **kwargs)

        self.text = text
        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.width = width
        self.height = height
        self.hover_color = self._lighten_color(bg_color)

        self.draw_button(self.bg_color)

        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def draw_button(self, color):
        """Draw rounded rectangle button"""
        self.delete("all")

        # Create rounded rectangle using polygons
        r = 12  # Corner radius
        x0, y0 = 0, 0
        x1, y1 = self.width, self.height

        points = [
            x0+r, y0,
            x1-r, y0,
            x1, y0,
            x1, y0+r,
            x1, y1-r,
            x1, y1,
            x1-r, y1,
            x0+r, y1,
            x0, y1,
            x0, y1-r,
            x0, y0+r,
            x0, y0
        ]

        self.create_polygon(points, fill=color, smooth=True, tags="button")

        # Add text
        self.create_text(
            self.width // 2,
            self.height // 2,
            text=self.text,
            fill=self.fg_color,
            font=("Segoe UI", 11, "bold"),
            tags="text"
        )

    def _on_click(self, event):
        if self.command:
            self.command()

    def _on_enter(self, event):
        self.draw_button(self.hover_color)

    def _on_leave(self, event):
        self.draw_button(self.bg_color)

    def _lighten_color(self, hex_color):
        """Lighten a hex color"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, int(r * 1.15))
        g = min(255, int(g * 1.15))
        b = min(255, int(b * 1.15))
        return f'#{r:02x}{g:02x}{b:02x}'


class RoundedCard(tk.Canvas):
    """Rounded card widget for modern look"""
    def __init__(self, parent, bg_color, width, height, **kwargs):
        super().__init__(parent, width=width, height=height,
                        bg=parent.cget('bg'), highlightthickness=0, **kwargs)

        self.bg_color = bg_color
        self.card_width = width
        self.card_height = height

        self.draw_card()

    def draw_card(self):
        """Draw rounded rectangle card with shadow"""
        # Shadow
        r = 20
        shadow_offset = 4
        x0, y0 = shadow_offset, shadow_offset
        x1, y1 = self.card_width + shadow_offset, self.card_height + shadow_offset

        shadow_points = [
            x0+r, y0,
            x1-r, y0,
            x1, y0,
            x1, y0+r,
            x1, y1-r,
            x1, y1,
            x1-r, y1,
            x0+r, y1,
            x0, y1,
            x0, y1-r,
            x0, y0+r,
            x0, y0
        ]

        self.create_polygon(shadow_points, fill="#D0D0D0", smooth=True, tags="shadow")

        # Main card
        x0, y0 = 0, 0
        x1, y1 = self.card_width, self.card_height

        card_points = [
            x0+r, y0,
            x1-r, y0,
            x1, y0,
            x1, y0+r,
            x1, y1-r,
            x1, y1,
            x1-r, y1,
            x0+r, y1,
            x0, y1,
            x0, y1-r,
            x0, y0+r,
            x0, y0
        ]

        self.create_polygon(card_points, fill=self.bg_color, smooth=True, tags="card")


class FlashcardApp:
    """Modern Flashcard Application"""

    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard Master")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)

        # Modern color scheme with gradients
        self.colors = {
            'gradient_start': '#667EEA',
            'gradient_end': '#764BA2',
            'primary': '#667EEA',
            'secondary': '#10B981',
            'accent': '#F59E0B',
            'danger': '#EF4444',
            'bg': '#F9FAFB',
            'card_front': '#FFFFFF',
            'card_back': '#EFF6FF',
            'text': '#1F2937',
            'text_light': '#6B7280',
            'text_lighter': '#9CA3AF'
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

        # Header with gradient
        header = GradientFrame(
            self.root,
            self.colors['gradient_start'],
            self.colors['gradient_end'],
            height=80
        )
        header.pack(fill=tk.X)

        # Title
        header.create_text(
            500, 40,
            text="✨ Flashcard Master",
            font=("Segoe UI", 28, "bold"),
            fill="white",
            tags="title"
        )

        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=25)

        # Stats bar
        stats_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        stats_frame.pack(fill=tk.X, pady=(0, 25))

        # Progress badge
        progress_container = tk.Frame(stats_frame, bg="#EEF2FF", relief=tk.FLAT)
        progress_container.pack(side=tk.LEFT)

        self.progress_label = tk.Label(
            progress_container,
            text="Card 0 of 0",
            font=("Segoe UI", 11, "bold"),
            bg="#EEF2FF",
            fg=self.colors['primary'],
            padx=20,
            pady=8
        )
        self.progress_label.pack()

        # Keyboard hint
        hint_label = tk.Label(
            stats_frame,
            text="💡 Tip: Use ← → arrows to navigate, Space to flip",
            font=("Segoe UI", 10),
            bg=self.colors['bg'],
            fg=self.colors['text_lighter']
        )
        hint_label.pack(side=tk.RIGHT)

        # Card display area
        card_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        card_frame.pack(pady=(0, 20))

        # Card canvas for rounded corners
        self.card_canvas = tk.Canvas(
            card_frame,
            width=720,
            height=324,
            bg=self.colors['bg'],
            highlightthickness=0
        )
        self.card_canvas.pack()

        # Card background with shadow and rounded corners
        self.card_bg = RoundedCard(
            self.card_canvas,
            self.colors['card_front'],
            700,
            300
        )
        self.card_bg.place(x=10, y=10)

        # Card text
        self.card_label = tk.Label(
            self.card_bg,
            text="Click 'Add Card' to begin!",
            font=("Segoe UI", 20),
            bg=self.colors['card_front'],
            fg=self.colors['text'],
            wraplength=650,
            justify=tk.CENTER
        )
        self.card_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Flip indicator badge
        self.flip_indicator = tk.Label(
            self.card_bg,
            text="",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['card_front'],
            fg=self.colors['text_light'],
            padx=15,
            pady=5
        )
        self.flip_indicator.place(x=20, y=20)

        # Button container
        button_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        button_frame.pack()

        # Navigation buttons
        nav_frame = tk.Frame(button_frame, bg=self.colors['bg'])
        nav_frame.pack(pady=(0, 12))

        self.prev_btn = ModernButton(
            nav_frame,
            text="← Previous",
            command=self.prev_card,
            bg_color=self.colors['primary'],
            width=130,
            height=42
        )
        self.prev_btn.pack(side=tk.LEFT, padx=8)

        self.flip_btn = ModernButton(
            nav_frame,
            text="🔄 Flip Card",
            command=self.flip_card,
            bg_color=self.colors['secondary'],
            width=150,
            height=42
        )
        self.flip_btn.pack(side=tk.LEFT, padx=8)

        self.next_btn = ModernButton(
            nav_frame,
            text="Next →",
            command=self.next_card,
            bg_color=self.colors['primary'],
            width=130,
            height=42
        )
        self.next_btn.pack(side=tk.LEFT, padx=8)

        # Management buttons
        manage_frame = tk.Frame(button_frame, bg=self.colors['bg'])
        manage_frame.pack()

        ModernButton(
            manage_frame,
            text="➕ Add Card",
            command=self.add_card,
            bg_color=self.colors['secondary'],
            width=120,
            height=40
        ).pack(side=tk.LEFT, padx=6)

        ModernButton(
            manage_frame,
            text="✏️ Edit",
            command=self.edit_card,
            bg_color=self.colors['accent'],
            width=100,
            height=40
        ).pack(side=tk.LEFT, padx=6)

        ModernButton(
            manage_frame,
            text="🗑️ Delete",
            command=self.delete_card,
            bg_color=self.colors['danger'],
            width=100,
            height=40
        ).pack(side=tk.LEFT, padx=6)

        ModernButton(
            manage_frame,
            text="🔀 Shuffle",
            command=self.shuffle_cards,
            bg_color="#8B5CF6",
            width=110,
            height=40
        ).pack(side=tk.LEFT, padx=6)

        # Keyboard bindings with focus check
        self.root.bind_all('<space>', self._safe_keyboard_handler(self.flip_card))
        self.root.bind_all('<Left>', self._safe_keyboard_handler(self.prev_card))
        self.root.bind_all('<Right>', self._safe_keyboard_handler(self.next_card))
        self.root.bind_all('<n>', self._safe_keyboard_handler(self.add_card))
        self.root.bind_all('<N>', self._safe_keyboard_handler(self.add_card))
        self.root.bind_all('<e>', self._safe_keyboard_handler(self.edit_card))
        self.root.bind_all('<E>', self._safe_keyboard_handler(self.edit_card))
        self.root.bind_all('<Return>', self._safe_keyboard_handler(self.flip_card))

    def _safe_keyboard_handler(self, callback):
        """Wrap keyboard callbacks to check if user is typing in a text widget"""
        def handler(event):
            # Don't trigger shortcuts if focus is on a Text widget
            focused = self.root.focus_get()
            if isinstance(focused, tk.Text):
                return
            callback()
        return handler

    def display_card(self):
        """Display the current card"""
        if not self.cards:
            self.card_label.config(
                text="No cards available.\nClick '➕ Add Card' to create one!",
                bg=self.colors['card_front'],
                fg=self.colors['text_lighter']
            )
            self.flip_indicator.config(text="", bg=self.colors['card_front'])
            self.progress_label.config(text="Card 0 of 0")

            # Reset card background
            self.card_bg.bg_color = self.colors['card_front']
            self.card_bg.delete("all")
            self.card_bg.draw_card()
            self.card_label.configure(bg=self.colors['card_front'])
            return

        card = self.cards[self.current_index]

        if self.is_flipped:
            text = card['back']
            bg_color = self.colors['card_back']
            indicator = "📖 ANSWER"
            indicator_bg = "#DBEAFE"
        else:
            text = card['front']
            bg_color = self.colors['card_front']
            indicator = "❓ QUESTION"
            indicator_bg = "#FEF3C7"

        # Update card background
        self.card_bg.bg_color = bg_color
        self.card_bg.delete("all")
        self.card_bg.draw_card()

        # Update text
        self.card_label.config(text=text, bg=bg_color, fg=self.colors['text'])
        self.flip_indicator.config(text=indicator, bg=indicator_bg)

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
        dialog = CardDialog(self.root, "Add New Card", self.colors)

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
            self.colors,
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
        messagebox.showinfo("Shuffled", "Cards have been shuffled! 🎲")

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
    """Dialog for adding/editing cards with modern design"""

    def __init__(self, parent, title, colors, initial_front="", initial_back=""):
        self.result = None
        self.colors = colors

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("600x600")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg=colors['bg'])

        # Make it modal
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (600 // 2)
        self.dialog.geometry(f"600x600+{x}+{y}")

        # Header
        header = tk.Frame(self.dialog, bg=colors['primary'], height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text=title,
            font=("Segoe UI", 18, "bold"),
            bg=colors['primary'],
            fg="white"
        ).pack(pady=20)

        # Content
        content_frame = tk.Frame(self.dialog, bg=colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=25)

        # Front of card
        tk.Label(
            content_frame,
            text="📝 Front (Question)",
            font=("Segoe UI", 12, "bold"),
            bg=colors['bg'],
            fg=colors['text']
        ).pack(anchor=tk.W, pady=(0, 8))

        front_container = tk.Frame(content_frame, bg="white", relief=tk.FLAT, bd=2)
        front_container.pack(fill=tk.X, pady=(0, 20))

        self.front_text = tk.Text(
            front_container,
            height=6,
            font=("Segoe UI", 11),
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=8,
            bg="white",
            fg=colors['text']
        )
        self.front_text.pack(fill=tk.BOTH, expand=True)
        self.front_text.insert("1.0", initial_front)

        # Back of card
        tk.Label(
            content_frame,
            text="💡 Back (Answer)",
            font=("Segoe UI", 12, "bold"),
            bg=colors['bg'],
            fg=colors['text']
        ).pack(anchor=tk.W, pady=(0, 8))

        back_container = tk.Frame(content_frame, bg="white", relief=tk.FLAT, bd=2)
        back_container.pack(fill=tk.X, pady=(0, 20))

        self.back_text = tk.Text(
            back_container,
            height=6,
            font=("Segoe UI", 11),
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=8,
            bg="white",
            fg=colors['text']
        )
        self.back_text.pack(fill=tk.BOTH, expand=True)
        self.back_text.insert("1.0", initial_back)

        # Buttons
        button_frame = tk.Frame(content_frame, bg=colors['bg'])
        button_frame.pack(fill=tk.X)

        ModernButton(
            button_frame,
            text="✓ Save Card",
            command=self.save,
            bg_color=colors['secondary'],
            width=180,
            height=50
        ).pack(side=tk.LEFT, padx=(0, 15))

        ModernButton(
            button_frame,
            text="✕ Cancel",
            command=self.cancel,
            bg_color="#6B7280",
            width=150,
            height=50
        ).pack(side=tk.LEFT)

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
