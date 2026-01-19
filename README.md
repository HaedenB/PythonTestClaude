# Flashcard Master 📚

A modern, beautiful flashcard application built with Python and Tkinter.

## Features

- 🎨 **Modern UI Design** - Clean, professional interface with smooth interactions
- 🔄 **Card Flipping** - Interactive card flipping to reveal answers
- ➕ **Add/Edit Cards** - Easy-to-use dialog for managing flashcards
- 🗑️ **Delete Cards** - Remove cards you no longer need
- 🔀 **Shuffle Deck** - Randomize card order for better learning
- 💾 **Auto-save** - Cards are automatically saved to JSON file
- ⌨️ **Keyboard Shortcuts** - Navigate efficiently with keyboard
- 📊 **Progress Tracking** - See your position in the deck

## How to Run

```bash
python3 flashcard_app.py
```

## Keyboard Shortcuts

- `Space` - Flip current card
- `Left Arrow` - Previous card
- `Right Arrow` - Next card
- `n` - Add new card
- `e` - Edit current card

## Features Breakdown

### Modern Design Elements
- Custom styled buttons with hover effects
- Shadow effects for depth
- Color-coded card sides (white for questions, blue for answers)
- Clean typography with Helvetica font
- Responsive button interactions

### Card Management
- **Add Cards**: Click "Add Card" or press `n` to create new flashcards
- **Edit Cards**: Click "Edit Card" or press `e` to modify existing cards
- **Delete Cards**: Remove cards with confirmation dialog
- **Shuffle**: Randomize the order of your flashcard deck

### Navigation
- Navigate through cards using Previous/Next buttons or arrow keys
- Flip cards to reveal answers using the Flip button or spacebar
- Progress indicator shows your position in the deck

## Data Storage

Flashcards are stored in `flashcards.json` in the same directory as the application. The file is automatically created with sample cards on first run.

## Sample Cards

The app comes with 3 sample cards about Python and programming. You can delete these and add your own!

## Requirements

- Python 3.x
- Tkinter (included with most Python installations)

No external dependencies required!
