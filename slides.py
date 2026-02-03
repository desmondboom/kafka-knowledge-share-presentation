#!/usr/bin/env python3
"""
Terminal Slideshow for Kafka share
Run your presentation entirely in the CLI!
"""

import sys
import os
import tty
import termios
from pathlib import Path

try:
    from rich.console import Console
    from rich.align import Align
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.text import Text
    import pyfiglet
except ImportError:
    print("Missing dependencies. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rich", "pyfiglet"])
    from rich.console import Console
    from rich.align import Align
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.text import Text
    import pyfiglet


def getch():
    """Get a single character from stdin"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


class TerminalSlideshow:
    def __init__(self, markdown_file: str = "PRESENTATION.md"):
        self.console = Console()
        self.markdown_file = markdown_file
        self.slides = []
        self.current_slide = 0
        self.load_slides()

    def load_slides(self):
        """Parse markdown file into individual slides separated by ---"""
        with open(self.markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split by --- (slide separator)
        raw_slides = content.split('\n---\n')

        # Clean up and store slides
        for slide_content in raw_slides:
            slide_content = slide_content.strip()
            if slide_content:
                self.slides.append(slide_content)

        if not self.slides:
            self.console.print("[red]No slides found in markdown file![/red]")
            sys.exit(1)

    def render_slide(self):
        """Render the current slide"""
        self.console.clear()

        # Create header with navigation info
        nav_info = Text()
        nav_info.append(f"Slide {self.current_slide + 1} / {len(self.slides)}", style="bold cyan")
        nav_info.append(" | ", style="dim")
        nav_info.append("←/→ h/l Space/Enter: Navigate | ", style="dim")
        nav_info.append("1-9: Jump | ", style="dim")
        nav_info.append("q: Quit", style="dim")

        self.console.print(Panel(nav_info, style="bold blue", expand=False))
        self.console.print()

        # Render the slide content
        slide_content = self.slides[self.current_slide]
        md = Markdown(slide_content)
        self.console.print(Panel(md, border_style="cyan", padding=(1, 2)))

        # Footer with progress bar
        progress = "█" * (self.current_slide + 1) + "░" * (len(self.slides) - self.current_slide - 1)
        self.console.print(f"\n[dim]{progress}[/dim]", justify="center")

    def next_slide(self):
        """Move to next slide"""
        if self.current_slide < len(self.slides) - 1:
            self.current_slide += 1
            return True
        return False

    def prev_slide(self):
        """Move to previous slide"""
        if self.current_slide > 0:
            self.current_slide -= 1
            return True
        return False

    def jump_to_slide(self, slide_num: int):
        """Jump to specific slide (1-indexed)"""
        slide_index = slide_num - 1
        if 0 <= slide_index < len(self.slides):
            self.current_slide = slide_index
            return True
        return False

    def run(self):
        """Main presentation loop"""
        self.console.clear()

        # Generate ASCII art using pyfiglet
        kafka_text = pyfiglet.figlet_format("K A F K A", font="big")
        kafka_lines = [line.rstrip() for line in kafka_text.splitlines()]
        max_width = max((len(line) for line in kafka_lines), default=0)
        divider = "━" * max_width

        welcome_text = Text()
        welcome_text.append(kafka_text, style="bold cyan")
        welcome_text.append("\n")
        welcome_text.append("Message Streaming & Event Processing", style="bold cyan")
        welcome_text.append("\n")
        welcome_text.append(divider, style="yellow")
        welcome_text.append("\n\n")
        welcome_text.append("Let's explore Kafka streaming together!", style="dim")
        welcome_text.append("\n\n")
        welcome_text.append("Ready to dive in? 🔄", style="green")

        # Welcome screen
        welcome = Panel(
            Align.center(welcome_text),
            border_style="cyan",
            padding=(1, 2)
        )
        self.console.print(welcome, justify="center")
        getch()

        # Main loop
        while True:
            self.render_slide()

            # Get keyboard input
            try:
                key = getch()

                # Handle arrow keys (escape sequences)
                if key == '\x1b':  # ESC
                    next_char = getch()
                    if next_char == '[':
                        direction = getch()
                        if direction == 'C':  # Right arrow
                            self.next_slide()
                        elif direction == 'D':  # Left arrow
                            self.prev_slide()
                # Navigation with regular keys
                elif key in ['l', ' ', '\n']:  # 'l', space, or enter for next
                    self.next_slide()
                elif key in ['h']:  # 'h' for previous
                    self.prev_slide()
                elif key == 'q':  # Quit
                    break
                elif key.isdigit():  # Jump to slide
                    self.jump_to_slide(int(key))

            except KeyboardInterrupt:
                break

        # Exit message
        self.console.clear()
        self.console.print("\n[bold green]Thanks for listening! 👾👩‍💻🧑‍💻🤖[/bold green]\n")


def main():
    # Find PRESENTATION.md in current directory
    presentation_path = Path("PRESENTATION.md")

    if not presentation_path.exists():
        print(f"Error: {presentation_path} not found!")
        print("Make sure to run this script from the presentation directory.")
        sys.exit(1)

    slideshow = TerminalSlideshow(str(presentation_path))
    slideshow.run()


if __name__ == "__main__":
    main()
    