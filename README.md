# Flashcard Master ✨

A modern, beautiful flashcard application built with Python and Tkinter featuring a contemporary web-inspired design.

## Features

- 🎨 **Modern Web Design** - Beautiful gradient header, rounded corners, and smooth hover effects
- 🔄 **Card Flipping** - Interactive card flipping to reveal answers with color-coded sides
- ➕ **Add/Edit Cards** - Clean, modern dialogs for managing flashcards
- 🗑️ **Delete Cards** - Remove cards you no longer need
- 🔀 **Shuffle Deck** - Randomize card order for better learning
- 💾 **Auto-save** - Cards are automatically saved to JSON file
- ⌨️ **Smart Keyboard Shortcuts** - Navigate efficiently with keyboard (won't interfere with typing)
- 📊 **Progress Tracking** - See your position in the deck with modern badge design
- 🎯 **Visual Feedback** - Color-coded question/answer badges and status indicators

## How to Run

```bash
python3 flashcard_app.py
```

## Keyboard Shortcuts

- `Space` or `Enter` - Flip current card
- `Left Arrow` - Previous card
- `Right Arrow` - Next card
- `N` - Add new card (case-insensitive)
- `E` - Edit current card (case-insensitive)

## Features Breakdown

### Modern Web-Inspired Design
- **Gradient Header** - Eye-catching purple gradient banner
- **Rounded Corners** - Smooth, modern button and card designs
- **Shadow Effects** - Subtle depth for visual hierarchy
- **Hover Animations** - Interactive button effects on mouse over
- **Color-Coded Cards** - White for questions, blue tint for answers
- **Badge Design** - Modern progress and status indicators
- **Segoe UI Font** - Clean, contemporary typography
- **Responsive Interactions** - Smooth visual feedback

### Card Management
- **Add Cards**: Click "➕ Add Card" or press `N` to create new flashcards
- **Edit Cards**: Click "✏️ Edit" or press `E` to modify existing cards
- **Delete Cards**: Remove cards with confirmation dialog
- **Shuffle**: Randomize the order of your flashcard deck

### Navigation & Smart Shortcuts
- Navigate through cards using Previous/Next buttons or arrow keys
- Flip cards to reveal answers using the Flip button, spacebar, or Enter key
- Progress indicator shows your position in the deck
- **Smart keyboard shortcuts** - Won't trigger when typing in text boxes
- Built-in keyboard hints displayed in the UI

## Data Storage

Flashcards are stored in `flashcards.json` in the same directory as the application. The file is automatically created with sample cards on first run.

## Sample Cards

The app comes with 3 sample cards about Python and programming. You can delete these and add your own!

## Requirements

- Python 3.x
- Tkinter (included with most Python installations)

No external dependencies required!
