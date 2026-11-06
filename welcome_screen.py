"""Premium welcome screen for the Chatterbox desktop application."""

from collections.abc import Callable
import tkinter as tk

import customtkinter as ctk


# ---------------- THEME ----------------

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

BG = "#F4FBF7"
SURFACE = "#FFFFFF"
SURFACE_SOFT = "#F8FCFA"
MINT = "#DDF5E9"
MINT_STRONG = "#C9EEDC"
PRIMARY = "#147D68"
PRIMARY_HOVER = "#0F6A59"
PRIMARY_SOFT = "#E8F7F0"
DARK = "#163F3D"
BODY = "#55726D"
MUTED = "#829893"
WHITE = "#FFFFFF"
BORDER = "#D9EBE3"
BORDER_STRONG = "#C7E1D5"
SUCCESS = "#2DBF91"
SHADOW = "#DCEDE5"

FONT = "Segoe UI"
DISPLAY_FONT = "Segoe UI"



class NetworkIllustration(tk.Canvas):
    """Premium local-network illustration drawn entirely with Canvas."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            height=172,
            background=MINT,
            highlightthickness=0,
            bd=0,
            **kwargs,
        )

        self.bind("<Configure>", self._draw)

    def _draw(self, _event=None):
        self.delete("all")

        width = max(self.winfo_width(), 500)
        height = max(self.winfo_height(), 172)

        center_y = 76

        left_x = int(width * 0.18)
        center_x = int(width * 0.50)
        right_x = int(width * 0.82)

        # Soft decorative background circles
        self.create_oval(
            center_x - 105, 5,
            center_x + 105, 147,
            fill="#D5F1E4",
            outline=""
        )

        self.create_oval(
            center_x - 75, 20,
            center_x + 75, 132,
            fill="#CBEBDD",
            outline=""
        )

        # Subtle decorative dots
        for x in range(18, width, 30):
            for y in range(15, height, 30):
                self.create_oval(
                    x, y, x + 2, y + 2,
                    fill="#B9E5D1",
                    outline=""
                )

        # Connection lines
        self.create_line(
            left_x + 30, center_y,
            center_x - 38, center_y,
            fill="#75BDA3",
            width=2,
            dash=(5, 5)
        )

        self.create_line(
            center_x + 38, center_y,
            right_x - 30, center_y,
            fill="#75BDA3",
            width=2,
            dash=(5, 5)
        )

        # Small connection points
        for x in (
            left_x + 65,
            left_x + 110,
            center_x - 65,
            center_x + 65,
            right_x - 110,
            right_x - 65,
        ):
            self.create_oval(
                x - 3, center_y - 3,
                x + 3, center_y + 3,
                fill="#70B99D",
                outline=""
            )

        # Draw connected users
        self._draw_person(left_x, center_y)
        self._draw_person(right_x, center_y)

        # Central Wi-Fi hub
        self._draw_hub(center_x, center_y)

        # Connection status
        pill_width = 154
        pill_x = center_x - pill_width // 2

        self.create_rectangle(
            pill_x, 132,
            pill_x + pill_width, 153,
            fill="#E8F8EF",
            outline=""
        )

        self.create_oval(
            center_x - 53, 139,
            center_x - 45, 147,
            fill=SUCCESS,
            outline=""
        )

        self.create_text(
            center_x + 8, 143,
            text="DIRECT CONNECTION",
            fill=PRIMARY,
            font=(FONT, 8, "bold")
        )

    def _draw_person(self, x, y):

        # Outer floating circle
        self.create_oval(
            x - 29, y - 29,
            x + 29, y + 29,
            fill="#FFFFFF",
            outline="#B8DFCC",
            width=2
        )

        # Head
        self.create_oval(
            x - 7, y - 13,
            x + 7, y + 1,
            fill=PRIMARY,
            outline=""
        )

        # Body
        self.create_arc(
            x - 15, y - 3,
            x + 15, y + 25,
            start=0,
            extent=180,
            fill=PRIMARY,
            outline=PRIMARY
        )

        # Online indicator
        self.create_oval(
            x + 17, y + 16,
            x + 25, y + 24,
            fill=SUCCESS,
            outline="#FFFFFF",
            width=2
        )

    def _draw_hub(self, x, y):

        # Outer halo
        self.create_oval(
            x - 43, y - 43,
            x + 43, y + 43,
            fill="#B9E8D3",
            outline=""
        )

        # Main hub
        self.create_oval(
            x - 32, y - 32,
            x + 32, y + 32,
            fill=PRIMARY,
            outline="#FFFFFF",
            width=3
        )

        # Wi-Fi symbol
        self.create_arc(
            x - 17, y - 16,
            x + 17, y + 16,
            start=45,
            extent=90,
            style="arc",
            outline="#FFFFFF",
            width=2
        )

        self.create_arc(
            x - 11, y - 9,
            x + 11, y + 12,
            start=45,
            extent=90,
            style="arc",
            outline="#FFFFFF",
            width=2
        )

        # Wi-Fi dot
        self.create_oval(
            x - 2, y + 7,
            x + 2, y + 11,
            fill="#FFFFFF",
            outline=""
        )

    """A lightweight, scalable network illustration with no image assets."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            height=172,
            background=MINT,
            highlightthickness=0,
            bd=0,
            **kwargs,
        )
        self.bind("<Configure>", self._draw)
        self._pulse = 0
        self.after(100, self._animate)

    def _animate(self):
       self._pulse = (self._pulse + 1) % 25
       self._draw()
       self.after(80, self._animate)

    def _draw(self, _event=None):
        self.delete("all")
        width = max(self.winfo_width(), 500)
        height = max(self.winfo_height(), 172)

        # Fine background grid.
        for x in range(0, width, 28):
            self.create_line(x, 0, x, height, fill="#D3EEDF", width=1)
        for y in range(0, height, 28):
            self.create_line(0, y, width, y, fill="#D3EEDF", width=1)

        center_y = 73
        left_x = int(width * 0.19)
        center_x = int(width * 0.50)
        right_x = int(width * 0.81)

        self.create_line(
            left_x + 25,
            center_y,
            center_x - 25,
            center_y,
            fill="#70BCA2",
            width=2,
            dash=(4, 6),
        )
        self.create_line(
            center_x + 25,
            center_y,
            right_x - 25,
            center_y,
            fill="#70BCA2",
            width=2,
            dash=(4, 6),
        )

        self._draw_person(left_x, center_y)
        # Animated expanding connection ring
        radius = 38 + self._pulse * 1.1
        ring_colors = [
        "#B9E8D3",
        "#C0EBD9",
        "#C8EFDF",
        "#D0F2E4",
        "#D8F5E9",
         ]

   

        ring_color = ring_colors[min(self._pulse // 5, 4)]

        self.create_oval(
        center_x - radius,
    center_y - radius,
    center_x + radius,
    center_y + radius,
    outline=ring_color,
    width=2
)

# Central Wi-Fi hub
        self._draw_hub(center_x, center_y)
        self._draw_person(right_x, center_y)

        self.create_oval(
            center_x - 4,
            128,
            center_x + 4,
            136,
            fill=SUCCESS,
            outline="",
        )
        self.create_text(
            center_x + 12,
            132,
            text="PRIVATE CONNECTION",
            anchor="w",
            fill=BODY,
            font=(FONT, 9, "bold"),
        )

    def _draw_person(self, x, y):
        self.create_oval(
            x - 28,
            y - 28,
            x + 28,
            y + 28,
            fill=WHITE,
            outline="#B7DCCA",
            width=1,
        )
        self.create_oval(
            x - 7,
            y - 12,
            x + 7,
            y + 2,
            fill=PRIMARY,
            outline="",
        )
        self.create_arc(
            x - 15,
            y,
            x + 15,
            y + 28,
            start=0,
            extent=180,
            fill=PRIMARY,
            outline=PRIMARY,
        )

    def _draw_hub(self, x, y):
        self.create_oval(
            x - 31,
            y - 31,
            x + 31,
            y + 31,
            fill=PRIMARY,
            outline="",
        )
        self.create_arc(
            x - 17,
            y - 13,
            x + 17,
            y + 18,
            start=38,
            extent=104,
            style="arc",
            outline=WHITE,
            width=2,
        )
        self.create_arc(
            x - 11,
            y - 7,
            x + 11,
            y + 12,
            start=38,
            extent=104,
            style="arc",
            outline=WHITE,
            width=2,
        )
        self.create_oval(x - 2, y + 7, x + 2, y + 11, fill=WHITE, outline="")


class ChatterboxWelcome(ctk.CTkFrame):
    """Chatterbox's desktop landing screen.

    Optional callbacks make this screen easy to connect to the existing host
    and join flows while preserving standalone preview behavior.
    """

    def __init__(
        self,
        master,
        on_host: Callable[[], None] | None = None,
        on_join: Callable[[], None] | None = None,
    ):
        super().__init__(master, fg_color=BG)

        self.on_host = on_host
        self.on_join = on_join

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._create_header()
        self._create_content()
        self._create_footer()

    # ---------------- HEADER ----------------

    def _create_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent", height=90)
        header.grid(row=0, column=0, sticky="ew", padx=56, pady=(24, 0))
        header.grid_columnconfigure(1, weight=1)

        brand = ctk.CTkFrame(header, fg_color="transparent")
        brand.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            brand,
            text="C",
            width=42,
            height=42,
            corner_radius=13,
            fg_color=PRIMARY,
            text_color=WHITE,
            font=(DISPLAY_FONT, 19, "bold"),
        ).pack(side="left", padx=(0, 12))

        ctk.CTkLabel(
            brand,
            text="Chatterbox",
            font=(DISPLAY_FONT, 23, "bold"),
            text_color=DARK,
        ).pack(side="left")

        network_badge = ctk.CTkFrame(
            header,
            fg_color=SURFACE,
            corner_radius=18,
            border_width=1,
            border_color=BORDER,
        )
        network_badge.grid(row=0, column=2, sticky="e")

        ctk.CTkLabel(
            network_badge,
            text="",
            width=8,
            height=8,
            corner_radius=4,
            fg_color=SUCCESS,
        ).pack(side="left", padx=(14, 8), pady=10)

        ctk.CTkLabel(
            network_badge,
            text="LOCAL NETWORK",
            font=(FONT, 10, "bold"),
            text_color=PRIMARY,
        ).pack(side="left", padx=(0, 14), pady=10)

    # ---------------- CONTENT ----------------

    def _create_content(self):
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=56,
            pady=(30, 26),
        )
        content.grid_columnconfigure(0, weight=6, uniform="content")
        content.grid_columnconfigure(1, weight=5, uniform="content")
        content.grid_rowconfigure(0, weight=1)

        self._create_hero(content)
        self._create_connection_card(content)

    def _create_hero(self, parent):
        hero = ctk.CTkFrame(parent, fg_color="transparent")
        hero.grid(row=0, column=0, sticky="nsew", padx=(0, 64))

        eyebrow = ctk.CTkFrame(hero, fg_color="transparent")
        eyebrow.pack(anchor="w", pady=(18, 20))

        ctk.CTkFrame(
            eyebrow,
            width=30,
            height=2,
            fg_color=PRIMARY,
            corner_radius=1,
        ).pack(side="left", padx=(0, 12))

        ctk.CTkLabel(
            eyebrow,
            text="A QUIETER WAY TO CONNECT",
            font=(FONT, 10, "bold"),
            text_color=PRIMARY,
        ).pack(side="left")

        title = ctk.CTkFrame(hero, fg_color="transparent")
        title.pack(fill="x", anchor="w")

        ctk.CTkLabel(
            title,
            text="Your people.",
            font=(DISPLAY_FONT, 48, "bold"),
            text_color=DARK,
            anchor="w",
        ).pack(fill="x", anchor="w")

        ctk.CTkLabel(
            title,
            text="Your network.",
            font=(DISPLAY_FONT, 48, "bold"),
            text_color=PRIMARY,
            anchor="w",
        ).pack(fill="x", anchor="w", pady=(0, 0))

        ctk.CTkLabel(
            hero,
            text=(
                "A calm, private space for the conversations that matter.\n"
                "Connect with people nearby without relying on the cloud."
            ),
            font=(FONT, 15),
            text_color=BODY,
            justify="left",
            anchor="w",
            wraplength=520,
        ).pack(fill="x", anchor="w", pady=(22, 26))

        features = ctk.CTkFrame(hero, fg_color="transparent")
        features.pack(fill="x", pady=(0, 26))
        features.grid_columnconfigure((0, 1), weight=1)

        self._create_feature(
            features,
            column=0,
            marker="01",
            title="Private by design",
            description="Your conversations stay close.",
        )
        self._create_feature(
            features,
            column=1,
            marker="02",
            title="Beautifully simple",
            description="Nothing gets in your way.",
        )

        illustration_frame = ctk.CTkFrame(
            hero,
            fg_color=MINT,
            corner_radius=24,
            border_width=1,
            border_color=MINT_STRONG,
        )
        illustration_frame.pack(fill="x")

        illustration = NetworkIllustration(illustration_frame)
        illustration.pack(fill="both", expand=True, padx=2, pady=2)

    def _create_feature(self, parent, column, marker, title, description):
        feature = ctk.CTkFrame(parent, fg_color="transparent")
        feature.grid(
            row=0,
            column=column,
            sticky="w",
            padx=(0, 26) if column == 0 else (8, 0),
        )

        ctk.CTkLabel(
            feature,
            text=marker,
            width=30,
            height=30,
            corner_radius=10,
            fg_color=PRIMARY_SOFT,
            text_color=PRIMARY,
            font=(FONT, 9, "bold"),
        ).pack(side="left", padx=(0, 10))

        copy = ctk.CTkFrame(feature, fg_color="transparent")
        copy.pack(side="left")

        ctk.CTkLabel(
            copy,
            text=title,
            font=(FONT, 11, "bold"),
            text_color=DARK,
            anchor="w",
        ).pack(anchor="w")

        ctk.CTkLabel(
            copy,
            text=description,
            font=(FONT, 9),
            text_color=MUTED,
            anchor="w",
        ).pack(anchor="w")

    # ---------------- CONNECTION CARD ----------------

    def _create_connection_card(self, parent):
        shadow = ctk.CTkFrame(
            parent,
            fg_color=SHADOW,
            corner_radius=31,
        )
        shadow.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(12, 0),
            pady=(8, 0),
        )

        card = ctk.CTkFrame(
            parent,
            fg_color=SURFACE,
            corner_radius=28,
            border_width=1,
            border_color=BORDER,
        )
        card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(4, 8),
            pady=(0, 8),
        )

        card_inner = ctk.CTkFrame(card, fg_color="transparent")
        card_inner.pack(fill="both", expand=True, padx=36, pady=34)

        top_row = ctk.CTkFrame(card_inner, fg_color="transparent")
        top_row.pack(fill="x")

        ctk.CTkLabel(
            top_row,
            text="WELCOME",
            font=(FONT, 10, "bold"),
            text_color=PRIMARY,
        ).pack(side="left")

        people = ctk.CTkFrame(top_row, fg_color="transparent")
        people.pack(side="right")
        for index, (text, color) in enumerate(
            (("AK", "#DFF2E9"), ("MS", "#F1E9DA"), ("+3", PRIMARY))
        ):
            ctk.CTkLabel(
                people,
                text=text,
                width=28,
                height=28,
                corner_radius=14,
                fg_color=color,
                text_color=WHITE if index == 2 else DARK,
                font=(FONT, 8, "bold"),
            ).pack(side="left", padx=(0, 0))

        ctk.CTkLabel(
            card_inner,
            text="Let's get you\nconnected.",
            font=(DISPLAY_FONT, 31, "bold"),
            text_color=DARK,
            justify="left",
            anchor="w",
        ).pack(fill="x", anchor="w", pady=(18, 10))

        ctk.CTkLabel(
            card_inner,
            text="Choose how you'd like to begin.",
            font=(FONT, 13),
            text_color=MUTED,
            anchor="w",
        ).pack(fill="x", anchor="w", pady=(0, 26))

        self._create_action(
            card_inner,
            title="Host a room",
            description="Create a space and invite people nearby.",
            command=self.host_room,
            primary=True,
        )

        self._create_action(
            card_inner,
            title="Join a room",
            description="Connect with an address from your host.",
            command=self.join_room,
            primary=False,
        )

        divider = ctk.CTkFrame(card_inner, fg_color="transparent")
        divider.pack(fill="x", pady=(26, 14))
        divider.grid_columnconfigure((0, 2), weight=1)

        ctk.CTkFrame(divider, height=1, fg_color=BORDER).grid(
            row=0, column=0, sticky="ew"
        )
        ctk.CTkLabel(
            divider,
            text="LOCAL-FIRST",
            font=(FONT, 8, "bold"),
            text_color=MUTED,
        ).grid(row=0, column=1, padx=10)
        ctk.CTkFrame(divider, height=1, fg_color=BORDER).grid(
            row=0, column=2, sticky="ew"
        )

        self.status_label = ctk.CTkLabel(
            card_inner,
            text="No accounts. No tracking. Just your network.",
            font=(FONT, 10),
            text_color=MUTED,
        )
        self.status_label.pack(pady=(0, 2))

    def _create_action(self, parent, title, description, command, primary):
        background = PRIMARY if primary else SURFACE_SOFT
        hover = PRIMARY_HOVER if primary else PRIMARY_SOFT
        title_color = WHITE if primary else DARK
        description_color = "#C9E8DE" if primary else MUTED
        border_color = PRIMARY if primary else BORDER_STRONG

        action = ctk.CTkFrame(
            parent,
            fg_color=background,
            corner_radius=16,
            border_width=1,
            border_color=border_color,
        )
        action.pack(fill="x", pady=(0, 12))
        action.grid_columnconfigure(0, weight=1)

        copy = ctk.CTkFrame(action, fg_color="transparent")
        copy.grid(row=0, column=0, sticky="ew", padx=(18, 8), pady=14)

        ctk.CTkLabel(
            copy,
            text=title,
            font=(FONT, 14, "bold"),
            text_color=title_color,
            anchor="w",
        ).pack(fill="x", anchor="w")

        ctk.CTkLabel(
            copy,
            text=description,
            font=(FONT, 10),
            text_color=description_color,
            anchor="w",
        ).pack(fill="x", anchor="w", pady=(3, 0))

        button = ctk.CTkButton(
            action,
            text="Open",
            width=60,
            height=34,
            corner_radius=11,
            fg_color=WHITE if primary else PRIMARY,
            hover_color="#E9F5EF" if primary else PRIMARY_HOVER,
            text_color=PRIMARY if primary else WHITE,
            font=(FONT, 10, "bold"),
            command=command,
        )
        button.grid(row=0, column=1, padx=(8, 16))

        # Clicking the surrounding copy should feel like clicking the action.
        for widget in (action, copy, *copy.winfo_children()):
            widget.bind("<Button-1>", lambda _event, callback=command: callback())
            widget.bind("<Enter>", lambda _event, frame=action: frame.configure(fg_color=hover))
            widget.bind(
                "<Leave>",
                lambda _event, frame=action, color=background: frame.configure(
                    fg_color=color
                ),
            )

    # ---------------- FOOTER ----------------

    def _create_footer(self):
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=2, column=0, sticky="ew", padx=56, pady=(0, 24))
        footer.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            footer,
            text="CHATTERBOX",
            font=(FONT, 8, "bold"),
            text_color=MUTED,
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            footer,
            text="MADE FOR THE PEOPLE WITHIN REACH",
            font=(FONT, 8, "bold"),
            text_color=MUTED,
        ).grid(row=0, column=1)

        ctk.CTkLabel(
            footer,
            text="PRIVATE BY NATURE",
            font=(FONT, 8, "bold"),
            text_color=MUTED,
        ).grid(row=0, column=2, sticky="e")

    # ---------------- ACTIONS ----------------

    def _set_status(self, message):
        self.status_label.configure(text=message, text_color=PRIMARY)
        self.after(
            2200,
            lambda: self.status_label.configure(
                text="No accounts. No tracking. Just your network.",
                text_color=MUTED,
            ),
        )

    def host_room(self):
        if self.on_host:
            self.on_host()
            return
        self._set_status("Host room selected.")
        print("Host Room selected")

    def join_room(self):
        if self.on_join:
            self.on_join()
            return
        self._set_status("Join room selected.")
        print("Join Room selected")


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1180x760")
    app = ChatterboxWelcome(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
